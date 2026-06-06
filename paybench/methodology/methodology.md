# PayBench Methodology

**v1.0 — FROZEN for pre-registration — 2026-06-05**

> **Status.** This is the **frozen methodology of record** for the settlement-finality
> pre-registration (§9). Every `TODO(calibration)` marker from the v0.2 rough draft is resolved —
> the per-rail finality definitions, the pass@k `k`-grid, and the calibration sources are now
> pinned to the first-party n=30 calibration runs (all 5 settling rails, 2026-06-04/05) and the
> content-addressed fixtures they parameterise. The method below is what the cryptographic
> anchors (OSF DOI + cosign/Rekor + OpenTimestamps + signed git tag + arXiv) commit to. No
> real-rail rankings appear here and none will until the conditions in §7 (Variant E) are met —
> the §9 anchoring covers the *method* and the *calibrated mock fixtures*, not a real-rail result.
>
> **Two disclosed limitations are pre-registered as such (no silent caps, §5.4 item 7), not
> hidden:** (1) the published-fixture spreads (`sigma_log`) for the testnet/devnet/regtest-measured
> rails — most sharply R9 and R11 — come from quiet conditions and likely understate mainnet
> congestion tails (§7); (2) R2's fixture is the *manual direct-payment* lower bound on the spec
> x402-on-Stellar path (§3, §7). Both are stated in-method so a later real-rail run is measured
> against a commitment that already names them.
>
> **Canonical home.** This document is AgentPay-canonical. It lives in `paybench/` — deliberately
> *outside* the upstream HELM `docs/` mkdocs tree — to keep the fork-first / upstream-second
> boundary clean. At Stage 2 it renames with the rest of `paybench/` to the canonical brand.

---

## 0. What this document is (and is not)

PayBench is the evaluation methodology and benchmark for **agent-to-agent payment rails**. This
document defines *how* PayBench measures, not *what the numbers are*. Under **Variant E** (§7) the
tool and its calibrated mock fixtures ship at POC Day-0 (2026-07-17); publication of real-rail
rankings is deferred.

| In scope for this doc | Out of scope for this doc |
|---|---|
| The measurement model (what a "trial" is, what we score) | Real-rail rankings (deferred — Variant E, Q3 HELD residual) |
| The statistical method (BT MLE + pass@k + Wilson LB CIs) | Worked BT-MLE math / harness code (lives in `paybench/`, separate) |
| The tiered schema (N6) | The pre-registration *artefact* itself (separate "pre-reg scaffolded" item) |
| The experimental design (rails, pairs, trials, seeding) | Calibration *values* (live in the provenance files + `calibration/`) |
| The reproducibility + pre-registration *protocol* | The IETF I-D / W3C explainer derivatives (downstream of this) |

This document *describes* the pre-registration protocol; it does not *execute* it. Executing it
(minting the OSF DOI, the cosign signature, the OpenTimestamps proof, the signed git tag, the
arXiv preprint) is the separate "pre-registration scaffolded" Friday-1 deliverable, gated on the
method below being frozen.

---

## 1. Purpose & positioning

PayBench exists to **define and publish the canonical metrics for agentic-payment rails** — the
benchmark a rail-neutral observer reaches for when asking "which rail settles fastest / most
predictably for agent commerce?". This is Founding Principle **P5 (Evaluation-as-marketing as a
pillar, not a tactic)**: methodology rigour is a product investment, not content marketing.

PayBench measures; it never touches funds. That is **P1 (non-custodial pass-through)** expressed
as a measurement posture — PayBench is an observer, not an intermediary, in every dimension it
scores.

**Prior art.** Other efforts touch adjacent ground — registries of x402 services, multi-rail
routing/analytics layers, and service-discovery surfaces. PayBench's distinct contribution is
*methodological*: a pre-registered, comparative benchmark published from a non-custodial,
rail-neutral posture. A neutral related-work treatment — naming specific efforts with sourced, dated
characterisations — belongs in the Related Work section of the eventual publication, not here.
Competitive positioning lives in the marketing collateral (`marketing/competitive-positioning.md` in
the agentpay working repo), deliberately kept out of the methodology so this document reads as the
neutral instrument it needs to be in front of standards bodies and reviewers.

