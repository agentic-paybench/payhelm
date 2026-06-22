# Adversarial Review: PayBench Dimension 2 — Authorization Latency

---

## 1. Strongest Objections (Severity-Ranked)

### Objection A — Category Error in the Measurand (Severity: **CRITICAL / Near-Fatal**)

**The six "authorization" checkpoints are not the same kind of operation.** You are racing:

| Rail | What "authorization" actually is | Computational character |
|---|---|---|
| L402/Spark | Server *generates* a bearer token (macaroon) + invoice | Cryptographic key-derivation + signing (~trivial) |
| x402 (all) | Facilitator *validates* counterparty signature + checks funds availability | ECDSA/EdDSA verify + balance/state lookup |
| MPP-Tempo | Server *validates* payment credential pre-broadcast | Signature verify + credential decode |
| Google AP2 | Full pipeline: mandate lookup → credential issuance → routing dispatch | DB/policy lookup + token mint + network dispatch |

L402's macaroon is **permission-to-pay granted before any payer commitment exists**. It is the *server's* unilateral act. x402's `/verify` is the facilitator **validating the payer's already-signed commitment**. AP2 is a **multi-stage policy decision**. These are not "different security objects at different moments" — they are *different workloads of different computational depth at different trust positions*. L402 will almost always "win" this race because it is doing the least work at the earliest point. You are not measuring who authorizes fastest; you are measuring **whose authorization concept requires the least computation at the earliest lifecycle stage**. Bradley-Terry MLE will happily produce a ranking, but the ranking measures architectural philosophy, not engineering quality.

**Verdict: Survivable only if the trust/equivalence classes are not footnotes but *headline qualifiers* on every reported number (e.g., "L402 — *grant-type, pre-commitment*").** Without this, the number is actively misleading.

---

### Objection B — The MPP-on-Tempo Charge/Session Asymmetry Creates a Poisoned Data Point (Severity: **HIGH**)

For the "Charge" (one-shot) intent, the MPP docs fuse verify+settle into a single ~500 ms step. For "Session," verify is near-zero on off-chain vouchers. The doctrine says "only the ACCEPT is raced" — but for Charge, accept *is* the fused step. You now face a trilemma:

1. **Race only Session**: cherry-picks the fast path, ignoring the dominant real-world usage (one-shot agentic payments).
2. **Race only Charge**: measures ~500 ms which *includes settlement work*, poisoning comparability with Dimension 1 and every other rail.
3. **Race both and average/mix**: conflates two incommensurable quantities within a *single rail*.

The doctrine does not resolve this. The fused-charge caveat is *disclosed* but not *operationalized*. A rail's score becomes a function of the test-workload mix, which is an uncontrolled confounder.

**Verdict: Fatal as currently specified.** The pre-registration must declare exactly which MPP intent types are in scope, justify the choice against real agent usage profiles, and either exclude Charge or move it to a separate sub-benchmark.

---

### Objection C — G1 Is Worse Than Stated: The Benchmark Measures a Path No Agent Will Take (Severity: **HIGH**)

Mandating that the x402 `/verify` endpoint be "called explicitly" solves the *spec-compliance* problem but creates a **representativeness** problem. In any realistic in-process facilitator deployment (which is the dominant topology for agent-integrated x402), no agent ever sees a distinct authorization signal — it receives one atomic "payment succeeded" (or failed) response. By forcing an explicit `/verify` call, the benchmark:

- Measures a **two-trip** path (`/verify` + `/settle`) where production agents take a **one-trip** path.
- Penalizes rails whose facilitators are *more helpful* (i.e., those that combine steps to reduce user-visible latency).
- Rewards rails with more granular — but not necessarily better — APIs.

This is a classic **Goodhart's Law** trap: the metric (authorization latency of an explicitly-called `/verify`) ceases to measure what it was designed to measure (the authorization experience of an agent developer) once it becomes a target.

**Verdict: Survivable**, but only if you publish *two* numbers per x402 rail — the explicit-`/verify` number (this dimension) and the agent-visible-accept number (a "developer-perceived-latency" quantity) — and label the former *internal-checkpoint latency*, not *authorization latency*.

---

### Objection D — Pass@k with Wilson CIs Has No Power Analysis and Different Variance Profiles Will Dominate Rankings (Severity: **MEDIUM-HIGH**)

The methodology reuses pass@k = P(authorization ≤ $k$ s) + Wilson lower-bound CIs from Dimension 1. But authorization latency distributions across these six rails will have **wildly different shapes**:

- L402 macaroon issuance: low mean, low variance (simple crypto).
- AP2: higher mean, potentially high variance (multi-hop policy decision, DB lookups).
- x402 on Base vs. Solana: same protocol, different L1/L2 latency floors → different right-tail behavior.

With a fixed $k$, the Wilson lower bound will systematically **favor low-variance rails** even when their median latency is worse. A rail with a tight distribution at 80 ms will beat a rail with a median of 40 ms but a long tail — and the Wilson CI will make this look statistically confident. Without:

