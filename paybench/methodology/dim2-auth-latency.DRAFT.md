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

**Proposed definition.** Authorization latency is the wall-clock time from a
payment intent being *presented* to a rail to the point the rail returns an
**authorization decision the agent may act on** — i.e. "this payment is approved
to proceed" — **prior to and distinct from settlement finality** (§3).

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

## 2. Per-rail operationalisation — the reliance-level analogue (PROPOSED, evidence-grounded)

§3 (finality) pins each rail to its **ecosystem-canonical reliance level**. The Day-30
analogue pins each rail to its **canonical authorization point** — the protocol step at
which the rail issues the **go-ahead that the payment is *authorized to proceed toward
settlement*** (explicitly **not** the point of irreversible reliance; §1). As in §3 this
is per-rail (rails do not share one authorization model) and — as in §3 — the asymmetry
is **named, not hidden**, via a trust/equivalence-class column. **Every row below is
primary-source-validated** (three research passes 2026-06-20, `dim2-auth-latency.research.md`).

| Rail | Authorization point — *pinned* | Trust / equivalence class |
|---|---|---|
| x402-Base (R1) | Facilitator **`/verify` accept** of the payer's signed EIP-3009 payload (off-chain: sig recovery + balance + simulation), before the on-chain `transferWithAuthorization` settle | Facilitator off-chain **validation of a payer-signed payment authorization** |
| x402-Stellar (R2) | Facilitator **`/verify` accept** (decode XDR, check Soroban auth-entry signatures, simulate), before OZ-Relayer submission | Facilitator off-chain **validation of a payer-signed payment authorization** |
| x402-Solana (R9) | Facilitator **`/verify` accept** of the signed SVM payload (off-chain) — **earlier than** Solana `confirmed` | Facilitator off-chain **validation of a payer-signed payment authorization** |
| MPP-on-Tempo (R10) | Server **`Verify` procedure** (validate the `Authorization: Payment` credential) before broadcast | **Payee/server** off-chain **validation of a payer credential** |
| MPP-on-Spark-Lightning (R11) | Server **issuance of the macaroon authorization grant + BOLT11 invoice** (the 402 challenge), before the payer pays / the Spark FROST+SSP preimage-release ceremony | **Server-issued authorization *grant* (token)** — *grant-to-pay*, **not** verify-of-payment ⚠ |
| GCP + AP2 (R6) | Authorization-layer **mandate verification → payment-credential issuance → dispatch** to the Merchant/processor | **Dedicated authorization layer** — cryptographic mandate proof, rail-agnostic, **does not settle** |

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
  finalize (the ~16.5s ceremony = settlement). See the named asymmetry in §2.3.
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

### 2.3 Named asymmetries (the §3-analogue — do not average away)

Authorization points are **not equi-conservative**, and the research showed the security
*object* differs across rails. Name it, exactly as §3 names the finality reliance-level
asymmetry:

- **Validation-of-payer vs grant-to-payer vs mandate-verify.** R1/R2/R9/R10 time the
  **validation of the payer's submitted payment authorization** ("your payment is valid").
  **R11 (L402)** times the **issuance of an authorization *grant*** (the macaroon — "here
  is your authorization to pay"), which sits **earlier in the flow** and is a *different
  security object* (server grants vs facilitator validates). **R6 (AP2)** times a
  **dedicated authorization layer's** mandate verification + credential issuance. The
  published table must carry the trust/equivalence-class column above and flag that R11's
  point is a grant, not a verify — a candidate **cross-lineage-gate question** (§8): is
  macaroon-issuance the right race analogue of an x402 facilitator-accept, or should R11
  be pinned to a later "payment-accepted" signal for apples-to-apples?
- **Off-chain vs on-chain.** All accepts are **off-chain** except R10's *Charge* path,
  where verify+settle fuse at the ~500ms on-chain point.
- **Per-rail structural variants are expected** (the §9 roadmap note): the timer will need
  rail-specific checkpoints (component splits, grant-vs-verify) — AP2's verify/orchestration
  split is the first instance, not a one-off.

### 2.4 Terminology honesty

No rail publishes a metric literally named *"authorization latency"*: x402 calls it
`/verify`, MPP calls it **"verification"**, AP2 calls it **"mandate verification /
credential issuance"**, L402 calls it the **macaroon/challenge**. The *separability from
settlement is genuine and published on every rail*, but **"authorization latency" is
PayBench's framing** over those primitives. Conceptual precedent exists — the card-network
**ISO-8583** split of real-time authorization (MTI 0100/0110) from settlement (0200/0220)
— so the dimension ports a long-standing distinction rather than inventing one; but **no
prior benchmark measures it** (novelty plausible, re-check before any published claim, §8).

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

## 4. Statistics — reused unchanged (no new methodology)

Authorization latency is another **lower-is-better, race-the-pair** dimension, so
the §5 methods transfer **without modification**:

- **Bradley-Terry MLE** over pairwise authorization races (lower latency wins;
  ties split 0.5/0.5) — same `bradley_terry_mle`, same `prior=1.0` smoothing.
- **pass@k = P(authorization ≤ k s)** — same estimator; the k-grid is finer/tighter
  than finality's `[2..20]s` because authorization is sub-second-to-a-few-seconds
  (proposed placeholder grid `[0.25, 0.5, 1, 2, 3, 5]s`, `TODO(calibration)`).
- **Wilson lower-bound CIs** — unchanged.

**Nothing in the statistical layer needed to change** to support this dimension —
the only generalisation was making the *dimension* (name, unit, rail set,
seed-namespace, k-grid, provenance/fixture paths) a first-class parameter. If a
future founder calibration shows authorization-latency distributions are *not*
adequately log-normal (e.g. bimodal from a verify-vs-cache-hit split), that is a
genuine non-transfer to flag for review — **not** something to paper over; the
fixture generator currently assumes log-normal (`family: lognormal`), as finality does.

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
- **Q3 — per-rail authorization-point doctrine.** ✅ **DRAFTED** in §2 — the pinned
  authorization point + trust/equivalence-class column + named asymmetries (§2.3),
  every row evidence-grounded. **Pending the §8 cross-lineage gate** (the open
  sub-question it must settle: is R11's macaroon *grant* the right race analogue of an
  x402 *verify*, or should R11 be pinned to a later accepted signal?) **then founder
  ratification**.
- **Q4 — calibration sourcing.** ⏳ **OPEN.** First-party measurement isolating the
  *authorize* leg from the *settle* leg per rail — invoke the verify primitive
  **explicitly** (research caveat C2); the D1 harnesses already capture
  confirmed/finalized, so the new work is the **accept timestamp** (validation run,
  credentialed testnet). Plus doc/telemetry spread, mirroring Hybrid (C).
- **Q5 — k-grid + scoring constants.** ⏳ **OPEN.** Confirm the finer pass@k grid and
  that the BT smoothing prior (1.0) suits sub-second separations.

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

**This dimension must pass a cross-lineage adversarial review before
pre-registration**, mirroring the gate dimension-1 cleared — the methodology
records a *four-model cross-LLM adversarial review (2026-06-06) that upheld the
finality doctrine 3–1* on the Solana `confirmed`-vs-`finalized` question
(artefacts: `Pre-reg-{Deepseek,Gemini,Kimi,Qwen}`, `pre-reg-adversarial-review.md`).
Dimension 2 has *more* contestable surface than dimension 1, so the gate is not
optional.

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
