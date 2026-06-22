# Adversarial Review: PayBench Dimension 2 — AUTHORIZATION LATENCY

---

## 1. Strongest Objections (Severity-Ranked)

### 🔴 Objection 1: L402's "Authorization" Measures Credential Minting, Not Payment Authorization (FATAL)

The L402 flow is: (1) client requests resource → (2) server returns `402` with macaroon + BOLT11 invoice → (3) **client pays the Lightning invoice** → (4) client presents `macaroon:preimage` → (5) server verifies and grants access. The benchmark pins authorization at step (2) — macaroon/invoice issuance. 

But step (2) is a **capability grant**: the server is saying "here is a token that will become valid IF you pay this invoice." No payment has been authorized, committed, or validated. Payment happens at step (3), and validation of payment happens at step (5). The macaroon is semantically equivalent to x402's payment-requirements response (the `402` with `WWW-Authenticate: Payment`), NOT to x402's `/verify` response.

The x402 `/verify` validates a **completed, signed payment authorization** from the payer (EIP-3009 `TransferWithAuthorization`). The payer has already cryptographically committed funds. L402's macaroon issuance validates nothing — it *creates* something for the payer to fulfill.

**Why fatal:** The dimension claims to measure "authorization to proceed toward settlement." For L402, the measured point is *before any payment commitment exists*. The ranking will systematically advantage L402 (macaroon generation is local crypto + optional Lightning node invoice creation) over rails that actually validate payment commitments. A naive reader will conclude "L402 authorizes payments fastest" when L402 hasn't authorized a payment at all — it has merely issued a challenge. No amount of trust-class labeling can fix a measurement of the wrong thing.

**This is a category error, not a comparison-methodology error.**

---

### 🔴 Objection 2: MPP-on-Tempo Cannot Be Validly Measured on This Dimension (FATAL)

The MPP-on-Tempo rail has two intents with irreconcilable measurement problems:

- **"Charge" intent:** The docs explicitly fuse verify+settle into one ~500ms step. There is **no separable authorization signal**. Measuring this conflates Dimensions 1 and 2, violating the dimension's foundational premise (authorization ≠ settlement). Any latency number includes on-chain broadcast and confirmation time.

- **"Session" intent:** Off-chain voucher verification in "near-zero time." This is structurally the fastest path by orders of magnitude, but it reflects a session-resumption optimization, not a payment authorization. Vouchers are pre-established credentials, not per-payment validations.

The benchmark faces an impossible trilemma:
- Measure "Charge" → includes settlement, violates D1/D2 separation
- Measure "Session" → measures credential reuse, not payment authorization
- Measure both and aggregate → meaningless composite of incommensurable operations

**Why fatal:** A rail included in the benchmark has no valid measurement point. Either the measurement is contaminated (Charge) or unrepresentative (Session). This isn't a methodological caveat — it's an absence of a measurable quantity matching the dimension's definition. The rail must either be excluded from this dimension or the dimension must be redefined to accommodate fused verify+settle paths (which would collapse D1 and D2).

---

### 🟠 Objection 3: Fast-Path Bias — Authorization Latency Ranking May Invert Agent-Experienced Latency (HIGH, SURVIVABLE)

Consider the agent's actual experience — "time from deciding to pay to receiving the resource":

| Rail | Authorization | Settlement/Gap | Total Agent Wait |
|------|--------------|----------------|-------------------|
| x402 `/verify` | 50ms | 2,000ms (on-chain `/settle`) | **2,050ms** |
| L402 macaroon grant | 100ms | 500ms (Lightning payment) | **600ms** |
| MPP Tempo Charge | ~500ms (fused) | 0ms (already done) | **500ms** |

The benchmark ranks authorization latency as: **x402 (50ms) > L402 (100ms) > Tempo Charge (500ms)**. But the agent experiences: **Tempo Charge (500ms) > L402 (600ms) > x402 (2,050ms)** — a complete inversion.

