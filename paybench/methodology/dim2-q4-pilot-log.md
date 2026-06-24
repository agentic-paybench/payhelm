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

> **UPDATE — n=30 re-run, 2026-06-24 (measurement-review action + DR4 tail mandate):** 30/30 ok,
> censoring 0%. **median 936 ms (lognormal), p50 850 ms, p95 1113 ms, p99 1487 ms, σ_log 0.157.** The
> median **shifted ~25% from the n=15 run (1252 ms → 936 ms)** — direct evidence for the cross-lineage
> panel's n-adequacy + tail concern (round 4): the network-bound rail's median is run-to-run unstable and
> the p99 (~1.5 s) is well above the median. Reinforces DR4 — report P50/P95/P99 (not median-only) and
> the ≥2-topology mandate; treat the single-topology median as indicative, not a point estimate.
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

## R2 x402-Stellar — 2026-06-23 (run-validated ✅, Sub-ranking A + B)

First live run of the R2 harness (`rail-stellar-x402/src/measure-rapl.ts`). Server :8403 (testnet);
buyer pre-checked funded via Horizon (USDC 19.97, trustline to the testnet issuer). **Gate passed:**
harness_error 0, **rejected 0** (funding sufficient — OZ `/verify` accepted), socket connects 2,
min-RTT floor 1.23 ms, 30/30 `ok`.

| Sub-ranking | primitive | n | median (raw) | σ_log | corrected median |
|---|---|---|---|---|---|
| **A — Payment-Validation** | OZ hosted facilitator `/verify` accept | 30 | **0.464 s** | 0.089 | 0.463 s |
| **B — Challenge-Issuance** | `GET /data` → 402 | 30 | **0.0022 s (2.2 ms)** | 0.052 | 0.00097 s |

- **Outcomes:** ok 30 / rejected 0 / timeout 0 / harness_error 0. **FR1 censoring-rate = 0%.**
- A is the **OZ hosted-facilitator network round-trip** (the real authorization work for a hosted-
  facilitator rail); B is a **local 402 emit** (joins Base/Tempo ~2–3 ms).

## R9 x402-Solana — 2026-06-23 (run-validated ✅, Sub-ranking A + B)

First live run of the R9 harness (`rail-solana-x402/src/measure-rapl.ts`). Server :3402 (devnet); free
`x402.org/facilitator` (no key). **Gate passed:** harness_error 0, **rejected 0** (buyer devnet USDC
sufficient), 30/30 `ok`. Minor: socket connects **3** (one recycle mid-burst; ≪ trial count, so pooling
held — acceptable, not the broken regime).

| Sub-ranking | primitive | n | median (raw) | σ_log | corrected median |
|---|---|---|---|---|---|
| **A — Payment-Validation** | x402.org facilitator `/verify` accept | 30 | **0.400 s** | 0.131 | 0.398 s |
| **B — Challenge-Issuance** | `GET /data` → 402 | 30 | **0.0022 s (2.2 ms)** | 0.051 | 0.00098 s |

- **Outcomes:** ok 30 / rejected 0 / timeout 0 / harness_error 0. **FR1 censoring-rate = 0%.**

## SYNTHESIS — full single-topology sweep complete (all 6 rails) · 2026-06-23

Every rail now has run-validated pilot data on one topology (devbox, localhost servers). Two findings
generalize across the whole set:

| Sub-ranking A (Payment-Validation) | median | kind |
|---|---|---|
| AP2 (ES256 SD-JWT verify) | **1.68 ms** | **local crypto** (in-process) |
| x402-Solana (`/verify`) | 400 ms | facilitator network round-trip |
| x402-Stellar (OZ `/verify`) | 464 ms | facilitator network round-trip |
| x402-Base (`/verify`) | 777 ms | facilitator → chain-RPC round-trips |

| Sub-ranking B (Challenge-Issuance) | median | kind |
|---|---|---|
| x402-Solana 402 | 2.2 ms | **local emit** |
| x402-Stellar 402 | 2.2 ms | **local emit** |
| x402-Base 402 | 3.0 ms | **local emit** |
| MPP-Tempo 402 | 3.0 ms | **local emit** |
| MPP-Lightning 402 | **1252 ms** | mint BOLT11 invoice (Spark round-trip) |

