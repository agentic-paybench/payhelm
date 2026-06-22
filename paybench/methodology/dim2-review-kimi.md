### 1. Severity-Ranked Objections

**Rank 1 — FATAL: The Authorization Homonym Fallacy (Construct Validity Collapse)**  
The six measured “accept” checkpoints are ontologically distinct events masquerading under one label. `L402` issues a **grant-to-access** (macaroon + invoice), `x402` performs a **readiness verification** (`/verify` of signature/funds), `MPP-on-Tempo` executes a **credential pre-check**, and `AP2` runs a **mandate verification** that explicitly outsources settlement. None of these are ISO 8583-style authorizations (transaction-specific fund reservation / risk acceptance). The `trust / equivalence class` wrapper is a cosmetic label; the benchmark headline will inevitably be consumed as a unified speed ranking, making this a category error dressed in neutral methodology. A single Bradley–Terry ranking across these events is like ranking “time to boarding-pass scan” against “time to pushback clearance” under the heading “time to departure approval.”

**Rank 2 — FATAL: Deferred-Workload Asymmetric Bias (The Empty-Promise Problem)**  
The computational and economic depth of the measured checkpoint varies by orders of magnitude across rails. `AP2` is fast *because* it deliberately does not settle; `L402` is fast *because* liquidity probing, route discovery, and HTLC resolution are deferred to the post-macaroon phase; `x402`’s `/verify` defers inclusion/finality to the subsequent on-chain `settle`. A rail can therefore “win” on this dimension simply by doing less work at the measured boundary. The benchmark provides no covariate for “assurance depth” or “settlement success probability conditional on accept,” rendering the lower-is-better ranking economically hollow and gameable.

**Rank 3 — SURVIVABLE: Bradley–Terry & Pass@$k$ Statistical Misspecification**  
Pairwise racing with Bradley–Terry MLE assumes a single latent trait $\theta_j$ explains all pairwise outcomes. This is violated by mechanistically heterogeneous generative processes: `L402` macaroon generation is local compute with near-zero variance, `x402-on-Solana` involves RPC to a consensus network with multimodal, congestion-dependent tails, and `AP2` depends on mandate-database latency. A single $\theta_j$ is formally estimable but substantively uninterpretable. Additionally, fixing one pass@$k$ threshold $P(T \le k)$ is arbitrarily favorable to one variance regime; a single $k$ cannot fairly represent sub-second local operations and multi-second networked ones simultaneously. Replace or augment BT with per-rail survival curves (Kaplan–Meier).

**Rank 4 — SURVIVABLE: Instrumented-Facilitator Fiction (G1, Elevated)**  
Mandating an explicit `x402` `/verify` call when production facilitators fuse `verify` and `settle` into one black-box response means the benchmark measures a **protocol-instrumentation artifact**, not an agent-observed reality. If the typical A2A agent never encounters the standalone accept signal, the recorded latency is a fiction induced by the benchmark’s own probing doctrine. External validity is compromised unless the metric is reframed as “protocol-primitive latency” rather than “agent-experienced latency.”

---

### 2. New High-Severity Flaw (Not in G1–G2)

**Predictive Nullity — Unnormed Assurance.**  
The benchmark treats every “accept” checkpoint as an informationally equivalent green light, yet the signals differ wildly in their predictive value for eventual settlement. A L402 macaroon says nothing about whether a later Lightning route will actually find liquidity; an `x402` `/verify` does not guarantee the transaction will be included in the next block; an AP2 mandate check does not imply the acquirer will honor the transaction. Without normalizing for $P(\text{settled} \mid \text{accept})$ — or at least bounding it by rail — the latency comparison is decoupled from the economic question agents actually care about: *how fast until the payment is reliably in flight?* A near-instant signal that frequently fails downstream is not comparable to a slower signal with downstream certainty.

---

### 3. Adjudication

**DA1 — (a) KEEP**  
Keep the verify-primitive definition, but stop pretending it is a uniform client-percept. CLIENT-ONLY would let sloppy, fused deployments dictate the measurement frontier, punishing rails that correctly expose separable pre-settlement primitives and conflating “what agents currently see” with “what the protocol affords.” Since `x402` natively specifies `/verify` and MPP natively separates `Verify` from `Settle`, mandating the explicit call is defensible as a standardized probe of architectural separability. However, this only survives if the dimension is immediately **rebranded** from “Authorization Latency” to **“Protocol-Accept Latency”** and the fused-topology caveat is promoted from a footnote to a structural external-validity warning. Measuring an instrumented facilitator checkpoint while calling it agent experience is fraud; measuring it while honestly labeling it as a protocol-internal accept boundary is sound engineering.

**DA2 — (c) SPLIT**  
Split the leaderboard into ontological sub-rankings. REPIN-R11 is operationally ill-defined for `L402`: there is no stable, rail-canonical “payment-accepted” signal between macaroon grant and preimage settlement that does not collapse into Dimension 1, so forcing semantic alignment would either make `L402` unmeasurable or arbitrarily invent a checkpoint the protocol does not expose. KEEP (a) is reckless aggregation that papers over the grant-versus-verify-versus-mandate chasm with a trust-class label that leaderboard consumers will ignore; the Bradley–Terry output will implicitly treat a macaroon and an on-chain `/verify` as differing only in degree, not in kind. SPLIT respects the heterogeneity: report **grant-to-pay** (`L402`), **verify-to-pay** (`x402` variants, `MPP`), and **mandate** (`AP2`) as separate sub-rankings. Preserves all data, prevents false ordinality, and honors the trust/equivalence classes structurally rather than cosmetically.

---

### 4. One-Line Verdict

The dimension is pre-registerable subject to three minimal changes—**rename to “Protocol-Accept Latency,” SPLIT into ontological sub-rankings (grant / verify / mandate), and drop the cross-rail Bradley–Terry aggregate**—or it must be rejected for fatal construct equivocation and the empty-promise problem.
