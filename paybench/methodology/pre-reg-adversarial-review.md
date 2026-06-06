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

---

# Cross-LLM review round — recorded 2026-06-06

Four independent model families reviewed `methodology.md` v1.0 + this file: **Gemini**, **DeepSeek**,
**Kimi**, **Qwen** (raw outputs: `Pre-reg-{Gemini,Deepseek,Kimi,Qwen}.{md,txt}` in this dir).
Synthesised under the triangulation rule (act on consensus; re-test isolated objections).

## F1 (finality doctrine) — D1-keep HOLDS (3–1)

- **Kimi, Qwen, DeepSeek: keep per-rail-canonical.** Switching Solana to `confirmed`
  (D1-uniform-optimistic) would publish a figure Solana's *own docs* call unsafe for irreversible
  action → **measurement invalidity**, a worse flank than the asymmetry. The doctrine is
  *descriptive* (what each rail tells its builders to rely on), not marketing-driven.
- **Gemini (isolated): switch to uniform-optimistic.** Re-tested against the Kimi/Qwen counter and
  **rejected** — the counter (confirmed = a rail-disavowed threshold) is decisive.
- **BUT all four demand the doctrine be HARDENED, two independent ways:**
  - **Trust-assumption / equivalence-class column** in §3 (Qwen "Trust Assumption"; Kimi
    "Equivalence class") — make the centralized-sequencer-promise vs decentralized-BFT-root vs
    optimistic-rollup distinction *visually explicit* so "apples-to-oranges" can't be claimed as hidden.
  - **Stop suppressing Solana `confirmed`** (DeepSeek, HIGH sub-finding): the 2.27 s figure was
    captured but not shown; not showing it reads as threshold-shopping. → at minimum acknowledge it.
- **Disposition: D1-keep + add the equivalence-class/trust-assumption column + acknowledge the
  Solana `confirmed` figure exists.** (Interacts with F14 — see below.)

## New HIGH findings the self-pass + first pass missed

- **F13 (DeepSeek, HIGH) — pre-registration AFTER calibration = HARKing on the k-grid.** Calibration
  ran 2026-06-04/05; method froze 2026-06-05. The k-grid `{2,3,5,10,15,20}` and the "two clusters"
  narrative were chosen *knowing* the medians. §5.2's own words ("chosen to discriminate across the
  calibrated medians") admit it. Corroborated by **Gemini F9 (grid-hacking)**. Pre-reg prevents
  p-hacking on the *mock run* but not on the only real data (the calibration). **Fix (prose, no
  regen):** re-justify the k-grid on *external* agent-SLA grounds (2 s HTTP norm, 10 s gateway
  timeout, …) AND candidly state the grid was finalised post-calibration so the mock run validates
  the *pipeline*, not an independent hypothesis; the same frozen grid carries to the real run (where
  it IS pre-data). Kimi/Qwen judged this acceptable *given* the grid is frozen a priori for the real
  run — consistent with the disclosure fix.
- **F14 (DeepSeek, HIGH) — the §7 calibration table IS a real-rail ranking → Variant-E / perimeter
  breach.** Five rails, real measured medians from real testnet/devnet/regtest infra, in rank order.
  "Calibration parameter" vs "ranking" is a distinction without a difference when the parameter is
  the ranked quantity. Regulatory risk: if the FCA reads this as published comparative rail
  performance, the Variant-E firewall (and the narrow-scope-publication posture) has a
  calibration-table-sized hole — in the *public* OSF/arXiv artefact. **Needs a Founder decision (see
  the decision gate).** *Tension with F1:* curing F1 by publishing Solana `confirmed` publishes MORE
  real-rail numbers, aggravating F14.

## Consensus prose fixes (4/4 or 3/4 — zero regen)

- **Rename R11 display label → "MPP-on-Spark-Lightning"** (all four). The fixture `rail_name` already
  says "via Lightspark/Spark" (no hash change); the *table/text* label "MPP-on-Lightning" overclaims
  generic Lightning when the ~16.5 s is the Spark FROST+SSP ceremony.
- **`run_hash` clarifier** (Kimi F12, Qwen): add a §9 sentence — it verifies bit-for-bit reproduction
  of the *mock* pipeline output; it is **not** a real-rail ranking result. (Consider renaming to
  `mock_pipeline_verification_hash`.)
- **BT prior-dependence caveat** (Qwen, Kimi, DeepSeek): §5.1 — under complete cluster separation the
  BT *magnitudes* are an artefact of the prior + trial count; only rank order + within-cluster
  differences are interpretable. Don't report fine-grained strengths as precise.
- **Wilson scope caveat** (Qwen, Gemini, DeepSeek): §5.3 — all Wilson CIs are *pointwise* 95% (no
  FWER/FDR adjustment across the ~40 CIs); and on mock fixtures they capture *Monte-Carlo sampling
  error of the harness*, not real-world network variance.