The benchmark records accept→finalized gap as a "separate published quantity," but the headline ranking is on authorization only. If the gap is merely *published* rather than *incorporated into the primary ranking*, the benchmark is optimizing a component metric that is inversely correlated with the outcome agents actually care about.

**Why survivable:** Add a co-primary ranking of total agent-experienced latency (authorization + settlement gap) and require both rankings to be displayed together. The ISO-8583 precedent (MTI 0100/0110 vs. 0200/0220) is fine for internal network operations but cardholders care about "time to approval on terminal," not the internal split. The benchmark should report what the agent *experiences*, not just what the rail *does internally*.

---

### 🟠 Objection 4: Google AP2's Authorization Checkpoint Includes External Dispatch — an Architectural-Scope Contaminant (HIGH, SURVIVABLE)

AP2's authorization checkpoint is: "mandate verification → payment-credential issuance → **dispatch to the merchant/processor**." The dispatch step is an external network call to the Merchant Payment Processor (MPP in AP2 parlance, distinct from "MPP-on-Tempo"). This is a fundamentally different scope from:

- x402 `/verify`: self-contained facilitator call (signature check + balance query to local/RPC state)
- L402 macaroon: server-side credential generation (possibly with Lightning node RPC for invoice)
- MPP-on-Tempo Verify: server-side transaction validation

AP2's measurement includes a party-to-party network hop that the other rails' authorization points do not. This is like measuring one car's 0-60 time on a closed track and another's on public roads with traffic lights. The trust/equivalence class label doesn't control for this — it names the difference but doesn't adjust for it.

**Why survivable:** Decompose AP2's authorization into sub-metrics (mandate-verification latency, credential-issuance latency, dispatch latency) and race the comparable sub-component. Alternatively, control for the dispatch hop by measuring dispatch latency independently and subtracting it for the cross-rail comparison. Without decomposition, AP2's numbers are not comparable to single-operation checkpoints.

---

### 🟡 Objection 5: "Payment Intent Presented" Has No Cross-Rail Definition — Clock-Start Ambiguity (MEDIUM, SURVIVABLE)

The dimension defines latency as "from a payment intent being presented to a rail." But:

- **x402:** Is the clock start when the resource server calls the facilitator's `/verify`? When the HTTP request hits the facilitator's edge? When the facilitator deserializes the payload? These differ by network RTT (facilitator colocation vs. remote).
- **L402:** Is it when the client's HTTP request hits the server triggering the 402? When the server begins macaroon minting? When the server begins invoice generation? These are server-internal events — if measured server-side, network latency from client is excluded; if measured client-side, network latency is included.
- **AP2:** Is it when the Shopping Agent presents the Payment Mandate to the Credential Provider? When the mandate enters the verification pipeline? AP2 has multiple actors — which one's clock?

If x402 is instrumented server-side (facilitator-internal timer) but L402 is instrumented client-side (agent measures round-trip to 402 response), L402 is penalized by network latency that x402 avoids. A 50ms difference in ranking could be entirely a measurement artifact.

**Why survivable:** Define a strict instrumentation standard: all checkpoints MUST be measured at the rail's edge (the first HTTP ingress point). Publish a clock-synchronization protocol (NTP, PTP, or cloud-provider clock bounds). Include a "measurement tax" sensitivity analysis showing that network RTT from the standard measurement point to the actual processing point is <5% of measured latency for all rails.

---

## 2. New High-Severity Flaw (Not in G1–G7)

### 🔴 NEW: The L402 Authorization Point Is a Non-Payment Event — It's the HTTP 402 Challenge Itself

This is related to Objection 1 but distinct in its mechanism. The L402 spec is explicit: the `402` response with macaroon + invoice is called a **"challenge."** The authorization happens when the client presents the completed `L402 <macaroon>:<preimage>` credential on a subsequent request, and the server verifies it. The L402 spec's own terminology distinguishes:

