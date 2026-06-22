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
> Still DRAFT — not ratified, not pre-registered; a short second gate round on this revised
> design is advisable before ratification.

**Dimension renamed (DR2): _Rail Authorization-Primitive Latency_ (RAPL)** — provisional;
alt "Protocol-Accept Latency". The rename is load-bearing: the metric times a rail/protocol
**authorization primitive**, *not* an agent-perceived latency (the accept is facilitator/server-
side, and on fused topologies an agent never sees it pre-settlement — §2.5/G1). A **companion
agent-observed total-latency** metric is reported alongside (DR2; §2.5).

**The dimension is SPLIT (DR1)** because authorization is *not one shared concept* across these
rails — the gate showed (0–4) that racing them together is a category error. Each rail is raced
**only against rails whose authorization point is the same kind of object**:

**Sub-ranking A — Payment-Validation Authorization** (the primitive *validates a payment/mandate
the payer has submitted*). Raced with BT + pass@k **within this group**; MPP-on-Tempo is
**bifurcated into two pseudo-rails** (DR3), so C(6,2)=15 pairs:

| Pseudo-rail | Authorization point (validates submitted payment/mandate) | Trust / equivalence class |
|---|---|---|
| x402-Base (R1) | Facilitator `/verify` accept of the signed EIP-3009 payload (off-chain) | Facilitator off-chain validation of a payer-signed payment |
| x402-Stellar (R2) | Facilitator `/verify` accept (Soroban auth-entry signatures, simulate) | Facilitator off-chain validation of a payer-signed payment |
| x402-Solana (R9) | Facilitator `/verify` accept of the signed SVM payload (off-chain; **earlier than `confirmed`**) | Facilitator off-chain validation of a payer-signed payment |
| **Tempo-Charge (R10a)** | Server `Verify` of the one-time `Authorization: Payment` credential (**verify+settle fused at ~500 ms**) | Payee/server validation — **fused with settlement** (disclose) |
| **Tempo-Session (R10b)** | Server `Verify` of an off-chain signed voucher (**near-zero**) | Payee/server validation — off-chain voucher (credential reuse) |
| GCP + AP2 (R6) | Mandate verification → credential issuance (the dispatch hop **decomposed out**, §2.5) | **Auth-only / no funds-check** — dedicated layer, **does not settle** |

**Sub-ranking B — Permission-Grant Authorization** (the primitive *issues a payable challenge
before the payer commits*):

| Rail | Authorization point (issues a grant-to-pay) | Trust / equivalence class |
|---|---|---|
| MPP-on-Spark-Lightning (R11) | Server issuance of the **macaroon + BOLT11 invoice** (the 402 challenge), before the payer pays | **Server-issued grant-to-pay** — not a validation of payment |

Sub-ranking B currently has **one member**, so it is **reported as a standalone quantity, not
raced** (a BT race needs ≥2). *Natural extension:* the x402/MPP **402-challenge issuance** is also
a grant-type event; measuring it would populate B with a real race — flagged for the founder, not
assumed. **L402 is NOT placed in A** (see §2.3 — that is the category-error fix).

All `{median_s, sigma_log}` are `TODO(calibration)` PLACEHOLDERS (footnote¹).

¹ The placeholders shipped in the harness live in
`calibration/provenance/<rail>-auth-latency.provenance.yaml`, each marked
**"PLACEHOLDER — pending founder calibration"** — they exercise the pipeline only;
not measurements, not for publication or pre-registration.

### 2.1 Per-rail mechanics & nuances (the cells above, expanded)

- **R9 (Solana): accept ≠ `confirmed`.** The facilitator accept is **earlier** than the
  on-chain `confirmed` (~2.27s); `confirmed` is the *settle-at-confirmed* checkpoint, not
  the accept (research caveat C1). → Record **three checkpoints** (§2.2).
- **R10 (Tempo): Charge vs Session.** The MPP core spec mandates a `Verify` procedure
  separate from `Settle`. For the one-time **Charge** intent the docs fuse verify+settle
  into one **~500ms** figure (accept instrumentable but not separately *published*); for
  **Session** intent per-payment authorization is a **near-zero off-chain voucher** check.
- **R11 (L402/Spark): a grant, not a verify.** The macaroon (authorization credential) +
  invoice are issued **before** the payer pays; the **preimage** is the settlement proof,
  obtained only by paying. Spark's **conditional-lock** step precedes the SSP-preimage
  finalize (the ~16.5s ceremony = settlement). → **Sub-ranking B** (§2.3 explains why).
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
prior benchmark measures it** (novelty plausible, re-check before any published claim, §8).

### 2.5 Measurement & statistics package (DR3 — gate-mandated)

The sub-100 ms regime is unforgiving; the gate required a tighter measurement contract than
finality's. All of the following are **pre-registered** before any scored run:

- **`t = 0` standard.** Start the clock when **the agent issues the ultimate pay command —
  the payment payload constructed and on the wire** (not an empty GET that merely triggers a
  402). Measure every checkpoint at the **rail edge** (first ingress), uniformly across rails,
  so one rail is not penalised by payload-construction or network RTT that another avoids.
- **Network normalisation.** Fix a **canonical client geography**, publish the **min-RTT floor
  per rail/endpoint**, and report **network-adjusted latency** (`observed − min-RTT`) alongside
  raw — otherwise AP2's anycast endpoints get a systematic edge and the ranking is not
  reproducible across run locations.
