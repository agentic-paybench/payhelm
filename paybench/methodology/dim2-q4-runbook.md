# Dim-2 (RAPL) — Q4 validation/calibration RUNBOOK

**Credentialed founder step.** This is the step-by-step for the Q4 validation run that (1) pilots the
FR1 fallback thresholds + power analysis and (2) replaces the PLACEHOLDER auth-latency fixtures with
real `{median, sigma}`. Pairs with `dim2-validation-run-plan.md` (the plan) and the adapter code on
the `dim2-rapl-instrumentation` branch of `mblake4u/agentpay`. **Nothing here runs until you, the
founder, execute it with credentials.**

## 0. Before you start — preconditions
- [ ] **Decide the AP2 (R6) path** — there is **no AP2 POC adapter** in `poc/`. Either build one, or
      source AP2 calibration from docs/telemetry (placeholder stays). R6 is **not** measurable by this
      runbook as-is. (See §"Per-rail status".)
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
  shape (see §"Per-rail status").

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
| **R9 x402-Solana** | `rail-solana-x402` (TS, Express, **hosted** facilitator) | ⏳ to fan out | clean mirror — add `/rapl/verify` proxy + `/rapl/rtt` + `measure_rapl.ts` |
| **R2 x402-Stellar** | `rail-stellar-x402` (TS, Express, hosted) | ⏳ to fan out | mirrors Solana |
| **R10 MPP-Tempo** | `rail-tempo-mpp` (TS, `route()` handler) | ⏳ rail-specific | **Charge excluded**; Session-only accept; non-Express shape |
| **R11 MPP-Spark-Lightning** | `rail-lightning-mpp` (TS, `route()`) | ⏳ rail-specific | **B only** (macaroon+invoice issuance); `rail-lightning-l402/` is empty |
| **R6 GCP+AP2** | **none in `poc/`** | ❌ blocked | build an AP2 adapter or doc/telemetry-source — founder decision |
