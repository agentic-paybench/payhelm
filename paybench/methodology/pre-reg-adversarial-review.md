# PayBench v1.0 — pre-registration adversarial review

**Gate:** methodology freeze (v1.0, 2026-06-05) → cryptographic pre-registration (§9).
**Purpose:** surface every flank a hostile reviewer (CRFM maintainer, statistician, competitor)
would attack *before* the method is irreversibly anchored. Full cross-LLM adversarial review is
reserved for this gate (per the `cross_llm_adversarial_review` + `regulatory_drafting_lessons`
operating memories) — this document is the input to that review.

This is an internal review artefact, not part of the pre-registered method. It is committed
alongside the methodology because publishing one's own adversarial pass *strengthens* a
pre-registration (it pre-empts the critique and demonstrates the Leaderboard-Illusion fix-list is
lived, not decorative).

---

## Findings — severity-ranked

| # | Finding | Severity | Status |
|---|---|---|---|
| F1 | Per-rail finality threshold is not equi-conservative (Base **soft** vs Solana **finalized**) | **HIGH** | Resolved in-doc via stated doctrine; **user decision D1** confirms or redirects |
| F2 | Quiet-condition `sigma_log` understates mainnet tails (R9, R11 sharpest) | MED | Pre-registered as disclosed limitation (§7); **user decision D2** = freeze-as-is vs widen |
| F3 | R2 fixture is the manual-path **lower bound**, not the spec x402-on-Stellar path | MED | Pre-registered as disclosed limitation (§3¹, §7) |
| F4 | `request → HTTP 200` unit bundles protocol/HTTP envelope with on-chain settlement | LOW–MED | Defended in §3 (agent-DX framing); disclosed |
| F5 | Log-normal family imposed on deterministic-finality rails (Stellar, Tempo) | LOW | Disclosed default; acceptable for mock fixtures |
| F6 | BT MLE is near-degenerate under this much cluster separation | LOW | Honest note; pass@k is the load-bearing metric here |
| F7 | R10 fixture = pure-Tempo path; Stripe acceptance leg is Variant-E mock | LOW | Disclosed (§3, §7); correct scoping |

---

## F1 — finality-threshold doctrine (HIGH) — **needs user decision D1**

