# PayBench v1.0 — Cross-LLM Adversarial Review (Model A)

**Reviewer:** Independent LLM instance (no access to `paybench/` harness code or `calibration/` provenance files; reasoning solely from `methodology.md` + `pre-registration-adversarial-review.md`).  
**Date:** 2026-06-06  
**Scope:** Pressure-test the frozen methodology prior to cryptographic anchoring (§9).  

---

## Executive Summary

The methodology is **methodologically sound and, with minor clarifications, defensible against the most likely hostile review vectors**.  
- **F1**, the highest-severity item, is **correctly resolved by D1-keep**; D1-uniform-optimistic would introduce a *larger* validity threat than it solves.  
- **D2-freeze** is the consistent choice under Variant E.  
- **Five novel findings (F8–F12)** are surfaced below; all are documentation/clarification gaps, not fixture-level blockers. **None require regen or re-freeze.**  
- The statistical apparatus (BT MLE + Wilson + pass@k) is technically correct but should add a prior-sensitivity note and clarify marginal-aggregation logic.  
- The **Variant-E firewall is strong but not foolproof**; the `run_hash` naming in §9 creates a subtle misreading risk that should be patched in prose before anchoring.

**Recommendation:** Accept D1-keep / D2-freeze, patch the six prose clarifications noted below, then proceed to §9 anchoring.

---

## 1. F1 Pressure-Test: Is “Per-Rail Canonical Reliance Level” Principled or Euphemistic?

### The strongest hostile framing
> “You have operationalized ‘finality’ as *the threshold each rail’s marketing team prefers*. Base gets the optimistic sequencer-inclusion figure because Coinbase wants 2-second payments; Solana gets the conservative `finalized` figure because that pushes it to the slow cluster. A symmetric doctrine—e.g., uniform-optimistic—would collapse the ranking. This is threshold-shopping dressed in agent-DX language.”

### Independent analysis

**1. Documentary sourcing audit.**  
The §3 table cites ecosystem-specific thresholds:
- **R1 (Base):** OP Stack documentation explicitly presents sequencer-level soft finality as the user-facing settlement experience; L1 finality is framed as a bridging/withdrawal threshold. This is an accurate characterization of public builder guidance.
- **R9 (Solana):** Anza/Helius documentation explicitly warns against relying on `confirmed` (12-of-16) for irreversible actions and designates `finalized` (32-slot rooted) as the safe reliance point.  
- **R2 (Stellar):** Ledger close is the protocol-defined irreversibility point.
- **R10 (Tempo):** BFT block finality is the protocol termination point.
- **R11 (Lightning):** Preimage release is the HTLC claimability point.

These are not marketing preferences; they are **protocol-layer builder contracts**. The doctrine is therefore *descriptive*, not *normative*—it asks “what does this rail tell its own builders to rely on?” rather than “what would we like to measure?”.

**2. Agent-DX coherence.**  
An autonomous agent integrating the Base stack *is* told to treat sequencer inclusion as the payment-reliance point; an agent integrating Solana *is* told to wait for `finalized`. Measuring the agent’s actual wait condition is the correct functional definition for a rail-DX benchmark. Uniform-optimistic (Solana `confirmed`) would misrepresent the operational risk the Solana ecosystem tells the agent to bear; uniform-irreversibility (Base L1) would measure a condition no Base agent waits for.

**3. Why D1-uniform-optimistic is *less* safe than D1-keep.**  
If Solana were switched to `confirmed` (median $2.27\,\text{s}$ per the doc’s own capture), the benchmark would report a settlement-finality figure that Solana’s own documentation labels **unsafe for irreversible downstream actions**. This would be a direct methodological contradiction: the benchmark would claim to measure “the point at which the payee can rely on the funds without risk of reversal” while using a threshold the underlying protocol explicitly says carries reversal risk. A CRFM reviewer or competitor would flag this as **measurement invalidity**, not as a fairness improvement.

**4. Residual risk and mitigation.**  
The genuine asymmetry—Base’s threshold is probabilistic/optimistic; Solana’s is cryptographic—remains. The doc already names this openly in §3. To further harden the flank, I recommend adding a **“Finality equivalence class”** column to the §3 table:

| Rail | Finality definition | Equivalence class |
|---|---|---|
| R1 | Soft finality, 1 block | Optimistic / probabilistic |
| R2 | Ledger close | Deterministic BFT |
| R9 | `finalized` (32-slot) | Cryptographic root |
| R10 | BFT block finality | Deterministic BFT |
| R11 | Preimage release | Hash-time-locked claim |

This makes the non-comparability of the cryptographic mechanisms **visually explicit**, so a reviewer cannot claim the asymmetry was hidden.

### Disposition on F1
**Accept D1-keep.** The doctrine is principled, documentary, and operationally coherent. The open naming of asymmetry in §3 is the correct defensive posture; D1-uniform-optimistic would trade a visible, defensible asymmetry for a hidden, indefensible misrepresentation of Solana’s safety model.