The category claim is **comparative, not absolute**: PayBench ranks rails *against each other* on
each dimension. It does not assert that a rail is "good" in the abstract — it asserts that rail A
reaches settlement-finality faster than rail B, with a stated confidence interval, under a
pre-registered protocol. The comparative framing is what makes the Bradley-Terry method (§5) the
right statistical tool and what keeps the claims defensible.

---

## 2. What PayBench measures — the tiered schema (N6)

PayBench answers three different *kinds* of question, and is honest about which is which. The
schema is **hybrid tiered** — this is the N6 day-one closed decision.

### Tier 1 — Benchmarked (pre-registered, measured, ranked)

Dimensions PayBench runs trials on, pre-registers, and ranks with confidence intervals. The
public expansion roadmap is committed at POC Day-0:

| Dimension | First published | Status |
|---|---|---|
| **Settlement-finality** | Day-0 (2026-07-17) | First dimension — §3 |
| Authorization latency | Day-30 | Roadmap-committed |
| Fee predictability | Day-60 | Roadmap-committed |

### Tier 2 — Factual lookup (queryable, *not* ranked)

Live, queryable capability + reference data per rail. Stated as fact, not scored, not ranked:

- Fees (headline schedule)
- Supported assets
- Custody model
- The auth / dispute / refund / sanctions capability bundle (polymorphic — most rails return
  "not supported" on several; that itself is the datum)

### Tier 3 — Roadmap (labelled, no measurements)

Dimensions named for transparency about direction, carrying **no measurements** and clearly
labelled as such. Prevents the roadmap from being mistaken for a result.

**Why tiered.** It lets PayBench ship a genuinely useful oracle on Day-0 (Tier-2 factual lookup is
valuable immediately) without over-claiming measurement we have not yet done. The tiering is also a
deliberate honesty mechanism: it keeps measured, looked-up, and roadmapped claims visibly distinct,
so nothing reads as a result that is not one.

---

## 3. First benchmark dimension — settlement-finality

**Definition.** Settlement-finality is the wall-clock time from payment *submission* to the point
at which the value transfer is **irreversible on the rail** — the moment the payee can rely on the
funds without risk of reversal.

**Why finality first.** Under solo + pre-product + Bazaar competitive pressure, settlement-finality
is the highest-credibility-per-dimension choice (this is the "first benchmark scope" closed
decision). For an autonomous agent transacting A2A, "when can I rely on this payment?" is the
dominant rail-DX question — it gates every downstream action the agent takes.

*Honest caveat on the choice.* Settlement-finality is also the dimension most comfortably
publishable under Variant E — it is a timing measurement, not a price or routing claim, so it
carries the least cryptoasset-arranging-perimeter exposure of the candidate dimensions. Both
rationales are real and they happen to point the same way; the doc states this openly rather than
presenting a convenience-driven choice as pure principle. The principled test stands on its own
(finality genuinely is the dominant rail-DX question for any class of rail), so the dimension order
is not reverse-engineered to fit AgentPay's regulatory posture — but the alignment is acknowledged.

**Per-rail operationalisation — the reliance-level doctrine.** "Final" is rail-specific. Rails do
not share a single cryptographic finality model (deterministic BFT close, probabilistic rooting,
optimistic-rollup soft finality, and HTLC preimage release are genuinely different mechanisms), so
PayBench cannot pin one uniform threshold across all five. Instead it pins each rail to its
**ecosystem-canonical reliance level** — the point that rail's own protocol/documentation designates
as the level at which a builder may rely on the payment for an irreversible downstream action. This
is the right doctrine for an *agent-DX* benchmark: it measures the moment an autonomous agent is told
it can act, which is the §3 question ("when can I rely on this payment?").