- A pre-registered **sensitivity analysis over $k$** (at minimum 3 values spanning the distribution),
- A **minimum $n$ per pairwise comparison** derived from a power analysis assuming the *highest-variance* rail,
- Reporting of **median + P95 + P99** alongside pass@k,

…you will publish a ranking that is an artifact of threshold choice and variance asymmetry.

**Verdict: Survivable** with the three amendments above pre-registered.

---

### Objection E — Google AP2 Is Incommensurable on Scope, Not Just Trust Class (Severity: **MEDIUM**)

AP2 does not settle. Its "authorization" covers *everything AP2 does*. For every other rail, authorization is a *proper subset* of the rail's total work. So AP2's number is its **total contribution to payment latency**, while for other rails it is a **partial contribution**. A downstream integrator reading the table will implicitly compare "what I wait for AP2 to do" vs. "the authorization slice of what I wait for x402 to do." These are different questions. The trust-class label helps, but the *denominator of effort* differs in a way that is not disclosed.

**Verdict: Survivable** with a scope-coverage qualifier (e.g., "AP2 score reflects the full scope of AP2; other scores reflect the authorization slice of a larger rail").

---

## 2. New High-Severity Flaw Not in G1-G2

### **N1 — Network Topology & Probe Placement Are Unspecified (Severity: HIGH)**

The doctrine defines the *logical* start and end of the latency window but is silent on:

- **Where the measurement probe lives** (same region as facilitator? same region as payer agent? midway?).
- **Whether facilitator, L1/L2 node, Lightning peer, and AP2 endpoint are co-located** or geographically distributed.
- **Whether TLS handshakes, DNS resolution, and connection pooling** are inside or outside the window.

These omissions are fatal for authorization latency specifically (unlike settlement latency, where block times dominate): authorization operations are **tens-to-hundreds of milliseconds**, so a 50 ms RTT difference from probe placement can **flip a pairwise ranking**. Without a pre-registered network topology (e.g., "all probes in `us-east-1`, facilitators in same AZ"), any published number has an uncontrolled ±50 ms confound — which, on this timescale, is the entire signal.

**This must be added to the pre-registration as a mandatory topology declaration, with a sensitivity analysis across at least two topologies** (co-located and cross-region).

---

## 3. Votes on DA1 and DA2

### DA1: (a) KEEP ✅ (with mandatory amendments)

Vote: **KEEP**, but only if three conditions are added to the pre-registration:

1. The `/verify` call must be explicitly labeled *instrumented internal checkpoint*, and every published table row carries a "client-visible: no" tag for x402 rails.
2. A companion "agent-perceived authorization latency" quantity is published alongside, even if only as descriptive statistics — so readers can see the gap.
3. The fused-topology caveat for MPP-on-Tempo is **operationalized**: Charge intent is excluded from the primary ranking (moved to an appendix benchmark) because its fused verify+settle step is incommensurable with other rails' accept checkpoints.

Option (b) CLIENT-ONLY would effectively remove x402 from the dimension, which defeats the purpose of benchmarking the most prominent A2A rail family. The problem is not that `/verify` is internal; the problem is that calling it internal while treating it as an agent-facing metric is misleading. Fix the *labeling*, not the *scope*.

### DA2: (c) SPLIT ✅ (modified)

Vote: **SPLIT**, but not into two equal sub-rankings. Instead:

- **Primary reported ranking** retains all six rails with per-rail canonical authorization points **(option a)** — because this is the most honest representation of what each rail's designers consider "authorization."
- **A required companion table** splits rails into two *interpretive groups*:
  - **Grant-type** (issuance of permission to pay): L402
  - **Verify-type** (validation of payer's commitment/ability): x402×3, MPP-Tempo, AP2
- Every headline ranking number carries its group label. Cross-group pairwise comparisons are reported with an explicit "cross-category comparison" warning, analogous to how medical meta-analyses flag heterogeneous populations.

Option (b) REPIN-R11 is wrong because it would force L402 to measure something that isn't its authorization model — the macaroon *is* the authorization in Lightning, and pushing to "payment-accepted" would conflate authorization with LN routing/settlement. Option (a) alone is what the 3-1 panel upheld for Dimension 1, but Dimension 2's authorization-point heterogeneity is *greater* than Dimension 1's finality-threshold heterogeneity, and deserves the added split-table safeguard.

---

## 4. Net Verdict

> **Publishable and pre-registerable, but only after four mandatory amendments: (1) pre-register measurement topology with sensitivity analysis; (2) exclude MPP-on-Tempo Charge intent from the primary ranking; (3) add per-row "checkpoint visibility" and "scope coverage" labels plus a grant-type/verify-type split table; (4) pre-register pass@k sensitivity over ≥3 $k$-values with a variance-aware power analysis.** Absent these, the dimension will produce a defensible-looking but confound-dominated ranking that overclaims comparability.
