Here is an adversarial review of your proposed benchmark methodology. 

Your proposal to keep these rails in single sub-rankings while papering over 500x latency gaps with a "disclosure bucket" is intellectually lazy and methodologically flawed. You are attempting to salvage a unified "race" where no meaningful race exists.

Here are the concrete answers to your questions, tearing down your assumptions:

**1. Is "one race + 3-bucket work-type disclosure" defensible?**
No, it is completely indefensible. Cross-class heterogeneity of 2–3 orders of magnitude makes a single pairwise ranking meaningless. A benchmark "race" inherently implies that the systems are solving the *exact same problem* under comparable constraints. They are not. 
AP2 (1.68 ms) is performing local, static cryptographic validation. x402 (777 ms) is performing dynamic, distributed state resolution across a network. Putting them in the same ranking and declaring AP2 the "winner" of the latency race is like racing a bicycle against a commercial airliner on a 10-meter track, then adding a footnote that the airliner had to start its engines. A disclosure bucket does not fix an apples-to-oranges comparison; it merely admits to it. 

**2. If you'd sub-split: on what boundary exactly? How to avoid infinite regress?**
You must sub-split strictly on the **Trust/State Dependency Boundary**: *Local Compute vs. External State Resolution*. 
*   **Class 1 (Local):** Authorization depends solely on data provided in the request payload and local, pre-shared keys/mandates (e.g., AP2, Tempo cache-hits, x402 issuance).
*   **Class 2 (External):** Authorization strictly requires querying an external state machine or third-party service (e.g., x402 verification, L402 invoice minting).

You avoid infinite regress because this is a hard, binary architectural boundary: Does the critical path require network I/O, or does it not? Stop at two classes. "Periodic" is not a class; it's a caching policy (see Q4).

**3. Is "disclose but never subtract" correct? Name cases where normalizing is fair.**
"Never subtract" is mostly correct—the user feels the latency—but you are ignoring a fatal variable: **Network Topology Ping**. 
If you measure x402 and the facilitator is hosted in AWS us-east-1, but your benchmark runner is in London, you aren't measuring the rail's authorization work; you are measuring transatlantic fiber-optic speed. 
*The case where you MUST normalize:* You must subtract the baseline network RTT (ping) between the benchmark runner and the backing service, reporting only the *processing delta*. Otherwise, your benchmark will rank rails based entirely on how physically close the benchmark server happens to be to the rail's chosen infrastructure provider. 

**4. Does the Tempo "periodic/amortized" class warrant its own bucket?**
Absolutely not. It is a measurement artifact of an arbitrary 5-second TTL caching configuration by one server implementation. If Tempo set the TTL to 1 millisecond, it would be a Class 2 (External) rail. If they set it to 24 hours, it would effectively be a Class 1 (Local) rail. 
You cannot build a benchmark methodology around one vendor's default configuration file. You must hold it constant: measure and report the **Cache Hit (Steady State)** and **Cache Miss (State Refresh)** as separate explicit phases, or mandate reporting P99 latency alongside the median. A 19.5ms median that hides a 360ms latency spike every 5 seconds is statistical malpractice.

**5. Anything missing that would embarrass this methodology?**
**Throughput and Rate Limiting.** By obsessing over latency in a vacuum, you are ignoring what happens when these distinct architectures scale. A pure in-process crypto check (AP2) will scale linearly with CPU cores. A network-dependent rail (x402, L402) will bottleneck on connection pools, TLS handshakes, or hit hard API rate-limits from the chain-RPC/facilitator. Publishing a latency benchmark for financial primitives without testing under concurrent load (e.g., 100 QPS, 1000 QPS) will embarrass you when developers adopt the "fast" rail and watch it collapse in production.

***

### DELIVERABLE

**Verdict:** REJECT

**The Single Strongest Argument Against It:**
Your methodology attempts to rank local, static cryptographic operations against synchronous, distributed network state queries in a single "race." This fundamentally misleads users by confusing architectural constraints with implementation efficiency, while masking severe latency spikes (Tempo) and network transit biases (L402/x402) behind medians and weak "disclosure" labels.

**Minimal Change Required to Ratify (if forced):**
1. **Abandon the single race:** Sub-split both A and B into two hard boundaries: *Local Compute* vs *External Network I/O*. Do not rank across this boundary.
2. **Normalize network RTT:** For External Network I/O rails, you must subtract the baseline ICMP/TCP ping to the backing service to isolate the actual processing latency of the rail.
3. **Ban Medians for Amortized Rails:** For any rail utilizing a cache (like Tempo), you must publish P99 latency alongside the median to expose the cache-miss penalty, rather than dumping it into a "periodic" disclosure bucket.
