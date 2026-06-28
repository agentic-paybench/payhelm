# Dimension 2: Authorization Latency — RAPL (Rail Authorization-Primitive Latency)

> **RATIFICATION-READY — proposed de-draft for founder sign-off.** This is the canonical doctrine
> de-drafted from `dim2-auth-latency.DRAFT.md` per the **founder ratification of 2026-06-24** (DR4
> group-and-decompose, FR1 thresholds, FR4 ≥2-topology). The `DRAFT/PROPOSED/PLACEHOLDER` language is
> removed and the placeholder fixtures are replaced by the **scored results** (`dim2-scored-results.md`,
> FR4-satisfied across 3 topologies, 2026-06-28). It is the candidate **frozen doctrine** for the dim-2
> pre-registration ceremony (`dim2-CEREMONY-RUNBOOK.md`). The founder confirms this file at the freeze;
> until the signed tag lands it is not yet anchored. The full decision arc lives in
> `dim2-adversarial-review.md`, `dim2-worktype-synthesis.md`, and the §9 decision log of the DRAFT.

## 1. What "authorization latency" measures

The dimension is **Rail Authorization-Primitive Latency (RAPL)**: it times a rail/protocol
**authorization primitive**, *not* an agent-perceived latency. A companion **agent-observed
total-latency** metric is reported alongside (§2.5).

**Definition.** Authorization-primitive latency is the wall-clock time from the agent issuing its **pay
command** (the payment payload constructed and on the wire — the standardised `t = 0`, §2.5) to the point
the rail returns an **authorization-primitive decision** — "this payment/mandate is validated" or "this
payable grant is issued" — **prior to and distinct from settlement finality** (§3). The *kind* of decision
differs by rail, which is why the dimension is **split** into validation-type and grant-type sub-rankings
(§2).

Where settlement-finality (dimension 1) answers *"when can I rely on this payment as irreversible?"*, RAPL
answers *"how fast does this rail tell me the payment is allowed to proceed?"* — the gate an agent hits
*before* it commits to a rail. The two are complementary Tier-1 timing dimensions on the same six rails.

**Unit.** Seconds, wall-clock, intent-presented → authorization-granted signal (per-rail: an HTTP 200 on a
verify/accept call, a mandate-verified response, or an invoice-issued event). The rail's protocol/HTTP
envelope is bundled in, because that is what the agent actually waits on.

**Direction.** Lower is better. The race semantics are identical to finality, so the BT/`P(auth≤k)`/Wilson
machinery applies within a sub-ranking (§4).

## 2. Per-rail operationalisation — the SPLIT design

The §8 cross-lineage gate **refuted the single-race doctrine 0–4** and found the L402 pin a **category
error**. The dimension is therefore **SPLIT**: authorization is *not one shared concept* across these rails,
so each rail is raced **only against rails whose authorization point is the same kind of object**. A rail is
measured on **whichever primitive(s) it actually has**. The x402 rails have *both* a challenge-issuance and a
validation primitive, so they appear in both A and B (two distinct, separately-measured quantities); L402 has
only a challenge-issuance primitive, so it appears only in B; AP2 has only a validation primitive, so only in
A.

The metric times an **authorization primitive** (facilitator/server-side); on fused topologies an agent never
sees it pre-settlement. A **companion agent-observed total-latency** metric is reported alongside (§2.5).

### Sub-ranking A — Payment-Validation Authorization
*(the primitive validates a payment/mandate the payer has submitted; raced within-group → C(5,2)=10 pairs)*

**Tempo-*Charge* is excluded** from the raced set (RR1): its verify+settle are fused at ~500 ms, so racing it
would measure settlement, not authorization. The exclusion is stated here in the main text (FR5), with the
developer-facing note that a one-shot 1-RTT *Charge* flow does **not** inherit the Group-A profile (Session
does); Charge's fused ~500 ms is reported in an appendix, not ranked.

