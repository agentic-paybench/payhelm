I've now analyzed the proposal in depth. Let me work through each question before delivering a verdict. I'll be deliberately unsparing.

---

## 1. Is "one race + 3-bucket work-type disclosure" defensible?

**No, not for a ranking that will be consumed as a leaderboard.** The disclosure is a necessary transparency mechanism but it doesn't fix the ranking problem — it merely annotates a category error.

The core issue: when within-class spread is at most ~2× but between-class spread is 250–800×, the ranking is *dominated* by work-class, not rail quality. A reader scanning the leaderboard sees AP2 at 1.68 ms "beating" x402/Base at 777 ms and forms a judgment. The bucket label — even if printed in bold — doesn't prevent the perceptual ranking. Human cognition defaults to ordinal position. The disclosure becomes a fig leaf: "we told you they're different, so it's your fault if you misread the ranking."

This is especially acute because the benchmark's stated purpose is comparing *rails*, but the ranking primarily measures architectural commitments (do you require a facilitator? do you mint invoices via LN?) rather than engineering quality within a given architecture. If x402/Base engineers optimize their facilitator by 30%, they move from 777 ms to 544 ms — still last place by an enormous margin. The ranking provides zero incentive or signal for within-class improvement; it's just an architectural taxonomy masquerading as a competition.

**The ISO-8583 precedent is inapposite.** Those comparisons involved rails that *all* had network dependencies — the variation was in hop count and clearing model, not in whether network I/O exists at all. Comparing a local ES256 verify to a multi-hop facilitator round-trip is like comparing a register-register CPU instruction to a disk seek and calling it a "storage benchmark."

---

## 2. If you'd sub-split: on what boundary, and how to avoid infinite regress?

**The principled boundary is:** does the authorization primitive's specification *intrinsically require* at least one network round-trip to complete?

This yields exactly two classes per sub-ranking:

| Class | Definition | Sub-ranking A members | Sub-ranking B members |
|-------|-----------|----------------------|----------------------|
| **Local-complete** | Authorization resolves without any network I/O in the primitive's critical path | AP2 (1.68 ms), Tempo warm path (19.5 ms) | x402 402 (2–3 ms), Tempo 402 (2–3 ms) |
| **Network-dependent** | Authorization intrinsically requires ≥1 network round-trip per instance | x402 Solana/Stellar/Base (400–777 ms), Tempo cold path (360 ms) | Lightning L402 (1252 ms) |

This boundary is:
- **Objective** — driven by protocol specification, not deployment choices.
- **Stable** — a rail can't migrate between classes without a protocol change.
- **Non-arbitrary** — the presence/absence of network I/O is the single largest latency cliff in distributed systems, universally recognized as a fundamental architectural distinction.
- **Terminal** — there's no plausible finer subdivision that isn't just measuring deployment-specific infrastructure (which facilitator host? which chain RPC endpoint?), and those belong in diagnostics.

**Infinite regress is avoided** because we stop at the architectural property of the *primitive definition*, not the *implementation quality*. "Which chain?" or "which facilitator software version?" are not primitive-level distinctions. The boundary is "does the spec require a network call?" — yes/no — and that's the end of the taxonomy.

**Tempo's amortized case** requires special handling (see Q4), but the principle holds: its cold path is network-dependent, its warm path is local-complete. Both are real properties of the rail, not measurement artifacts.

---

## 3. Is "disclose the backing-service hop but never subtract it" correct?

**Partially, but the absolutist framing is wrong.** There are at least two legitimate scenarios where subtraction/normalization is the *only* fair comparison:

### Case A: Protocol design comparison
If the question is "which authorization *protocol* has the lowest inherent overhead?" — i.e., you're comparing cryptographic construction and state-machine design — then the network round-trip *must* be subtracted because it's not a property of the protocol. An ES256 verify costs what it costs regardless of whether it's embedded in a facilitator call. Normalizing out the network hop lets you evaluate whether AP2's JWT-based mandate design is fundamentally more efficient than Tempo's EIP-712 sign-and-verify approach. Without this normalization, you can't answer the protocol-design question at all.

### Case B: Co-located deployment
If a rail *can* be deployed with the backing service co-located (facilitator on same machine, Lightning node on localhost), the network cost becomes near-zero and the comparison shifts. A benchmark that always measures across a WAN hop is measuring deployment topology, not the rail. Reporting the local-compute floor lets deployers understand what latency they'd get in a co-located architecture.

### Case C (bonus): Fairness to network-dependent rails
If you refuse to subtract network costs, then you're essentially punishing rails for architectural honesty. A rail that *could* do everything locally but chooses to offload to a facilitator for security/decentralization reasons looks 250× worse than a rail that does everything locally with no such guarantees. You're not comparing latency; you're comparing architectural tradeoffs that the benchmark doesn't capture. At minimum, you need a companion metric that isolates compute from network so the full picture is visible.

**The right approach:** Report *both* the local-compute floor (what the crypto/state-machine costs in isolation) AND the full-path latency (including backing-service round-trips). Don't subtract one from the ranking, but publish both so the reader can see the architectural tax explicitly. This is what good systems benchmarks do — they don't force a single number to carry all the meaning.

---

## 4. Does Tempo's "periodic/amortized" class warrant its own bucket?

**Yes, but not for the reason given.** The ~5 s TTL refresh isn't a measurement artifact — it's a first-class architectural property of the rail. However, treating it as a *third bucket* is the wrong solution. The right treatment is:

### The problem with a separate "periodic/amortized" bucket
The TTL is a **server-side configuration parameter**, not an intrinsic property of the Tempo protocol. A different deployment could set the TTL to 1 second or 1 hour or infinity (never expire). The bucket assignment would then be a function of the operator's configuration choice, not the rail's design. This makes the bucket boundary soft and gaming-prone — an operator wanting to look "local-only" could set TTL to infinity and never measure a cold path.

