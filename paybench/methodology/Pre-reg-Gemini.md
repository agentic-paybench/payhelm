Here is the synthesized **Cross-LLM Adversarial Review** executed by two independent analytical personas (Model Alpha: Distributed Systems/Consensus Expert; Model Beta: Statistician & CRFM Maintainer). 

These findings are designed to be deliberately hostile to pressure-test the frozen methodology prior to cryptographic anchoring.

---

### 1. Attacking F1 Hardest: The Finality-Threshold Doctrine
**Critique (Model Alpha - Systems Expert):** 
The defense of the "per-rail-canonical reliance level" is rhetorically clever but fundamentally hollow. By letting each rail's documentation define the finish line, you are not measuring finality; you are measuring **marketing confidence**.
*   **The Equivalence Flaw:** Base’s "soft finality" (1 block, ~2s) is a single, centralized sequencer promising it won't equivocate. Solana’s `finalized` (~14.6s) is the economic guarantee of a decentralized BFT validator set reaching max lock-out. You are conflating *trusted single-operator latency* with *trustless economic finality*. 
*   **The Attack:** A hostile competitor will say: *"PayBench ranks Web2 database writes (Base Sequencer) faster than decentralized consensus (Solana), calls them both 'finality', and hides behind the docs."* 
*   **Verdict on D1:** D1-keep is highly vulnerable to this exact critique. **D1-uniform-optimistic** (Base soft vs. Solana `confirmed`) is methodologically superior. Solana `confirmed` (~2.3s, 66%+ stake vote) represents the exact same milestone as Base soft finality: *the first high-confidence signal of inclusion before absolute economic irreversibility*. If this is an "agent-DX" benchmark, an agent accepts Solana `confirmed` for low-value payments just as it accepts Base soft finality.

### 2. Uncovering Missed Finality-Threshold Inconsistencies
**Critique (Model Alpha & Beta):**
We found three material inconsistencies the internal review missed:
*   **F8: Layer-2 vs. Layer-4 Confounding (Lightning/R11).** R11 measures the "Spark FROST-signing + SSP preimage-swap ceremony." This means you are racing a *hosted application layer's API ceremony* (R11) against a *base layer's consensus protocol* (R1). A statistician will flag this as a severe apples-to-oranges confounder. You aren't measuring Lightning's finality; you are measuring Lightspark's enterprise custody overhead.
*   **F9: Grid-Hacking (pass@k Threshold Selection).** §5.2 states: *"The grid is chosen to discriminate across the calibrated medians."* **This is a direct violation of pre-registration principles.** If you choose your evaluation thresholds *after* looking at the n=30 calibration data to maximize visual separation between rails, a CRFM maintainer will accuse you of "grid-hacking" (a form of p-hacking). The k-values must be derived from *external business logic* (e.g., standard API timeout SLAs), not reverse-engineered from the data. 
*   **F10: The Tempo Testnet-to-Mainnet Gap.** Tempo BFT block finality is deterministic, but network latency is not. An n=30 median of 1.75s on a testnet with geographically constrained, lightly loaded nodes is an aggressive baseline to freeze. When compared to Base's battle-tested mainnet/sepolia sequencer, Tempo is receiving an artificially pristine environment.

### 3. Stressing Pre-Registration Mechanics (Variant E / Mock Fixtures)
**Critique (Model Beta - Statistician):**
*   **The Mock Hash Footgun:** Pre-registering a `run_hash` of *mock* fixtures is a massive credibility risk. The public will see an OSF DOI, an arXiv preprint, and a Bitcoin timestamp cementing a specific ranking (e.g., R10 > R1 > R2...). Even with the Variant E firewall (§0, §7) saying "these are mock fixtures," the numbers *will* be screenshotted and shared by competitors (e.g., Tempo claiming victory over Solana). 
*   **The Future Re-run Vulnerability:** When you run the real-rail production data in Q3, you will generate a *new* run hash. A hostile reviewer will ask: *"If the first pre-registration was just a 'mock tool' test, what proves you didn't run the Q3 real-rail benchmark 50 times and only pre-register the hash of the best one?"* 
*   **Fix required:** You must cleanly decouple the *Methodology Pre-registration* from the *Data Pre-registration*. The current freeze should only hash the harness code, methodology text, and the mock *seed* definitions. Explicitly state that the real-rail Q3 run will have a separate, timestamped pre-registration of its specific run configuration 24 hours *before* execution.

### 4. Checking the Statistics
**Critique (Model Beta - Statistician):**
*   **BT Degeneracy & Prior (Confirmed F6):** A smoothing prior of 1.0 (Laplace smoothing) prevents the MLE from blowing up to infinity when rails are completely separated (e.g., fast rails win 100% of the time vs slow rails). However, using Bradley-Terry on multimodal, non-overlapping distributions is statistically inappropriate. BT assumes a continuous probability of A beating B. If the overlap is effectively zero, the model reduces to sorting medians, making the BT MLE scores meaningless pseudo-probabilities. Pass@k is the only valid metric here.
*   **Wilson LB Application:** Using the Wilson Lower Bound on pass@k is mathematically sound for empirical proportions near 1.0 or 0.0. *However*, because you are applying it to 500 trials sampled from a *mock log-normal distribution*, the Wilson interval only represents the *Monte Carlo sampling error* of your harness, **not** the real-world variance of the network. This must be explicitly stated to avoid statisticians claiming you are misrepresenting network variance as sampling variance.

---

### Recommended Dispositions (To record in adversarial-review.md before anchoring)

| Finding | Source | Proposed Disposition (Action before freeze) |
| :--- | :--- | :--- |
| **F1 (Threshold)** | Cross-LLM | **Reopen D1.** Strong recommendation to pivot to **D1-uniform-optimistic** (Base soft vs Solana confirmed). "Canonical" is easily attacked as "marketing-driven." Both represent the first high-confidence inclusion. Warrants R9 regen. |
| **F8 (L2 vs L4)** | Cross-LLM | **Disclose in §3/§7.** Explicitly note that R11 captures application-layer/custody overhead, whereas R1 captures base-layer consensus. Accept the apples-to-oranges as an intentional reflection of "Agent DX" (the API they actually call). |
| **F9 (Grid-hacking)** | Cross-LLM | **Amend §5.2 text.** Remove language saying the grid was "chosen to discriminate across calibrated medians." Justify the `{2, 3, 5, 10, 15, 20}` grid based on standard Web/Agent timeout SLAs (e.g., 2s standard HTTP threshold, 10s gateway timeout), not the data itself. |
| **F10 (Tempo Testnet)** | Cross-LLM | **Add to §7 Disclosed Limitations.** Note that R10 (Tempo testnet) lacks the geographic latency penalties of a fully distributed mainnet, explicitly labeling it an optimistic bound like R2. |
| **Mechanics (Hash)** | Cross-LLM | **Clarify §9.** Add a single sentence to §9: *"This pre-registration anchors the measurement tool and mock baseline. The Q3 real-rail execution will be preceded by a separate Data Pre-registration committing to the production fixture hashes."* |
