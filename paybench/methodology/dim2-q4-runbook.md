# Dim-2 (RAPL) — Q4 validation/calibration RUNBOOK

**Credentialed founder step.** This is the step-by-step for the Q4 validation run that (1) pilots the
FR1 fallback thresholds + power analysis and (2) replaces the PLACEHOLDER auth-latency fixtures with
real `{median, sigma}`. Pairs with `dim2-validation-run-plan.md` (the plan) and the adapter code on
the `dim2-rapl-instrumentation` branch of `mblake4u/agentpay`. **Nothing here runs until you, the
founder, execute it with credentials.**

## ⚡ QUICK START — Base (R1), copy-paste (the one rail runnable TODAY)

> R2/R9/R10/R11 follow after the TS fan-out; R6/AP2 needs the build-or-doc-source decision.
> Everything below is absolute-path and copy-paste. Two terminals.

**A. One-time setup**
```bash
# 1. get on the instrumentation branch
cd /home/michael/dev/github/mblake4u/agentpay && git checkout dim2-rapl-instrumentation

# 2. confirm creds + deps exist
ls -l /home/michael/dev/github/mblake4u/agentpay/poc/rail-x402-base/.env
/home/michael/dev/github/mblake4u/agentpay/poc/rail-x402-base/venv/bin/python -c "import requests; print('requests OK')"
```
If `.env` is missing → copy `poc/rail-x402-base/.env.example` to `.env` and fill the CDP keys + RPC.
If `requests` errors → `/home/michael/dev/github/mblake4u/agentpay/poc/rail-x402-base/venv/bin/pip install requests`

**B. Terminal 1 — start the server (leave running)**
```bash
cd /home/michael/dev/github/mblake4u/agentpay/poc/rail-x402-base
./venv/bin/python seller_server.py
```
Wait for: `Listening on : http://0.0.0.0:8082`. Keep this terminal open.

**C. Terminal 2 — run the measurement**
```bash
cd /home/michael/dev/github/mblake4u/agentpay/poc/rail-x402-base
./venv/bin/python measure_rapl.py --trials 30 --warmup 5 --rtt-burst 12 --sleep 1.0
```

**D. What you should see**
- `min-RTT floor (warm, n=12): X.XXX ms`  (small + stable)
- 30 lines: `[  i] accept=…ms challenge=…ms`
- a summary block: `outcomes: {...}`, `FR1 censoring-rate = …`, and `ACCEPT`/`CHALLENGE` RAW + corrected.

**E. PASS gate — only trust the numbers if ALL hold**
- [ ] `harness_error: 0`  (any > 0 = instrumentation bug — fix before the numbers count)
- [ ] `ok` is most of the 30  (a wall of `rejected` = wallet/payment misconfigured, not a result)
- [ ] min-RTT floor is sub-ms-to-few-ms and stable  (else keep-alive isn't pooling — check the server)

**F. Output file**
```
/home/michael/dev/github/mblake4u/agentpay/poc/rail-x402-base/samples/R1-x402-base.rapl.samples.jsonl
```

**G. Record + send me** (from the summary), for ACCEPT (A) and CHALLENGE (B):
`median_s_lognormal`, `sigma_log`, plus the `FR1 censoring-rate`. Paste them back — I'll sanity-check,
help set the FR1 thresholds, and write them into provenance.

**H. Stop:** `Ctrl+C` in Terminal 1.

---

## 0. Before you start — preconditions
- [ ] **AP2 (R6):** no adapter yet, but **buildable locally** — see `dim2-ap2-build-plan.md` (Google's
      AP2 reference impl, instrument the Credentials Provider verify→issue directly, LLM-free). Build
      decision: **yes** (scoping `w56fqhjyl`). Needs a free Google AI Studio API key for the agent runtime.
- [ ] **One-writer:** do this on a single machine; agentpay syncs via Syncthing. Confirm no other
      session is mid-write in agentpay before you start.
- [ ] **Branch:** `git -C ~/dev/github/mblake4u/agentpay checkout dim2-rapl-instrumentation`.
- [ ] **Creds present:** each rail's `.env` (CDP buyer/seller keys, RPC URLs, wallet addresses). These
      are yours; the harness never touches them.
- [ ] **Funded test wallets** on each rail's testnet/devnet (the buyer must be able to pay; the
      `/verify` work-clause needs a real balance read).
