# Dim-2 (RAPL) — first-run-validate runbook

**Turnkey copy-paste blocks for the four BUILT-but-not-yet-run harnesses.** Each rail = (1) bring a
backend up, (2) two shells: `server` + `measure-rapl`, (3) the **sanity gate** before trusting numbers.
Base (R1) and AP2 (R6) are already run-validated — not repeated here.

All harnesses live on the agentpay branch **`dim2-rapl-instrumentation`** (repo
`/home/michael/dev/github/mblake4u/agentpay`). Switch to it first:

```bash
cd /home/michael/dev/github/mblake4u/agentpay && git checkout dim2-rapl-instrumentation
```

Results are **pilot data, not calibration** — append outcomes to
`/home/michael/dev/github/agentic-paybench/payhelm/paybench/methodology/dim2-q4-pilot-log.md`
(do NOT write provenance/calibration yet; that needs ≥2 topology + all rails + the FR1 confirmation).

---

## The sanity gate (apply to EVERY run before trusting a single number)

The harness prints these at the end. **All must pass or the run does not count:**

- [ ] **`harness_error` = 0** — any harness_error is an instrumentation bug; FIX before scoring.
- [ ] **socket connects ~1–2** (`socket connects observed:` line) — proves undici keep-alive pooled
      (B1). If it ≈ trial count, pooling broke → the number is handshake-inflated; lower `--sleep` (<4 s).
- [ ] **min-RTT floor printed and small** (localhost, ~1–3 ms) — the S1 floor that gets subtracted.
- [ ] **outcomes are `ok` (+ maybe `rejected`/`timeout`), never silent** — the S3 taxonomy.
- [ ] A rails only: **the accept actually verified** (`isValid=true` in the per-trial log / no 401s).
- [ ] B rails: **status was 402** (not 200/404) on the unpaid GET.

Common knob: `--trials 30 --warmup 5 --rtt-burst 12 --sleep 1` (all four harnesses accept these).
Keep `--sleep < 4` (undici keepAliveTimeout ~4 s).

---

## Easiest first — the two B-only MPP rails need NO buyer funding

> Issuing a 402 challenge requires only the **server** up. No payment is signed, so no funded buyer
> wallet, no faucet. These are the lowest-friction validations.

### R10 — MPP-on-Tempo (Sub-ranking B only)  ·  port 8404

Backend: keyless Tempo Moderato auto-fund (no browser faucet).

```bash
cd /home/michael/dev/github/mblake4u/agentpay/poc/rail-tempo-mpp
npx tsx src/setup-accounts.ts          # one-time: generates EOAs, keyless-funds, writes .env
# shell 1 — server (leave running):
npx ts-node src/server.ts              # -> "Rail 10 — MPP-on-Tempo server on port 8404"
# shell 2 — measure:
npx ts-node src/measure-rapl.ts --trials 30 --sleep 1
# -> samples: poc/rail-tempo-mpp/samples/R10-mpp-tempo.rapl.samples.jsonl
```
Note: **A (Tempo-Session) is intentionally NOT here** — deferred founder decision. B only.

### R11 — MPP-on-Lightning / Spark (Sub-ranking B only)  ·  port 8411

Backend: Spark **regtest** wallets via setup script. For B (issue invoice) **no funding needed** —
`setup-wallets.ts` creating the SERVER wallet is sufficient to generate BOLT11 invoices.

```bash
cd /home/michael/dev/github/mblake4u/agentpay/poc/rail-lightning-mpp
npx tsx src/setup-wallets.ts           # one-time: generates SERVER+CLIENT Spark regtest wallets, writes .env
# shell 1 — server (leave running):
npx tsx src/server.ts                  # -> "Rail 11 — MPP-on-Lightning (Spark) server on port 8411"
# shell 2 — measure:
npx tsx src/measure-rapl.ts --trials 30 --sleep 1
# -> samples: poc/rail-lightning-mpp/samples/R11-mpp-lightning.rapl.samples.jsonl
```
Expect B here to be **larger / noisier than x402's 402** — it includes an intrinsic Spark
invoice-generation hop (disclosed; NOT removed by the RTT floor). That's a real finding, not a bug.

