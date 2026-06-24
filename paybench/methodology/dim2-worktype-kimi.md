Your proposal collapses the moment you treat a $460\times$ latency gap as a pairwise “race.” Here is the concrete dismantling.

### 1. Is “one race + 3-bucket disclosure” defensible?

**No.** The heterogeneity does not merely make the ranking misleading; it renders it *mathematically degenerate*. When class (i) median is $1.68\,\text{ms}$ and class (iii) median is $777\,\text{ms}$, the ranking is a lexicographic sort on work-class with probability near $1$. The pairwise comparison is no longer measuring rail quality; it is measuring whether a network `syscall` occurs on the critical path. A disclosure label does not fix an ordinal scale that has lost its cardinal meaning. You would not rank sorting algorithms by running in-process `qsort` against a petabyte external merge sort across a trans-Atlantic link, label the latter “per-call backing-service,” and call it a single race.

Your ISO-8583 precedent is a false equivalence. Those historical comparisons measured **end-to-end settled rails** whose regulated infrastructure was definitionally inseparable from the rail. Here, the x402 facilitator is a *deployment choice*: if I colocate the facilitator on `localhost`, x402 drops to $2\,\text{ms}$ and “wins” AP2. Your single-race scoreboard therefore reflects topology shopping, not protocol merit.

### 2. Sub-split boundary and the right instrument

**You must sub-split.** The boundary is the **critical-path I/O dependency boundary**: separate primitives whose minimum theoretical latency is bounded by CPU cycles from those bounded by an unavoidable network round-trip (or IPC that cannot be eliminated without violating the protocol spec).

Stopping criterion to avoid infinite regress: split until the within-class dynamic range is $<10\times$. If a class still spans $>10\times$, you have accidentally mixed distinct primitives (e.g., different facilitator codebases or different L1 RPC endpoints) and should normalize by operation count or bytestring size. This is not infinite regress; it is basic variance decomposition.

The 3-bucket disclosure is the wrong instrument because it is a **scalar label on a vector phenomenon**. The correct instrument is a **mandatory tuple**: $(t_{\text{local}}, t_{\text{io}}, \rho_{\text{io}})$, where $t_{\text{local}}$ is the measured local compute floor (isolated on a null-backing-service stub), $t_{\text{io}}$ is the observed backing-service component, and $\rho_{\text{io}} = t_{\text{io}}/t_{\text{total}}$ is its share. This preserves the rail-as-deployed reality while actually showing where competitive pressure exists.

### 3. “Disclose but never subtract”

**Dogma.** Subtracting (or reporting against a normalized local stub) is mandatory when you are comparing **protocol designs** rather than **SaaS instances**. If your goal is to advise a rail adopter, that adopter may colocate or cache the backing service. A merchant running both the acceptor and the LND node on the same rack will see an L402 issuance far closer to your “local” class. Not subtracting conflates network geography with authorization logic.

You **must** subtract or normalize when:
- the backing service is swappable or co-locatable by the operator;
- the backing-service variance swamps the signal ($\sigma_{\text{io}} \gg \mu_{\text{total}}$), which is exactly your case;
- you claim to measure the rail’s *primitive* rather than a specific infrastructure lease.

### 4. Tempo’s “periodic/amortized” bucket

**It is a measurement artifact of your arrival process and cache TTL,** not a rail taxonomy. A $5\,\text{s}$ TTL under an unspecified request distribution yields a median that is uninterpretable and unrecoverable. If your $n \approx 20$–$30$ requests were back-to-back, the cache never expired and you measured $L_{\text{hot}}$ exclusively; if they were Poisson at $1\,\text{Hz}$, you should see a bimodal distribution with a materially different median.

You must hold cache state constant or report **conditional metrics**: $L_{\text{hot}}$ vs. $L_{\text{cold}}$ with the exact inter-arrival time distribution disclosed. Giving it a special bucket merely invites vendors to game you with infinite TTLs.

### 5. Embarrassing omissions

- **Statistical infantilism.** $n \approx 20$–$30$ per rail is inadequate for WAN tail latencies. You cannotresolve $400\,\text{ms}$ vs. $464\,\text{ms}$ with any confidence; your “raced pairwise” is noise.
- **No workload specification.** No arrival process, concurrency level, keep-alive status, or payload size. A cold TLS handshake dwarfs protocol logic; you do not disclose which it was.
- **Tail blindness.** You report medians while admitting $360\,\text{ms}$ spikes. Authorization latency is tail-sensitive; publishing a median is a vanity metric.
- **Harness topology coupling.** AP2 is “in-process” only because your benchmark harness shipped the verifier in the same binary. If AP2 is deployed as a sidecar (the realistic deployment), it gains an IPC cost you conveniently erased. You measured your harness, not the rail.
- **Interference under race.** “Raced pairwise” on a single topology with shared chain-RPC and Lightning-node endpoints creates head-of-line blocking. One rail’s measurement pollutes another’s backing-service latency.

---

## Deliverable

**Verdict: REJECT**

**Single strongest argument:**  
A ranking whose order is determined almost surely by whether a network syscall occurs—spanning a $460\times$ dynamic range within the same ordinal scale—is not a performance benchmark; it is a regime-classification tautology. The scalar latency values convey no competitive signal because the work-class dominates the variance. Disclosure does not resuscitate a broken measurement scale.
