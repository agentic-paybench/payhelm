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

## 2. Per-rail operationalisation — the reliance-level analogue (PROPOSED)

§3 pins each rail to its **ecosystem-canonical reliance level** for *finality*.
The Day-30 analogue is to pin each rail to its **canonical authorization point** —
the protocol step at which that rail considers the payment *authorized to proceed*.
As in §3, this is per-rail (rails do not share one authorization model), and — as
in §3 — the asymmetry should be named, not hidden.

| Rail | PROPOSED authorization point (the D1-reliance analogue) | Placeholder¹ |
|---|---|---|
| x402-Base (R1) | x402 **verify/accept** of the signed payment payload (402 challenge → signed payload → facilitator accept), before on-chain settlement | `TODO(calibration)` |
| x402-Stellar (R2) | x402 **verify/accept** (402 → `createAuthHeaders` → facilitator/manual verify), before ledger close | `TODO(calibration)` |
| x402-Solana (R9) | x402 **verify/accept**; *candidate* signal is Solana `confirmed`-level (~optimistic), explicitly **not** `finalized` — see Open Question Q2 | `TODO(calibration)` |
| MPP-on-Tempo (R10) | MPP **payment-authorization handshake** (mppx envelope), before Tempo BFT settlement; Stripe-mediated acceptance leg is Variant-E mock (scope TBD) | `TODO(calibration)` |
| MPP-on-Spark-Lightning (R11) | L402-family challenge → **BOLT11 invoice issuance / authorization**, before the Spark FROST+SSP preimage-release ceremony | `TODO(calibration)` |
| GCP + AP2 (R6) | **AP2 mandate-verification + orchestration decision** — the authorization layer itself; see §3 (this is AP2's proper, well-defined dimension) | `TODO(calibration)` |

¹ The placeholder `{median_s, sigma_log}` actually shipped in the harness live in
`calibration/provenance/<rail>-auth-latency.provenance.yaml`, each marked
**"PLACEHOLDER — pending founder calibration"**. They exist only to exercise the
pipeline end-to-end; they are not measurements and must not be published or
pre-registered.

**The §3 asymmetry caution carries over.** Just as finality mixes optimistic
(Base soft) and conservative (Solana `finalized`) reliance levels, authorization
points are not equi-conservative across rails (a facilitator "accept" is a
different security object from an AP2 mandate-verify). The published table should
carry the same **trust / equivalence-class** column §3 uses, and name the
asymmetry rather than averaging it away.

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

## 6. Open questions for the founder (must resolve before pre-registration)

- **Q1 — AP2 scope.** Time mandate-verify only, or verify + orchestration to first
  underlying-rail dispatch? (Affects R6's whole meaning.)
- **Q2 — Solana authorization point.** Is `confirmed`-level (~optimistic) the right
  authorization signal for R9? The D1 run already captured a Solana `confirmed`
  latency (~2.27s) "for free"; it is **deliberately not** used in the placeholder
  fixture pending this decision (the §3 doctrine disavows `confirmed` for
  *finality*, but authorization is a different question — `confirmed` may be exactly
  right *here*). The real number is withheld until ratified.
- **Q3 — per-rail authorization-point doctrine.** Ratify the §2 table (the D1
  reliance-level analogue), including the trust/equivalence-class column and the
  named asymmetry, exactly as §3 does for finality.
- **Q4 — calibration sourcing.** First-party measurement isolating the *authorize*
  leg from the *settle* leg per rail (the D1 calibration plan instruments full
  request→finality; auth-latency needs the authorize sub-interval), plus the
  doc/telemetry spread, mirroring the Hybrid (C) approach.
- **Q5 — k-grid + scoring constants.** Confirm the finer pass@k grid and confirm
  the BT smoothing prior (1.0) still suits sub-second separations.

## 7. What is done vs. what a founder must do

**Done this session (mechanical):** dimension-parametric harness; 6-rail/15-pair
auth-latency benchmark runs end-to-end on placeholder fixtures; content-addressed
fixtures + provenance; tests mirroring the finality suite; finality still
reproduces bit-for-bit.

**Founder, next (judgment):** resolve Q1–Q5; replace every placeholder with real
calibration; ratify this doctrine into the methodology; *then* (separately) the
pre-registration ceremony (OSF / cosign / OpenTimestamps / signed tag). See
`SESSION-1-HANDOFF.md`.