### The correct treatment
Tempo should be reported with a **two-number latency profile**: warm-path latency (cache hit, ~19.5 ms) and cold-path latency (cache miss triggering chain RPC, ~360 ms), plus the cache TTL and hit-rate assumption under the benchmark's workload. This makes the amortized nature *visible* without creating a fragile taxonomy bucket.

More importantly, Tempo should appear in **both** the local-complete ranking (using its warm-path number, annotated) and the network-dependent ranking (using its cold-path number, annotated). A rail with amortized network dependency genuinely belongs in both conversations, and forcing it into one bucket loses information.

### A deeper concern
If the benchmark doesn't control for cache state (i.e., it doesn't explicitly measure warm and cold paths separately and report both), then the median of ~19.5 ms is **misleading** — it's just an artifact of the measurement schedule. A different measurement cadence (e.g., bursts separated by >5 s) could produce a median of ~360 ms. This is a methodological vulnerability that a separate bucket doesn't fix — only explicit warm/cold separation does.

---

## 5. Anything we're missing that would embarrass this methodology at publication?

Several things. I'll be blunt.

### 5a. The "competitive signal" justification is circular
The proposal argues that normalizing away backing-service costs would "erase the competitive signal." But if the competitive signal is just "networks are slower than CPU cycles," that's not a useful signal — it's a tautology. The benchmark is measuring physics, not engineering. Any methodology that produces a ranking where the top and bottom are separated by 800× and the explanation is "one does network I/O, one doesn't" hasn't produced a benchmark — it's produced a network-connectivity detector.

### 5b. n≈20–30 per rail is inadequate for the network-dependent class
Network latency distributions have long tails. With n=20–30, you're not characterizing the 95th or 99th percentile with any confidence. For x402/Base at 777 ms median, the p99 could plausibly be 2–5 seconds depending on chain RPC congestion. Reporting medians alone for network-dependent rails without tail latency characterization is a significant omission that a networking reviewer would flag immediately.

### 5c. Single-topology measurement
All measurements are from "a single topology." The 400–777 ms range for x402 facilitators is entirely a function of where the facilitator and chain RPC endpoints are hosted relative to the measurement point. Move the benchmark client to a different region or cloud provider and these numbers could shift by 100–300 ms. The local-crypto numbers (1.68 ms, 19.5 ms) are topology-invariant. This means the *entire between-class variance* is actually measuring the benchmark's network topology, not the rails. A methodology that doesn't characterize topology sensitivity is measuring its own test harness.

### 5d. The Lightning L402 case is under-analyzed
The L402 402 issuance at ~1252 ms is presented as a single number, but BOLT11 invoice minting involves multiple sub-operations (channel selection, route hint construction, possibly on-chain fee estimation). Some LN implementations are significantly faster than others (CLN vs. LND vs. LDK). Collapsing "Lightning" to a single rail while x402 gets three chain-specific entries is an asymmetric treatment that needs justification — or it's cherry-picking the worst LN number.

### 5e. Missing: latency vs. security/decentralization tradeoff
If the benchmark publishes a leaderboard showing AP2 at 1.68 ms "winning" against everything else, it will be used to argue that AP2 is "the fastest payment authorization rail." But AP2's local-only ES256 verify has fundamentally different trust assumptions than x402's facilitator-mediated on-chain balance check. The benchmark measures speed but silently ignores what the speed buys or costs in security terms. A sophisticated adversary will point out that the benchmark is optimizing for the wrong variable in a payment system.

### 5f. The 3-bucket taxonomy has a boundary problem
Is a rail that calls a *local* facilitator (Unix socket, localhost) "local-only" or "per-call backing-service"? Technically it's a per-call service call, but the latency is microseconds, not hundreds of milliseconds. The taxonomy conflates "network I/O" with "backing service," but these are separable concerns. The disclosure needs to distinguish *where* the service runs, not just *whether* it runs.

---

## Verdict

**RATIFY-WITH-CHANGES**

### Single strongest argument against the proposal as written

> A ranking whose ordinal positions are determined 250–800× by architectural category membership rather than by implementation quality is not a benchmark — it's a taxonomy diagram rendered as a bar chart. The "3-bucket disclosure" annotates the category error but does not prevent it. Readers will rank-order the numbers regardless of the labels, and the methodology authors will be unable to resist headline claims about "the fastest rail" that elide the architectural distinction. The disclosure is transparency theater — it creates a paper trail of having "warned" readers while the ranking itself does the misleading.

### Minimal change required

**Split each sub-ranking into two separate leaderboards, using the intrinsic-network-dependency boundary** (does the primitive's *protocol specification* require a network round-trip to complete? Yes/No). Tempo's amortized case appears in *both* leaderboards with explicit warm/cold-path disaggregation (not a single median) and its cache TTL disclosed. Additionally, each network-dependent rail must report the **local-compute floor** (what the crypto/state-machine costs without the network hop) alongside the full-path latency, so the "architectural tax" is explicitly visible and the protocol-design comparison (Q3, Case A) remains possible.

This requires:
1. Two leaderboards per sub-ranking: **Local-Complete** and **Network-Dependent**.
2. No cross-leaderboard ranking comparisons permitted in the text or visual presentation.
3. Tempo reported in both with warm (`p50_warm`, TTL) and cold (`p50_cold`) numbers.
4. Every network-dependent rail reports a `local_compute_ms` diagnostic (the measured or modeled cost of the crypto/state-machine portion in isolation).

This stops the infinite regress at a principled boundary (protocol spec, not deployment config), makes the category distinction structural rather than annotational, and preserves the "measure rails as deployed" goal within architecturally comparable groups.
