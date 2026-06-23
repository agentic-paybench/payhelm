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

## R10 MPP-on-Tempo — 2026-06-23 (run-validated ✅, Sub-ranking B only)

First live run of the R10 B harness (`rail-tempo-mpp/src/measure-rapl.ts`, branch
`dim2-rapl-instrumentation`). Server booted on :8404 (Moderato 42431, keyless-funded seller); unpaid
`GET /data` → 402. **Gate passed:** harness_error 0, socket connects **2** (keep-alive pooled),
min-RTT floor 1.68 ms, 30/30 `ok`.

| Sub-ranking | primitive | n | median (raw) | σ_log | corrected median |
|---|---|---|---|---|---|
| **B — Challenge-Issuance** | `GET /data` → 402 (MPP charge challenge) | 30 | **0.00295 s (2.95 ms)** | 0.14 | 0.00127 s |

- **Outcomes:** ok 30 / timeout 0 / harness_error 0. **FR1 censoring-rate = 0%.**
- **A (Tempo-Session) not run** — adapter not built (deferred founder decision). Tempo-Charge fuses
  verify+settle → excluded from A (RR1).
- **Finding:** Tempo's B is a **local template emit** (~3 ms, no node hop) — ≈ x402-Base's local 402.
  Confirms Base's B regime, and sets up the contrast with R11 below.

## R11 MPP-on-Lightning (Spark) — 2026-06-23 (run-validated ✅, Sub-ranking B only)

First live run of the R11 B harness (`rail-lightning-mpp/src/measure-rapl.ts`). Server on :8411 (Spark
regtest); unpaid `GET /data` → 402 carrying a freshly-minted BOLT11 invoice. **Gate passed:**
harness_error 0, socket connects **2**, min-RTT floor 1.20 ms, 15/15 `ok`.

| Sub-ranking | primitive | n | median (raw, warm) | σ_log | corrected median |
|---|---|---|---|---|---|
| **B — Challenge-Issuance** | `GET /data` → 402 (mint BOLT11 invoice via Spark) | 15 | **1.252 s** | 0.12 | 1.251 s |

- **Outcomes:** ok 15 / timeout 0 / harness_error 0. **FR1 censoring-rate = 0%.** (n=15 for a quick
  instrument-validate; each trial pays a real Spark round-trip. Scale n later for calibration.)
- **Cold-start:** the very first unpaid `/data` took **10.2 s** (lazy Spark wallet init) — absorbed by
  the harness warmup; the warm steady-state is ~1.25 s and tight (σ_log 0.12).
- **min-RTT floor (1.2 ms) is negligible vs the signal** — the correction removes only the localhost
  HTTP hop, NOT the intrinsic invoice-mint, exactly as designed (no over-correction).

### Headline — heterogeneous-B is now PROVEN with data (founder doctrine question)
Within Sub-ranking B: **Tempo 2.95 ms vs Lightning 1252 ms — a ~420× gap** for the *same* "issue a
payable challenge" primitive. This is not noise and not a bug: Tempo emits a local 402 template, while
Lightning must **mint a BOLT11 invoice** (a Spark/LND round-trip). Both are the genuine
challenge-issuance work for their rail (RR5/FR2 work-clause), so neither number is "wrong."

**But it forces a doctrine decision** (parallel to the original A/B category-error the cross-lineage gate
caught): is **Sub-ranking B a single valid race with per-rail disclosure** (work-clause owns the gap —
"issuing a Lightning challenge genuinely costs an invoice-mint"), **or does B need a further split**
(local-issuance vs backing-service-issuance) so we don't rank "has a local 402" against "must mint an
invoice"? **Recommendation:** keep B as one race but **mandate per-rail disclosure of the issuance
work-type** (local-emit vs node-round-trip) in §2.5, and report the backing-service hop as a diagnostic
(as for Base's A→RPC). Surface to founder before pre-reg — this is a ratify-level call, not autonomous.
