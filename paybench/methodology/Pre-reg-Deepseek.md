# PayBench v1.0 — DeepSeek Adversarial Pre-Registration Review

**Model:** DeepSeek (independent review, 2026-06-06)  
**Role:** Hostile reviewer — CRFM maintainer / statistician / competitor  
**Inputs:** `methodology.md` v1.0 (frozen 2026-06-05) + `adversarial-review.md` (7-finding self-review)  
**Output:** Findings for recording back into `adversarial-review.md` before §9 anchoring executes.

---

## Executive summary

The methodology is well-constructed and the self-review's willingness to surface its own flanks is genuinely credit-earning. However, this review identifies **four findings the self-review and any prior cross-LLM pass did not surface**, of which **two are HIGH severity** and represent the most damaging lines of attack available to a hostile reviewer. The single most dangerous finding (F13) is that the calibration data was collected *before* the methodology freeze, meaning the k-grid, the statistical framework, and the "two well-separated clusters" narrative were all shaped with knowledge of the outcomes — undermining the pre-registration's core claim to have prevented HARKing. The second (F14) is that the calibration table itself constitutes a published ranking derived from real infrastructure, punching a hole through the Variant-E firewall.

---

## 1. F1 — The per-rail-canonical doctrine (HIGH)

### 1.1 The attack, from a different angle than previously surfaced

The self-review frames F1 as an inconsistency problem. The prior cross-LLM review frames it as a sensitivity-analysis problem. I want to frame it as a **documentation-arbitrage problem**:

> The methodology outsources a measurement decision — the finality threshold — to each rail's documentation team. Documentation teams are not neutral parties. They are employed by organisations with commercial interest in their rail appearing fast, reliable, or both. A rail that wants to win a settlement-finality benchmark can simply update its documentation to designate a more optimistic reliance level. The methodology has no defence against this — it would be *obligated* to adopt the new threshold, because the doctrine defers to ecosystem-canonical guidance. The benchmark doesn't measure rails; it measures documentation-team aggressiveness.

This is sharper than the "inconsistent thresholds" framing because it attacks the doctrine's *sustainability*, not just its current application. Even if the current per-rail thresholds are defensibly sourced, the doctrine creates a race-to-the-bottom incentive: rails that publish more aggressive builder guidance get better benchmark numbers. A CRFM maintainer would ask: *"What happens when Base updates its docs to say 'soft finality is sufficient for all payment amounts under $X' — does your benchmark automatically adopt that? What if Solana publishes guidance saying `confirmed` is safe for payments under 10 SOL? Your methodology delegates measurement to marketing."*

### 1.2 The doctrine's hidden dependency on English-language, web-accessible documentation

The methodology assumes every rail has a single, unambiguous, English-language, web-accessible "canonical" documentation source that states a reliance level. This is not true for many global payment systems. If PayBench ever expands beyond the initial five rails, it will encounter rails where:

- The "canonical" guidance exists only in a forum post by a pseudonymous core developer
- The guidance exists in multiple languages with inconsistent translations
- The guidance is versioned and the "current" version differs from the "stable" version
- There is active community debate about what the safe reliance level is

The per-rail-canonical doctrine doesn't scale. It works for five well-documented Western rails in 2026; it fails as a general measurement doctrine.

### 1.3 The Solana `confirmed` number is captured but suppressed

The self-review reveals that Solana `confirmed` = 2.27s median (σ_log 0.267) was measured and is available. The methodology publishes only `finalized` = 14.63s. This is the single most damning fact a reviewer can cite: **the methodology possesses the data that would make Solana competitive with the fast cluster but chooses not to publish it.**

The defence — "Solana's docs say `finalized` is the safe level" — doesn't withstand scrutiny when Base's "safe level" is soft finality with non-zero reorg risk. If the standard is "what the docs say is safe," the methodology is inconsistent about whose docs it trusts and how it interprets them. If the standard is "irreversibility," Base fails. If the standard is "when the agent can act," Solana's `confirmed` is the right number. The methodology picks the standard that produces the most dramatic cluster separation, then constructs a doctrine to justify it.

**This is not a methodological choice — it's a narrative choice dressed as methodology.** The fast-vs-slow cluster structure that makes the benchmark "interesting" and "discriminating" is an artefact of choosing `finalized` over `confirmed` for Solana. If both numbers are published, the cluster structure partially collapses (Solana joins the fast cluster at `confirmed`), and the benchmark's headline finding becomes "all rails settle within ~3 seconds except Lightning-via-Spark" — a much less dramatic story.

