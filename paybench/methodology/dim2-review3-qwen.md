## FINAL CONFIRMATION — RAPL (Round 3)

| # | Question | Verdict |
|---|----------|---------|
| **FC1** | Tempo-Charge exclusion | **yes** |
| **FC2** | Group B fix + x402 dual membership | **yes** |
| **FC3** | Hardened-BT vs. survival-primary | **adequate** |
| **FC4** | RR4 / RR5 / RR6 sufficiency | **sufficient** |

---

### FC1 — Tempo-Charge exclusion: **yes**
Charge's fused verify+settle (~500 ms) *is* settlement, not an authorization primitive — including it would have been the contamination. Excluding it and disclosing it in an appendix is methodologically correct and transparently non-cherry-picked, because Session-Grant is the mandate-validation primitive and Charge is a different operation entirely.

### FC2 — Group B + x402-in-both: **yes**
Group B gives L402/MPP-on-Tempo a properly populated cohort (5 rails → 10 pairs), closing the Round-1 n=1 gap. x402 appearing in both A and B is *clear, not confusing*, provided the table labels them as two distinct protocol checkpoints (header-generation vs. payment-validation) — which the as-built design explicitly does. A and B remain orthogonal ranking universes.

### FC3 — Hardened-BT with Cox-PH fallback: **adequate**
Davidson-ties + KM/P(auth ≤ k) already surface the survival-analytic picture *alongside* BT; the Cox-PH fallback is a guardrail, not a hidden escape hatch. BT-as-primary preserves the one-spine-across-dimensions story for D1 (seconds-scale, tie-free fixtures) where survival modeling would be superfluous complexity. **One caveat:** the fallback trigger thresholds (censoring-rate, tie-rate, transitivity-violation count) must be *numerically quantified* in the pre-registration, not left as prose — otherwise a hostile reviewer can allege post-hoc method-switching.

### FC4 — RR4/RR5/RR6: **sufficient**
Ping-RTT subtraction, sigverify+state-read gating, and scope-tagging close the major gaming vectors. **One minor implementation note (non-fatal):** the `/ping` baseline must traverse the *same network path and TLS termination* as the authorization endpoint; otherwise the subtraction is invalid and a rail could game it by routing `/ping` through a slower CDN tier. Confirm same-path routing in the measurement spec.

---

### New fatal introduced by refinements?
**None.** No new category errors, no re-merged populations, no statistical gaps wider than the quantified-threshold caveat above.

---

### VERDICT

> **Pre-registerable.** Condition the registration on one line: *state numeric thresholds for the Cox-PH fallback trigger (e.g., censoring > X%, tie-rate > Y%, Kendall-transitivity < Z) before data collection begins.* With that sentence in the pre-registration, ship it.