- [ ] **Server reachable with keep-alive** (review B1): the Python server forces HTTP/1.1 + threaded;
      for a representative cross-region run, front it with waitress/gunicorn.

## 1. The measurement, per rail (what you'll run)
Two terminals per rail. Numbers are **milliseconds**, RAW is primary, corrected = raw − min-RTT floor.

### Base (R1) — the reference (Python), DONE + review-fixed
```bash
cd ~/dev/github/mblake4u/agentpay/poc/rail-x402-base
./venv/bin/python seller_server.py                       # terminal 1 (keep-alive enabled)
./venv/bin/python measure_rapl.py --trials 30 --warmup 5 --rtt-burst 12 --sleep 1.0   # terminal 2
```
Output: per-trial `accept=… challenge=…`, then `outcomes`, `FR1 censoring-rate`, and RAW+corrected
summaries for **A (accept)** and **B (challenge)**. Samples → `samples/R1-x402-base.rapl.samples.jsonl`.

### Per-rail facilitator topology (affects what "accept" measures — NOT a blind clone)
- **Base (R1):** facilitator is **in-process**; `/rapl/verify` work = sig-verify + a **Base-RPC balance
  read** + simulation. The RTT baseline subtracts client↔server; the corrected number is the
  server-side authorization *work* (incl. the RPC balance read).
- **Solana/Stellar (R9/R2):** facilitator is **hosted** (`x402.org/facilitator`). The same
  `/rapl/verify` proxy pattern works — the measured work just *includes the hosted-facilitator network
  hop*, which is the real authorization work. (Same measurement structure, different work.)
- **Tempo/Lightning (R10/R11):** **MPP**, not x402 — the server is a `route()` handler, the accept is
  the MPP `Verify` (Tempo, Session-only) / the macaroon+invoice issuance (L402 = **B only**). Distinct
  shape (see §"Per-rail status"). Both POC servers use `mppx.charge()`, which **fuses verify+settle**
  (Charge intent) → **no separable accept → excluded from Sub-ranking A** (RR1). Tempo *could* join A
  via an unbuilt **Tempo-Session** flow (deferred, founder decision); Lightning is **B-only by
  methodology** so there's no A to build. Both B harnesses are built (fixed shape) and type-check.
- **Finding — B is not always local (heterogeneous challenge-issuance work).** x402's 402 is a local
  template emit (~3 ms, Base R1). But **L402/Lightning's B includes a Spark/LND round-trip to GENERATE
  the BOLT11 invoice** — so its challenge-issuance is **node-RTT-bound**, the B-side analogue of Base's
  RPC-dominated A (R1 pilot). Implication: within Sub-ranking B, rails are NOT all measuring the same
  *kind* of work — disclose per-rail what the issuance entails (local template vs invoice-generation
  hop), and note the min-RTT floor removes the **localhost HTTP** hop but **not** the intrinsic
  server→node invoice hop (it's part of the RR5/FR2 work-clause). Flag for founder review alongside the
  R1 server→RPC finding — both push toward §2.5 disclosure of the *backing-service hop* per rail.

## 2. Sanity checks BEFORE trusting any numbers (the runtime-check list)
On the **first** run of each rail, verify (these could not be exercised at draft time):
- [ ] **`harness_error` count is 0** in the outcome summary. Any `harness_error` means an
      instrumentation bug (bad `accepts[0]`, pydantic round-trip, status, SDK call) — **fix before the
      numbers count.** (Only `rejected`+`timeout` are real censoring; `harness_error` is excluded.)
- [ ] **Keep-alive actually pools** — confirm the client Session reuses the socket (the min-RTT floor
      should be a stable sub-ms-to-few-ms, not a per-call handshake). If the floor ≈ a fresh-handshake
      time, keep-alive isn't working (check the server's HTTP/1.1 setting / use waitress).
- [ ] **`isValid=true`** on accepts (a funded, correctly-signed payment) — a run of all `rejected`
      means the test wallet/payment is misconfigured, not a rail result.
