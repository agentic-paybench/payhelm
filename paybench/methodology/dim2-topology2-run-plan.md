# Dim-2 RAPL — FR4 topology-2 run plan

**Purpose (FR4 / D4e, founder-confirmed 2026-06-24):** a second **network-distinct** vantage to test that
the RAPL ranking is robust to the measuring host's network path. The single-topology pilots
(`dim2-q4-pilot-log.md`) are **indicative, not scored**, until this lands. This is the last gate before the
dim-2 pre-registration ceremony (see `dim2-auth-latency.DRAFT.md` §7 checklist).

## The hypothesis = the test (which rails move vs. stay put)

| Rail / primitive | class | T1 (devbox) | prediction at T2 |
|---|---|---|---|
| x402-Solana **A** (`/verify`) | network (facilitator) | 400 ms | **moves** (abs.) — ranking holds |
| x402-Stellar **A** (OZ `/verify`) | network (facilitator) | 464 ms | **moves** — ranking holds |
| x402-Base **A** (`/verify`→RPC) | network (facilitator→RPC) | 777 ms | **moves** — ranking holds |
| Lightning **B** (BOLT11 mint) | network (Spark node) | ~0.9–1.25 s | **moves** — still ≫ local-402 |
| Tempo **A** (voucher, warm) | local-crypto | 19.5 ms | **~invariant** (warm); the ~5 s TTL tick's RPC read is the only network-sensitive part |
| AP2 **A** (HP 0.68 / DPC 1.58 ms) | local-crypto (in-process) | 0.68 / 1.58 ms | **invariant by construction** (no network) — pure control |
| local-402 **B** (Base/Solana/Stellar/Tempo ~2–3 ms) | local emit | ~2–3 ms | **~invariant** |

**The invariance of the local-crypto rails IS the built-in control.** If they shift materially across
topology, suspect the harness/host, not the rail. **What must hold is the RANKING + the group separation**
(local ≪ network), not the absolute network numbers — those *will* move with host→endpoint distance, by design.

## Topologies

- **T1 = devbox** (done; the pilot numbers).
- **T2a = GitHub Codespaces (Azure)** — *fast robustness check*. Repo already present; ephemeral; x64.
- **T2b = OCI Always-Free VM, named region** (e.g. `eu-frankfurt-1`) — the **documented/citable topology-2**;
  ARM64; persistent. **Cite T2b** in the methodology; T2a is the quick confirmation.

Do **T2a first** (cheap signal), then **T2b** for the record. Run the **network-dependent** rails on T2 (+
the local control set). AP2 is in-process → note "topology-invariant by construction" rather than re-run.

## Per-vantage setup

1. **Sync repos:** `mblake4u/agentpay` (branch `dim2-rapl-instrumentation`) for the rail harnesses; AP2 repo
   only if re-running R6 (optional — invariant).
2. **Install:** Node (TS rails: Solana/Stellar/Tempo/Lightning), Python+uv (Base + AP2). Per-rail
   `npm install` / venv. **ARM64 (T2b):** undici/viem/mppx/`@buildonspark/spark-sdk`/AP2-python all run on
   arm64 — record the arch; watch any native build.
3. **Secrets (NEVER commit):** Codespaces = encrypted Codespaces secrets; OCI = `scp` the rail `.env`s over
   SSH. Needed: Solana `BUYER_PRIVATE_KEY`+`SELLER_WALLET_ADDRESS` (funded devnet USDC); Stellar
   `STELLAR_BUYER_SECRET`+`OZ_X402_TESTNET_KEY` (funded testnet USDC + trustline); Base
   `BASE_SEPOLIA_RPC_URL`+buyer key; Tempo `.env` (keyless faucet — works anywhere); Lightning Spark
   regtest (re-run `setup-wallets.ts` per host). **Reuse the same funded buyer wallets** across T1/T2 — only
   the measuring host changes.
4. **FR7 — hold endpoints constant:** same facilitator/RPC/LN-operator across T1↔T2, so the delta is the
   host→endpoint *path*, not an endpoint swap.

## What to run (per rail, T2)

Same harnesses, same sanity gate (`harness_error 0`, keep-alive socket count ~1–2, min-RTT floor,
outcome taxonomy), **n ≥ 30**. The **min-RTT floor is re-measured locally per vantage** (normalizes the
localhost transport per host). Record the topology in the sample/pilot-log `topology` field.

- **Network-dependent (the point):** Solana-A, Stellar-A, Base-A, Lightning-B. (Buyers funded.)
- **Local control:** ≥1 local-402 B + Tempo-A (warm, `--sleep <5s`) + a note that AP2 is invariant.
- Run commands per rail: see `dim2-first-run-validate.md` (identical, just on the new host).

## Expected outcome / how to read it

- **Pass:** within the A network group the T1 order holds (Solana ≈ Stellar < Base, or whatever T1 gave);
  local ≪ network in both A and B; Lightning ≫ local-402. The local-crypto rails barely move (control OK).
- **Absolute network numbers shift** — expected; not a failure.
- **A within-group pair FLIPS** (e.g. Solana↔Stellar reverse across topology) → a genuine FR4 finding: that
  pair is **not separable across topology** → report as a **tie / topology-sensitive** (feeds FR1 tie
  handling; the Davidson ties extension + the rank-stability heatmap absorb it).
- **A local rail moves a lot** → harness/host problem (e.g. keep-alive broke, noisy neighbour) → investigate
  before trusting the network numbers from that host.

## Scoring / write-back (the gate)

After T2a (quick) **and** T2b (citable), the network-dependent numbers move from *indicative* to **scored**
(D4e); write the real `{median, P95, P99}` per the **group-and-decompose** tuple (DR4 §2.5.1) into the
placeholder provenance. **Only then** is the dim-2 doctrine ready for the **pre-registration ceremony**
(`CEREMONY-RUNBOOK.md` dim-2 pass). Record T2a/T2b as a second + third block in `dim2-q4-pilot-log.md`.
