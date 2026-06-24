# DRAFT — Dimension 2: Authorization Latency (PROPOSED, not adopted)

> **STATUS: DRAFT / PROPOSED — for founder review. NOT part of the frozen
> methodology.** This is a separate, clearly-marked proposed section, written
> alongside the dimension-2 harness build (Session 1). It does **not** amend the
> pre-registered, Bitcoin-anchored `methodology.md` v1.2, and nothing here is
> pre-registered. Every per-rail number referenced is a **PLACEHOLDER**
> (`TODO(calibration)`); the per-rail *doctrine* below is **proposed, not
> ratified** — finalising it is a founder decision (see §"Open questions"). It
> deliberately stops short of the four tripwires for this session: it does not
> touch frozen v1.2 artefacts, does not pre-register, does not finalise the
> per-rail reliance doctrine, and commits no real calibration numbers.

This addendum proposes how **authorization latency** — the methodology roadmap's
**Day-30, Tier-1** dimension (§11), and the dimension on which **AP2 (R6) debuts**
(§8, Resolution B) — would be operationalised, by analogy to the settlement-finality
template (§3). The harness already implements the mechanical extension; this
document is the methodology side that a founder must complete and ratify before
any pre-registration.

## 1. What "authorization latency" measures

> **Renamed post-gate (DR2): _Rail Authorization-Primitive Latency_ (RAPL)** — provisional; alt
> "Protocol-Accept Latency". It measures a rail/protocol *primitive*, not an agent-perceived
> latency. A co-primary **agent-observed total-latency** metric is reported alongside (§2.5).
> "Authorization latency" is kept below as the descriptive gloss.

**Proposed definition.** Authorization(-primitive) latency is the wall-clock time from the agent
issuing its **pay command** (the payment payload constructed and on the wire — the standardised
`t = 0`, §2.5) to the point the rail returns an **authorization-primitive decision** — i.e. "this
payment/mandate is validated / this payable grant is issued" — **prior to and distinct from
settlement finality** (§3). The *kind* of decision differs by rail, which is why the dimension is
**split** into validation-type and grant-type sub-rankings (§2).

Where settlement-finality (§3) answers *"when can I rely on this payment as
irreversible?"*, authorization latency answers *"how fast does this rail tell me
the payment is allowed to proceed?"* — the gate an agent hits *before* it commits
to a rail. The two are complementary Tier-1 timing dimensions on the same six
rails (§11).

**Unit.** Seconds, wall-clock, intent-presented → authorization-granted signal
(per-rail this may be an HTTP 200 on a verify/accept call, a mandate-verified
response, or an invoice-issued event). As with §3, the rail's protocol/HTTP
envelope is bundled in, because that is what the agent actually waits on.

**Direction.** Lower is better (same as finality). The race semantics are
therefore identical and the existing BT/pass@k/Wilson machinery applies unchanged
(see §4).

## 2. Per-rail operationalisation — the SPLIT design (revised post-gate, evidence-grounded)

> **REVISED post-gate (2026-06-22), DR1–DR3 adopted.** The §8 cross-lineage gate
> (`dim2-adversarial-review.md`) **refuted the single-race doctrine 0–4** and found the L402
> pin a **category error**. §2 below is the **rewritten SPLIT design** that resolves it. The
> pre-gate single-race draft is preserved in git history + the review doc. Adopted founder
> decisions: **DR1 SPLIT** (payment-validation vs permission-grant sub-rankings), **DR2 rename**
> (rail-*primitive* latency + an agent-observed companion metric), **DR3** (Tempo Charge/Session
> bifurcation, standardised `t=0`, ms k-ladder, AP2 auth-only tag, network normalisation).
> **Rounds 2–3 (2026-06-22) — SPLIT validated 3–1, then PRE-REGISTERABLE (4/4).** Round 2 endorsed
> the SPLIT + a refinement list (**RR1–RR6**, folded in); round 3 confirmed the as-built design is
> **pre-registerable** conditional on a small fix-list (**FR1–FR5**, also folded in): FR1 numeric
> fallback triggers, FR2 RR5-clause restricted to Group A, FR3 last-byte stopwatch, FR4 same-path
> RTT baseline, FR5 main-text Charge disclosure. **Status: ready for founder ratification →
> pre-registration** (still DRAFT until the founder ratifies). Full arc + verdicts:
> `dim2-adversarial-review.md`.

**Dimension renamed (DR2): _Rail Authorization-Primitive Latency_ (RAPL)** — provisional;
alt "Protocol-Accept Latency". The rename is load-bearing: the metric times a rail/protocol
**authorization primitive**, *not* an agent-perceived latency (the accept is facilitator/server-
side, and on fused topologies an agent never sees it pre-settlement — §2.5/G1). A **companion
agent-observed total-latency** metric is reported alongside (DR2; §2.5).

**The dimension is SPLIT (DR1)** because authorization is *not one shared concept* across these
rails — the gate showed (0–4) that racing them together is a category error. Each rail is raced
**only against rails whose authorization point is the same kind of object**:

A rail is measured on **whichever primitive(s) it actually has**, and raced only within a
sub-ranking. The x402 rails have *both* a challenge-issuance and a validation primitive, so they
appear in both A and B (two distinct, separately-measured quantities); L402 has only a
challenge-issuance primitive (no pre-settlement validation), so it appears only in B; AP2 has only
a validation primitive (no 402 challenge), so only in A.

**Sub-ranking A — Payment-Validation Authorization** (the primitive *validates a payment/mandate the
payer has submitted*). Raced within-group → C(5,2)=10 pairs. **Tempo-*Charge* is excluded** from the
raced set (RR1): its verify+settle are fused at ~500 ms, so racing it would measure settlement, not
authorization. The exclusion is stated **here in the main text** (not buried — FR5), with a
**developer-facing note**: a one-shot 1-RTT *Charge* flow does **not** inherit the Group-A latency
profile (Session does); Charge's fused ~500 ms is reported in an appendix, not ranked.

