# Dim-2 RAPL — work-type scan (round 4): synthesis

Cross-lineage scan of the work-type heterogeneity decision (prompt: `dim2-worktype-scan.md`; replies:
`dim2-worktype-{deepseek,gemini,kimi,qwen}.md`, 2026-06-24). **Outcome: our proposal was refuted 4/4 —
REVISE the doctrine.** This is a course-correction, not a confirmation. It does NOT reopen the A/B SPLIT
(rounds 1–3, 4/4) and does NOT invalidate any rail harness or pilot number — it changes the **reporting +
analysis layer (§2.5)** only.

## Verdict tally
- **REJECT:** Gemini, Kimi. **RATIFY-WITH-CHANGES:** DeepSeek, Qwen.
- But all four refute the *specific* proposal ("one race + scalar 3-bucket disclosure + median-only +
  never-subtract"). Effective gate (≥3/4) → **reopen + revise.**

## What all four AGREE on (the mandate — implement these)
1. **Median-only is indefensible.** Report **P50 / P95 / P99 + N + timestamp + topology** per rail.
   Authorization latency is tail-sensitive; a P50=3 ms / P99=2000 ms rail is worse than P50=5 ms /
   P99=8 ms, and the median hides it. (All 4; Qwen: "skip this and you should not publish at all.")
2. **Report a per-rail DECOMPOSITION**, not a scalar class label: a local-compute floor **and** the
   backing-service component (DeepSeek `local_compute_ms`; Kimi tuple `(t_local, t_io, ρ_io)`; Qwen
   `(E2E, backing-service-only)`; Gemini processing-delta). Headline = E2E (what the operator feels);
   decomposition = the science (serves the protocol-designer audience). (All 4.)
3. **Tempo's "periodic/amortized" is NOT a rail class** — it's the reference impl's 5 s TTL config. Kill
   the third bucket. Report **warm (L_hot) vs cold (L_cold)** explicitly with the arrival distribution /
   TTL disclosed; or a TTL sweep {0, 5 s, 60 s, ∞}; or a cache-disabled protocol-baseline (min required
   backing hops/call). Never publish ref-impl TTL as a rail property (gaming-prone: set TTL=∞ → looks
   local). (All 4.)
4. **Single topology is fatal for network-bound rails** — the 400/464/777 ms are functions of where we
   measured. **≥2 topologies mandatory** (this is our FR4 — reinforced from "nice to have" to required;
   the local rails being topology-invariant is itself the control). (All 4.)

Also raised (incorporate as scope/disclosure): n≈20–30 underpowered for WAN tails (DeepSeek/Kimi/Qwen);
**workload realism** held constant — macaroon caveat count (L402 verify is superlinear in caveats),
voucher/header/payload size (Qwen/Kimi); **AP2 "in-process" is harness coupling** — a sidecar deployment
would add IPC, so disclose the deployment assumption (Kimi); concurrency/throughput out of scope but name
it (Gemini); race interference on shared RPC/LN endpoints → head-of-line blocking (Kimi).

## The one UNRESOLVED axis — split vs. decompose
- **Split into two leaderboards** by intrinsic network-dependency (does the *protocol spec* require ≥1
  network round-trip per call? yes/no): DeepSeek, Gemini, Kimi (3/4).
- **Don't split** — it makes each group an n=1/n=2 "shopping list"; instead one table + the richer
  decomposed tuple: Qwen (1/4).

**These converge more than they look.** Both camps reject the same thing: *a single cross-class ordinal
as the headline*. Reconciliation (recommended): **group rails by work-class** (Local-complete vs
Network-dependent), **rank within group**, and present **across** groups as a labelled, decomposed
comparison — never a single pairwise order. Qwen's n=1/n=2 objection is real but is answered by the
decomposition tuple carrying the cross-group story (you don't "race" across the line, you compare the
components). So: **adopt the grouping AND the decomposition** — that satisfies all four.

**Subtraction reconciled:** don't subtract from the E2E headline (DeepSeek/Qwen), but DO publish the
decomposed local-floor + backing-component, which is exactly the protocol-design view Gemini/Kimi demand
(they want the *processing delta* available, not necessarily as the headline). Net: report both; the
subtracted/normalized number is the secondary "protocol-design" view, E2E stays the headline.

## How much of this we ALREADY have (reassuring — mostly an analysis-layer change)
- **Tail stats:** the harnesses already record **raw per-trial samples** and the summary already prints
  **p95/p99** — P50/P95/P99 reporting is a formatting change, not re-instrumentation. ✅
- **Decomposition:** the **min-RTT floor** + the "report backing-service hop as a diagnostic" clause are
  the start of the local-floor/backing-component split — needs formalizing into the per-rail tuple. ◑
- **Tempo warm/cold:** the pilot log (R10b) **already** recorded both modes (19.5 ms warm; 359 ms TTL
  tick) and flagged the TTL caveat — the panel confirms the instinct; we just stop calling it a bucket. ✅
- **Keep-alive / TLS-handshake concern (Kimi/Gemini):** the **B1 fix** already asserts socket pooling
  (diagnostics_channel), so the timed window is not paying per-call handshakes. ✅
- **≥2 topology:** already the FR4 plan (Codespaces → named-region OCI). ✅

## Recommendation (founder ratification — NOT autonomous)
Revise §2.5 to:
1. report **P50/P95/P99 + N + timestamp + topology** (drop median-only);
2. report a **per-rail decomposition** `(local_compute_floor, backing_service_component, E2E)` — E2E
   headline, decomposition as the protocol-design view;
3. **group by work-class** (Local-complete / Network-dependent), rank within, compare across via the
   decomposition — no single cross-class ordinal;
4. treat **Tempo's TTL as ref-impl config**: report L_hot/L_cold + arrival distribution (or a TTL sweep);
   delete the "periodic/amortized" bucket;
5. make **≥2 topologies mandatory** for network-bound rails (FR4);
6. disclose **workload constants** (macaroon caveats, payload sizes) and the **AP2 in-process/sidecar**
   deployment assumption; note concurrency/throughput as out-of-scope.

This is a bounded revision (reporting + grouping + Tempo framing), not a redesign — the SPLIT, the rails,
and the pilot numbers stand. **Founder decision needed on the one open axis:** confirm "group-and-
decompose" (recommended) vs DeepSeek/Gemini/Kimi's harder "two separate leaderboards." Logged as **round-4
/ decision DR4** pending ratification; do not finalize §2.5 until ratified.