**This doctrine is stated openly, including its one sharp edge.** Because the canonical reliance
level differs by rail, the thresholds are not equi-conservative: Base's canonical level is
*optimistic* (soft finality), whereas Solana's is *conservative* (`finalized`, not the optimistic
`confirmed`). A uniform-optimistic doctrine (Base soft **and** Solana `confirmed`) or a
uniform-irreversibility doctrine (Base hard-L1 **and** Solana `finalized`) would each be internally
symmetric but would each misrepresent at least one rail's own builder guidance. PayBench takes the
per-rail-canonical doctrine and names the asymmetry rather than hiding it. *(This is the dimension's
most exposed flank under adversarial review; the choice is deliberate and defended here, not
defaulted.)*

| Rail | Finality definition (pinned) | Empirical median | Measured on |
|---|---|---|---|
| x402-Base (R1) | **Soft finality, 1 Base block (~2s)** — optimistic-rollup sequencer inclusion + ~0 reorg; this is Base's canonical payment-reliance level. Hard L1 finality (~min–20 min) is the bridging/withdrawal threshold, not the payment one, and no agent waits it — **excluded**. | 2.05 s | Base Sepolia, n=30 |
| x402-Stellar (R2) | **Ledger close** — deterministic, single-ledger, no reorg. | 2.74 s¹ | testnet, n=30 (manual path) |
| x402-Solana (R9) | **Commitment `finalized`** (32-slot rooted) — *not* `confirmed`. Solana's own docs designate `finalized` as the irreversibility level. | 14.63 s | devnet, n=30 |
| MPP-on-Tempo (R10) | **Tempo BFT block finality** (Simplex consensus) — deterministic. Calibrated on Moderato **testnet** (chain 42431); mainnet `Presto` (chain 4217) shares the consensus. Fixture is the **pure-Tempo MPP path**; the Stripe-mediated acceptance leg is Variant-E mock (§7). | 1.75 s | Moderato testnet, n=30 |
| GCP + AP2 (R6) | **Excluded from finality** — AP2 does not settle independently; measured on Day-30 authorization latency (§8). | — | — (Resolution B) |
| MPP-on-Lightning (R11) | **Preimage release** — the payment is final when the preimage is revealed. Operationally the wall-clock is dominated by the **Spark FROST-signing + SSP preimage-swap ceremony**, *not* the (sub-second) Lightning HTLC; R11 benchmarks the Spark hosted-operator path specifically (a raw-LND L402 path would settle far faster). | 16.52 s | Spark hosted regtest, n=30 |

¹ R2's median is a **lower bound** on the spec x402-on-Stellar finality: it was measured on the
manual direct-payment path, which omits the OZ-facilitator verify+settle round-trip the spec path
adds. Pre-registered as a disclosed limitation (§7), not as the spec-path figure.

**Unit.** Seconds, wall-clock, request → HTTP 200 (submission → the agent's reliance point). This
deliberately bundles the rail's protocol/HTTP envelope (e.g. the x402 facilitator round-trip, the
MPP/L402 flow) *with* on-chain settlement, because that full round-trip is what the agent actually
experiences and waits on — consistent with the agent-DX framing above. Each trial yields one
finality time per rail in the pair.

---

## 4. Rails under test

The locked POC rail set is **six rails** (Session 9, 2026-05-20); the **settlement-finality
benchmark races the five that settle independently.** Per Resolution B (§8), AP2 is covered by
PayBench but enters on the Day-30 authorization-latency dimension, not on finality.

**Settle independently — race on finality (Day-0):**

1. **R1** x402-Base
2. **R2** x402-Stellar
3. **R9** x402-Solana
4. **R10** MPP-on-Tempo (Stripe PSP)
5. **R11** MPP-on-Lightning (Lightspark)

**Covered, but measured elsewhere:**

6. **R6** GCP + AP2 — authorization/mandate layer; debuts on Day-30 authorization latency (§8).

The "first benchmark scope" closed decision committed six rails to align benchmark coverage with the
POC rail set. Resolution B honours that coverage — all six rails are in PayBench — while keeping the
finality *dimension* to the five rails for which finality is well-defined. AP2 is deferred to its
proper dimension, not dropped.