| Member | Validation primitive | Trust/equivalence class · visibility |
|---|---|---|
| x402-Base (R1) | Facilitator `/verify` of the signed EIP-3009 payload (off-chain) | payer-signed-payment validation · client-visible: spec yes / fused no |
| x402-Stellar (R2) | Facilitator `/verify` (Soroban auth-entry signatures, simulate) | payer-signed-payment validation · client-visible: spec yes / fused no |
| x402-Solana (R9) | Facilitator `/verify` of the signed SVM payload (**earlier than `confirmed`**) | payer-signed-payment validation · client-visible: spec yes / fused no |
| Tempo-Session (R10b) | Server `Verify` of an off-chain signed voucher | payee/server voucher validation · client-visible: yes |
| GCP + AP2 (R6) | Mandate verification (dispatch hop **decomposed out**, §2.5) | **auth-only / no funds-check**, does not settle · **scope = whole rail** |

### Sub-ranking B — Challenge-Issuance Latency
*(the primitive issues a payable 402 challenge before the payer commits; raced within-group → C(5,2)=10 pairs)*

| Member | Challenge-issuance primitive | Trust/equivalence class |
|---|---|---|
| x402-Base (R1) | Issue the `402` + `accepts` payment requirements | server-issued payment challenge |
| x402-Stellar (R2) | Issue the `402` + Soroban payment requirements | server-issued payment challenge |
| x402-Solana (R9) | Issue the `402` + SVM payment requirements | server-issued payment challenge |
| MPP-on-Tempo (R10) | Issue the `402` + `WWW-Authenticate: Payment` challenge | server-issued payment challenge |
| MPP-on-Spark-Lightning (R11) | Issue the **macaroon + BOLT11 invoice** (the L402 challenge) | server-issued grant-to-pay (invoice incl.) |

**AP2 is absent from B** (no 402 challenge — mandate-validation only). **L402 is absent from A** — it has no
pre-settlement payment-validation point (§2.3). L402's challenge issuance includes **BOLT11 invoice
generation** (a real Lightning operation), so B is not a pure constant across rails.

**Scored values:** the per-rail `{median, P95, P99}` (group-and-decompose tuple, 3 topologies) live in
`dim2-scored-results.md` — the FR4-satisfied scored set (2026-06-28). The **scored result is the
within-group order**, not the absolute ms (which are path-dependent for network rails): A-network
**Solana < Stellar < Base** (robust across all 3 topologies); A-local **AP2 (DPC 1.58 ms headline / HP 0.68
ms) and Tempo-Session (warm 8–20 ms, host-dependent)**; B spans local-402 (~1.6–3 ms) to Lightning invoice
mint (~0.55–0.94 s).

### 2.1 Per-rail mechanics & nuances
- **R9 (Solana): accept ≠ `confirmed`.** The facilitator accept is **earlier** than on-chain `confirmed`
  (~2.27 s); `confirmed` is the *settle-at-confirmed* checkpoint, not the accept. → Record three checkpoints
  (§2.2).
- **R10 (Tempo): only Session is raced (RR1).** The MPP spec mandates a `Verify` separate from `Settle`. The
  one-time **Charge** fuses verify+settle into ~500 ms → **excluded from A** (racing it = racing settlement),
  disclosed in an appendix; **Tempo-Session** (near-zero off-chain voucher verify) is the raced A member.
  Tempo also appears in **B** for its `402`-challenge issuance.
- **R11 (L402/Spark): challenge-issuance only (B).** The macaroon + invoice are issued **before** the payer
  pays; the **preimage** is the settlement proof (Spark's conditional-lock → SSP-preimage finalize, the
  ~16.5 s ceremony = settlement). L402 has **no pre-settlement validation primitive** (§2.3) → absent from A,
  races in B on challenge-issuance.
- **R6 (AP2): mandate verify.** Authorization = mandate-verify; the external dispatch/orchestration hop is
  **decomposed out** of the raced quantity (§2.5, Q1 resolved). AP2 does not settle.