| Member | Validation primitive (validates submitted payment/mandate) | Trust / equivalence class · visibility |
|---|---|---|
| x402-Base (R1) | Facilitator `/verify` of the signed EIP-3009 payload (off-chain) | payer-signed-payment validation · client-visible: spec yes / fused no |
| x402-Stellar (R2) | Facilitator `/verify` (Soroban auth-entry signatures, simulate) | payer-signed-payment validation · client-visible: spec yes / fused no |
| x402-Solana (R9) | Facilitator `/verify` of the signed SVM payload (**earlier than `confirmed`**) | payer-signed-payment validation · client-visible: spec yes / fused no |
| Tempo-Session (R10b) | Server `Verify` of an off-chain signed voucher (**near-zero**) | payee/server voucher validation · client-visible: yes |
| GCP + AP2 (R6) | Mandate verification → credential issuance (dispatch hop **decomposed out**, §2.5) | **auth-only / no funds-check**, does not settle · **scope = whole rail** (not a slice) |

**Sub-ranking B — Challenge-Issuance Latency** (the primitive *issues a payable 402 challenge before
the payer commits*; renamed from "Permission-Grant" — RR2). Raced within-group → C(5,2)=10 pairs.
This populates the grant-type sub-ranking with a real race (fixing the round-1 *n*=1 problem):

| Member | Challenge-issuance primitive | Trust / equivalence class |
|---|---|---|
| x402-Base (R1) | Issue the `402` + `accepts` payment requirements | server-issued payment challenge |
| x402-Stellar (R2) | Issue the `402` + Soroban payment requirements | server-issued payment challenge |
| x402-Solana (R9) | Issue the `402` + SVM payment requirements | server-issued payment challenge |
| MPP-on-Tempo (R10) | Issue the `402` + `WWW-Authenticate: Payment` challenge | server-issued payment challenge |
| MPP-on-Spark-Lightning (R11) | Issue the **macaroon + BOLT11 invoice** (the L402 challenge) | server-issued grant-to-pay (invoice incl.) |

**AP2 is absent from B** (it presents no 402 challenge — its primitive is mandate-validation, A
only). **L402 is absent from A** — it has no pre-settlement payment-validation point (§2.3, the
category-error fix). Note L402's challenge issuance includes **BOLT11 invoice generation** (a real
Lightning operation), so B is not a pure constant across rails.

All `{median_s, sigma_log}` are `TODO(calibration)` PLACEHOLDERS (footnote¹).

¹ The placeholders shipped in the harness live in
`calibration/provenance/<rail>-auth-latency.provenance.yaml`, each marked
**"PLACEHOLDER — pending founder calibration"** — they exercise the pipeline only;
not measurements, not for publication or pre-registration.

### 2.1 Per-rail mechanics & nuances (the cells above, expanded)

- **R9 (Solana): accept ≠ `confirmed`.** The facilitator accept is **earlier** than the
  on-chain `confirmed` (~2.27s); `confirmed` is the *settle-at-confirmed* checkpoint, not
  the accept (research caveat C1). → Record **three checkpoints** (§2.2).
- **R10 (Tempo): only Session is raced (RR1).** The MPP core spec mandates a `Verify` procedure
  separate from `Settle`. For the one-time **Charge** intent the docs fuse verify+settle into one
  **~500ms** figure, so **Charge is excluded from sub-ranking A** (racing it = racing settlement) and
  only **disclosed in an appendix**; **Tempo-Session** (near-zero off-chain voucher verify) is the
  raced member of A. Tempo also appears in **sub-ranking B** for its `402`-challenge issuance.