### 1.4 Verdict on F1

The per-rail-canonical doctrine is the methodology's most exposed flank, and it is *more* exposed than the self-review or the prior cross-LLM review acknowledged. The doctrine is vulnerable on three independent grounds:

1. **Incentive incompatibility** — it rewards documentation-team aggressiveness
2. **Scalability failure** — it depends on a documentation model that doesn't generalise
3. **Selective suppression** — it withholds data (Solana `confirmed`) that would weaken the benchmark's narrative structure

**Minimum viable defence:** Publish both `confirmed` and `finalized` for Solana, both soft and hard finality for Base, and let the reader apply their own threshold doctrine. Rank on the per-rail-canonical level but show the sensitivity. Anything less is threshold-shopping.

---

## 2. PRE-REGISTRATION MECHANICS — Two HIGH findings the prior review missed

### 2.1 F13 (NEW, HIGH): The pre-registration was performed AFTER calibration data was collected

This is the most damaging finding in this review, and neither the self-review nor the prior cross-LLM pass identified it.

**Timeline (from the methodology):**

| Date | Event |
|---|---|
| 2026-06-04 | Calibration plan decided (Hybrid C) |
| 2026-06-04/05 | n=30 calibration runs executed on all 5 settling rails |
| 2026-06-05 | Methodology v1.0 frozen for pre-registration |
| 2026-06-05 | k-grid pinned, BT framework confirmed, fixture hashes computed |

**The problem.** The calibration data was collected *before* the methodology freeze. The designers knew the cluster structure — R10 1.75s, R1 2.05s, R2 2.74s (fast) vs. R9 14.63s, R11 16.52s (slow) — *before* finalising the k-grid, the statistical framework, and the narrative framing. The k-grid {2, 3, 5, 10, 15, 20} is suspiciously well-tailored to the known cluster structure:

- `k=2` discriminates within the fast cluster (R10 ≈ 0.77 vs R1 ≈ 0.37 vs R2 ≈ 0.00) — chosen because the designers *knew* the medians were at 1.75, 2.05, and 2.74
- `k=10` sits perfectly in the 3.5s–8.5s gap between clusters — chosen because the designers *knew* the gap existed
- `k=15` discriminates within the slow cluster (R9 ≈ 0.66 vs R11 ≈ 0.26) — chosen because the designers *knew* the medians were at 14.63 and 16.52

**The attack.** A hostile reviewer will say:

> "This is not pre-registration. This is post-hoc optimisation with a pre-registration wrapper. The authors collected calibration data, observed that the rails fall into two clean clusters with a wide gap, designed a k-grid that makes those clusters look maximally interpretable, wrote a narrative about 'fast cluster' and 'slow cluster' that the data already revealed, and then cryptographically anchored the whole thing as if the design preceded the data. The pre-registration prevents p-hacking on the *mock run*, but the mock run is a deterministic transformation of distributions the authors already fully characterised. The real design choices — which dimensions to measure, which thresholds to use, which k values to report — were all made with full knowledge of the calibration outcomes."

**Why this matters.** Pre-registration's core purpose is to prevent Hypothesising After Results are Known (HARKing). The methodology's pre-registration doesn't prevent HARKing on the calibration data, which is the only real data in the system. The mock run adds no new information — it's a seeded Monte Carlo draw from distributions fully characterised by the calibration. Freezing the mock-run design after calibration is like running an experiment, seeing the results, and then pre-registering the analysis plan for a bootstrap resampling of the same data.

**The calibration table IS a result.** The methodology says "no real-rail rankings appear here." But the calibration table (§7) is a ranking: R10 1.75s, R1 2.05s, R2 2.74s, R9 14.63s, R11 16.52s. Those are real measurements from real testnet/devnet/regtest infrastructure. They are presented in rank order. A reader sees: Tempo is fastest, Lightning (via Spark) is slowest. The Variant-E firewall doesn't prevent publication of this ranking — it only prevents publication of the *mock-run* ranking, which is a noisier version of the same thing.

### 2.2 F14 (NEW, HIGH): The calibration table punches through the Variant-E firewall

**The attack, sharpened:**

