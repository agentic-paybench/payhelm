# Adversarial Review: PayBench Dimension 2 — Authorization Latency

## §1 Objections, Severity-Ranked

### 🔴 OBJ-1 — L402's Macaroon Is a Payment *Request*, Not an Authorization (FATAL as-designed)

**Severity: Critical · Fatal for L402's inclusion at the current pin-point**

In every other rail, "authorization" is a **validation of the payer's intent/credentials** (x402 `/verify` checks signature + funds; MPP `Verify` checks the payment credential; AP2 checks the mandate). In L402, the macaroon + BOLT11 invoice is issued by the **payee** *before the payer has signed, committed, or transmitted anything*. This is, in ISO-8583 terms, the *merchant's MTI 0100 authorization request* — not the issuer's MTI 0110 authorization response.

In Lightning semantics the nearest analog to "authorization granted" is the HTLC lock (payer-side commitment) or, at the very latest, the payee's `update_fulfill_htlc` — but the doctrine pins **earlier** (macaroon grant). Racing L402's macaroon against x402's `/verify` is therefore racing *invoice-generation time* against *payment-validation time*. That is roughly equivalent to comparing "how fast a Shopify store renders a checkout page" to "how fast Visa approves a card swipe."

- **Why fatal:** the trust/equivalence-class label does not cure this — it *names* the asymmetry but does not remove it. Readers, agent-developers, and downstream model-card consumers will interpret the published ranking as "who authorizes fastest," not "whose invoice-printer is quickest."
- **Survivable only via** DA2 option **(b) REPIN-R11** or **(c) SPLIT**.

---

### 🟠 OBJ-2 — AP2 Is an Authorization-Only Layer; Full-Stack Rails Are Doing Strictly More Work (HIGH, survivable)

**Severity: High · Survivable with prominent disclosure**

AP2 performs mandate verification and credential issuance. It **does not** (a) validate an on-chain signature, (b) check UTXO/balance state, (c) route a Lightning payment, or (d) talk to a facilitator. Full-stack rails perform (a) + one or more of (b)–(d) inside their authorization window. Racing a dedicated auth microservice against a monorail that does auth + funds-check is structurally asymmetric — like timing a bouncer's ID check against a TSA line that includes ID + luggage scan + body scan.

- **Survivable** if (i) the trust/equivalence class is renamed from e.g. `"mandate-only"` → `"auth-only (no funds-check)"` so the asymmetry is load-bearing in the label itself, and (ii) AP2's ranking is footnoted with the work-quantum difference. Do **not** present AP2 at the top of a unified leaderboard without this.

---

### 🟠 OBJ-3 — MPP-on-Tempo Charge-vs-Session Is a 500× Degree of Freedom (HIGH, survivable iff pre-registered)

**Severity: High · Survivable only with pre-registration and bifurcated reporting**

The doctrine notes in passing that Charge fuses verify+settle into ~500 ms while Session's off-chain vouchers verify in "near-zero time." That is not a caveat — it is **the entire ranking** for MPP-on-Tempo. An MLE-Bradley-Terry model seeded with Charge intents will place Tempo last; one seeded with Session intents will place Tempo first. The choice of intent is therefore a **researcher degree of freedom with ~500× leverage**, which is exactly the kind of garden-of-forking-paths failure a pre-registered benchmark exists to prevent.

- **Survivable** iff both intents are benchmarked and reported as **two separate sub-rows** (`MPP-Tempo/Charge`, `MPP-Tempo/Session`), with the intent choice pre-registered, not chosen post-hoc.

---

### 🟡 OBJ-4 — Agent-DX Validity Gap (G1): the "Mandate an explicit /verify call" Fix Is a Measurement Artifact (MEDIUM-HIGH, survivable)

**Severity: Medium-High · Survivable with honest framing**

In fused/in-process facilitator deployments the agent sees a single `intent → settled` round-trip; the `/verify` checkpoint is an **instrumentation point the benchmark forces into existence** by requiring a two-call flow. This is defensible as a measurement of *rail-primitive latency* but is **not** a measurement of *agent-perceived authorization latency*. Calling it the latter misleads agent builders who will integrate via the fused path.

- **Survivable** iff the dimension is renamed to make this explicit — e.g. **"Rail Authorization Primitive Latency (RAPL)"** — and a companion column reports *agent-observed time-to-first-useful-signal* for each rail (which for fused x402 equals settlement time, collapsing into Dim-1).

---

