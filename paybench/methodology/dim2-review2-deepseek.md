# Adversarial Review: PayBench Dimension 2 — Authorization Latency

---

## 1. Strongest Objections (Severity-Ranked)

### 🔴 Objection 1: CATEGORY ERROR — "Authorization" means three different lifecycle stages across rails (FATAL unless split)

The six rails measure fundamentally different moments in the payment lifecycle:

| Rail | What is actually being timed | Lifecycle stage |
|---|---|---|
| **L402 (Spark)** | Server generates macaroon + BOLT11 invoice | **Pre-payment**: invoice *issuance*, before any funds move |
| **x402 rails** | Facilitator validates signed payload + funds sufficiency | **Intra-payment**: payment validation, funds locked but not settled |
| **AP2** | Mandate verification + credential issuance + dispatch to processor | **Payment-instrument setup**: establishing a recurring authorization, not a single payment |

Racing these together is like measuring "time to issue a menu," "time to validate a credit card," and "time to sign a standing order," then ranking restaurants by "speed." The L402 macaroon issuance is an **OAuth-style capability grant** — it doesn't validate a payment, it doesn't check funds, it doesn't even require the client to *intend* to pay yet. It's the server saying "here's what you need to pay to access this resource." The x402 `/verify` is a **cryptographic funds-locking validation**. The AP2 flow is **mandate onboarding**.

The per-rail-canonical doctrine (Dimension 1's precedent) doesn't rescue this. Dimension 1 compared *different finality thresholds* (e.g., probabilistic vs. deterministic settlement), but all measured the same semantic event: *irreversible transfer*. Here, the events are different species. A L402 macaroon issued in 5ms "beats" an x402 `/verify` at 200ms only because the macaroon does less — it's a hollow victory. A ranking that confuses *doing less* with *being faster* is a validity-killing construct.

**Verdict:** **Fatal if a unified ranking is published.** Survivable only if rails are split into separate sub-rankings by authorization type (see DA2).

---

### 🟠 Objection 2: MPP "Charge" intent fuses Verify+Settle — the dimension's own premise is violated for one rail (FATAL for Charge intents)

The MPP spec's one-time "Charge" intent deliberately **fuses** the Verify and Settle procedures into a single ~500ms step. There is no separable "authorization" event. The doctrine claims authorization = "Verify procedure," but for Charge, Verify *is* Settle. The dimension's core premise — "explicitly NOT the point of irreversible settlement" — collapses for this intent type. If you include Charge intents in the benchmark, you are measuring settlement latency and calling it authorization latency, contaminating the dimension. If you exclude Charge intents and only test Session intents (near-zero voucher verification), you are cherry-picking the trivially fast path and hiding the rail's real-world behavior.

**Verdict:** **Fatal for any measurement that includes Charge intents.** Survivable only with explicit scope restriction to Session intents and prominent disclosure that Charge behavior is excluded because it violates the dimension's separation premise.

---

### 🟠 Objection 3: L402's measured event is NOT a payment authorization — it's API access control (FATAL unless relabeled)

L402 (Lightning Labs' protocol) is an **HTTP 402 Payment Required** flow: a client requests a resource, the server responds with a macaroon (capability token) + Lightning invoice. The client *has not yet paid*. The macaroon is an **access credential**, not a payment authorization. The payment authorization in the Lightning sense is the **preimage revelation** at settlement time (already Dimension 1's territory). Calling the macaroon issuance "authorization to proceed toward settlement" is semantically wrong: the invoice generation is the rail saying "pay this to proceed," not "you are authorized to settle." This is a pre-transaction setup step. Benchmarks that measure setup and call it authorization will systematically favor L402 for doing zero payment validation, creating a perverse incentive to push all security checks post-"authorization."

**Verdict:** **Fatal if the macaroon grant is the raced checkpoint.** Survivable only if L402's checkpoint is moved to a post-payment signal (e.g., invoice-payment-received acknowledgment before preimage release) — i.e., DA2 option (b) — or if L402 is split into a separate "grant-type" sub-ranking with explicit relabeling.

---

### 🟡 Objection 4: Measurement start-point ambiguity and cross-rail instrumentation asymmetry (HIGH severity, survivable)

"Payment intent presented to a rail" is undefined at the precision needed for millisecond-scale racing. When does the clock start?

- **x402**: agent sends `/verify` request? Facilitator receives it? First byte parsed?
- **L402**: client requests resource (triggering 402)? Server begins constructing macaroon?
- **AP2**: mandate verification request sent? Received by AP2 servers?
- **MPP**: credential presented to Verify endpoint?

If start times are measured at different OSI layers (client-side send vs. server-side receive), network RTT asymmetrically contaminates results. Rails with co-located facilitators (x402 on same machine) get an artificial ~0ms network advantage vs. cloud-hosted AP2. The "accept" checkpoint is also facilitator-internal; instrumenting it requires white-box access that may not be equally available across all six rails (AP2 is a Google service — can benchmarkers instrument its internal mandate verification?). Without **identical measurement topography** (client-side start, client-visible accept), systematic bias is guaranteed.

**Verdict:** Survivable with a rigorous measurement protocol specifying: (a) clock-start = client-side `send()` syscall timestamp, (b) clock-stop = first byte of response received at client, (c) all rails measured from identical vantage points with controlled network topology, (d) disclosure of any rail where server-side instrumentation is the only option.

---

### 🟡 Objection 5: Bradley-Terry + pass@k collapses latency distributions into a scalar that discards tail behavior agents actually care about (MEDIUM severity, survivable)

Agents making economic decisions care about **expected latency** and **tail latency** (p99, p99.9). The pass@k metric $P(T \le k \text{ s})$ with a fixed $k$ is sensitive to the arbitrary choice of $k$. A rail with $\mu=200\text{ms}$, $\sigma=50\text{ms}$ and a rail with $\mu=150\text{ms}$, $\sigma=300\text{ms}$ could have identical pass@k at $k=1\text{s}$ but radically different agent experiences. Bradley-Terry MLE on pass@k transforms a continuous distribution into a binary win/loss per race, discarding *how much* faster one rail was. This loses statistical power and can produce rankings that don't reflect expected latency ordering. Wilson lower-bound CIs compound this by penalizing rails with fewer observations, which could disadvantage newer rails in a way unrelated to their actual latency.

**Verdict:** Survivable. The methodology is inherited from Dimension 1 for consistency. But the dimension should **also** report mean/median/p95/p99 latencies and the accept→finalized gap distribution, not just the Bradley-Terry ranking. The pass@k choice should be pre-registered with sensitivity analysis across multiple $k$ values.

---

## 2. New High-Severity Flaw (not in G1 or G2)

### 🔴 FLAW N1: "Trust/equivalence class" labeling creates an illusion of safe comparison without preventing it

The doctrine proposes naming each rail's "trust / equivalence class" (e.g., "grant-type," "verify-type," "mandate-type") while still publishing a **unified Bradley-Terry ranking**. This is the worst of both worlds: it acknowledges incommensurability in a footnote while the leaderboard visually asserts commensurability. Users — especially those scanning a benchmark table — will compare ranks across equivalence classes regardless of disclaimers. Behavioral evidence from ML benchmarks (e.g., HELM's scenario groupings routinely ignored by Twitter screencappers) shows that a single sorted table *is* the message. If the maintainers believe the classes are genuinely incommensurable, they must not produce a unified ranking. Otherwise the "trust class" label is safety-washing.