- [ ] **Fresh nonce per trial** — accepts should not fail as replays after trial 1.
- [ ] **The work-clause is real** — `verify()` issues a fresh balance/`eth_call` per trial (spot-check
      RPC logs), else A under-measures (review N2).

## 3. Recommended run shape
- **Warm-up:** `--warmup 5` (discarded; FR4 warm-start) + `--rtt-burst 12` (min = floor).
- **Trials:** start at `--trials 30` per rail (matches the D1 calibration n). For the FR1 pilot you may
  want more (e.g. 100) to get a stable tie/censoring-rate — but keep it a **pilot**, separate from any
  scored run.
- **Topology sensitivity (FR4):** run from **≥2 client locations** (co-located + cross-region) and
  record both; the min-RTT floor and the ranking should be reported per topology.

## 4. What to read off each run
Per rail, per sub-ranking (A, B):
- `median_s_lognormal`, `sigma_log` → the **real calibration** to write into the rail's
  auth-latency provenance (replacing PLACEHOLDER).
- `p50/p95/p99` (raw) → distributional detail (RR3 wants these alongside).
- `FR1 censoring-rate` (rejected+timeout / decisions) and the observed **tie-rate** → the inputs that
  decide whether BT stays or the **Cox-PH fallback** fires (FR1 thresholds: tie>20% / censoring>5% /
  cyclic-triples>10% — confirm/tune these *from* this pilot, but do **not** reverse-engineer them to
  flatter BT).

## 5. After the runs — hand back to the methodology
1. **Confirm/tune FR1 thresholds** from the observed rates (§2.5/§9 of the DRAFT).
2. **Write the real `{median, sigma}`** into `paybench/calibration/provenance/<rail>-auth-latency.*`
   (replace the PLACEHOLDER markers) and regenerate fixtures via the (re-aligned) harness.
3. **Ratify** the doctrine into `methodology.md`; then the **pre-registration ceremony**.

## Per-rail status (what's ready vs. what needs work)
| Rail | Adapter | Instrumentation | Notes |
|---|---|---|---|
| **R1 x402-Base** | `rail-x402-base` (Python) | ✅ done + review-fixed | the reference |
| **R9 x402-Solana** | `rail-solana-x402` (TS, Express, **hosted** facilitator) | ✅ built + reviewed + fixed → first-run-validate | `npx ts-node src/server.ts` + `src/measure-rapl.ts` (devnet `BUYER_PRIVATE_KEY`) |
| **R2 x402-Stellar** | `rail-stellar-x402` (TS, Express, OZ hosted facilitator) | ✅ built (fixed shape) → first-run-validate | `npx ts-node src/server.ts` + `src/measure-rapl.ts` (`STELLAR_BUYER_SECRET` + `OZ_X402_TESTNET_KEY`) |
| **R10 MPP-Tempo** | `rail-tempo-mpp` (TS, `route()` handler) | ✅ **B built** (fixed shape) → first-run-validate · ⏳ A=Session deferred | `npx ts-node src/server.ts` + `src/measure-rapl.ts` — **B only** (unpaid `GET /data`→402, no signer). **Charge excluded from A** (verify+settle fused); A=**Tempo-Session** needs an unbuilt mppx session flow (founder decision). ESM/nodenext |
| **R11 MPP-Spark-Lightning** | `rail-lightning-mpp` (TS, `route()`) | ✅ **B built** (fixed shape) → first-run-validate (needs Spark regtest wallet up) | `npx tsx src/server.ts` + `src/measure-rapl.ts` — **B only** (unpaid `GET /data`→402 = BOLT11 invoice + macaroon issuance; no buyer wallet). **B-only by methodology** (no A). Discloses an intrinsic Spark invoice-generation hop (cf. x402's local 402). ESM/nodenext. (NB `rail-lightning-l402/` is a separate older Python "Rail 3" L402, not this dim-2 rail) |
| **R6 GCP+AP2** | `poc/rail-ap2` (Python, capture-replay) | ✅ **done + run-validated** (~1.68 ms, n=30) → review | `measure_rapl_ap2.py` replays a captured PaymentMandate SD-JWT through `_verify_payment_mandate` n× (LLM-free). **A only** (in-process; no B, no RTT floor). Mock issuance excluded+disclosed; pin AP2 commit. See `dim2-q4-pilot-log.md` R6 |