### 🟡 OBJ-5 — Statistical: `pass@k` Threshold `k` Is Load-Bearing and Not Robustness-Checked (MEDIUM, survivable)

**Severity: Medium · Survivable with pre-registered `k` ladder**

`pass@k = P(auth ≤ k s)` converts a continuous latency distribution to a binomial, then Wilson-bounds it. The ranking at $k = 50\text{ ms}$ can invert the ranking at $k = 500\text{ ms}$, especially when comparing a fast-tail rail (low median, fat P99) against a steady rail (higher median, thin P99). Borrowing the `k` from Dim-1 (settlement, measured in seconds) is inappropriate for authorization, which lives in the 1–200 ms regime.

- **Survivable** iff a pre-registered ladder (e.g. $k \in \{20, 50, 100, 250, 500\}\text{ ms}$) is reported with a **rank-stability heatmap**, and the headline `k` is chosen *before* data collection.

---

## §2 New High-Severity Flaw Not in G1–G7

### 🔴 NEW-1 — Co-Location / Network-Topology Confound (HIGH, potentially fatal to reproducibility)

Wall-clock authorization latency on these rails is **dominated by network RTT** at the sub-100 ms regime the benchmark is targeting:

- x402 facilitators are HTTP endpoints whose geographic deployment is the benchmark operator's choice.
- Solana/Base/Stellar RPC endpoints vary by hundreds of ms by region.
- MPP-on-Tempo and L402 servers can be spun up anywhere.
- AP2's Google-fronted endpoints ride Anycast and will appear 10–30 ms from any PoP, systematically **advantaging AP2**.

A benchmark run from US-East yields a different B-T ranking than one from Singapore or Frankfurt. Without (a) specifying a **single canonical client geography** co-located with each rail's declared endpoint, (b) publishing the RTT floor per rail, and (c) reporting a **network-adjusted** latency (`observed – min-RTT-to-endpoint`) alongside raw, the leaderboard is **not reproducible across runs** — which is the cardinal sin of a pre-registered benchmark.

**Additional minor new flaw (NEW-2):** warm-vs-cold-start confound (TLS handshake + connection pool on first call adds 30–150 ms). Must pre-register whether runs are warm-start-only (discarding first $N$ calls) or cold-start-inclusive, and report both.

---

## §3 Adjudication of DA1 and DA2

### DA1 — KEEP the `/verify` primitive (option **a**) ✅

Vote: **(a) KEEP.** The `/verify` endpoint is specified in x402 as independently callable, and the doctrine's requirement to call it explicitly plus disclose the fused-topology caveat is the correct epistemic move. Option (b) CLIENT-ONLY would exclude the most widely-deployed facilitator topology and silently privilege rails whose specs happen to surface an auth signal to the client — that is a spec-cosmetic property, not a substantive one. The price of (a) is honest framing: rename the dimension so "primitive latency" is in the title (OBJ-4), and publish the fused-path agent-observed number as a companion column. That's a documentation fix, not a methodology retreat.

### DA2 — SPLIT grant-type vs. verify-type (option **c**) ✅

Vote: **(c) SPLIT.** Option (a) KEEP is untenable because of OBJ-1: L402's macaroon is a categorically different security event from the other five rails' authorization points, and slapping a `"grant-type"` equivalence label on it does not make the B-T pairwise race meaningful — B-T assumes items are comparable along a single latent quality axis, which they are not here. Option (b) REPIN-R11 is attractive in principle but **there is no clean later authorization signal in Lightning** between macaroon issuance and preimage revelation; the HTLC is payer-side and the `update_fulfill_htlc` is settlement, so repinning either collapses into Dim-1 or forces an invented checkpoint. Option (c) SPLIT is the clean answer: two sub-rankings — **(i) Payment-Validation Authorization** (x402×3, MPP-Tempo, AP2) and **(ii) Permission-Grant Authorization** (L402) — with a one-line legend explaining the split. This preserves coverage of all six rails, makes the B-T transitivity assumption true *within* each sub-ranking, and gives downstream consumers a ranking they can act on.

---

## §4 One-Line Net Verdict

> **Publishable/pre-registerable with three mandatory changes: split L402 into its own "grant-type" sub-ranking (DA2-c); pre-register and bifurcate MPP-Tempo into Charge and Session sub-rows; and fix a canonical client geography with published RTT floors and network-adjusted latencies — after which the dimension is sound, modulo a rename to "Rail Authorization *Primitive* Latency" to cure the Agent-DX framing gap.**
