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

> **UPDATE — blocker-fixed re-measurement, 2026-06-24 (`measure_rapl_ap2_full.py`):** the measurement
> review found the old 1.68 ms timed window included per-trial PEM reads + SDK log-writes (blockers
> #1/#2). Fixed (keys/provider pre-loaded once; `_log_event` no-op'd → crypto-only window) and re-run on
> a fresh capture (n=30):
>
> | mode | n | median (raw) | σ_log | p99 |
> |---|---|---|---|---|
> | **issuer-signature-only (1 ES256)** | 30 | **0.00068 s (0.68 ms)** | **0.023** | 0.75 ms |
>
> - The clean number is **0.68 ms vs the contaminated 1.68 ms (~2.5× inflation)**, and **σ_log
>   0.14 → 0.023 (~6× tighter)** — the disk I/O the review flagged was real and material. Makes AP2's A
>   even more extreme vs x402 (0.68 ms vs 400–777 ms) — *reinforces* the A-heterogeneity finding.
> - **FINDING — the AP2 human-present CARD flow verify is ISSUER-SIGNATURE-ONLY.** The fresh capture
>   (driven through the cards flow, both MPP + CP hooks) has **no key-binding JWT** (empty trailing `~`)
>   and an **empty `checkout_jwt_hash`** — so the aud/nonce binding is never enforced; the real verify is
>   1 ES256 check. The founder-chosen **2-check "full verify"** (issuer + holder KB) does **not** occur in
>   this flow — it requires AP2's **DPC / delegated `~~`-chain** scenario (a different flow). So the
>   earlier "full verify" decision rested on an assumption the evidence overturns.
> - Pin: AP2 capture via the cards flow; signing key from the run's `.temp-db`. Independent re-review
>   before scoring. The capture artifact `captured-kb.json` is gitignored.

> **UPDATE 2 — DPC chain (2-check) captured + measured, 2026-06-24.** The 2-check "full verify" the
> founder chose is NOT in the human-present cards flow — it's the **human-not-present / delegated (DPC)**
> flow (MCP roles, `merchant_payment_processor_mcp/server.py:250`, `token=payment_mandate_chain`). Drove
> that scenario (web-client + price-drop trigger), captured a real `~~` chain (2 hops, nonce len 20) and
> measured it (harness matches the MCP's plain-key-lambda verify; agent-provider key is a JWK-JSON from
> the HNP run's `.temp-db`):
>
> | AP2 mode | verify | n | median (raw) | σ_log | p99 |
> |---|---|---|---|---|---|
> | **human-present** (issuer-only) | 1 ES256 | 30 | **0.68 ms** | 0.023 | 0.75 ms |
> | **delegated / DPC** (chain) | 2 ES256 (issuer + holder KB) | 30 | **1.58 ms** | 0.020 | 1.74 ms |
>
> - The 2-check is **~2.3× the 1-check** (0.68 → 1.58 ms) — consistent with one extra ES256 verify +
>   chain parse/binding. Both tight (σ_log ~0.02), blocker-fixed (crypto-only window).
> - **AP2 has TWO authorization variants**, both local-crypto, both ≪ x402 (400–777 ms) — A-heterogeneity
>   unchanged/reinforced. For an *agentic* benchmark the **DPC/delegated (1.58 ms)** is arguably the more
>   representative headline (autonomous agent acting on a delegated credential), with human-present
>   (0.68 ms) as the user-signs-each-purchase variant.
> - **Founder decision (lighter now — we have both numbers):** report AP2 as **two variants** (rec) and
>   pick which is the headline, OR collapse to one. Feeds DR4 (AP2 itself spans two work-modes within the
>   local-crypto class). Pin the AP2 commit; independent re-review before scoring.

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
| AP2 — human-present (1 ES256) | **0.68 ms** | **local crypto** (in-process; blocker-fixed) |
| AP2 — delegated/DPC (2 ES256) | **1.58 ms** | **local crypto** (in-process; blocker-fixed) |
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
- **pure local crypto:** AP2 (blocker-fixed: 0.68 ms human-present / 1.58 ms delegated-DPC, in-process).
- **local crypto + periodic RPC refresh:** Tempo-Session (~19.5 ms warm; ~360 ms on the ~5 s TTL tick).
- **backing-service round-trip every call:** x402-Solana 400 ms / Stellar 464 ms / Base 777 ms.
Reinforces (does not change) the 2.5 work-type-disclosure recommendation - but the disclosure taxonomy
needs a THIRD bucket ("amortized/periodic backing-service"), not just local-vs-network. Founder review.

## FR4 TOPOLOGY-2 — T2a GitHub Codespaces (Azure), 2026-06-24

First second-topology pass (`poc/topology2/run-topology2.sh`, `TOPOLOGY=T2a-codespaces`). 30/30 ok, 0
rejected on all rails that ran (buyers funded, same wallets, different host). **Verdict: the RANKING
HOLDS — FR4 pass on T2a** (T2b/OCI still pending for the citable point).

### Sub-ranking A (network-dependent) — the test

| Rail | T1 devbox median | T2a Codespaces median | T2a p95 / p99 | order |
|---|---|---|---|---|
| x402-Solana | 400 ms | **180 ms** | 257 / 300 ms | 1st (both) |
| x402-Stellar | 464 ms | **364 ms** | 631 / 754 ms | 2nd (both) |
| x402-Base | 777 ms | **420 ms** | 494 / 521 ms | 3rd (both) |

**Order preserved: Solana < Stellar < Base at BOTH topologies.** Absolute numbers compressed (Azure host
is closer to the facilitators/RPC than devbox); Solana dropped most proportionally (×0.45). The *spacing*
shifted but the *order* (the FR4 question) is robust. → **A ranking robust to topology.**

### Sub-ranking B

- **Lightning (network, invoice-mint):** 936 ms (T1 n=30) → **771 ms** (T2a), p99 1357 ms — still ≫
  local-402; B heterogeneity holds.
- **local-402 (Base/Solana/Stellar/Tempo-B):** **medians ~invariant** (Base 4.6 / Solana 3.7 / Stellar 3.0
  / Tempo-B 2.88 ms vs T1 ~2–3 ms — control passes on the median) **BUT tails EXPLODED**: σ_log **0.05 →
  ~0.45–0.91**, p99 up to **20–63 ms** (vs T1 ~2–3 ms tight). **Cloud-host CPU-scheduling jitter** (shared
  Azure VM vs dedicated devbox).
- **Tempo-A (local-crypto control, session voucher):** **19.5 ms (T1) → 11.2 ms (T2a)** — the median
  *moved*, because Tempo-A is a **compute-heavy** local primitive (EIP-712 + secp256k1 + 2 localhost
  round-trips), so the faster/less-loaded Codespace CPU lowers it (its min-RTT floor was also lower, 0.66 vs
  1.2 ms). Still ≪ the x402 A's (180–420 ms) → the **local ≪ network** group separation holds.

### NEW FINDING (refined) — LOCAL rails are HOST-sensitive; NETWORK rails are PATH-sensitive
Network primitives move in the **median** (the route changed). Local primitives get no network-path penalty
but ARE host-sensitive, in two modes: (i) **tiny** local primitives (402 emit ~3 ms) keep a ~invariant
median (round-trip-floor-bound) while their **tails** fatten ~10–20× on a shared cloud host (scheduling
jitter); (ii) **compute-heavy** local primitives (Tempo-A ~11–19 ms) have a **median that also tracks CPU
speed** (19.5→11.2 ms). **Diagnostic: network → median tracks PATH; local → tail tracks host SCHEDULING,
and (compute-heavy) median tracks host CPU.** Implication for §2.5/DR4: D4a's P95/P99 is essential; the
decomposition (D4b) should split host-CPU/scheduling from the rail's compute floor; and **local rails'
absolute numbers are NOT portable across hosts** — report per-host (a reason D4e wants ≥2 topologies even
though the local *ranking* is robust).

### Issues / gaps
- **Tempo ran after the `MPP_SECRET_KEY` driver fix** (setup-accounts.ts omits it — a manual SETUP step;
  driver now appends a fresh one). Tempo-A 11.2 ms / Tempo-B 2.88 ms, 30/30 ok. (First T2a attempt failed
  to boot — fixed.)
- Socket connects 3 on Solana/Lightning/Tempo-A (≈ ok; the local tail noise is host jitter, not a pooling
  break — medians confirm pooling held).
- AP2 invariant by construction (skipped) — use the devbox 0.68 / 1.58 ms.

**Status:** T2a (Codespaces) = **ranking robust** (A order held Solana<Stellar<Base; B heterogeneity held;
local ≪ network preserved) + the refined **host-sensitivity** finding (local→host CPU/scheduling,
network→path). All rails ran (Tempo after the driver fix). **Pending: T2b (OCI named region)** — the citable
topology-2. Still pilot, not scored, until T2b lands.

## FR4 TOPOLOGY-2 — T2b OCI uk-london-1 (AMD/x64), 2026-06-28

The citable named-region topology. Always-Free **A1 (ARM)** was capacity-blocked in uk-london-1 (London
A1 is scarce) → pivoted to a paid **VM.Standard.E5.Flex x64** (`payhelm-dim2-e2`, 2 OCPU/12 GB) in the SAME
region; ran the driver via `git archive` of the branch (devbox working tree was on `main`). All 5 rails ran.

### Sub-ranking A — three-topology comparison (the FR4 test)

| Rail | T1 devbox | T2a Codespaces | T2b OCI London | order |
|---|---|---|---|---|
| x402-Solana | 400 ms | 180 ms | **212 ms** | 1st (all 3) |
| x402-Stellar | 464 ms | 364 ms | **289 ms** | 2nd (all 3) |
| x402-Base | 777 ms | 420 ms | **492 ms** | 3rd (all 3) |

**Order HOLDS across all three topologies: Solana < Stellar < Base.** Absolute numbers shift with the
egress path (London differs from devbox + Azure), but the *order* — the FR4 question — is invariant. → **A
ranking robust to topology, confirmed from a third network-distinct path.**

### Sub-ranking B
- **Lightning (network):** 936 (T1) → 771 (T2a) → **552 ms** (T2b) — faster from London (closer to the
  Spark operators), still ≫ local-402. Heterogeneity holds at every topology.
- **local-402 (Base/Solana/Stellar/Tempo):** ~1.6–2.2 ms — invariant median (host-jitter tails, as T2a).

### Local control
- **Tempo-A:** 19.5 (T1) → 11.2 (T2a) → **8.2 ms** (T2b) — keeps dropping with a faster host CPU (E5 London
  is quick), confirming the **compute-heavy-local = CPU-sensitive median (host, not path)** finding. Still
  ≪ the x402 A's (212–492 ms): **local ≪ network holds.** AP2 invariant (skipped).

### Stellar "censoring" — RE-CHECKED 2026-06-28: it was a HARNESS bug, NOT real censoring → FR1 does NOT fire
The T2b run showed Stellar A 26/30 ok / 4 "rejected" (13.3%), which *looked* like the first FR1 trigger
crossing. **The re-check overturns that.** Added reject-reason capture to the harness and re-ran from
**devbox** (n=100): **12% "rejected", ALL with the same reason `invalid_exact_stellar_payload_auth_expiration_too_far`** —
i.e. the **OZ facilitator rejecting our own malformed payload** (the Soroban auth expiration lands beyond
OZ's allowed window), **not** a payment decision (funds/signature). So:
- It is **NOT transient** and **NOT London-specific** — it reproduces ~12–43% on **every** vantage (the
  earlier "transient OZ" read was wrong).
- It is an **instrumentation bug → reclassified as `harness_error`** (the harness now matches
  `expiration|malformed|…` reasons and counts them as harness_error, NOT `rejected`). **FR1 censoring →
  0.0%.** So **FR1 does NOT fire for Stellar** — the "trigger" was self-inflicted by the payload builder.
- **Lever found NOT to work:** `maxTimeoutSeconds` (server *and* client-side) does **not** control it — the
  reject rate is *insensitive* to it (12%/25%/43% across attempts), pointing to a **client↔OZ ledger-view
  race** in `@x402/stellar` on this testnet facilitator, not a window-size issue.
- **OPEN (engineering, not methodology):** to get a **clean Stellar scored run (`harness_error = 0`)**,
  add a **retry-on-construction-error** (re-fetch challenge + rebuild payload until OZ accepts) or pin a
  facilitator/RPC that shares OZ's ledger view. The successful 75–88% of trials give the **clean A median
  (~0.44 s, unchanged)** — the latency number is unaffected; only the yield is. Commit: `1f6acc0`
  (reject-reason capture + reclassification).

### Verdict — FR4 SATISFIED
Across **T1 + T2a + T2b** (three network-distinct vantages, incl. the citable named region uk-london-1):
A order robust (Solana<Stellar<Base ×3), B heterogeneity robust, local ≪ network preserved. **Per D4e the
network numbers move from *indicative* → eligible to be SCORED** (≥2 topologies met). Caveats to carry into
the scored/pre-reg pass: report the **per-topology spread** (absolute medians are path-dependent), **re-check
Stellar censoring**, and local rails are **host-dependent** (report per-host). Bonus A1 (ARM) still pending
(free). The E5 VM is PAID — terminate after the artifact pull (done: `results-T2b-oci-e2/`, 20 files).