---

## 2. Novel Findings (F8–F12)

| ID | Finding | Severity | Disposition |
|---|---|---|---|
| **F8** | R11 provenance mislabelled “real-rail”; measured on **regtest** | MED | Relabel in provenance; no fixture regen |
| **F9** | R10 testnet→mainnet “shares the consensus” implies empirical identity; unverified | LOW–MED | Add disclosed limitation in §7 |
| **F10** | `request → HTTP 200` semantic boundary is ambiguous across rails | MED | Clarify harness spec in §3 |
| **F11** | “Deterministic” finality (R2, R10) collides with non-zero $\sigma_{\log}$ spreads | LOW | Add parenthetical in §3 |
| **F12** | `run_hash` over *output report* invites misreading as real-rail result anchor | LOW | Rename or clarify in §9 |

### F8 — R11 “real-rail” provenance label (MED)
The calibration table (§7) tags R11 as `first-party-empirical (real-rail)`. This is inaccurate: the measurement is on **Spark hosted regtest**, not the Lightning mainnet. Regtest is a local, zero-difficulty network. While the Spark FROST+SSP ceremony is real hosted-operator infrastructure, the underlying Lightning HTLC and peer propagation are simulated.  
**Fix:** Change the provenance tag to `first-party-empirical (hosted-operator stack on regtest)`. This is not a silent cap—it is a precision correction.

### F9 — R10 testnet→mainnet extrapolation (LOW–MED)
§7 states: “Moderato testnet … mainnet Presto … shares the consensus.” Sharing the consensus *algorithm* (Simplex) does not imply sharing the empirical latency *distribution*. Testnet validator topology, geographic dispersion, and load differ from mainnet. The central tendency ($1.75\,\text{s}$) is pinned to testnet, yet the prose implies it parameterizes mainnet.  
**Fix:** Add a third disclosed limitation in §7 (alongside the R9/R11 tail spreads and R2 lower bound): *“R10 fixture is calibrated on Moderato testnet; mainnet Presto may differ in empirical latency despite shared consensus logic.”*

