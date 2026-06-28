# Dim-2 RAPL — cross-lineage scan: the work-type heterogeneity decision

**Purpose.** A focused, *confirmatory* cross-lineage adversarial scan (round 4) on ONE decision surfaced
by the Q4 validation runs: how to handle the fact that, within each sub-ranking, rails span very
different *work classes*. This is NOT a re-litigation of the A/B SPLIT (settled in rounds 1–3, verdict
4/4) — it assumes the split and asks only about within-sub-ranking heterogeneity.

Send the **prompt below** verbatim to each lineage (DeepSeek / Gemini / Kimi / Qwen); collect replies as
`dim2-worktype-{model}.md`. Looking for: does the panel confirm "one race + disclosure," propose a better
disclosure taxonomy, or make a principled case for sub-splitting? Majority-refute (≥3/4) of our
recommendation = reopen; otherwise = ratify and proceed to pre-reg.

---

## PROMPT (send verbatim)

You are an adversarial reviewer of a benchmark methodology. Challenge the proposal below; do not be
agreeable. Be concrete. End with an explicit verdict.

**Context.** We benchmark "authorization latency" (RAPL) for agentic-payment rails — the time for the
rail's authorization primitive, lower-is-better, raced pairwise. After adversarial review we SPLIT it
into two never-cross-compared sub-rankings, because they are different *kinds* of operation:
- **Sub-ranking A — Payment-Validation:** the accept of a presented payment (e.g. an x402 facilitator
  `/verify`, an AP2 mandate verify, a Tempo session voucher accept).
- **Sub-ranking B — Challenge-Issuance:** issuing the "payment-required" challenge (e.g. an HTTP 402, an
  L402 macaroon+invoice).

**The new finding (from live measurement, single topology, n≈20–30/rail).** Within EACH sub-ranking the
rails span very different *work classes*, spanning 2–3 orders of magnitude:

Sub-ranking A (medians):
- AP2 mandate verify: **1.68 ms** — pure in-process crypto (ES256), no network.
- Tempo session voucher: **~19.5 ms** warm — local crypto (EIP-712 sign + secp256k1 verify), BUT the
  server caches on-chain channel state for ~5 s; on cache expiry it does one chain-RPC read (~360 ms
  spike). So: **local crypto with an amortized/periodic backing-service hop.**
- x402 on Solana / Stellar / Base: **400 / 464 / 777 ms** — every accept is a network round-trip to a
  hosted facilitator (Base's also fans out to chain-RPC balance reads).

Sub-ranking B (medians):
- x402 (Solana/Stellar/Base) 402, and Tempo 402: **~2–3 ms** — a local template emit.
- Lightning (L402) 402: **~1252 ms** — issuance must mint a BOLT11 invoice via a Lightning-node
  round-trip.

So each sub-ranking contains: (i) pure-local-crypto members, (ii) members with an intrinsic
backing-service round-trip every call, and (in A) (iii) a member that is local-crypto with a *periodic*
backing-service refresh. The latency gap between classes (~250–800×) dwarfs the within-class spread.

**Our proposal (defend or refute).** Keep each sub-ranking as ONE race (no further split), but:
1. mandate a per-rail **"work-type" disclosure** with three buckets — {local-only, periodic/amortized
   backing-service, per-call backing-service} — published alongside every rail's number;
2. report the backing-service hop (facilitator / chain-RPC / Lightning-node / TTL-refresh) as a
   published **diagnostic**, but do NOT subtract it (it is the rail's real authorization work — minting a
   Lightning invoice genuinely costs an invoice; an x402 facilitator round-trip genuinely is the accept);
3. justification: a *rail* benchmark's entire purpose is to measure rails as deployed; normalizing away
   the backing-service cost would erase the competitive signal. (Precedent: payment-rail latency
   comparisons, ISO-8583-era onward, compare rails with very different backing infrastructure by design.)

**Questions — answer each:**
1. Is "one race + 3-bucket work-type disclosure" defensible, or does cross-class heterogeneity of this
   magnitude make a single pairwise ranking misleading enough to require sub-splitting by work-class?
2. If you'd sub-split: on what boundary exactly, and how do you avoid an infinite regress of ever-finer
   classes? If you'd NOT split: is the 3-bucket disclosure the right instrument, or is there a better one
   (e.g. report a "local-compute floor" + a separate "backing-service" component per rail)?
3. Is "disclose the backing-service hop but never subtract it" correct, or are there cases where
   subtracting/normalizing is the only fair comparison? Name them.
4. Does the Tempo "periodic/amortized" class (local + ~5 s TTL refresh) actually warrant its own bucket,
   or is it a measurement artifact of one server's caching choice that we should hold constant or disclose
   differently?
5. Anything we're missing that would embarrass this methodology at publication?

**Deliverable:** a verdict on our proposal (RATIFY / RATIFY-WITH-CHANGES / REJECT), the single strongest
argument against it, and — if RATIFY-WITH-CHANGES — the minimal change you'd require.

---

## Our prior (for synthesis, not part of the prompt)

We expect RATIFY or RATIFY-WITH-CHANGES. The strongest anticipated challenge: "a pairwise race implies
fungibility; if AP2 (1.68 ms) and Base (777 ms) are both 'A', a reader will conclude AP2's *authorization*
is 460× faster when really they're doing categorically different work." Our answer: that IS true and is
the point — but the work-type bucket must sit in the *same visual field* as the number so the reader
can't read the rank without the class. If the panel's minimal required change is "rank WITHIN work-class,
report ACROSS as a labelled scatter, not a single pairwise order," that is an acceptable refinement and
arguably strengthens the result — flag it for founder ratification. Cross-reference: pilot data in
`dim2-q4-pilot-log.md` (R1/R2/R6/R9/R10/R10b/R11), decision context in `dim2-q4-runbook.md` §2.5.