---

## 5. Statistical method

The eval methodology is **Bradley-Terry MLE + pass@k + Wilson lower-bound confidence intervals**
(closed decision — supersedes the earlier Bayesian Beta-Binomial approach because PayBench's use
case is *comparative*, not *absolute*). The Chatbot Arena Bradley-Terry MLE leaderboard is the
proof point.

### 5.1 Bradley-Terry MLE — the comparative ranking

For each unordered rail pair we run repeated **finality races**: in a trial, both rails in the pair
execute the same payment scenario against the same fixture; the rail reaching finality first
"wins". Aggregating wins/losses across all trials and all pairs, Bradley-Terry maximum-likelihood
estimation produces a latent **strength score per rail** — a single comparative ranking that is
internally consistent across all pairwise comparisons (it reconciles, e.g., A>B and B>C into a
coherent A>B>C with strengths).

### 5.2 pass@k — the absolute-threshold complement

BT strength is purely relative. Operationally an agent also needs an *absolute* answer: "will this
rail settle within my SLA?" So we report **pass@k defined as P(finality ≤ k seconds)** — the
empirical probability a rail reaches finality within a `k`-second budget, for a small set of
pre-registered `k` values.

**Pinned `k`-grid: `{2, 3, 5, 10, 15, 20}` seconds.** The grid is chosen to discriminate across the
calibrated medians, which fall in two well-separated clusters — a *fast* cluster (R10 1.75 s, R1
2.05 s, R2 2.74 s) and a *slow* cluster (R9 14.63 s, R11 16.52 s):

- `k=2` separates *within* the fast cluster (R10 ≈ 0.77 vs R1 ≈ 0.37 vs R2 ≈ 0.00).
- `k=3` and `k=5` clear the fast cluster (R2 resolves at `k=3`; all three reach ≈ 1.0 by `k=5`).
- `k=10` is the clean cluster separator — ≈ 1.0 for every fast rail, ≈ 0 for every slow rail —
  carrying no within-cluster discrimination by design (it sits in the empirical gap, R2 p99 ≈ 3.5 s
  to R11 min ≈ 8.5 s).
- `k=15` separates *within* the slow cluster (R9 ≈ 0.66 vs R11 ≈ 0.26).
- `k=20` clears the slow cluster (R9 ≈ 1.0; R11 ≈ 0.89, its tail still resolving).

The grid is frozen with the rest of the design (§9); it is not re-fit per run.

### 5.3 Wilson lower-bound confidence intervals

All proportions — pairwise win rates and pass@k probabilities — are reported with **Wilson score
intervals**, and we lead with the **lower bound** as the conservative published figure. The Wilson
interval is well-behaved at the extremes (near 0 and 1) and for the per-pair sample sizes here,
where the normal approximation would mislead.

### 5.4 Post-"Leaderboard Illusion" fix-list

The Chatbot Arena lineage carries known failure modes (the "Leaderboard Illusion" critique).
PayBench pre-commits to the fix-list:

1. **Pre-register** the rail set, trial counts, metrics, seed, and fixture hashes *before* running (§9).
2. **No private or selective trials** — every trial run is published, not just favourable ones.
3. **Symmetric sampling** — equal trial counts across every pair (no pair over- or under-sampled).
4. **Frozen methodology version** per benchmark run — the run is tagged to a methodology version.
5. **Disclosed roster changes** — any rail added or removed between runs is disclosed, not silently absorbed.
6. **Content-addressed fixtures + seeded RNG** (§6) so any result is bit-for-bit reproducible.
7. **No silent caps** — if coverage is bounded, it is logged, not presented as completeness.

---

## 6. Experimental design

This instantiates the **N16 MockBench architecture** closed decision.

- **Pairs.** The settlement-finality benchmark races the 5 settling rails (§4; §8 Resolution B) →
  C(5,2) = **10 unordered pairs**. *(The 6-rail / C(6,2)=15-pair figure from the N16 MockBench closed
  decision applies only to a future dimension in which all six rails compete; for finality, AP2 is
  measured on the Day-30 dimension instead — see §8.)*