- **R11 (L402/Spark): challenge-issuance only (Sub-ranking B).** The macaroon + invoice are issued
  **before** the payer pays; the **preimage** is the settlement proof, obtained only by paying
  (Spark's conditional-lock → SSP-preimage finalize, the ~16.5s ceremony = settlement). L402 has **no
  pre-settlement validation primitive** (§2.3), so it is **absent from A** and races in **B** on
  challenge-issuance (macaroon + BOLT11 invoice generation).
- **R6 (AP2): the two-process timer.** Authorization = mandate-verify **+** orchestration
  to dispatchable; the **total** is raced, the **verify** and **orchestration** components
  are recorded separately (Q1, §9). AP2 does not settle (settlement out of AP2 scope).

### 2.2 Checkpoint-recording model (the "record all three" decision)

Where a rail exposes them, record up to **three checkpoints** per payment and **race the
authorization (accept) checkpoint**:

1. **accept** — the authorization go-ahead (the table above). *Raced; lower-is-better.*
2. **intermediate settle signal** — e.g. Solana `confirmed`, Tempo ~500ms block, the L402
   preimage / Spark SSP finalize (rail-dependent; may equal #3).
3. **finalized** — the §3 settlement-finality point (the Day-0 dimension).

The **accept → finalized gap** is itself a publishable quantity (e.g. Solana ≈ accept vs
~14.6s). Capturing the accept requires invoking the rail's **verify primitive explicitly**
(research caveat C2) — some integrations call only `/settle` (which verifies internally),
so a fused HTTP 200 does **not** expose the accept.

### 2.3 Why the SPLIT (and not a trust-class label) — the category-error fix

The pre-gate draft put all six rails in one race and *named* the asymmetry with a
trust/equivalence-class column. The cross-lineage gate (0–4) rejected that: a label **names** a
category error without **removing** it, and a single Bradley-Terry race implicitly treats the
items as differing in *degree* along one latent axis when they differ in *kind*. The security
*object* genuinely differs:

- **Validation-of-payment** (Sub-ranking A) — x402 `/verify`, MPP `Verify`, AP2 mandate-verify
  all validate *something the payer has already submitted* (a signed payload / credential /
  mandate). "Is this payment/mandate valid?"
- **Grant-to-pay** (Sub-ranking B) — L402's macaroon+invoice is the server *issuing a payable
  challenge before the payer has committed anything*. "Here is what to pay." In ISO-8583 terms it
  is the merchant's `0100` *request*, not the issuer's `0110` *response* — measured at an earlier
  protocol step than A's checkpoint.

**Why not REPIN-R11 into A.** L402 has **no pre-settlement payment-validation checkpoint**: in
Lightning, *payment is settlement* (the preimage is revealed by paying). Re-pinning L402 to a
"payment-accepted" signal would land on preimage-verification — i.e. **settlement (dimension 1)**,
not authorization. So L402 cannot join A without collapsing into D1; it belongs in its own
grant-type sub-ranking B. This is the gate's unanimous fatal finding, resolved.

**AP2 stays in A but tagged.** AP2 validates a *mandate* (not an on-chain payment) and **does not
settle**, so it is labelled **auth-only / no-funds-check** (load-bearing, not cosmetic) and its
**external dispatch hop is decomposed out** of the raced quantity (§2.5), so A races the
comparable mandate-verify+credential-issuance step, not a party-to-party network call.

### 2.4 Terminology honesty

No rail publishes a metric literally named *"authorization latency"*: x402 calls it
`/verify`, MPP calls it **"verification"**, AP2 calls it **"mandate verification /
credential issuance"**, L402 calls it the **macaroon/challenge**. The *separability from
settlement is genuine and published on every rail*, but **"authorization latency" is
PayBench's framing** over those primitives. Conceptual precedent exists — the card-network
**ISO-8583** split of real-time authorization (MTI 0100/0110) from settlement (0200/0220)
— so the dimension ports a long-standing distinction rather than inventing one; but **no
prior benchmark measures it** (novelty **checked & defensible** — Pass 4, `wktco3m7a`,
`research.md`: card-network limits are *SLAs*, not a comparative benchmark, so the
benchmark *dimension* is new; state as "no prior we identified").

### 2.5 Measurement & statistics package (DR3 + round-2 RR3–RR6 — gate-mandated)

The sub-100 ms regime is unforgiving; the gate required a tighter measurement contract than
finality's. All of the following are **pre-registered** before any scored run:

- **`t = 0` standard.** Start the clock when **the agent issues the ultimate pay command —
  the payment payload constructed and on the wire** (not an empty GET that merely triggers a
  402), uniformly across rails so no rail is advantaged by excluded payload-construction work.
- **Client-side, RTT-subtracted measurement (RR4 + FR3/FR4).** Measure **client `send()` → the
  *last byte of the authorization response payload*** (an explicit end-of-auth marker) — **not first
  byte** (FR3): a first-byte stopwatch lets a rail emit early HTTP framing before finishing the
  mandated work (RR5/FR2) and game the metric. Subtract a **baseline RTT from a same-path,
  app-layer (TCP/TLS) probe** that traverses the **same route + TLS termination** as the auth
  endpoint (FR4 — an ICMP `/ping` is invalid here: it neither matches the TLS path nor the
  handshake cost); **report raw *and* RTT-corrected**, with a TCP/TLS-handshake sensitivity check.
  Fix a **canonical client geography**, publish the **min-RTT floor per endpoint**, and report a
  **≥2-topology sensitivity** (co-located + cross-region) — at this timescale a 50 ms probe-placement
  difference can flip a pair.
- **Warm vs cold start.** Pre-register **warm-start-only** (discard the first *N* calls: TLS +
  connection-pool warmup) vs cold-inclusive, and report both.
- **`P(auth ≤ k)` in the right regime (RR3 — *not* "pass@k").** The metric is a latency **CDF**,
  not pass@k (which means ≥1 success in *k* stochastic attempts → wrong here); rename it. Use a
  **millisecond k-ladder** (e.g. `{20, 50, 100, 250, 500} ms`) with a **rank-stability heatmap**
  and a **variance-aware power analysis** for minimum *n* per pair; report **median / P95 / P99**
  alongside (a fixed *k* + Wilson otherwise favours low-variance rails over lower-median ones).
- **Hardened Bradley-Terry, with a survival-model fallback (RR3).** Keep BT (within a sub-ranking
  only — never across A/B) as the comparative backbone, **consistent with the frozen dimension-1
  spine**, but plug the holes the panel named: a **Davidson ties extension** (sub-second networked
  races tie often within clock jitter) and an explicit **censoring / competing-risks rule** for
  authorization *failures* (reject / timeout) — they must enter the model, not be silently dropped.
  Report **Kaplan-Meier survival curves** for description. **Pre-specify a survival model (Cox PH /
  Aalen-Johansen competing-risks) as the *data-triggered fallback*** with **numeric triggers (FR1 —
  unanimous round-3 condition; values pre-registered):** switch to it if, in any sub-ranking, the
  **tie-rate > 20%**, OR any rail's **auth-failure/censoring-rate > 5%**, OR **> 10% of triples are
  cyclic** (transitivity violation) / a BT goodness-of-fit LR test gives **p < 0.05**. *(Proposed
  defaults — founder confirms/tunes at pre-reg.)* We do **not** swap the engine pre-emptively — that
  would fragment the one-method-across-dimensions story and re-expose frozen D1 to the same critique
  without evidence the pathology bites (D1 is mock-fixture, seconds-scale, tie-free; the pathologies
  are a *live sub-second* phenomenon).
- **Anti-gaming work-clause (RR5 — *Group A only*, FR2).** For **Sub-ranking A (validation)** the
  timed response must include **signature verification + a *fresh* balance/state read**, else a rail
  games it by emitting `/verify` early and deferring real checks to settle. **This clause does NOT
  apply to Sub-ranking B** — challenge issuance (e.g. an L402 macaroon + BOLT11 invoice) is a
  **stateless cryptographic** operation; mandating a ledger read there would break native L402 or
  inflate latency artificially (round-3 FR2). B is timed as pure issuance work.
- **Assurance normalisation — `P(settled | accept)`.** Record, per rail, the probability that an
  accept actually leads to settlement (and the assurance depth). A near-instant accept that
  frequently fails downstream is **not** comparable to a slower, near-certain one; without this
  covariate the lower-is-better race is gameable by "doing less" at the boundary.
- **Labels (RR6).** Every reported row carries a **checkpoint-visibility** tag (`client-visible:
  yes/no`, so the instrumented-on-fused-topologies x402 rows are honest) and, for AP2, a
  **scope-coverage** qualifier (AP2's number is its *whole* scope; other rails' is the
  authorization *slice* of a larger flow).
- **RPC / facilitator pinning (FR7 — pilot-informed, 2026-06-22).** The Q4 Base pilot showed the
  accept (~777 ms, σ≈0.016) is **RPC-dominated** — it is the facilitator's *fresh balance read +
  `eth_call` simulation round-trips to the chain RPC* (the work-clause), not crypto. So a rail on a
  fast/co-located RPC would look "faster to authorize" — an **artifact of RPC choice**, not the rail.
  Treat the **server→RPC hop like FR4 treats the client→server hop: disclose + diagnose, never hide,
  never subtract** (the RPC read *is* authorization work): **(1)** pre-register + **pin a canonical
  RPC endpoint per chain-backed rail**; **(2)** hold the **RPC tier roughly constant** across rails
  (same provider class / region) so cross-rail deltas reflect rail+chain logic, not RPC luck;
  **(3)** report a **server→RPC-RTT diagnostic** alongside the accept (don't subtract it). For
  **hosted-facilitator** rails (Solana/Stellar via x402.org) the RPC reads happen *inside* the
  facilitator we don't control → there, pin/disclose the **facilitator** endpoint instead.
- **Companion agent-observed total latency (co-primary).** Alongside the primitive latency,
  report **time-from-pay-command-to-usable-signal** (accept + the accept→settle gap). The
  primitive ranking can *invert* the end-to-end experience (a fast-accept/slow-settle rail loses
  overall); the two must be displayed together so the headline is not optimised against the
  outcome agents actually care about. (On fused topologies this companion equals settlement time,
  i.e. collapses into dimension 1 — which is itself the honest disclosure for those rails.)

### 2.5.1 Work-type decomposition & grouping (DR4 — PROPOSED, founder-ratify-pending, 2026-06-24)

The Q4 first-party runs (`dim2-q4-pilot-log.md`, all 6 rails) showed that **within each sub-ranking the
rails span 2–3 orders of magnitude of *work-class*** — A: AP2 local crypto 1.68 ms / Tempo-Session
local+periodic-RPC ~19.5 ms / x402 facilitator 400–777 ms; B: local-402 ~2–3 ms / Lightning invoice-mint
~0.9–1.25 s. A confirmatory cross-lineage scan (round 4; `dim2-worktype-{scan,synthesis}.md`) **refuted
4/4** the original "one race + scalar work-type label + median-only + never-subtract" framing. The panel's
convergent fixes are folded in below. Most *sharpen* existing §2.5 bullets; one (work-class grouping) is
structurally new. **Pending founder ratification + the open fork at the end.**

- **(D4a) Tail as headline, not "alongside" (sharpens the RR3 bullet).** Promote **P50 / P95 / P99 + N +
  measurement-timestamp + topology** to the *reported headline tuple* per rail (not a fixed-`k` Wilson
  headline with percentiles in a footnote). Live evidence: the Lightning median moved **1252 ms (n=15) →
  936 ms (n=30)** with p99 ≈ 1.49 s — the median alone is not a point estimate for network-bound rails.
- **(D4b) Per-rail decomposition tuple (NEW — extends the FR4/FR7 raw+corrected + RPC-diagnostic).** Report,
  per rail, **`(local_compute_floor, backing_service_component, E2E)`**: the local crypto/state-machine
  cost in isolation, the backing-service component (facilitator / chain-RPC / Lightning-node / session
  TTL-refresh), and the end-to-end. **E2E stays the headline** (what the agent feels; we still never
  subtract from it — RR5/FR2/FR7 work-clause). The decomposition is the **protocol-design view** that the
  panel's "subtract for protocol comparison" camp (Gemini/Kimi) needs, served as a *secondary* number, not
  the headline. The min-RTT floor (FR4) and server→RPC-RTT diagnostic (FR7) are the inputs to
  `local_compute_floor` / `backing_service_component`.
- **(D4c) Work-class grouping (NEW — the structural change).** Within a sub-ranking, **group rails by work
  class** — *Local-complete* (no network round-trip in the primitive's critical path) vs *Network-dependent*
  (≥1 intrinsic backing-service round-trip per call). **Rank within a group; compare across groups only via
  the decomposition tuple (D4b) — never as a single cross-class ordinal.** Rationale: when between-class
  spread (250–800×) dwarfs within-class spread (≤~2×), a single ordinal encodes class membership, not rail
  quality, and a bare leaderboard misleads any reader who skips the label.
- **(D4d) Tempo TTL is reference-impl config, not a rail class (resolves the R10b caveat).** The
  ~19.5 ms-warm / ~360 ms-on-the-~5 s-TTL-tick behaviour is the *reference server's* `channelStateTtl`, not a
  Tempo-protocol property. **Do NOT give it a third taxonomy bucket** (gaming-prone: TTL=∞ → looks local).
  Instead report **`L_hot` (cache-hit) and `L_cold` (cache-miss → chain read) with the request
  inter-arrival distribution disclosed**, and/or a **TTL sweep** {0, 5 s, 60 s, ∞} or a cache-disabled
  protocol-baseline (minimum required backing hops per call). Tempo then appears in *both* groups by its
  warm (Local-complete) and cold (Network-dependent) numbers, each annotated.
- **(D4e) ≥2 topologies MANDATORY for network-dependent rails (promotes FR4 from advisory).** The 400/464/
  777 ms A-numbers are functions of the measuring host's network path; a single topology measures the
  harness, not the rail. A second network-distinct vantage (e.g. a named cloud region) is **required**
  before any network-dependent number is scored. Local-complete rails being topology-invariant is the
  built-in control.
- **(D4f) Workload + deployment disclosure (NEW).** Hold and disclose **workload constants** — macaroon
  caveat count (L402 verify is superlinear in caveats), voucher / x402-header / payload sizes. Disclose the
  **AP2 in-process vs sidecar** deployment assumption (the in-process number omits an IPC hop a sidecar
  deployment would add — RR6 scope label, extended). Note **concurrency / throughput** as explicitly
  out-of-scope (latency-only).

**OPEN FORK — founder decision (the one axis the panel split on):**
- **(recommended) group-and-decompose** — one table per sub-ranking, grouped by work class (D4c) with the
  decomposition tuple (D4b) carrying the cross-group story. Reconciles all four reviewers.
- **(harder) two separate leaderboards** per sub-ranking, split on intrinsic network-dependency, no
  cross-leaderboard comparison in text or figure (DeepSeek/Gemini/Kimi, 3/4). Cleaner separation, but Qwen's
  objection (a Local-complete-A leaderboard is n=2) bites.

Until ratified, **D4a–D4f are proposed, not adopted**; the rails + pilot numbers are unaffected (this is a
reporting/analysis-layer change). Tracked as **DR4** in §9.

## 3. How AP2 (R6) is measured here

Per §8 Resolution B, AP2 does **not** settle independently and is therefore
excluded from finality; authorization latency is the dimension where it is
**well-defined and apples-to-apples**. AP2's distinctive cost is
**mandate-verification + orchestration overhead** — an authorization-layer
phenomenon — so on this dimension R6 is a first-class competitor, not a
mislabelled finality entrant. This is the debut §8 anticipated. *(The single
6-rail / C(6,2)=15-pair race is the **superseded pre-gate design**; post-SPLIT,
AP2 competes only in **Sub-ranking A — Payment-Validation** (§2): C(5,2)=10 pairs,
AP2 tagged auth-only/whole-scope; it is absent from Sub-ranking B.)*

**Open scope question (Q1).** What exactly is timed for AP2: mandate-verify
*only*, or mandate-verify *plus* orchestration through to first underlying-rail
dispatch? These measure different things; the founder must choose and the choice
must be pre-registered. The placeholder times mandate-verify + orchestration as a
single envelope (median set above the settling rails to reflect the extra
round-trips) — illustrative only.

## 4. Statistics — core methods reused, but **not** unchanged (see §2.5)

> **Pre-gate this section read "reused unchanged."** The cross-lineage gate (rounds 1–2) corrected
> that: the BT/CDF/Wilson *spine* is kept (consistent with frozen D1), but **§2.5 imposes real
> changes** — run **per sub-ranking only**; **ms k-ladder**; the metric is **renamed `P(auth ≤ k)`**
> (it is a latency CDF, not pass@k); BT is **hardened** (Davidson ties + censoring/competing-risks)
> with a **survival-model fallback**; KM curves + median/P95/P99 + a `P(settled|accept)` covariate
> are added. Read §4 with §2.5.

Authorization-primitive latency is still **lower-is-better, race-the-pair**, so the §5 spine applies
*within a sub-ranking*, hardened:

- **Bradley-Terry MLE** over pairwise races — same `bradley_terry_mle`, `prior=1.0`, **same-kind
  rails only**, **plus a Davidson ties term** and an explicit **censoring/competing-risks** rule for
  reject/timeout (RR3). A **Cox PH / competing-risks survival model is pre-specified as the
  data-triggered fallback** if real-data checks show BT is pathological (we do not swap pre-emptively;
  §2.5 explains why — it would re-expose frozen D1 without evidence the pathology bites).
- **`P(auth ≤ k)`** (the latency CDF — **not** "pass@k", RR3) — **millisecond k-ladder** with a
  rank-stability heatmap + variance-aware power analysis; **median/P95/P99** reported alongside.
  *(The earlier placeholder grid `[0.25..5]s` is superseded.)*
- **Wilson lower-bound CIs** — unchanged; **Kaplan-Meier survival curves** added for description.

The harness *generalisation* (making the dimension a first-class parameter — name, unit, rail
set, seed-namespace, k-grid, paths) is unchanged and correct. But the **scoring contract is not
a clean reuse**: per §2.5 it is per-sub-ranking, ms-gridded, survival-curve-augmented, and
assurance-normalised. The gate also confirmed the **bimodality risk**: Tempo is *genuinely*
bimodal (Charge ~500 ms vs Session ~0), which is exactly why DR3 **bifurcates it into two
pseudo-rails** rather than fitting one log-normal — a single mixture would make BT/Wilson
meaningless. The generator still assumes `family: lognormal` per (pseudo-)rail; any further
non-log-normal shape is flagged for review, not papered over.

## 5. Reproducibility / seed-namespace design (PROPOSED)

The harness keeps the **single published master seed** (§6) and **domain-separates
the auth-latency RNG streams** from finality's, so the two dimensions never share
a stream while both derive from the one seed:

- finality fixture/pair domains stay `fixture:<rail>` / `pair:<a>:<b>` (frozen);
- auth-latency uses `fixture:auth-latency:<rail>` / `pair:auth-latency:<a>:<b>`.

This namespace scheme is a **proposed** design to be ratified at pre-registration
(it is not yet frozen). It is what lets the frozen finality artefact reproduce
bit-for-bit while auth-latency draws independent streams (asserted in
`tests/test_auth_latency.py::test_dimensions_are_rng_domain_separated`).

## 6. Open questions for the founder (status against pre-registration)

Q1–Q3 are **resolved/drafted** (founder-directed + research-grounded; see §2 and the
§9 decision log) but **not yet ratified** — ratification is a founder act gated by the
§8 cross-lineage review. Q4–Q5 remain genuinely open.

- **Q1 — AP2 scope.** ✅ **RESOLVED** — mandate-verify **+** orchestration → dispatchable;
  total raced, components recorded (§9). AP2's published structure matches this.
- **Q2 — authorization point per rail.** ✅ **RESOLVED (A1)** — off-chain accept/verify,
  primary-source-validated for all six rails (§2; `dim2-auth-latency.research.md`).
  *Solana clarified:* the accept is the facilitator `/verify`, **earlier** than
  `confirmed` (~2.27s); `confirmed`/`finalized` are recorded as separate checkpoints
  (§2.1–§2.2). Real numbers withheld pending Q4 calibration.
- **Q3 — per-rail authorization-point doctrine.** ✅ **GATE-CLEARED, PRE-REGISTERABLE (2026-06-22).**
  Three cross-lineage rounds: 0–4 (category error) → 3–1 (SPLIT validated) → **4/4 pre-registerable**.
  RR1–RR6 + FR1–FR5 applied (§9). **Remaining: founder ratification**, then pre-registration.
- **Q4 — calibration sourcing.** ⏳ **OPEN — scoped, runs *before* FR1/pre-registration.**
  Plan in `dim2-validation-run-plan.md`. First-party measurement isolating the *authorize* leg per
  sub-ranking — A: explicit `/verify` accept (client-side, last-byte, RTT-subtracted, with the
  work-clause); B: `402`-challenge issuance — capturing failures as censored events. **Sequencing
  (mirrors D1 calibrate-before-freeze):** this run is the **pilot that informs the FR1 fallback
  thresholds + the power analysis** (the tie/censoring/transitivity pathologies cannot appear on the
  mock log-normal fixtures, so the *live* run is the only place to observe them) — *informing*
  principled thresholds, **not** tuning them to the scored data. Then it replaces the PLACEHOLDER
  fixtures with real `{median, sigma}`. **Instrumentation gap:** POC servers expose only the fused
  `/resource`; a thin standalone `/verify` route + a same-path RTT-baseline endpoint must be added
  (founder/credentialed step, `mblake4u/agentpay`).
- **Q5 — k-grid + scoring constants.** ✅ **RESOLVED via RR3 (§2.5/§4).** ms k-ladder
  ({20,50,100,250,500} ms) + rank-stability heatmap + power analysis; metric renamed
  **`P(auth ≤ k)`** (latency CDF, not pass@k); BT within-sub-ranking only, **hardened** (Davidson
  ties + censoring), with a **Cox-PH/competing-risks survival model pre-specified as the
  data-triggered fallback**; KM curves + median/P95/P99 reported. Final values pre-registered with
  the design.

## 7. What is done vs. what a founder must do

**Done this session (mechanical):** dimension-parametric harness; 6-rail/15-pair
auth-latency benchmark runs end-to-end on placeholder fixtures; content-addressed
fixtures + provenance; tests mirroring the finality suite; finality still
reproduces bit-for-bit.

**Founder, next (judgment), in order:** resolve Q1–Q5; replace every placeholder
with real calibration; draft the doctrine into this addendum; **pass it through the
cross-lineage adversarial review gate (§8)**; revise; ratify into the methodology;
*then* (separately) the pre-registration ceremony (OSF / cosign / OpenTimestamps /
signed tag). See `SESSION-1-HANDOFF.md`.

## 8. Planned validation gate — cross-lineage adversarial review (PRE-PRE-REGISTRATION)

> **Drafted and ready to run:** `dim2-adversarial-review.md` carries the self-pass
> (severity-ranked findings G1–G7, the two contested decisions DA1/DA2, and the
> "what to pressure-test" list) **plus the self-contained cross-lineage prompt** for
> the founder to paste to each external lineage. The synthesis section there is empty,
> awaiting the run.

**This dimension must pass a cross-lineage adversarial review before
pre-registration**, mirroring the gate dimension-1 cleared — the methodology
records a *four-model cross-LLM adversarial review (2026-06-06) that upheld the
finality doctrine 3–1* on the Solana `confirmed`-vs-`finalized` question
(artefacts: `Pre-reg-{Deepseek,Gemini,Kimi,Qwen}`, `pre-reg-adversarial-review.md`).
Dimension 2 has *more* contestable surface than dimension 1 (G1 facilitator-internal
accept, G2 heterogeneous authorization objects), so the gate is not optional.

**Position in the sequence (§7):** after the doctrine is drafted and (ideally)
after the validation test run that confirms A1's empirical claim, **before** the
founder pre-registration ceremony. Running it earlier just yields split votes on an
under-specified proposal; running it on a grounded proposal yields a citable verdict.

**What to put to the panel (the exposed flanks):**

- **A1 vs A2** — off-chain facilitator *accept* vs optimistic on-chain
  *confirmation* as the authorization point (a measurement-validity fork).
- **Accept is facilitator-internal, not client-perceived.** In the fused/in-process
  x402 topologies the POC uses, the agent receives no "authorized" signal before the
  post-settle 200 (the facilitator's `verify()` return is server-side; see the
  scoping note below). Is racing a facilitator-side checkpoint a valid *agent-DX*
  benchmark, or does legitimacy require the x402 spec's separately-exposed `/verify`
  endpoint? This is the sharpest flank.
- **AP2 scope** (verify-only vs verify + orchestration to dispatch) and the per-rail
  authorization-point asymmetry / apples-to-apples across different facilitator
  topologies.
- **Is "authorization latency" measurement-valid as defined** at all, distinct from
  finality?

**Mechanics.** Founder-run multi-lineage ceremony (the doctrine pasted to each
external lineage, as the `Pre-reg-*` files were). Claude drafts the cross-lineage
prompt and synthesises the responses into `dim2-adversarial-review.md`, the
dimension-2 analogue of `pre-reg-adversarial-review.md`.

**Honest limit.** The gate *hardens and red-teams*; it does not resolve empirical
facts (that is the research + validation run) and may return a split that still needs
founder judgment.

## 9. Decision log (session-directed — TENTATIVE, pending the §8 gate)

Records founder-directed decisions taken while building the harness. **Not yet
ratified** — all remain subject to the deep research, the validation run, and the
§8 cross-lineage gate before they enter the frozen methodology.

- **Q1 — RESOLVED (founder-directed).** AP2's authorization timer runs **mandate
  presented → dispatchable** (verify **+** orchestration to first underlying-rail
  dispatch). The **total** is what the benchmark races; the **verify** and
  **orchestration** component distributions are *additionally recorded and published*
  (approach: measure/record all three independently; benchmark on the total; race and
  stats consume one value per rail, so BT/pass@k/Wilson and the frozen finality path
  are untouched). **AP2-only for now** — it is the only rail whose authorization is
  genuinely two processes. *Evidence (Pass 2):* AP2's published structure —
  mandate-verify → credential issuance → dispatch to the Merchant/processor, with
  settlement out of AP2 scope — **matches this framing exactly** (primary spec); no
  AP2 latency figures are published, so its calibration is first-party/placeholder.
- **Q2 — A1, VALIDATED for ALL SIX RAILS** by primary specs (three passes 2026-06-20,
  `dim2-auth-latency.research.md`): R1/R2/R9 (x402 `/verify`), R6 (AP2 mandate-verify),
  R10 (MPP-Tempo Verify procedure), R11 (L402 macaroon+invoice; Spark conditional-lock).
  Conceptual precedent = ISO-8583 auth-vs-settlement MTIs; no prior "authorization
  latency" benchmark surfaced (**novelty plausible**, prior-art verification partly
  truncated by a session limit — re-check before any published novelty claim).
  Authorization = the
  off-chain facilitator **`/verify` accept** signal (payload validated: signature +
  funds), recorded with `confirmed` and `finalized` as separate checkpoints. The
  x402 spec normatively separates `/verify` (off-chain; response `{"isValid":true,
  "payer":…}` with **no** tx hash) from `/settle` (on-chain) — so the accept is a
  discrete, separately-timeable event before settlement, on EVM (Base) *and* Soroban
  (Stellar). *Scoping + research agree:* the Solana `confirmed_s` (~2.27s) is the
  **settle-at-confirmed** checkpoint, **not** the accept (which is the earlier
  facilitator `/verify`); accept / settle@confirmed / finalized are **three**
  recorded checkpoints (research caveat C1). *Earlier "facilitator-internal vs
  client-perceived" tension — RESOLVED in A1's favour:* the spec exposes `/verify` as
  a client-observable endpoint; the benchmark must **call `/verify` explicitly** to
  capture the accept (research caveat C2), since some integrations call only
  `/settle`. *No published "authorization-latency" benchmark surfaced* — apparent
  novelty pending a dedicated prior-art check (in the gap pass).
- **Roadmap note (founder).** The authorization timer will likely need **per-rail
  structural variants** (component splits, different protocol checkpoints) as we learn
  each rail — AP2's verify/orchestration split is the **first instance, not a
  one-off**. The provenance schema's optional `components:` block is the generalisation
  point.

### Post-gate resolutions — DR1–DR3 (founder-directed 2026-06-22, after the §8 gate)

The cross-lineage gate refuted the single-race doctrine 0–4 (`dim2-adversarial-review.md`).
Founder adopted the recommended package; §2 re-drafted accordingly. **Still DRAFT — a short
second gate round on the revised split is advisable before ratification.**

- **DR1 — SPLIT (adopted).** Two ontological sub-rankings: **A Payment-Validation** (x402×3,
  Tempo-Charge, Tempo-Session, AP2) and **B Permission-Grant** (L402). BT/pass@k run **within**
  a sub-ranking only. L402 is **not** re-pinned into A — it has no pre-settlement
  payment-validation point (payment = settlement in Lightning), so a re-pin collapses into D1.
  B currently has one member → reported standalone (a 402-issuance race could populate it later).
  *This supersedes the Q2 "all six rails, one race" framing above.*
- **DR2 — RENAME + companion (adopted).** Dimension renamed **Rail Authorization-Primitive
  Latency (RAPL)** (provisional; alt "Protocol-Accept Latency") to make explicit it measures a
  rail/protocol primitive, **not** an agent-perceived latency (G1). A **co-primary
  agent-observed total-latency** metric is reported alongside (addresses fast-path inversion).
- **DR3 — measurement/stats package (adopted, §2.5).** Tempo bifurcated into **Charge/Session**
  pseudo-rails; **`t = 0`** standardised to payload-on-the-wire measured at the rail edge;
  **network-adjusted** latency + canonical geography + RTT floor; **warm/cold** pre-registered;
  **millisecond k-ladder** + rank-stability heatmap (supersedes Q5's placeholder grid); **BT
  within-sub-ranking + Kaplan-Meier** survival curves; **`P(settled|accept)`** assurance
  covariate; **AP2 tagged auth-only** with the dispatch hop decomposed out.
- **Harness re-alignment (follow-up, not yet done).** The placeholder harness still runs the
  *pre-gate* single 6-rail race with the seconds k-grid. Re-aligning it to the final design (the two
  sub-rankings below, Tempo-Session-only in A, the challenge-issuance race in B, the ms k-ladder, the
  hardened-BT spine) is a **post-ratification implementation task** — deliberately deferred so it is
  not built against an un-ratified design.

### Round-2 resolutions — RR1–RR6 (founder-directed 2026-06-22, after the round-2 gate)

Round 2 validated the SPLIT **3–1** and added a bounded refinement list; founder adopted the
recommended package (RR3 as hardened-BT-with-survival-fallback). §2 updated. **Still DRAFT — a
*short final* confirmation after RR1–RR6 is advisable before ratification.**

- **RR1 — Exclude Tempo-Charge from the raced set.** Sub-ranking A is now x402×3 + **Tempo-Session**
  + AP2 (C(5,2)=10); **Tempo-Charge** (verify+settle fused ~500 ms) is **disclosed in an appendix**,
  not ranked. *Supersedes DR1's "Tempo-Charge in A" and DR3's bifurcate-both.*
- **RR2 — Sub-ranking B is a real *challenge-issuance* race** (renamed from Permission-Grant) across
  the 402-issuers (x402×3, MPP-Tempo, L402; C(5,2)=10) — fixes the *n*=1 problem. *Supersedes DR1's
  "B standalone, one member."* x402 rails appear in **both** A and B (two distinct primitives); AP2
  in A only; L402 in B only.
- **RR3 — Hardened BT, survival-model fallback.** Keep the BT/CDF/Wilson spine (D1-consistent), add
  **Davidson ties** + **censoring/competing-risks**, rename **`P(auth ≤ k)`** (not pass@k), ms
  k-ladder + power analysis + median/P95/P99 + KM curves; **Cox-PH/competing-risks pre-specified as
  the data-triggered fallback** (not swapped pre-emptively — would re-expose frozen D1 without
  evidence; see `dimension-design-lessons.md`).
- **RR4 — Client-side, RTT-subtracted measurement** (client `send()`→**last byte** of the auth
  response per FR3, minus a same-path app-layer baseline per FR4), canonical geography + ≥2-topology
  sensitivity. *Supersedes DR3's "rail edge".*
- **RR5 — Anti-gaming work-clause:** verification + a *fresh* balance/state read must be inside the
  timed response.
- **RR6 — Labels:** per-row `client-visible: yes/no`; AP2 `scope = whole rail` qualifier.

### Round-3 resolutions — FR1–FR5 (final confirmation, 2026-06-22)

Round 3 returned **PRE-REGISTERABLE** (4/4, conditional), caught two real bugs in the refinements,
and closed the arc (0–4 → 3–1 → pre-registerable). Fixes applied to §2.5/§2:

- **FR1 (gating, unanimous):** the BT→Cox-PH fallback triggers are now **numeric** (tie-rate > 20%,
  censoring-rate > 5%, cyclic-triples > 10% / LR p < 0.05) — *proposed defaults, founder confirms at
  pre-reg.*
- **FR2:** the RR5 work-clause (sig-verify + fresh state read) is **restricted to Group A**; Group B
  (stateless challenge issuance) is exempt (Gemini caught RR5-on-B would break native L402).
- **FR3:** the measurement stopwatch stops at the **last byte of the authorization response** (not
  first byte) — closes Kimi's framing-byte gaming gap.
- **FR4:** RTT baseline is a **same-path app-layer (TCP/TLS) probe**, **raw + corrected** reported,
  with a handshake sensitivity check (ICMP `/ping` was invalid).
- **FR5:** the Tempo-Charge exclusion is stated in the **main text** + a developer note on the
  Charge (1-RTT) profile.

**Status (pre-Q4):** doctrine was *ready for founder ratification*. **SUPERSEDED by round 4 (DR4) below**
— the Q4 validation runs surfaced a new finding that re-opened §2.5. Deferred to post-ratification:
harness re-alignment. *(Prior-art novelty re-check — **done** 2026-06-22, Pass 4 `wktco3m7a`: novelty
defensible; see `research.md`.)*

### Round-4 resolution — DR4 (work-type heterogeneity; PENDING founder ratification, 2026-06-24)

The Q4 first-party runs (all 6 rails; `dim2-q4-pilot-log.md`) showed that **within each sub-ranking the
rails span 2–3 orders of magnitude of *work-class*** — A: AP2 local crypto 1.68 ms / Tempo-Session
local+periodic-RPC ~19.5 ms / x402 facilitator 400–777 ms; B: local-402 ~2–3 ms / Lightning invoice-mint
1252 ms. A confirmatory cross-lineage scan (round 4; prompt `dim2-worktype-scan.md`, replies
`dim2-worktype-{deepseek,gemini,kimi,qwen}.md`, synthesis `dim2-worktype-synthesis.md`) **refuted 4/4**
the proposal "one race + scalar 3-bucket disclosure + median-only + never-subtract" (2 REJECT, 2
RATIFY-WITH-CHANGES). Does **not** reopen the A/B SPLIT or invalidate any rail/pilot number — a §2.5
reporting/analysis-layer revision only.

- **DR4 (proposed, founder ratifies):** revise §2.5 to (1) report **P50/P95/P99 + N + timestamp +
  topology** (not median-only); (2) a **per-rail decomposition** `(local_compute_floor,
  backing_service_component, E2E)` — E2E headline, decomposition = protocol-design view; (3) **group by
  work-class** (Local-complete / Network-dependent), rank within, compare across via the decomposition —
  no single cross-class ordinal; (4) treat **Tempo's TTL as ref-impl config** → report L_hot/L_cold +
  arrival distribution (or a TTL sweep), delete the "periodic/amortized" bucket; (5) **≥2 topologies
  mandatory** for network-bound rails (promotes FR4 from advisory to required); (6) disclose **workload
  constants** (macaroon caveats, payload sizes) + the **AP2 in-process/sidecar** deployment assumption.
- **One OPEN axis for the founder:** "group-and-decompose" (recommended; reconciles all four) vs the
  harder "two separate leaderboards" split (DeepSeek/Gemini/Kimi, 3/4). 
- Much is already in place: harnesses record raw samples (→ P95/P99), the min-RTT floor (decomposition
  start), B1 keep-alive assertion (handshake concern), and the Tempo warm/cold split are all built.

**Status:** doctrine **back to founder ratification**, now gated on DR4 (the §2.5 revision + the open
split-vs-decompose axis) in addition to the prior FR1 threshold confirmation. Pre-registration follows
ratification.