> "You claim Variant-E prevents publication of real-rail rankings. But §7 publishes a table with five rails, their real measured medians (from real testnet/devnet/regtest infrastructure), in rank order, with n=30 first-party calibration runs. That IS a real-rail ranking — it's just a low-n, testnet-caveated one. The FCA doesn't distinguish between 'ranking with n=30 on testnet' and 'ranking with n=500 on mainnet' when assessing whether an activity falls within the arranging perimeter. If publishing comparative rail performance data is arranging, you're already doing it in §7. The Variant-E firewall has a calibration-table-sized hole in it."

The methodology's defence would be: "These are calibration parameters, not a ranking; they're published to document the mock-fixture provenance, not to compare rails." But a regulator or a hostile reviewer doesn't have to accept that framing. The table is headlined "median_s", ordered from fastest to slowest, and the numbers are real measurements. The distinction between "calibration parameter" and "ranking" is a distinction without a difference when the parameter IS the quantity being ranked.

**The regulatory risk is real.** If the FCA views this table as a published ranking, the Variant-E posture collapses, and the methodology's publication may itself require authorisation. The self-review's confidence that Variant-E "sidesteps the perimeter" is an untested legal theory.

**Mitigation:** Either (a) randomise the row order of the calibration table and remove the `median_s` column (reporting only the log-normal parameters μ and σ, which are not directly interpretable as ranking numbers), or (b) obtain external legal review confirming that the calibration table as currently structured does not constitute a ranking for perimeter purposes. Without one of these, the Variant-E firewall is reputational theatre backed by an untested legal theory.

---

## 3. Statistical method — independent review

### 3.1 The log-normal assumption is a poor fit for deterministic-finality rails (sharpening F5)

F5 (LOW) acknowledges the log-normal assumption is "acceptable for mock fixtures." But the assumption is not just a convenience — it *creates* variance that doesn't exist in reality, and this variance propagates into the mock ranking in ways that could mislead even as pipeline validation.