- **Trials.** **500 trials per pair × 10 pairs = 5,000 total trials** for the settlement-finality
  benchmark. Symmetric across pairs (fix-list item 3).
- **Seeded RNG.** A single published seed drives all stochastic fixture selection and ordering, so
  the entire run is reproducible.
- **Content-addressed fixtures.** Every fixture is hash-addressed; a trial records the fixture hash
  it consumed, making inputs immutable and verifiable.
- **Pre-signed credentials as static artefacts.** Credentials are pre-signed at issuance and served
  as static artefacts (R2 object storage / GitHub Pages) — **no runtime signing exposure**. This is
  both a security posture (no online signing key on a request path) and a non-custodial posture
  (PayBench never holds or moves value at runtime). Signing-key custody follows a standing split:
  **production** credentials are signed only by offline hardware keys (YubiKey 5 ×2, PIV ECDSA
  P-256; primary online for the issuance ceremony, backup in cold storage); **dev/test** fixtures
  are signed with exportable software ECDSA P-256 keys (frequent re-signing + CI automation make
  hardware impractical there, and the split keeps production key material off dev paths). Hardware
  keys are now in hand (2026-06), which fires the production issuance-ceremony cutover; dev/test
  stays on software keys regardless.
- **Harness.** A unified Python harness inside `agentic-paybench/payhelm` (this fork). The HELM
  scaffolding gives us run-spec / scenario / metric structure; PayBench adds the rail adapters,
  fixtures, and the BT/pass@k/Wilson metric layer.

---

## 7. Mock-fixture & calibration posture (Variant E + Path C-tight)

**Variant E (closed decision).** PayBench ships as an open / source-available **tool** with
**calibrated mock-data fixtures** bundled as the test harness. Running PayBench against actual
production rails and publishing rail-by-rail scoring is **deferred** — it is the Q3 HELD residual,
held pending either FCA authorisation for the relevant activity or FCA guidance narrowing the
cryptoasset arranging perimeter. Variant E sidesteps that perimeter on PayBench's *publication*
while preserving the full methodology + tooling story.

**Calibration — what "calibrated mock fixtures" means.** The fixtures are *not* arbitrary synthetic
numbers. Each fixture is a seeded **log-normal** population (finality times are positive and
right-skewed; log-normal is the parameter-light default — calibration-plan §"Distribution approach")
whose `{median_s, sigma_log}` is parameterised from real reference data. As of the freeze, **all five
settling rails carry first-party n=30 calibration runs** (0 failures each), so the medians are
measured, not doc-derived:

| Rail | `median_s` | `sigma_log` | Approach | First-party source (n=30) | Doc cross-check |
|---|---|---|---|---|---|
| R1 x402-Base | 2.05 | 0.082 | first-party-empirical | Base Sepolia (`poc/rail-x402-base`) | Base docs: 2 s block, ~0 reorg, soft ≈ 2 s |
| R2 x402-Stellar | 2.74 | 0.116 | first-party-empirical¹ | testnet manual path (`poc/rail-stellar-x402`) | Stellar ledger close (deterministic) |
| R9 x402-Solana | 14.63 | 0.057 | hybrid (first-party central + doc tail) | devnet (`poc/rail-solana-x402`) | Helius/Anza: `finalized` = 32 slots ≈ 13 s |
| R10 MPP-on-Tempo | 1.75 | 0.177 | first-party-empirical (real-rail) | Moderato testnet (`poc/rail-tempo-mpp`) | Tempo ≈ 500 ms block finality target |
| R11 MPP-on-Lightning | 16.52 | 0.156 | first-party-empirical (real-rail) | Spark hosted regtest (`poc/rail-lightning-mpp`) | Spark FROST+SSP ceremony (HTLC sub-second) |

