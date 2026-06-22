# Dim-2 (RAPL) — Q4 pilot log

**Pilot data, NOT calibration.** Records first-party RAPL pilot runs as they happen. These inform the
FR1 fallback thresholds + the real `{median, sigma}` write-back, but are **not** frozen calibration
until multi-topology (FR4 ≥2 locations) + all rails + the FR1 confirmation are done. Do not write
these into provenance yet.

## R1 x402-Base — 2026-06-22 (run-validated ✅)

First live run of the review-fixed Base reference (`measure_rapl.py`, branch
`dim2-rapl-instrumentation`). **Instrumentation validated end-to-end** — the runtime checks that
could not be exercised at draft time all passed: `harness_error=0`, 30/30 `ok`, keep-alive pooling
(min-RTT floor 2.03 ms stable), `isValid=true`, fresh nonce per trial.

| Sub-ranking | primitive | n | median (raw) | σ_log | corrected median |
|---|---|---|---|---|---|
| **A — Payment-Validation** | facilitator `/verify` accept | 30 | **0.777 s** | 0.016 | 0.775 s |
| **B — Challenge-Issuance** | `GET /resource` → 402 | 30 | **0.0030 s** | 0.077 | 0.00096 s |

- **Outcomes:** ok 30 / rejected 0 / timeout 0 / harness_error 0. **FR1 censoring-rate = 0%.**
- Env: devbox, localhost server (port 8082, keep-alive), facilitator **in-process** → Base Sepolia
  **remote RPC** (`BASE_SEPOLIA_RPC_URL`). Single topology.

### Key finding — the accept is RPC-dominated, not crypto-dominated
777 ms with σ_log 0.016 (extremely tight) is **not** signature verification (sub-ms local crypto) —
it is the facilitator's **fresh balance read + `eth_call` simulation round-trips to the Base Sepolia
RPC** (the RR5/FR2 work-clause). i.e. A's number ≈ a fixed count of server→chain-RPC round-trips.
Implications for the methodology:
- The accept latency for a **chain-backed facilitator** is **bound by RPC-endpoint latency**, which
  is provider/region-dependent → **§2.5 network-normalisation should arguably extend to the
  server→RPC hop**, or at minimum the **RPC endpoint must be disclosed/pinned** per rail (a different
  RPC gives a different A number). Flag for founder review.
- The **challenge (B) is local** (~3 ms, no RPC) — and here the **min-RTT floor matters** (2 ms floor
  vs 3 ms signal → 0.96 ms corrected), exactly the regime the S1 fix targets; the correction is
  negligible for the 777 ms accept, as intended (no over-correction).
- **FR1 read (Base only):** censoring 0%, σ tiny, ties improbable → the BT→Cox-PH fallback would
  **not** fire on Base. (FR1 is a *cross-rail* decision — pending the other rails.)

**Status:** Base reference **run-validated**; safe to fan out the (review-fixed) pattern. Real
calibration write-back deferred (needs ≥2 topology + the other rails + FR1 confirmation).
