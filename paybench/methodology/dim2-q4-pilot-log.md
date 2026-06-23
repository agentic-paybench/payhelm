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

## R6 GCP-AP2 — 2026-06-23 (run-validated ✅, via capture-replay)

First first-party AP2 measurement. The interactive cards run (Google's AP2 reference impl, founder
drove a purchase with the Gemini key) produced a **signed PaymentMandate SD-JWT**, which the LLM-free
harness (`poc/rail-ap2/measure_rapl_ap2.py`) **replayed through `_verify_payment_mandate` n=30**.

| Sub-ranking | primitive | n | median (raw) | σ_log |
|---|---|---|---|---|
| **A — Payment-Validation** | PaymentMandate SD-JWT verify (ES256) | 30 | **0.00168 s (1.68 ms)** | 0.14 |

- **Outcomes:** ok 30 / rejected 0 / harness_error 0. **FR1 censoring-rate = 0%.**
- **AP2 is in-process** (no HTTP, no chain RPC, no settlement) → **A only** (no Sub-ranking B / no 402
  challenge), **no RTT floor**, **dispatch decomposed out**, **scope = whole rail**.

### Findings from the live run
- The cards flow **failed at the MPP/dispatch step on a Gemini free-tier 429** (15 req/min), **not**
  the OTP (`123` was correct). Dispatch is the decomposed-out hop, so this did not block the capture —
  the signed mandate is produced upstream of it.
- **The timed primitive is the mandate *verify* (real local ES256 crypto), not verify→issue.** The
  credential-issuance lookup (`account_manager`) needs the live CP's per-process state (absent in a
  fresh harness) and is a negligible mock dict lookup → **excluded + disclosed** (like the dispatch
  hop). The `checkout_jwt_hash` nonce isn't exposed in the trace; the no-nonce verify path is the one
  the live flow ran. **So AP2's number is authorization-LOGIC latency** (ES256 SD-JWT verification),
  excluding any production issuer round-trip — disclose this, alongside the whole-scope tag.

**Caveats:** mock-issuance excluded (above); pin the AP2 repo commit; **review** (independent
measurement review) like Base/Solana before calibration write-back. Pilot data only — not the scored set.