### F10 — `request → HTTP 200` semantic ambiguity (MED)
§3 defines the unit as “request → HTTP 200 (submission → the agent's reliance point).” In x402 and MPP flows, the initial HTTP 200 from a facilitator typically signals **acceptance**, not **finality**. If the harness stops timing at the initial 200, it measures authorization latency for some rails and finality latency for others. If the harness instead polls/webhooks until finality, the “HTTP 200” label is semantically wrong—the finality signal may be a subsequent HTTP response, a streaming event, or a callback.  
**Fix:** Clarify in §3 that the unit is “request → **agent-perceived finality signal** (which may be an HTTP 200, a webhook, or a polled state transition, depending on rail adapter semantics).” This prevents an adversary from claiming the unit mixes acceptance and finality.

### F11 — “Deterministic” vs. timing variance (LOW)
§3 labels R2 and R10 as “deterministic.” Yet their $\sigma_{\log}$ values are $0.116$ and $0.177$—meaningful multiplicative spreads ($\approx \pm 12\%$ and $\pm 18\%$ at one standard deviation). “Deterministic” in distributed systems refers to **finality guarantee** (no reorg), not **clock determinism** (zero jitter). A hostile reader could quote this as internal contradiction.  
**Fix:** Add a parenthetical in §3: *“Deterministic finality guarantee; empirical timing variance is from network latency, ledger-boundary alignment, and operator ceremony overhead.”*

### F12 — `run_hash` over output report (LOW)
§9 lists a `run_hash` as part of the frozen manifest. The doc states it is “deterministic over the report with no wall-clock written into it.” Hashing the *output* rather than the *input manifest* is unusual in reproducibility protocols. If the harness contained a deterministic bug (e.g., an off-by-one in the BT smoother), the run_hash would faithfully commit to the buggy output without signalling that anything is wrong. More importantly, a casual reader may interpret a pre-registered hash of a “run” as a **real-rail result**, undermining the Variant-E firewall.  
**Fix:** Either (a) rename to `mock_pipeline_verification_hash`, or (b) add a parenthetical in §9: *“This hash verifies bit-for-bit reproduction of the mock-fixture pipeline output; it is not a real-rail ranking result.”*

---

## 3. Pre-Registration Mechanics & Variant-E Firewall

The pre-registration protocol (OSF + cosign + OpenTimestamps + git tag + arXiv) is **defence-in-depth done correctly**. The trust-anchor triad (DOI / Bitcoin block / Rekor) satisfies the “no single point of trust” requirement.

**Firewall strength:**  
- §0 and §7 are explicit that the anchors commit to the *method* and *calibrated mock fixtures*, not a real-rail ranking.  
- The §9 manifest includes fixture hashes and a run hash, but no real-rail identifiers or production endpoints.

**Residual gap:**  
The frozen manifest in §9 lists a `run_hash`. Under Variant E, this hash is computable from mock fixtures. However, the **existence of a run hash in a cryptographic manifest creates pragmatic implicature**: readers expect a hash in a pre-registration to be a *result commitment*. The doc should add one sentence to §9: *“Under Variant E, the run_hash is computed over the mock-fixture report; it will be replaced by a production-rail run_hash only upon Q3 HELD residual clearance.”*

**Telemetry signing:** The exclusion of VCDM 2.0 / SD-JWT for bulk telemetry in favor of Merkle+cosign is correct. VCDM is over-engineered for dataset integrity; Merkle roots are the standard approach (e.g., ClaimData, Certificate Transparency).

---

## 4. Statistical Verification

### 4.1 Bradley-Terry MLE
The model specification is:
$$ P(i \succ j) = \frac{e^{\beta_i}}{e^{\beta_i} + e^{\beta_j}} $$

With $n=500$ trials per pair and near-complete separation (fast cluster $\sim 2\,\text{s}$ vs. slow cluster $\sim 15\,\text{s}$), the unregularized MLE would diverge. The symmetric smoothing prior of $1.0$ keeps estimates finite. This is statistically legitimate, but **the prior contributes non-trivially to the precise strength values** in the degenerate regime. For transparency, the eventual publication should report that BT strengths are prior-dependent under separation and should display a **sensitivity table** (e.g., prior $\in \{0.5, 1.0, 2.0\}$) or, more simply, report raw pairwise win/loss matrices alongside latent strengths so readers can verify that the ranking is driven by the data, not the prior.

### 4.2 pass@k and the $k$-grid
The grid $\{2, 3, 5, 10, 15, 20\}$ is well-motivated by the calibrated medians. For each rail, pass@k is estimated from $4 \times 500 = 2000$ marginal trials (each rail appears in 4 pairs). The standard error at $\hat{p} \approx 0.5$ is:
$$ \text{SE} = \sqrt{\frac{\hat{p}(1-\hat{p})}{n}} \approx \sqrt{\frac{0.25}{2000}} \approx 0.011 $$
so the Wilson 95% LB is tight enough for discrimination.

**One subtlety:** The $k$-grid is frozen and was chosen post-calibration. While the doc states it will not be re-fit per run, a critic could argue the grid is **overfitted to the mock-cluster structure**. If a real-rail run shifts R2 to $4\,\text{s}$ (spec path) or R9 mainnet collapses toward $10\,\text{s}$, the grid may become less informative. However, because the grid is frozen *a priori* in the pre-registration, this is not a p-hacking threat—merely a potential informativeness issue for future real-rail runs. Acceptable.

### 4.3 Wilson lower-bound confidence intervals
The Wilson interval is:
$$ \frac{\hat{p} + \frac{z^2}{2n} \;-\; z \sqrt{\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}} $$
with $z = 1.96$ for 95% confidence. This is the correct choice for binomial proportions, especially near boundaries. The lower-bound reporting policy is appropriately conservative.

**Note:** For pairwise win rates ($n=500$ per pair), the LB at extreme win rates (e.g., $0.99$ or $0.01$) will be less tight than the normal approximation but still well-behaved. No issue.

### 4.4 Sample size and power
5,000 total trials is modest but sufficient for the BT + pass@k combination. The complete-graph design (10 pairs for 5 rails) ensures connectivity for MLE identifiability.

---

## 5. Dispositions & Recommendations

| Decision / Finding | Disposition | Action before anchoring |
|---|---|---|
| **D1** Per-rail canonical doctrine | **KEEP** (D1-keep) | Add “Equivalence class” column to §3 table |
| **D2** Quiet-condition $\sigma_{\log}$ | **FREEZE** (D2-freeze) | None (disclosure in §7 is sufficient) |
| F8 R11 “real-rail” label | Accept | Edit provenance table in §7: regtest stack |
| F9 R10 testnet→mainnet | Accept | Add 3rd disclosed limitation in §7 |
| F10 HTTP 200 semantics | Accept | Clarify agent-perceived finality signal in §3 |
| F11 Deterministic vs. spread | Accept | Add parenthetical in §3 |
| F12 `run_hash` naming | Accept | Rename or add Variant-E clarifier in §9 |
| BT prior sensitivity | Note | Add sensitivity sentence in eventual publication |
| Firewall pragmatics | Strengthen | Add Variant-E sentence to §9 run_hash paragraph |

**Bottom line:** The methodology is冻结-ready. The six prose patches above are zero-regen clarifications that close the remaining misreading surfaces. No fixture regeneration, no re-freeze, no change to D1 or D2. Proceed to §9 cryptographic anchoring.

---
*End of Model A review.*