**The attack.** "You measure Base at *soft* finality (~2 s, 1 block, optimistic-rollup sequencer
inclusion) but Solana at *`finalized`* (~14.6 s, 32-slot rooted) rather than `confirmed` (~2.3 s).
Those are different reliance thresholds. Apply Base's lenient doctrine to Solana and R9 drops to
~2.3 s and leaps up the ranking; apply Solana's strict doctrine to Base and R1's number becomes its
~minutes hard-L1 finality and it falls to last. Your ranking is an artefact of an inconsistent
threshold choice." This is the single most damaging line of attack — it is the one a CRFM reviewer
or a competitor reaches for first, and it materially moves the ranking (R1 is currently #2; R9 #4).

**Why it is not fatal, and the resolution taken.** Rails genuinely do not share one cryptographic
finality model, so *some* per-rail definition is unavoidable. PayBench v1.0 names the doctrine
explicitly (§3): **each rail is pinned to its ecosystem-canonical reliance level** — the level that
rail's own docs tell a builder to rely on for an irreversible downstream action. Under that doctrine
Base-soft and Solana-`finalized` are each *individually* canonical (Solana docs explicitly warn
against treating `confirmed` as irreversible; Base/OP-stack docs present soft finality as the
practical payment-reliance level, reserving hard L1 for bridging/withdrawal). The doctrine is the
right one for an **agent-DX** benchmark — it measures the moment the agent is *told* it can act. The
asymmetry is stated openly in §3 rather than hidden, which is the defensible posture.

**The residual risk.** "Per-rail canonical" is a *judgment* doctrine, not a mechanical one. A
reviewer can still say "canonical-per-rail is a euphemism for cherry-picking the threshold that
flatters each rail." The defence holds only because the doctrine is (a) named, (b) sourced per rail,
and (c) the same doctrine a working agent-builder would apply. If that defence is judged too soft,
the alternative is **D1-alt** below.

> **RESOLVED 2026-06-06 — D1-keep.** Founder confirmed the per-rail-canonical reliance-level
> doctrine as written in §3. No fixture regen. The cross-LLM pass should still attack it hardest
> (see below); if a model lands a decisive refutation, D1 reopens before anchoring.

### Decision D1 (user / Founder + Architect)

- **D1-keep (recommended):** adopt the per-rail-canonical reliance-level doctrine as written in §3.
  No fixture regen. Defensible; names its own flank.
- **D1-uniform-optimistic:** switch to "when can the agent act" everywhere → Solana uses `confirmed`
  (we already captured it: median 2.27 s, σ_log 0.267). Internally symmetric and arguably the
  purest agent-DX choice. **Cost:** regenerate the R9 fixture (new hash), re-run, re-freeze; R9 jumps
  from #4 to near the top — a very different headline.
- **D1-uniform-irreversibility:** strict no-reversal everywhere → Base would need a hard-L1 number
  (~minutes). **Rejected as a live option:** no agent waits minutes for a payment, so this makes the
  benchmark operationally meaningless. Listed only for completeness.

> **D1 is the gating decision for §3 and therefore for the whole pre-registration.** The doc is
> currently written to D1-keep. Confirm, or choose D1-uniform-optimistic and I will regen R9 +
> re-run + re-freeze before anything is anchored.

---

## F2 — quiet-condition spreads (MED) — **needs user decision D2**

**The attack.** "Your own provenance files say to *widen* R9 (σ 0.057) and R11 (σ 0.156) before
publishing — yet you pre-registered the narrow spreads. You've cryptographically frozen distributions
you already flagged as preliminary."

**Resolution.** §7 pre-registers this as an explicit disclosed limitation (no-silent-caps, fix-list
item 7): central tendencies are high-confidence empirical, tails are the disclosed soft spot, and the
fixtures are frozen *as mock fixtures under Variant E* — not as a real-rail ranking. Real-rail
publication re-runs the same frozen method against production fixtures.

> **RESOLVED 2026-06-06 — D2-freeze.** Founder confirmed freezing the empirical σ as-measured +
> the §7 disclosure. Committed hashes unchanged; no regen.

### Decision D2 (user / Founder)

- **D2-freeze (recommended):** freeze the empirical σ as measured + the §7 disclosure. Keeps every
  number first-party-measured (no judgment-call σ inflation), keeps the committed hashes, matches the
  "Built 2026-06-05" closed-decision state.
- **D2-widen:** widen R9/R11 σ toward the doc-informed ~0.15–0.25 before freezing. More realistic
  tails, but introduces a non-empirical σ that weakens the "every number is measured" story and
  changes the committed hashes (regen + re-run + re-freeze).

> Recommendation: **D2-freeze.** The whole point of Variant E is that these are mock fixtures; a
> disclosed-preliminary-tail on a mock fixture is honest, whereas a hand-widened σ on a mock fixture
> trades a measured number for a guessed one to no real-rail benefit.

---

## F3 — R2 manual-path lower bound (MED) — resolved by disclosure

R2's median (2.74 s) is the manual direct-payment path; the spec x402-on-Stellar path adds the OZ
facilitator round-trip and would be slower. Pre-registered as a lower bound (§3 footnote 1, §7
limitation 2). No further action — the spec path is wired and validated end-to-end; the spec-path
n=30 re-measure is a deferred follow-up, not a freeze blocker.

## F4 — `request → 200` unit (LOW–MED) — defended

The unit bundles the protocol/HTTP envelope (x402 facilitator round-trip, MPP/L402 flow) with
on-chain settlement. A purist would want pure on-chain settlement time. PayBench defends the bundled
unit in §3: the full round-trip is what the agent experiences and waits on, which is exactly the
agent-DX quantity the benchmark exists to measure. Disclosed; defensible.

## F5 — log-normal on deterministic rails (LOW) — disclosed default

Stellar (ledger close) and Tempo (BFT block) have near-deterministic finality whose true shape is
tighter-than-log-normal (closer to "constant + small jitter"). Log-normal is the parameter-light
default disclosed in the calibration plan, and for *mock* fixtures whose purpose is to exercise the
pipeline this is acceptable. A future real-rail run can fit the empirical shape directly.

## F6 — BT degeneracy (LOW) — honest note

With clusters this separated (fast ~2 s, slow ~15 s), the slow rails almost never beat the fast ones,
so BT strengths collapse toward the extremes (R10 0.78 … R11 3e-5) and the BT *ranking* reduces to
median order. The symmetric smoothing prior (1.0) keeps the MLE well-defined under near-complete
separation. This is not wrong — but pass@k, not BT, is the metric that actually discriminates here,
and the method should not over-sell BT as if it were adding independent signal in this regime. Worth
a sentence in any write-up; not a freeze blocker.

## F7 — R10 pure-Tempo scoping (LOW) — correct, disclosed

R10's fixture is the pure-Tempo MPP path (real-rail, non-custodial, no Stripe). The Stripe-mediated
acceptance leg is Variant-E mock (US-only). §3 and §7 state this. Correct scoping, not a flaw.

---

## What the cross-LLM review should pressure-test

Feed this document + `methodology.md` to ≥2 independent models and ask each to:

1. **Attack F1 hardest.** Is "per-rail-canonical reliance level" a principled doctrine or a
   euphemism for threshold-shopping? Would a CRFM maintainer accept it? Is D1-uniform-optimistic the
   safer choice despite the R9 regen?
2. Find any finality-threshold inconsistency the seven findings missed (e.g. is Stellar "ledger
   close" the optimistic or conservative Stellar level? is Tempo testnet→mainnet a hidden gap?).
3. Stress the pre-registration mechanics: does freezing a `run_hash` over *mock* fixtures invite the
   reading that the mock ranking is a result? Is the Variant-E firewall in §0/§7 strong enough?
4. Check the statistics independently: Wilson LB usage, BT prior, pass@k definition.

Record dispositions back into this file (one line per finding per model) before executing §9.