- **`request → 200` semantics** (Kimi F10): §3 — re-word the unit to "agent-perceived finality signal
  (HTTP 200 / webhook / polled state transition per adapter)" so it can't be read as mixing
  acceptance with finality.
- **R10 testnet→mainnet caveat** (Kimi F9, Qwen, Gemini F10): §7 — add a third disclosed limitation:
  Moderato testnet may differ from mainnet Presto (validator count / topology / O(N²) BFT message
  complexity) despite shared consensus.
- **R11 "real-rail" → "hosted-operator stack on regtest"** (Kimi F8): precision correction in the §7
  approach label.
- **"Deterministic" vs σ spread** (Kimi F11): §3 parenthetical — "deterministic" = finality guarantee
  (no reorg), not zero timing jitter.
- **R2 ledger-window note** (Qwen): provenance/§3 — 2.74 s reflects uniform submission within the
  ~5.5 s ledger-close window (half-interval), not sub-ledger finality.

## Defer to the real-rail run / ops (noted, not freeze blockers)

- **F15 (DeepSeek, MED)** master seed = POC date, not random → for the real run, derive from a future
  Bitcoin block hash (can't be known at design time). (Mock seed staying = fine.)
- **Distributional fix (DeepSeek/Gemini)** discrete "constant + jitter" for deterministic rails (R2,
  R10) instead of log-normal → real-rail run.
- **σ_log parameter CIs** (DeepSeek §3.2): n=30 is thin for the tail; bootstrap + propagate → real run.
- **F16/F17 (DeepSeek)** anchor robustness: OSF URL SPOF + arXiv post-freeze edits → handle in
  CEREMONY-RUNBOOK (independent archival; v1-only canonical; Rekor+OTS sufficient without OSF).
- **Watermark artefacts** (Qwen, DeepSeek, Kimi): arXiv title + OSF abstract + harness CLI must say
  "Mock / Simulated Fixtures — not production rankings" → runbook + (optional) CLI banner.
- **F18 (DeepSeek, LOW)** move the defamation/right-of-reply legal framing out of §10 into ops docs
  (tonal — "neutral instrument" claim vs lawyering-up).

## Net verdict

D1/D2 both **survive** the cross-LLM round. No fixture regen is required by any consensus finding.
The freeze needs **one batch of zero-regen prose hardening** (the consensus fixes above) plus **two
Founder decisions** — F14 (the calibration-table-as-ranking perimeter question) and the F1↔F14
disclosure tension — before re-freezing the manifest and anchoring.

## Resolution — methodology v1.1 (2026-06-06)

**Founder decisions:** F14 → **de-rank + caveat**; F1 → **acknowledge in prose only**. Applied in
v1.1 (no fixture regen; fixture hashes + mock-pipeline hash `895f99ed…` unchanged):

- **§0** banner → v1.1; cross-LLM round + hardening recorded.
- **§3** — trust/equivalence-class column added; Solana `confirmed` (~2.3 s) acknowledged as captured
  (doctrinal, not suppression) + the 3–1 cross-LLM upholding noted; **median column removed** (F14);
  R11 → **MPP-on-Spark-Lightning**; unit → "agent-perceived finality signal" (F10); deterministic-vs-σ
  + R2 ledger-window notes added.
- **§5.1** — BT-magnitude-is-prior-artefact caveat (only rank order / within-regime interpretable;
  raw win/loss matrix published).
- **§5.2** — `k`-grid re-justified on **external agent-SLA grounds** + explicit candour that
  calibration preceded the freeze (F13/grid-hacking); per-rail pass@k values removed.
- **§5.3** — Wilson pointwise-not-FWER + mock-is-Monte-Carlo-not-network-variance caveats.
- **§7** — calibration table **de-ranked to log-space μ/σ**, alphabetical, seconds-medians moved to
  repo provenance, explicit "not a ranking" caveat (F14); R11 regtest precision; **3rd disclosed
  limitation** = R10 testnet≠mainnet (F11).
- **§9** — `run_hash` → **mock-pipeline verification hash** + Variant-E clarifier (F12);
  **methodology-vs-data pre-registration decoupled** (real-rail run gets its own prior registration).

**Manifest re-frozen:** v1.1 manifest hash =
`sha256:f0b9b079e72fcfdadde976be9ee5cdcd5ac893e86e86e875b440ac13e3009d99` (methodology.md is the only
manifest file changed; all fixtures/provenance/harness/run-report bytes identical to v1.0).

**Deferred to the real-rail run / ops (recorded, not v1.1 blockers):** random seed (F15); discrete
distributions for deterministic rails (F5); σ_log bootstrap CIs; legal-posture relocation (F18). The
**watermark** (F-watermark) + **anchor-robustness** (F16/F17) items are folded into
`CEREMONY-RUNBOOK.md` (OSF abstract + arXiv title watermark; independent archival; arXiv-v1-canonical).

**Status: cross-LLM gate CLEARED; v1.1 is the frozen method of record. Ready for §9 anchoring** (still
gated only on the interactive-machine / YubiKey / tooling logistics, per the runbook).