### 2.2 Checkpoint-recording model (record all three)
Where a rail exposes them, record up to three checkpoints per payment and **race the accept**:
1. **accept** — the authorization go-ahead (the §2 tables). *Raced; lower-is-better.*
2. **intermediate settle signal** — Solana `confirmed`, Tempo ~500 ms block, the L402 preimage / Spark SSP
   finalize (rail-dependent; may equal #3).
3. **finalized** — the dimension-1 settlement-finality point.

The **accept → finalized gap** is itself a publishable quantity (e.g. Solana ≈ accept vs ~14.6 s). Capturing
the accept requires invoking the rail's **verify primitive explicitly** — a fused HTTP 200 does not expose
the accept.

### 2.3 Why the SPLIT (and not a trust-class label) — the category-error fix
A label *names* a category error without *removing* it, and a single Bradley-Terry race implicitly treats the
items as differing in degree along one latent axis when they differ in **kind**:
- **Validation-of-payment** (A) — x402 `/verify`, MPP `Verify`, AP2 mandate-verify all validate *something the
  payer has already submitted*. "Is this payment/mandate valid?"
- **Grant-to-pay** (B) — L402's macaroon+invoice is the server *issuing a payable challenge before the payer
  has committed anything*. "Here is what to pay." In ISO-8583 terms it is the merchant's `0100` *request*, not
  the issuer's `0110` *response* — an earlier protocol step than A's checkpoint.

**Why not re-pin L402 into A.** In Lightning, *payment is settlement* (the preimage is revealed by paying); a
"payment-accepted" signal would land on preimage-verification — i.e. **settlement (dimension 1)**, not
authorization. So L402 belongs in its own grant-type sub-ranking B. **AP2 stays in A but tagged** auth-only /
no-funds-check (load-bearing), with its external dispatch hop decomposed out, so A races the comparable
mandate-verify step, not a party-to-party network call.

### 2.4 Terminology honesty
No rail publishes a metric literally named "authorization latency": x402 calls it `/verify`, MPP
"verification", AP2 "mandate verification", L402 the macaroon/challenge. The *separability from settlement is
genuine and published on every rail*, but "authorization latency" is **PayBench's framing** over those
primitives. Conceptual precedent exists (the card-network **ISO-8583** split of real-time authorization
0100/0110 from settlement 0200/0220), so the dimension ports a long-standing distinction rather than inventing
one; but **no prior benchmark measures it** (novelty checked & defensible — `research.md`: card-network limits
are SLAs, not a comparative benchmark).

### 2.5 Measurement & statistics package
The sub-100 ms regime is unforgiving; all of the following are pre-registered before any scored run:

- **`t = 0` standard.** Start the clock when the agent issues the ultimate pay command — the payment payload
  constructed and on the wire (not an empty GET that merely triggers a 402) — uniformly across rails.
- **Client-side, RTT-subtracted measurement (FR3/FR4).** Measure **client `send()` → last byte of the
  authorization response payload** (an explicit end-of-auth marker), not first byte (FR3: a first-byte
  stopwatch lets a rail emit early framing before finishing the mandated work and game the metric). Subtract a
  baseline RTT from a **same-path, app-layer (TCP/TLS) probe** that traverses the same route + TLS termination
  (FR4 — an ICMP ping is invalid here). **Report raw and RTT-corrected**, publish the **min-RTT floor per
  endpoint**, and report a **≥2-topology sensitivity** (FR4/D4e, below).
- **Warm vs cold start.** Pre-register warm-start-only (discard the first *N* calls: TLS + pool warmup) vs
  cold-inclusive; report both.
- **`P(auth ≤ k)` — a latency CDF (RR3), not "pass@k".** Millisecond k-ladder `{20, 50, 100, 250, 500} ms`
  with a rank-stability heatmap and a variance-aware power analysis for minimum *n* per pair; report
  **median / P95 / P99** alongside.
- **Hardened Bradley-Terry, with a survival-model fallback.** BT within a sub-ranking only (never across A/B),
  consistent with the frozen dimension-1 spine, plus a **Davidson ties extension** and an explicit
  **censoring / competing-risks rule** for authorization *failures* (reject / timeout enter the model, not
  silently dropped). Report **Kaplan-Meier** curves for description. **Pre-specify a survival model (Cox PH /
  Aalen-Johansen) as the data-triggered fallback** with **FR1 numeric triggers (founder-confirmed 2026-06-24,
  frozen at the ceremony):** switch to it if, in any sub-ranking, the **tie-rate > 20%**, OR any rail's
  **auth-failure/censoring-rate > 5%**, OR **> 10% of triples are cyclic** (transitivity violation) / a BT
  goodness-of-fit LR test gives **p < 0.05**. We do **not** swap the engine pre-emptively (that would fragment
  the one-method-across-dimensions story and re-expose frozen D1 without evidence the pathology bites).
- **Anti-gaming work-clause (RR5 — Group A only, FR2).** For Sub-ranking A the timed response must include
  **signature verification + a fresh balance/state read**. This clause does **not** apply to B — challenge
  issuance (e.g. an L402 macaroon + BOLT11 invoice) is a stateless cryptographic operation; B is timed as pure
  issuance work.
- **Assurance normalisation — `P(settled | accept)`.** Record, per rail, the probability that an accept leads
  to settlement (and the assurance depth); without this covariate the lower-is-better race is gameable by
  "doing less" at the boundary.
- **Labels (RR6).** Every row carries a **checkpoint-visibility** tag (`client-visible: yes/no`) and, for AP2,
  a **scope-coverage** qualifier (AP2's number is its *whole* scope; other rails' is the authorization *slice*
  of a larger flow).
- **RPC / facilitator pinning (FR7).** The accept is often RPC-dominated (the facilitator's fresh balance read
  + simulation round-trips — the work-clause), not crypto. Treat the server→RPC hop like FR4 treats the
  client→server hop — disclose + diagnose, never subtract: (1) pin a canonical RPC endpoint per chain-backed
  rail; (2) hold the RPC tier roughly constant across rails; (3) report a server→RPC-RTT diagnostic. For
  hosted-facilitator rails (Solana/Stellar via x402.org) pin/disclose the **facilitator** endpoint instead.
- **Companion agent-observed total latency (co-primary).** Alongside the primitive latency, report
  time-from-pay-command-to-usable-signal (accept + the accept→settle gap). The primitive ranking can invert
  the end-to-end experience, so the two are displayed together. (On fused topologies this companion equals
  settlement time — the honest disclosure for those rails.)

### 2.5.1 Work-type decomposition & grouping (DR4 — group-and-decompose)
The Q4 first-party runs showed that **within each sub-ranking the rails span 2–3 orders of magnitude of
*work-class*** (A: AP2 local crypto ~1.6 ms / Tempo-Session ~8–20 ms / x402 facilitator 200–800 ms; B:
local-402 ~2–3 ms / Lightning invoice-mint ~0.55–0.94 s). A round-4 cross-lineage scan refuted the
"one race + scalar label + median-only" framing 4/4; the convergent fixes:

- **(D4a) Tail as headline.** Report **P50 / P95 / P99 + N + measurement-timestamp + topology** as the
  headline tuple per rail (the median alone is not a point estimate for network-bound rails — Lightning moved
  1252 ms@n=15 → 936 ms@n=30).
- **(D4b) Per-rail decomposition tuple.** Report `(local_compute_floor, backing_service_component, E2E)`. E2E
  stays the headline (we never subtract from it — RR5/FR2/FR7 work-clause); the decomposition is the
  protocol-design view served as a secondary number. The min-RTT floor (FR4) and server→RPC-RTT diagnostic
  (FR7) are the inputs.
- **(D4c) Work-class grouping (the structural change).** Within a sub-ranking, group rails by work class —
  *Local-complete* (no network round-trip in the primitive's critical path) vs *Network-dependent* (≥1
  intrinsic backing-service round-trip per call). **Rank within a group; compare across groups only via the
  decomposition tuple (D4b) — never as a single cross-class ordinal.** When between-class spread (250–800×)
  dwarfs within-class spread (≤~2×), a single ordinal encodes class membership, not rail quality.
- **(D4d) Tempo TTL is reference-impl config, not a rail class.** Report `L_hot` (cache-hit) and `L_cold`
  (cache-miss → chain read) with the request inter-arrival distribution disclosed (and/or a TTL sweep
  {0, 5 s, 60 s, ∞}); do **not** give TTL a third taxonomy bucket (gaming-prone). Tempo appears in both groups
  by its warm (Local-complete) and cold (Network-dependent) numbers, each annotated.
- **(D4e) ≥2 topologies MANDATORY for network-dependent rails (FR4, founder-confirmed 2026-06-24).** A single
  topology measures the harness, not the rail; a second network-distinct vantage (a named cloud region) is
  **required** before any network-dependent number is scored. Local-complete rails being topology-invariant is
  the built-in control. **Satisfied 2026-06-28** across T1 devbox / T2a Codespaces (Azure) / T2b OCI
  (uk-london-1).
- **(D4f) Workload + deployment disclosure.** Disclose workload constants (macaroon caveat count, voucher /
  x402-header / payload sizes) and the AP2 **in-process vs sidecar** assumption (the in-process number omits an
  IPC hop a sidecar would add). Concurrency / throughput are explicitly out of scope (latency-only).
- **(D4g) AP2 worked example — within-class work-modes (DPC headline).** AP2 spans two authorization modes
  inside the Local-complete class: **delegated / DPC** (`~~` KB chain, human-not-present — **2 ES256**,
  **1.58 ms**, σ_log 0.009) and **human-present** (issuer-only single token — **1 ES256**, **0.68 ms**, σ_log
  0.027). **The DPC/delegated number is the AP2 headline** (an agent acting autonomously on a delegated
  credential is the agentic-representative case); human-present is a reported variant. Both numbers are from
  durable, replayable captures (`dim2-scored-results.md`; `agentpay` `poc/rail-ap2`).

**Fork resolution — GROUP-AND-DECOMPOSE.** One table per sub-ranking, grouped by work class (D4c), with the
decomposition tuple (D4b) carrying the cross-group story. Rank within a group; compare across groups only via
the decomposition — no single cross-class ordinal. *(Not adopted: the "two separate leaderboards" split —
rejected because a Local-complete-A group is n=2 and grouping-within-one-table preserves the same
anti-misleading guarantee without fragmenting into n=1/n=2 "races.")*

## 3. How AP2 (R6) is measured here
AP2 does not settle independently and is excluded from finality; authorization latency is the dimension where
it is well-defined and apples-to-apples. AP2's distinctive cost is **mandate-verification** — an
authorization-layer phenomenon — so on this dimension R6 is a first-class competitor in **Sub-ranking A**
(C(5,2)=10 pairs), tagged auth-only/whole-scope; it is absent from B. **Scope (Q1) resolved:** the timed
quantity is the **mandate-verify** (the external dispatch/orchestration hop is decomposed out — §2.5/D4b), and
AP2 is reported as two within-class modes (DPC headline / human-present variant — D4g).

## 4. Statistics — core methods reused, hardened (see §2.5)
Authorization-primitive latency is lower-is-better, race-the-pair, so the dimension-1 spine applies **within a
sub-ranking**, hardened:
- **Bradley-Terry MLE** over pairwise races — `prior=1.0`, same-kind rails only, **plus a Davidson ties term**
  and a **censoring/competing-risks** rule for reject/timeout. **Cox PH / competing-risks pre-specified as the
  FR1-triggered fallback** (we do not swap pre-emptively; §2.5).
- **`P(auth ≤ k)`** (latency CDF, not pass@k) — millisecond k-ladder + rank-stability heatmap + variance-aware
  power analysis; **median/P95/P99** reported alongside.
- **Wilson lower-bound CIs** — unchanged; **Kaplan-Meier** survival curves added for description.

BT within-sub-ranking only keeps the one-method-across-dimensions story intact. Tempo is genuinely bimodal
(Charge ~500 ms vs Session ~0), which is why DR3 **bifurcates it into two pseudo-rails** rather than fitting
one log-normal; the generator assumes `family: lognormal` per (pseudo-)rail and flags any further non-log-
normal shape for review.

---

## Pre-registration scope (what the dim-2 ceremony freezes)
- **This doctrine** (§1, §2 + §2.1–§2.5.1, §3, §4) — the SPLIT design, the measurement/stats package, FR1
  numeric thresholds, the FR4 ≥2-topology requirement + named topologies, and DR4 group-and-decompose.
- **`dim2-scored-results.md`** — the scored per-rail `{median, P95, P99}` (group-and-decompose, 3 topologies).
- Ceremony mechanics per `dim2-CEREMONY-RUNBOOK.md` (OpenTimestamps → cosign/Rekor → signed tag → OSF/DOI →
  arXiv), a dim-2 pass distinct from the landed dim-1/v1.2 finality pre-reg.

**Excluded by design** (process / disposition-accruing, mirrors the dim-1 manifest's exclusion of its
adversarial-review companion): the cross-LLM review files (`dim2-review*`, `dim2-worktype-*`,
`dim2-measurement-review*`), the pilot log, and the runbooks.
