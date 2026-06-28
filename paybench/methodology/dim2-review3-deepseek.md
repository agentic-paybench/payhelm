## Final Confirmation (Round 3)

### FC1: Excluding Tempo-Charge from Payment-Validation (A)

**yes**

The exclusion is construct-valid, not a cherry-pick. Tempo-Charge fuses verify+settle (~500ms), making it a *different kind of operation* from pure authorization — including it would re-introduce the very category error that Round 1 identified. The appendix disclosure (+ the Session variant remaining in the race) provides transparency without contaminating the ranking with settlement latency.

---

### FC2: Challenge-Issuance Race (B)

**yes**

C(5,2) = 10 pairs resolves the n=1 problem. A and B remain firewalled (category-error fix preserved). x402 appearing in both is *not* confusing — it is precisely the correct design: the same rail exposes two distinct authorization primitives, measured separately, like benchmarking a database's read latency and write latency as different metrics. The RR6 labeling (primitive name + client-visible tag) disambiguates this.

---

### FC3: Hardened-BT with Cox-PH Fallback

**adequate**

A pre-specified fallback with objective triggers (transitivity, tie-rate, censoring-rate) is methodologically sound adaptive analysis — not p-hacking. The one-method-across-dimensions rationale is somewhat weakened by the Davidson/censoring hardening already differentiating this from D1's pure BT, but the core logic holds: don't abandon the incumbent without evidence it actually fails on real data. The *one gap*: the trigger thresholds for "transitivity failure" and "pathological censoring-rate" must be numerically pre-specified (e.g., "transitivity violations in >X% of triples" or a Bayes p-value threshold). Without that, the trigger is fuzzy and the fallback looks ad-hoc.

---

### FC4: RR4/RR5/RR6 Sufficiency

**yes, with one minor gap**

RR4 (RTT subtraction + canonical geography + ≥2 topologies), RR5 (sig-verify + fresh state read in the timed window), and RR6 (client-visible + scope tags) collectively close the obvious gaming and confound vectors. The remaining gap: **ICMP ping RTT ≠ TCP/TLS application-layer RTT**. A rail could optimize its ICMP path independently of its HTTPS path, and TCP handshake + TLS negotiation overhead varies by rail (e.g., session resumption, 0-RTT). The subtraction may not cleanly isolate compute. This is a measurement-engineering concern, not a fatal design flaw — but it should be acknowledged with a sensitivity analysis (e.g., also measuring TCP-handshake RTT via a stripped-down TCP probe, or reporting raw uncorrected latencies alongside corrected ones).

---

### New Fatal Issues Introduced by Refinements?

None. The split into A/B, the Davidson/censoring hardening, and the pre-specified fallback are all net improvements with no backsliding. The two gaps above (fallback trigger thresholds, ICMP-vs-TCP RTT mismatch) are **pre-registration clarifications**, not design flaws.

---

### Verdict

**PRE-REGISTERABLE** — with one required fix: numerically specify the BT-to-Cox-PH fallback trigger thresholds (transitivity-violation rate, tie-rate, censoring-rate cutoffs) before data collection.