The mock harness is therefore *meaningful* — it exercises the full measurement + statistics pipeline
against realistic, first-party-anchored distributions — without publishing a real-rail ranking. Full
per-source detail (refs, dates, sample sizes, parameterisation rationale) lives in
`calibration/provenance/<rail>-finality.provenance.yaml`; the sourcing method is in
`calibration/calibration-plan.md` (Hybrid (C), decided 2026-06-04).

**Per-fixture provenance.** Every fixture ships with a provenance file recording its calibration
source(s), the date sourced, and the parameterisation. Provenance is a Day-0 artefact.

**Path C-tight posture (closed decision).** Calibrated fixtures + provenance live Day-0;
right-of-reply infrastructure (§10) live Day-0; rankings *derived from* calibrated mock fixtures are
**not published** at POC (they stay in the Q3 HELD residual). The triage/evidence/response agent
ladder (L1 triage within 30 days; L2 human-in-loop Day-30+; L3 draft-only response MVP-era; L4 auto
NOT shipped) governs the right-of-reply operations.

**Pre-registered disclosed limitations (no silent caps, §5.4 item 7).** Two calibration facts are
committed *into* the frozen method so a later real-rail run is measured against a prior that already
names them — not surfaced after the fact:

1. **Quiet-condition spreads understate mainnet tails.** The `sigma_log` values are measured under
   quiet testnet/devnet/regtest load. Most sharply for **R9** (`sigma_log` 0.057 from quiet devnet;
   docs + a single devnet excursion to 19.46 s indicate the real tail is heavier — widen toward
   ~0.15–0.25 on a mainnet/congested run) and **R11** (`sigma_log` 0.156 from quiet Spark regtest,
   likely understating mainnet operator-latency variance). The *central tendencies* are
   high-confidence empirical; the *tails* are the disclosed soft spot. The fixtures are frozen at the
   measured spreads (they are mock fixtures under Variant E, not a real-rail ranking); the limitation
   is registered rather than silently corrected.
2. **R2 is a lower bound.** R2's fixture is the manual direct-payment path, which omits the
   OZ-facilitator round-trip the spec x402-on-Stellar path adds — so R2's finality is registered as a
   *lower bound*, expected to rise on a spec-path re-measure (the spec path is wired and validated
   end-to-end; the n=30 spec re-measure is deferred).

These are the only two non-empirical-tightness caveats in the calibration set, and both are visible
in the per-rail provenance `confidence`/`notes` fields. Real-rail publication (the Q3 HELD residual)
re-runs the *same frozen method* against production-rail fixtures.

---

## 8. AP2 as a "rail" — RESOLVED (Resolution B, adopted 2026-06-04)

**The problem.** AP2 (R6, GCP + AP2) **does not settle independently**. AP2 is an authorization /
mandate layer; its settlement-finality *reduces to the underlying settlement rail* it routes to. A
finality "race" (§5.1) between AP2 and, say, x402-Base is therefore ill-defined — "AP2 finality" is
just some underlying rail's finality wearing an AP2 label. Worse, AP2 adds its own mandate-verify +
orchestration overhead on top of the underlying rail — a real cost, but an *authorization*-layer
cost, not a finality one — so a finality number for AP2 would conflate two different things.

**Decision: Resolution B.** AP2 is pulled out of the Tier-1 settlement-finality benchmark and
measured on the **Day-30 authorization-latency** dimension instead, where its mandate / orchestration
behaviour is well-defined and apples-to-apples. Settlement-finality ranks only the five rails that
settle independently.

**Why B (over keeping AP2 in finality):**

- **Statistical validity.** BT MLE (§5.1) assumes independent competitors. Racing AP2 against its own
  underlying rail violates independence and double-counts that rail.
- **No confounding.** AP2's distinctive cost is mandate-verify + orchestration overhead — an
  authorization-layer phenomenon. On authorization latency it is captured cleanly; on finality it is
  mislabelled and unfair to AP2.
- **Definability.** You cannot pre-register (§9) a metric you cannot define per rail; "AP2 finality"
  has no clean definition (it was the open cell in §3).