**Verdict:** **High severity.** Not fatal if addressed by splitting the ranking (DA2 option c). Fatal to the benchmark's interpretability if a unified ranking is published with only textual caveats.

---

## 3. Adjudication of DA1 and DA2

### DA1: (a) KEEP — with three mandatory conditions

I vote **(a) KEEP**, but only with these non-negotiable conditions:

1. **The agent must explicitly call `/verify`** (or the rail's equivalent) and the clock must measure **client-side round-trip**: `send()` to first byte of response. The benchmark must never rely on facilitator-internal instrumentation as the primary measurement.
2. **Fused-topology deployments are disqualified** from the benchmark unless they expose a separable authorization endpoint. A rail whose canonical deployment fuses auth+s settle must be listed as "not measurable" for this dimension, not shoehorned in.
3. **The accept→finalized gap must be reported alongside the authorization latency** in every result table, not buried in an appendix, so users can see the full picture.

The alternative (b) CLIENT-ONLY would eliminate x402 rails entirely if no facilitator deployment exposes `/verify` to the agent in practice — an outcome that may be too restrictive given the spec does define it. KEEP preserves coverage while forcing honesty.

---

### DA2: (c) SPLIT — report grant-type vs. verify-type vs. mandate-type as separate sub-rankings

I vote **(c) SPLIT**. Reasoning:

Option (a) KEEP with per-rail-canonical points and trust labels is the Dimension 1 doctrine, but the semantic gap here is a **category difference**, not a threshold difference. Dimension 1 compared "finality after 6 confirmations" vs. "finality after probabilistic settlement" — both are *settlement finality*, just at different confidence levels. Here, L402 measures an *invoice generation*, x402 measures a *funds validation*, and AP2 measures a *mandate setup*. These are not points on the same spectrum; they're different spectra entirely. A unified ranking is actively misleading.

Option (b) REPIN-R11 (move L402 to a later signal) would make L402's measurement more comparable but would **destroy** the per-rail-canonical doctrine: you'd be imposing an external definition of "authorization" on L402 that its own spec doesn't recognize. That's methodological imperialism that undermines the benchmark's claim to measure each rail on its own terms.

Option (c) SPLIT preserves each rail's canonical definition while preventing invalid cross-type comparisons. Three leaderboards — "Grant-type authorization latency," "Verify-type authorization latency," "Mandate-type authorization latency" — are honest, interpretable, and still allow within-type racing (e.g., x402-on-Base vs. x402-on-Solana vs. MPP-on-Tempo can race in verify-type). The L402 rail races only against itself (or future grant-type rails), which is appropriate until more rails share that model.

---

## 4. Net Verdict

> **Publishable only if the ranking is split into grant/verify/mandate sub-leaderboards, Charge intents are excluded, and all measurements are client-side round-trips with disclosed instrumentation gaps; without these changes, the unified ranking would measure incommensurable lifecycle events and mislead users about relative rail performance.**