**Stellar (R2).** Stellar's ledger close is deterministic at ~5 seconds per ledger (the methodology measured 2.74s on testnet, but the principle holds: ledger close is fixed-interval). The true distribution is "constant ledger interval + small network-jitter." The methodology's log-normal with σ_log=0.116 artificially creates a right tail. In 500 mock trials, the log-normal will occasionally produce finality times of 4s, 5s, or 6s for Stellar — times that would never occur in reality (they'd fall into the next ledger, which is a discrete, not continuous, phenomenon). The mock ranking is therefore *misleading even as pipeline validation* for the Stellar rail specifically.

**Tempo (R10).** Similar issue. BFT block finality is a discrete event occurring at block-interval boundaries. A log-normal with σ_log=0.177 produces continuous variation that doesn't reflect the underlying mechanism.

**The consequence.** When the mock run compares Stellar (continuous log-normal with artificial tail) against Base (continuous log-normal, which is a reasonable approximation of its actual behaviour), the comparison is between a model that *exaggerates* Stellar's variance and a model that *reasonably approximates* Base's variance. This biases against Stellar in any metric sensitive to the right tail (pass@k at higher k, BT upset frequency).

**Recommendation.** For deterministic-finality rails, use a discrete distribution: "constant + jitter" for Stellar (ledger-close-aligned), "constant + small gamma" for Tempo (BFT-block-aligned). This doesn't require more parameters — a two-parameter discrete model is no more complex than a two-parameter log-normal. For mock-fixture purposes, the log-normal is acceptable *if* the methodology explicitly acknowledges that it disadvantages deterministic-finality rails in tail-sensitive metrics. Currently it doesn't.

### 3.2 n=30 is thin for estimating σ_log (the tail parameter)

The methodology's calibration uses n=30 per rail. For estimating a log-normal median, n=30 gives reasonable precision. For estimating σ_log, n=30 is quite thin.

**Standard error of the MLE for σ in a log-normal:** approximately σ/√(2n).

| Rail | σ_log | SE(σ_log) | Approx 95% CI for σ_log |
|---|---|---|---|
| R1 (Base) | 0.082 | 0.011 | [0.061, 0.103] |
| R2 (Stellar) | 0.116 | 0.015 | [0.087, 0.145] |
| R9 (Solana) | 0.057 | 0.007 | [0.043, 0.071] |
| R10 (Tempo) | 0.177 | 0.023 | [0.132, 0.222] |
| R11 (Lightning) | 0.156 | 0.020 | [0.117, 0.195] |

The CI for R10's σ_log spans 0.132–0.222. At σ=0.132, pass@2 for R10 (from its log-normal with median 1.75) is approximately Φ(ln(2/1.75)/0.132) ≈ Φ(1.01) ≈ 0.844. At σ=0.222, pass@2 is Φ(ln(2/1.75)/0.222) ≈ Φ(0.60) ≈ 0.726. A 12-percentage-point swing in pass@2 from parameter uncertainty alone. The Wilson CIs reported on the mock run won't reflect this — they'll reflect only the finite-sample variation from 500 draws from the point-estimate distribution.

**This is disclosed in spirit (§7 says tails are the "soft spot") but not quantified.** The methodology should bootstrap the n=30 calibration data to produce parameter CIs and propagate them. For the mock run this is a disclosure item; for the real-rail run it's essential.

### 3.3 The k-grid circularity

As noted in F13, the k-grid was chosen with knowledge of the calibration data. The methodology's own description of the k-grid (§5.2) admits this: "The grid is chosen to discriminate across the calibrated medians, which fall in two well-separated clusters." But it's presented as a frozen design choice, not as a post-calibration optimisation.

A pre-registered analysis plan should specify the k-grid *before* seeing data. If the grid was data-informed, the methodology should say so explicitly: "The k-grid was selected after calibration to provide within-cluster and between-cluster discrimination. This means pass@k results from the mock run are not independent of the calibration data — they are circular for pipeline-validation purposes. The real-rail run will use the same pre-registered grid, so the circularity affects only the mock validation, not the eventual published results."

### 3.4 BT MLE with 5 nodes — the "strength" illusion (sharpening F6)

F6 correctly notes BT strengths become near-degenerate under cluster separation. But there's a deeper issue: **with only 5 nodes, the BT model has very little structure to fit.** C(5,2) = 10 pairwise win probabilities, and the model estimates 4 free strength parameters (one rail fixed at 0). With 10 data points and 4 parameters, the model is overdetermined — it has 6 degrees of freedom to detect transitivity violations, which sounds adequate. But in practice, with two well-separated clusters, the 10 pairwise win probabilities are essentially:

- Fast vs Fast: ~0.5 (within-cluster noise)
- Slow vs Slow: ~0.5 (within-cluster noise)
- Fast vs Slow: ~1.0 (cluster dominance)

The model fits "fast cluster gets high strength, slow cluster gets low strength, within-cluster differences are noise." The BT strengths will report fine-grained numbers (e.g., R10: 2.34, R1: 2.28, R2: 2.15) but these differences are driven by a handful of upsets in 500 trials — they are not stable under seed variation. **Reporting BT strengths to multiple decimal places, as is conventional for Chatbot Arena, is misleading here.** The methodology should report BT strengths with confidence intervals derived from seed sensitivity, or should report only the cluster-level finding ("fast cluster dominates slow cluster; within-cluster ordering is not statistically distinguishable at n=500").

### 3.5 Statistical verdict

The BT + pass@k + Wilson framework is fundamentally appropriate. The issues are in:

1. **Distributional assumptions** — log-normal is a poor fit for deterministic-finality rails, and this biases mock-run comparisons
2. **Parameter uncertainty** — n=30 is thin for σ_log, and this uncertainty isn't propagated
3. **k-grid circularity** — the grid was chosen post-calibration, and this isn't disclosed
4. **BT precision illusion** — fine-grained BT strengths are unstable under seed variation and shouldn't be reported as precise

None of these are fatal for a mock-fixture pipeline validation. Several would become material for a real-rail publication.

---

## 4. Additional findings missed by both prior reviews

### 4.1 F15 (NEW, MED): The master seed `20260717` is a human-chosen memorable date, not a random seed

**The attack.** "Your master seed is the POC launch date. This is a cute easter egg, but it's not a randomly generated seed. A properly randomised seed provides assurance that the trial ordering isn't structured to favour any rail. A human-chosen date seed doesn't provide that assurance — it signals that the seed was chosen for narrative purposes, not statistical ones."

This is a minor point in isolation, but it compounds with F13 (post-calibration design) to suggest a pattern: the designers made choices that are narratively satisfying (a k-grid that produces clean clusters, a seed that's the launch date, a doctrine that produces a dramatic fast-vs-slow story) rather than statistically conservative. A hostile reviewer will connect these dots.

**Recommendation.** Generate the seed from a random source (e.g., `/dev/urandom` 32 bytes, or a Bitcoin block hash from a future block that couldn't have been known at design time) and document the generation method. This is a one-line change that closes a flank.

### 4.2 F16 (NEW, MED): The anchor chain has a URL-based single point of failure

The methodology's cryptographic anchoring uses five mechanisms: OSF DOI, cosign/Rekor, OpenTimestamps, signed git tag, arXiv preprint. The trust-anchor triad (OSF DOI + Bitcoin block + Rekor entry) is genuinely defence-in-depth. However:

**The OSF DOI resolves to a URL.** If OSF's infrastructure changes, the DOI becomes a dead link. The other anchors (Rekor, OpenTimestamps, git tag) are cryptographic but they anchor *to the OSF registration* — the methodology says "OSF pre-registration → DOI (the human-readable trust anchor)." If the OSF registration is withdrawn, modified, or becomes inaccessible, the anchor chain's human-readable root breaks. The cryptographic proofs remain valid but become unverifiable without the original OSF artefact.

**This isn't theoretical.** OSF has had outages. Pre-registrations can be withdrawn (though OSF preserves a withdrawal record). The methodology should specify: (a) which anchor is authoritative in case of discrepancy, (b) that all artefacts are independently archived (Internet Archive, IPFS) beyond OSF, and (c) that the Rekor entry and OpenTimestamps proof are independently sufficient to establish the methodology's freeze date even if OSF is unavailable.

### 4.3 F17 (NEW, LOW-MED): The arXiv preprint can be updated post-freeze

The methodology lists "arXiv preprint" as a cryptographic anchor. But arXiv allows updates. A preprint submitted on 2026-06-05 can be revised on 2026-07-01 with changes to the methodology, while retaining the same arXiv ID. A reader seeing the arXiv version on 2026-08-01 has no way to know whether it matches the frozen v1.0.

**Mitigation.** The arXiv submission should be a single-version PDF with the content hashes embedded in the document. Alternatively, the methodology should specify that only v1 of the arXiv submission is the canonical frozen version, and subsequent revisions are labelled as post-freeze errata.

### 4.4 F18 (NEW, LOW): The right-of-reply legal posture undermines the "neutral instrument" claim

The methodology invokes UK Defamation Act 2013 s.4, DSA Articles 16/17/20, and describes pre-publication right-of-reply as "part of the defamation defence." This is unusually aggressive legal framing for a document that claims to be "the neutral instrument it needs to be in front of standards bodies and reviewers" (§1).

**The attack.** "You're pre-emptively lawyering up against defamation claims from rails you haven't even ranked yet. This signals that you expect to publish findings that rails will consider defamatory — i.e., findings that make some rails look bad. A genuinely neutral benchmark doesn't need a defamation defence strategy in its methodology document."

This is a tonal issue, not a methodological one, but it matters for how the document is received. The legal posture belongs in a separate operational document, not in the methodology that goes to standards bodies and reviewers.

---

## 5. Summary of all findings

### Previously identified (confirmed or upgraded)

| # | Finding | Original severity | DeepSeek assessment |
|---|---|---|---|
| F1 | Per-rail finality threshold doctrine | HIGH | **Confirmed and upgraded.** Three independent vulnerabilities: incentive incompatibility, scalability failure, selective suppression of Solana `confirmed`. Most exposed flank. |
| F2 | Quiet-condition σ_log | MED | Confirmed. Adequately disclosed. D2-freeze is correct. |
| F3 | R2 manual-path lower bound | MED | Confirmed. Adequately disclosed. |
| F4 | request→200 bundling | LOW-MED | **Upgraded to MED.** Protocol overhead asymmetry compounds with F10. |
| F5 | Log-normal on deterministic rails | LOW | **Upgraded to MED.** Actively biases mock-run comparisons against Stellar and Tempo in tail-sensitive metrics. Not just a convenience — a distortion. |
| F6 | BT near-degenerate | LOW | **Upgraded to MED.** BT strengths should not be reported as precise; seed-sensitivity analysis needed. |
| F7 | R10 pure-Tempo scoping | LOW | Confirmed. Correctly scoped. |

### New findings (DeepSeek)

| # | Finding | Severity | Description |
|---|---|---|---|
| **F8** | Deterministic vs probabilistic incommensurability | **MED-HIGH** | Ranking Stellar's deterministic finality alongside Base's probabilistic soft finality without quantifying reorg risk. The numbers are incommensurable — 2.74s deterministic ≠ 2.05s probabilistic. |
| **F9** | R11 measures Spark, not Lightning | **MED** | "MPP-on-Lightning" label is misleading. The 16.52s is Spark ceremony overhead; native Lightning HTLC settlement is sub-second. Rail should be relabeled. |
| **F10** | x402 vs MPP protocol overhead asymmetry | **MED** | The x402 rails share an OZ facilitator round-trip; MPP rails don't. This is a structural overhead difference unmeasured and unattributed, biasing within-fast-cluster comparisons. |
| **F11** | Tempo testnet→mainnet block interval gap | **LOW-MED** | Block interval not confirmed against mainnet `Presto`. Potential 2× finality gap undisclosed. |
| **F12** | Mock run_hash as performative pre-registration | **HIGH** | Anchoring a disclaimed non-result invites "security theatre" critique. |
| **F13** | Pre-registration performed AFTER calibration data collected | **HIGH** | **MOST DAMAGING.** Calibration data (2026-06-04/05) preceded methodology freeze (2026-06-05). k-grid, cluster narrative, and statistical framing were all chosen with full knowledge of outcomes. Pre-registration prevents HARKing on the mock run but not on the only real data in the system. |
| **F14** | Calibration table IS a published ranking — Variant-E firewall breached | **HIGH** | §7 publishes real measured medians from real infrastructure in rank order. Distinction between "calibration parameter" and "ranking" is specious when the parameter IS the ranked quantity. Regulatory risk if FCA views this as arranging. |
| **F15** | Master seed is human-chosen date, not random | **MED** | `20260717` is the POC launch date — narratively satisfying but not randomly generated. Compounds with F13 to suggest pattern of narrative-driven choices. |
| **F16** | Anchor chain has URL-based single point of failure | **MED** | OSF DOI resolves to a URL. If OSF is unavailable, the human-readable trust anchor breaks. Independent archival not specified. |
| **F17** | arXiv allows post-freeze updates | **LOW-MED** | arXiv preprints can be revised. Methodology doesn't specify v1-only as canonical. |
| **F18** | Legal posture undermines neutrality claim | **LOW** | Defamation defence strategy in a methodology document signals expectation of publishing contentious findings. Tonal issue; belongs in ops docs. |

---

## 6. Recommendations — priority-ordered

### Immediate (before §9 anchoring)

1. **Publish Solana `confirmed` alongside `finalized`** (addresses F1). The data exists. Suppressing it is the methodology's single most exposed flank. Show both, rank on the per-rail-canonical doctrine, and let the reader see the sensitivity.

2. **Acknowledge the calibration-timing problem** (addresses F13). Add a candid statement: "The k-grid and cluster analysis framework were finalised after calibration data was collected. This means the mock-run design is informed by the calibration outcomes. Pre-registration prevents HARKing on the mock run itself; it does not retroactively blind the designers to the calibration data. The real-rail run will use the same pre-registered design without recalibration, so the circularity affects only the mock validation."

3. **Randomise or restructure the calibration table** (addresses F14). Either randomise row order and replace `median_s` with log-normal μ/σ parameters, or obtain external legal review confirming the current structure doesn't constitute a ranking.

### Before real-rail publication

4. **Replace the master seed** with a randomly generated one (addresses F15).
5. **Switch deterministic-finality rails to discrete distributions** (addresses F5).
6. **Bootstrap calibration data for parameter CIs** and propagate into pass@k (addresses §3.2).
7. **Add seed-sensitivity analysis for BT within-cluster rankings** (addresses F6).
8. **Specify authoritative anchor and independent archival** (addresses F16, F17).
9. **Move legal posture language out of methodology** into ops documentation (addresses F18).

---

## 7. The decisive question

The self-review asks: *"Would a CRFM maintainer accept it?"*

**Answer: Yes, but only if F1 and F13 are addressed before anchoring.** A CRFM maintainer will accept the per-rail-canonical doctrine IF they can see the sensitivity analysis (both Solana thresholds, both Base thresholds) and IF the methodology acknowledges that the k-grid was chosen post-calibration. Without these, a CRFM maintainer will identify the suppressed Solana `confirmed` data and the post-calibration design timing as evidence of threshold-shopping and HARKing, and will recommend rejection.

The methodology is 85% of the way to being genuinely defensible. The remaining 15% is: show your work on the sensitivity analysis, and be honest about the calibration timing. These are disclosure items, not redesign items. The cost of addressing them is a few paragraphs of candid text; the cost of not addressing them is the credibility of the pre-registration itself.

---

*End of DeepSeek adversarial review. Submitted for recording into `adversarial-review.md` before §9 anchoring executes.*