- **Reviewer-proofing.** Keeping AP2 in finality is the methodology's most exposed flank — a CRFM
  maintainer, a statistician, or a hostile competitor would flag the non-independence / confounding /
  undefinability at once, and it would contradict our own Leaderboard-Illusion fix-list (§5.4).

**Coverage is preserved.** Resolution B does **not** drop AP2 from PayBench or from the six-rail POC
set. All six rails are covered; only five settle, so only five race on finality; AP2 (the sixth)
debuts on its proper dimension at Day-30. This reconciles the "six rails" benchmark-scope commitment
with the AP2 wrinkle — both decided in Session 9 — rather than trading one off against the other.

**Consequence for the design.** The settlement-finality benchmark is **5 rails → 10 pairs → 5,000
trials** (§6), not 6 / 15 / 7,500. The N16 MockBench 15-pair / 7,500-trial figure now applies only to
a hypothetical future dimension racing all six rails. With AP2 resolved, pre-registration (§9) can
freeze the finality design.

---

## 9. Reproducibility & pre-registration protocol

Pre-registration is the **load-bearing canonical artefact** — it is what defends PayBench against
Leaderboard-Illusion-style critique and establishes AgentPay as an early-mover on benchmark
pre-registration. Protocol (closed decision):

**Pre-register, before any scored run:** the rail set, per-rail finality definitions, trial counts,
metric definitions (BT MLE + pass@k `k`-grid + Wilson), the RNG seed, the fixture hashes, and the
analysis plan.

**Frozen manifest (this pre-registration — methodology v1.0, 2026-06-05).** The concrete values the
anchors below commit to:

| Item | Frozen value |
|---|---|
| Settling rail set (race on finality) | R1, R2, R9, R10, R11 (AP2/R6 on Day-30 latency, §8) |
| Pairs × trials | C(5,2) = 10 pairs × 500 = **5,000 trials** |
| Master seed | `20260717` |
| Metrics | BT MLE (symmetric smoothing prior 1.0) + pass@k `P(finality ≤ k)`, `k ∈ {2,3,5,10,15,20}` s + Wilson 95% LB |
| Fixture hashes (sha256) | R1 `05099bcb…46af` · R2 `b002e832…b38c` · R9 `b0765414…348f` · R10 `2d77a6cb…785f4` · R11 `b31f7945…8910` |
| Run hash (the scored mock run) | `895f99ed52567421a1d7e9068ab9a0d7147d6381ec137e1b130b805e63b14ee0` |

The full-length fixture hashes are authoritative in each fixture file's `content_hash` and the rail's
provenance `fixture_content_hash`; the harness re-verifies them on every load (§6). The run hash is
deterministic over the report with no wall-clock written into it (§5.4 item 6) — re-running the
harness on the frozen fixtures reproduces it byte-for-byte.

**Cryptographic grounding (defence-in-depth):**

- **OSF pre-registration** → DOI (the human-readable trust anchor)
- **cosign** signature over the pre-registration bundle → Rekor transparency-log entry
- **OpenTimestamps** → Bitcoin block anchor (independent time proof)
- **Signed git tag** on the methodology + harness commit
- **arXiv preprint** of the methodology

**Trust-anchor triad:** OSF DOI + Bitcoin block + Rekor entry — three independent anchors, no single
point of trust.

**Bulk telemetry signing.** Trial telemetry / datasets are signed with a **Merkle root + cosign** —
**not** VCDM 2.0 / SD-JWT. VCDM 2.0 + SD-JWT are for *credentials* (per the schema closed decision:
JSON-LD core + VCDM 2.0 signing for the capability schema); they are explicitly *not* the mechanism
for bulk dataset signing.

**Versioning.** The methodology version is frozen per benchmark run and recorded in the run's tag.

---

## 10. Right-of-reply & corrections (publisher posture)

AgentPay publishes as a **publisher, not a platform** (DSA framing closed decision; Recital 13
"minor and ancillary feature" exclusion; UK Defamation Act 2013 governs, primary shield is s.4
public-interest). PayBench voluntarily mirrors DSA Articles 16/17/20 *inside the right-of-reply
channel only*.