---

## The two x402 A+B rails — need a FUNDED BUYER (the accept calls facilitator `/verify`, which checks funds)

### R9 — x402-on-Solana (Sub-ranking A + B)  ·  port 3402

Backend: **buyer funded with devnet USDC** + seller ATA created. Facilitator is the free hosted
`https://x402.org/facilitator` (no key).

```bash
cd /home/michael/dev/github/mblake4u/agentpay/poc/rail-solana-x402
# one-time setup (if .env not already populated):
npm run keygen                         # writes keypair-seller.json / keypair-buyer.json (gitignored)
#   then fill .env: SELLER_WALLET_ADDRESS + BUYER_PRIVATE_KEY (base58, 64-byte) from those files
#   FUND buyer devnet USDC:  https://faucet.circle.com  (chain "Solana Devnet", paste buyer pubkey)
#   CREATE seller ATA:  spl-token create-account 4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU --owner $SELLER_WALLET_ADDRESS
# shell 1 — server:
npx ts-node src/server.ts              # -> listens on :3402
# shell 2 — measure (A=accept via facilitator /verify, B=402 issuance):
npx ts-node src/measure-rapl.ts --trials 30 --sleep 1
# -> samples: poc/rail-solana-x402/samples/ (R9 ...rapl.samples.jsonl)
```
Extra gate: confirm the **buyer USDC balance > price** before the run, else every accept `rejected`
(insufficient funds) and A is uninformative.

### R2 — x402-on-Stellar (Sub-ranking A + B)  ·  port 8403

Backend: **buyer funded with testnet USDC (trustline required)** + a free OZ facilitator key.
Secrets come from KeePass (`agentpay.kdbx > Stellar`).

```bash
cd /home/michael/dev/github/mblake4u/agentpay/poc/rail-stellar-x402
# one-time .env (NEVER commit):
#   STELLAR_SELLER_SECRET / STELLAR_BUYER_SECRET  <- KeePass agentpay.kdbx > Stellar > {seller,buyer}
#   OZ_X402_TESTNET_KEY   <- generate (no signup): https://channels.openzeppelin.com/testnet/gen
#   buyer needs a USDC SEP-41 trustline + testnet USDC funded (see rail SETUP.md)
# shell 1 — server:
npx ts-node src/server.ts              # -> listens on :8403 (warns if OZ key missing)
# shell 2 — measure:
npx ts-node src/measure-rapl.ts --trials 30 --sleep 1
# -> samples: poc/rail-stellar-x402/samples/ (R2 ...rapl.samples.jsonl)
```
Extra gate: if accepts come back 401 → `OZ_X402_TESTNET_KEY` unset/expired. If `rejected` →
buyer trustline missing or unfunded.

---

## After a clean run (per rail)

1. Append a row to `dim2-q4-pilot-log.md` (sub-ranking, primitive, n, median raw, σ_log, corrected,
   outcome counts, censoring-rate) — mirror the R1/R6 entries. Mark **run-validated** only if the gate passed.
2. Note the topology (devbox, localhost server, which facilitator/RPC/node) — FR4 wants **≥2 locations**
   eventually, so record where this run happened.
3. Leave provenance/calibration write-back untouched until: all rails run + ≥2 topology + FR1 confirmed.

## What this runbook deliberately does NOT cover

- **Tempo-A (Session)** — not built (deferred founder decision).
- **AP2 bulk-n / 2nd topology** — R6 instrument is validated; more n is a calibration-stage concern.
- **Independent measurement review** of the AP2/Tempo/Lightning harnesses — do before calibration write-back.
- **Multi-topology (FR4 ≥2 locations)** — these blocks are single-topology (devbox); a 2nd location is a
  separate pass.