**The heterogeneity is in BOTH sub-rankings, not just B.** Each race spans a *local-logic* member and
*backing-service-round-trip* members:
- **A:** AP2 (local ES256, 1.68 ms) vs the x402 rails (facilitator network, 400–777 ms) — a ~250–460× gap.
- **B:** the four local-402 rails (~2–3 ms) vs Lightning (invoice-mint, 1252 ms) — a ~420× gap.

So the doctrine question raised under R11 is **not Lightning-specific** — it's the general shape of
RAPL: within a sub-ranking, the work-clause spans pure-local-crypto vs an intrinsic backing-service hop
(facilitator, chain-RPC, or Lightning node). **Recommendation (unchanged, now generalized):** keep each
sub-ranking as one race, but **§2.5 must mandate a per-rail "work-type" disclosure** (local vs
backing-service) and report the backing-service hop as a published diagnostic — NOT subtracted (it is
the real authorization work). This is the headline Q4 result for founder review at pre-reg. Still pilot
data: single topology; needs the FR4 ≥2-location pass + independent measurement review before any
calibration write-back.

## R10b MPP-on-Tempo SESSION — 2026-06-24 (run-validated, Sub-ranking A)

First live run of the Tempo-Session A harness (`rail-tempo-mpp/src/measure-rapl-session.ts`). The Charge
intent fuses verify+settle, so Tempo joins A via the **session** intent: open an on-chain channel ONCE
(not timed), then time the per-request **voucher** accept. Channel opened on Moderato (`0x148131c8...`),
20/20 ok, 0 rejected. Gate passed: harness_error 0, censoring 0%.

| Sub-ranking | primitive | n | median (raw, warm) | sigma_log | corrected |
|---|---|---|---|---|---|
| **A - Payment-Validation** | session voucher accept (EIP-712 sign + secp256k1 verify) | 20 | **0.0195 s (19.5 ms)** | 0.053 | 0.0184 s |

- **Outcomes:** ok 20 / rejected 0 / timeout 0 / harness_error 0. **FR1 censoring-rate = 0%.** (n=20
  fast-burst; the n=10 validation run was also clean.)
- **KEY FINDING - Tempo-A is local-crypto with a PERIODIC RPC refresh.** The voucher accept is local
  (EIP-712 + secp256k1, no per-call RPC) - but the server caches on-chain channel state for
  `channelStateTtl` (~5 s); when it expires it re-reads on-chain (one RPC hop). The `--sleep 1` run showed
  this exactly: trials 1-5 ~ 22 ms, trial 6 = **359 ms** (TTL expiry -> RPC), then re-cached. A fast burst
  (`--sleep 0`, whole run inside one TTL window) removed all spikes -> 19.5 ms, sigma_log 0.053. So
  **Tempo-Session sits BETWEEN AP2 (pure in-process, 1.68 ms) and x402 (RPC every call, 400-777 ms):
  local-crypto accept + amortized periodic RPC** - a novel third class.
- **CAVEAT (harness, disclosed):** the mppx SessionManager does 402-then-retry per request, so the
  ~19.5 ms window includes the challenge hop + 2 localhost round-trips (every trial `saw_challenge=true`),
  NOT the bare voucher verify. To isolate the verify, subtract the B challenge median (~3 ms) + one
  localhost hop, or build a low-level single-hop voucher-POST harness. **So 19.5 ms is an UPPER BOUND on
  the Tempo voucher accept; the bare verify is smaller.** Independent measurement review before scoring.

### SYNTHESIS UPDATE - Sub-ranking A now has THREE classes
With Tempo-Session, A is no longer a clean local-vs-network dichotomy:
- **pure local crypto:** AP2 (1.68 ms, in-process; being re-measured per the measurement review).
- **local crypto + periodic RPC refresh:** Tempo-Session (~19.5 ms warm; ~360 ms on the ~5 s TTL tick).
- **backing-service round-trip every call:** x402-Solana 400 ms / Stellar 464 ms / Base 777 ms.
Reinforces (does not change) the 2.5 work-type-disclosure recommendation - but the disclosure taxonomy
needs a THIRD bucket ("amortized/periodic backing-service"), not just local-vs-network. Founder review.