The corrections mechanism is the **8-axis right-of-reply (A1–A8)** + form template + 10-point
response policy (trigger / evidence / remedy / target-response per axis). **Pre-publication notice
and right-of-reply are part of the defamation defence**, not an add-on. Right-of-reply
infrastructure is live Day-0 (Path C-tight, §7).

This document only *points* at the taxonomy; the full A1–A8 specification is canonical in Notion.

---

## 11. Roadmap (tiered dimension expansion)

| When | Dimension | Tier |
|---|---|---|
| Day-0 (2026-07-17) | Settlement-finality | Tier-1 (pre-registered) |
| Day-30 | Authorization latency *(AP2 debuts here — §8 Resolution B)* | Tier-1 |
| Day-60 | Fee predictability | Tier-1 |
| Day-0 onward | Fees / assets / custody / capability bundle | Tier-2 (factual lookup) |
| Future | (labelled, unmeasured) | Tier-3 |

> **The dates are scheduled targets, not methodological constants.** Day-0 / Day-30 / Day-60 come
> from the POC-duration closed decision, not from the method. The methodology fixes only the
> *sequence* (pre-register → run → publish) and the *gates* (§9): the schedule can compress without
> changing the methodology, provided it does not compress past the pre-registration dependency chain
> (AP2 resolved — done, §8; calibration in; method frozen v1.0; cryptographic anchors to land) or
> skip the pre-publication adversarial review.

---

## 12. Glossary (brief — canonical glossary in Notion)

- **Rail** — an agentic-payment settlement or authorization network under test.
- **Settlement-finality** — wall-clock time from submission to irreversibility (§3).
- **Authorization latency** — time to authorize a payment intent (Day-30 dimension).
- **Fee predictability** — variance/spread of effective fees (Day-60 dimension).
- **pass@k** — P(finality ≤ k seconds) (§5.2).
- **Bradley-Terry MLE** — latent-strength comparative ranking from pairwise outcomes (§5.1).
- **Wilson lower-bound CI** — conservative interval on a proportion (§5.3).
- **Fixture** — a content-addressed, calibrated input to a trial (§6, §7).
- **Provenance** — per-fixture record of calibration source (§7).
- **Pre-registration** — cryptographically anchored prior commitment to the design (§9).

---

## Appendix — closed decisions this document instantiates

- Eval methodology = Bradley-Terry MLE + pass@k + Wilson lower-bound CIs (supersedes Bayesian Beta-Binomial)
- N6 day-one schema = hybrid tiered (Tier-1 benchmarked / Tier-2 factual lookup / Tier-3 roadmap)
- First benchmark scope = 6 rails covered; settlement-finality benchmark races the 5 settling rails (AP2 on Day-30 per §8 Resolution B)
- N16 MockBench architecture (Python harness, calibrated fixtures, content-addressed, seeded; finality run = 10 pairs / 5,000 trials)
- AP2-as-rail wrinkle resolved 2026-06-04 (Resolution B): AP2 measured on authorization latency, not settlement-finality (§8)
- Pre-registration protocol = OSF + cosign + OpenTimestamps + signed git tag + arXiv
- Variant E for PayHELM publication scope (tool + mock fixtures ship; real-rail rankings deferred)
- Path C-tight mock-fixture posture (calibrated fixtures + provenance + right-of-reply Day-0)
- Schema pattern = JSON-LD core + VCDM 2.0 signing (credentials only; bulk telemetry uses Merkle + cosign)
- Dispute taxonomy = 8-axis right-of-reply (A1–A8); DSA framing = publisher not platform; UK Defamation Act 2013 s.4
- N8 Split A — filings front-loaded into the POC window (this doc anchors the bundle)

## Appendix — pointers

- Project context + full closed-decisions table: `CLAUDE.md` (repo root of the agentpay working repo)
- Canonical decisions, glossary, dispute taxonomy: Notion (AgentPay parent)
- Sibling Friday-1 deliverable (reference task shape): the x402_base adapter at `poc/rail-x402-base/`
