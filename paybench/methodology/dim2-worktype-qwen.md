# Adversarial Review: RAPL Sub-Ranking Methodology v2

I'm going to be blunt: your proposal has a real core (the ISO-8583 precedent argument is sound and I won't re-litigate it), but it ships with two methodological debts that will get it shredded at any venue where reviewers know latency measurement, and one conflation that's actively dishonest. The 3-bucket disclosure is a fig leaf for a problem it doesn't solve.

---

## 1. Is "one race + 3-bucket disclosure" defensible?

**No, not as currently specified — but not because splitting is the right fix either.** The problem isn't the single ranking; it's that you're reporting **medians only**. A 462× gap between AP2 (1.68 ms) and x402/Base (777 ms) is not a *finding* — it is a **tautology of your work-class taxonomy**. You already proved this when you wrote "the latency gap between classes dwarfs the within-class spread." If that's true, then your headline ranking is encoding class membership, not rail quality. A reader who skips the disclosure table (i.e., every reader except the authors) learns nothing new from the ranking that the 3-bucket legend didn't already tell them.

That is **not** an argument to further split. Splitting by work class turns each sub-sub-ranking into an n=2 or n=1 "race," which is no longer a benchmark — it's a shopping list. The right fix is not a deeper taxonomy; it is a richer **per-rail** latency profile (see §2).

## 2. Where to split, or what to do instead

**Don't split. Report a richer per-rail number.** Concretely, replace your single "median" column with a tuple:

```
<rail> :: (P50, P95, P99, N, topology, date) × (E2E, backing-service-only)
```

That kills three birds:

- **Statistical honesty**: your n≈20–30 is borderline for a pairwise race over 6+ rails with heterogeneous classes. P95/P99 expose how much tail you're hiding in the median — especially for Tempo's cache-expiry spikes (your own text admits ~360 ms spikes you're currently burying).
- **Decomposed view** for the rail-designer audience, which you explicitly refuse to serve (see §3).
- **Topology anchoring**, which you need anyway (§5).

This is a *different instrument* than your 3-bucket legend and strictly better.

## 3. "Disclose but never subtract" — where this is wrong

You're right that E2E is what an agent operator cares about. But you named **one** audience and ignored another. There are at least three cases where subtracting / normalizing is the only honest move:

| Case | Why normalization is mandatory |
|---|---|
| **Two rails sharing the same facilitator** (e.g. x402 Solana vs x402 Stellar presumably hit the same hosted service and differ only on chain-RPC). Comparing E2E conflates "shared facilitator overhead" with "chain choice." | The delta (E2E − facilitator baseline) is the only fair signal of chain-side contribution. |
| **Comparing protocol *design* across rails**, e.g. "is BOLT11 invoice issuance inherently slower than x402 challenge emission?" | If the Lightning node is 1240 ms and x402's template is 2 ms, the gap is mostly your Lightning node's implementation, not BOLT11. Subtracting node RTT is how a designer learns whether the *protocol* is the bottleneck. |
| **Comparing the same rail across deployments or time.** | E2E is non-portable (facilitators move, RPCs upgrade). Subtracting the backing-service component is what gives you a baseline you can reproduce next year. |

Rule: **E2E is the headline; the decomposed view is the science.** Pretending one serves both audiences is false economy. Report both. This is standard practice in every systems benchmark since SPECint (overall score + sub-benchmarks) and SPECvirt (composite + per-tier).

## 4. The Tempo "periodic/amortized" bucket is a measurement artifact — own it

This is the conflation I called dishonest in the preamble.

A 5-second TTL is **one reference implementation's caching policy**, not a property of the Tempo protocol. If a different deployer ships Tempo with a 500 ms TTL, or no TTL, or a 1-hour TTL, they land in a different bucket with a radically different number. You cannot label this a **rail** property without one of:

- **(a) Protocol-baseline measurement**: disable the cache, measure the protocol's *minimum required* backing-service hops per call. If Tempo-the-protocol genuinely requires a chain read every N calls, report N as a protocol constant and the chain read latency as a protocol cost.
- **(b) TTL sweep**: report numbers at TTL ∈ {0, 5 s, 60 s, 300 s} so the reader sees the curve and understands they are buying into a caching contract, not a rail.
- **(c) Renaming**: call the bucket `periodic-backing-service (ref-impl, TTL=5s)` and never use it as a general rail property.

As written, you are effectively benchmarking "the opinion of a particular caching engineer" and publishing it as "how fast Tempo authorizes." That will be noticed.

## 5. What will embarrass you at publication

Five things, in descending order of severity:

1. **Medians-only is indefensible for a latency benchmark.** You know this — you already mentioned the 360 ms Tempo spike. A rail with P50=3 ms and P99=2000 ms is *worse* for an agent than a rail with P50=5 ms and P99=8 ms. Median erases that. Any competent reviewer will reject on this alone.
2. **"Single topology" is a fatal caveat for network-bound rails.** For x402, latency is dominated by RTT to the hosted facilitator. Your 400 / 464 / 777 ms numbers are functions of where you ran the test. Without at least 2–3 topologies (same-region, cross-region, client-continent), you cannot generalize. Reviewers will ask "where was this measured?" and your answer will be "one place, once."
3. **Temporal stability**: when were these measured? Facilitators and chain-RPC endpoints change. If x402's facilitator upgraded its infra three months after your measurement, your ranking is stale. You need a measurement timestamp and a re-measurement cadence commitment.
4. **Workload realism**: is the authorization request payload (macaroon size, voucher structure, x402 header size) realistic and held constant? Macaroon-verification latency is **superlinear in caveat count**; a contrived tiny macaroon will make L402 look better than a real one would.
5. **n≈20–30 per rail is underpowered for pairwise race.** With 6 rails, you have ~15 pairs. 20 samples × 15 pairs × P99 estimation = confidence intervals that will overlap *within* a work class, which is exactly where the interesting signal lives. Power analysis is missing.

---

## Verdict

### **RATIFY-WITH-CHANGES**

**Single strongest argument against the proposal:**
> A latency benchmark that reports only the median and relies on a 3-bucket disclosure legend to prevent readers from misusing a 462× cross-class gap is — for readers who skip the legend — actively misleading. The disclosure is a patch for a number that shouldn't be the headline.

**Minimal changes required** (none individually burdensome; together they rescue the work):

1. **Mandate P50 / P95 / P99** (not just median) per rail, with N and measurement timestamp.
2. **Add the decomposed view**: per rail, publish `(E2E, backing-service-component)` so the protocol-designer audience is served alongside the agent-operator audience.
3. **Resolve the Tempo conflation**: pick (a), (b), or (c) from §4 and stop publishing reference-impl TTL as a rail property.
4. **Run ≥ 2 topologies** or explicitly bound the scope of your ranking to a named region / facilitator distance, and commit to a re-measurement cadence.

Adopt those four and the methodology ships. Skip #1 and you should not publish at all.