- **Warm vs cold start.** Pre-register **warm-start-only** (discard the first *N* calls: TLS +
  connection-pool warmup) vs cold-inclusive, and report both.
- **pass@k in the right regime.** A **millisecond k-ladder** (e.g. `{20, 50, 100, 250, 500} ms`,
  not finality's seconds grid), reported with a **rank-stability heatmap** (the headline `k` is
  load-bearing and can invert the order; fix it before data collection).
- **BT only *within* a sub-ranking.** Bradley-Terry's single-latent-axis assumption holds only
  among same-kind items, so it is run **per sub-ranking**, never across A and B. Report
  **Kaplan-Meier survival curves** alongside, since the generative processes (local crypto vs
  networked-consensus RPC) are mechanistically heterogeneous.
- **Assurance normalisation — `P(settled | accept)`.** Record, per rail, the probability that an
  accept actually leads to settlement (and the assurance depth). A near-instant accept that
  frequently fails downstream is **not** comparable to a slower, near-certain one; without this
  covariate the lower-is-better race is gameable by "doing less" at the boundary.
- **Companion agent-observed total latency (co-primary).** Alongside the primitive latency,
  report **time-from-pay-command-to-usable-signal** (accept + the accept→settle gap). The
  primitive ranking can *invert* the end-to-end experience (a fast-accept/slow-settle rail loses
  overall); the two must be displayed together so the headline is not optimised against the
  outcome agents actually care about. (On fused topologies this companion equals settlement time,
  i.e. collapses into dimension 1 — which is itself the honest disclosure for those rails.)

## 3. How AP2 (R6) is measured here

Per §8 Resolution B, AP2 does **not** settle independently and is therefore
excluded from finality; authorization latency is the dimension where it is
**well-defined and apples-to-apples**. AP2's distinctive cost is
**mandate-verification + orchestration overhead** — an authorization-layer
phenomenon — so on this dimension R6 is a first-class competitor, not a
mislabelled finality entrant. This is the debut §8 anticipated: the rail set is
the **6 POC rails → C(6,2) = 15 pairs → 7,500 trials** (the N16 MockBench
15-pair figure §6/§8 reserved "for a future dimension in which all six rails
compete" — this is that dimension).

**Open scope question (Q1).** What exactly is timed for AP2: mandate-verify
*only*, or mandate-verify *plus* orchestration through to first underlying-rail
dispatch? These measure different things; the founder must choose and the choice
must be pre-registered. The placeholder times mandate-verify + orchestration as a
single envelope (median set above the settling rails to reflect the extra
round-trips) — illustrative only.

## 4. Statistics — core methods reused, but **not** unchanged (see §2.5)

> **Pre-gate this section read "reused unchanged."** The cross-lineage gate corrected that: the
> BT/pass@k/Wilson *core* transfers, but **§2.5 (DR3) imposes real changes** — BT/pass@k run
> **per sub-ranking only**, the **k-grid moves to milliseconds**, and **Kaplan-Meier survival
> curves + a `P(settled|accept)` covariate** are added. Read §4 with §2.5.

Authorization-primitive latency is still **lower-is-better, race-the-pair**, so the §5 core
methods apply *within a sub-ranking*:

- **Bradley-Terry MLE** over pairwise races (lower wins; ties 0.5/0.5) — same `bradley_terry_mle`,
  `prior=1.0` — **but only among same-kind rails** (a single latent axis is invalid across the
  grant/validation kinds; §2.3). Report **survival curves** alongside (heterogeneous processes).
- **pass@k = P(authorization ≤ k)** — same estimator, **millisecond k-ladder** (not finality's
  seconds grid), pre-registered with a rank-stability heatmap (§2.5). *(The earlier placeholder
  grid `[0.25..5]s` is superseded.)*
- **Wilson lower-bound CIs** — unchanged.

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
- **Q3 — per-rail authorization-point doctrine.** ♻️ **GATE-FAILED then RE-DRAFTED
  (2026-06-22).** The single-race draft was refuted 0–4 (`dim2-adversarial-review.md`); §2 is
  now the **revised SPLIT design** with DR1–DR3 adopted (§9). **Remaining:** (optionally) a
  short second cross-lineage round on the *revised split* before founder ratification.
- **Q4 — calibration sourcing.** ⏳ **OPEN.** First-party measurement isolating the
  *authorize* leg from the *settle* leg per rail — invoke the verify primitive
  **explicitly** (research caveat C2); the D1 harnesses already capture
  confirmed/finalized, so the new work is the **accept timestamp** (validation run,
  credentialed testnet). Plus doc/telemetry spread, mirroring Hybrid (C).
- **Q5 — k-grid + scoring constants.** ⏳ **OPEN, gate-informed.** The cross-lineage panel
  says the k-grid must move to the **millisecond** regime (finality's seconds grid is wrong
  for a 1–200 ms quantity), be a **pre-registered k-ladder** (e.g. {20,50,100,250,500} ms)
  reported with a **rank-stability heatmap**, and that **BT is only valid *within* a
  sub-ranking** (post-SPLIT) — consider **Kaplan–Meier survival curves** alongside it.

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
  *pre-gate* single 6-rail race with the seconds k-grid. Re-aligning it to the split (two
  sub-rankings), the bifurcated Tempo pseudo-rails, and the ms k-ladder is a **post-ratification
  implementation task** — deliberately deferred so it is not built against an un-ratified design.