- **Challenge issuance** (what the benchmark measures): server generates macaroon, mints BOLT11 invoice, returns `402` — this is *asking* for payment, not *authorizing* it.
- **Credential verification** (what happens after payment): server checks `SHA256(preimage) == hash` and validates the macaroon HMAC chain — this is *validating* that payment occurred.

By the benchmark's own ISO-8583 analogy: the macaroon+invoice issuance is the equivalent of the terminal displaying "Amount: $5.00 — Insert Card" (pre-authorization prompt), NOT the equivalent of MTI 0110 "Authorization Response — Approved." The benchmark has mistaken the challenge for the authorization.

**Why this matters:** This isn't just a "different security object" (G2) — it's a measurement taken at the wrong step in the protocol, before the event being measured has occurred. It's like measuring "settlement finality" at the point the transaction is submitted to the mempool rather than when it's confirmed.

---

## 3. Adjudication of DA1 and DA2

### DA1: (a) KEEP — with mandatory supplementation

**Vote: (a) KEEP, conditioned on adding an agent-observable latency co-primary metric.**

The CLIENT-ONLY option would eliminate x402 (standard deployments don't expose `/verify` results to the agent pre-settlement), L402 (the macaroon isn't a pre-settle accept; it's a pre-payment challenge), and possibly AP2 (mandate verification results may not be surfaced to the agent before dispatch). This collapses the benchmark to MPP-on-Tempo Session — a sample size of one. The x402 spec *does* define `/verify` as a separately callable endpoint, and the doctrine mandates calling it explicitly; this is a valid component-level measurement. However, the fused-topology caveat must be upgraded from a footnote to a **mandatory stratification variable**: deployments must be classified as "separated-verify" (agent can observe `/verify` result) vs. "fused" (agent sees only final settled response), and results must be reported separately. Additionally, the benchmark MUST co-report agent-observable latency (time from agent payment intent to agent receiving the resource or a pre-settle signal) alongside the internal authorization latency, so that the gap is not merely "published separately" but is visually and statistically integrated into the primary ranking display.

---

### DA2: (c) SPLIT — with a path to eventual convergence

**Vote: (c) SPLIT, with a recommendation to work toward REPIN-R11 semantics across all rails in a future revision.**

The KEEP option fails because the "per-rail-canonical" doctrine that worked for Dimension 1 (finality) does not transfer to Dimension 2 (authorization). Finality is a well-defined concept with a shared meaning across all payment rails — the point after which a payment is irreversible. Every rail has such a point, even if achieved differently. Authorization, by contrast, does not have a shared meaning across these six rails: for x402 it's post-commitment validation (`/verify`), for L402 it's pre-commitment challenge issuance (macaroon), for AP2 it's a multi-step pipeline ending in dispatch. These are not different mechanisms achieving the same concept — they are different concepts. REPIN-R11 fails because moving L402 to the "payment-accepted" signal (credential verification) puts authorization *after* Lightning settlement, inverting the temporal relationship this dimension exists to measure (authorization → settlement). L402's architecture genuinely lacks a pre-settlement authorization point — payment IS the authorization. SPLIT acknowledges this structural reality: grant-type rails (L402) measure how fast a payment challenge is issued; verify-type rails (x402, MPP, AP2) measure how fast a payment commitment is validated. These are two distinct benchmarks that should not be merged. The trust/equivalence classes should be elevated from labels to the primary grouping structure. If a future protocol revision adds a pre-payment validation step to L402 (e.g., a balance-probe or pre-authorization call), it could join the verify-type group at that time.

---

## 4. Net Verdict

**Not publishable as designed — SPLIT the ranking into grant-type and verify-type sub-benchmarks, add a co-primary agent-experienced-latency metric, exclude or stratify MPP-on-Tempo by intent, and standardize clock-start instrumentation before pre-registration.**
