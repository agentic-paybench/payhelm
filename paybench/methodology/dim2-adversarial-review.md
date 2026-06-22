# Dimension-2 (authorization latency) — adversarial review (DRAFT, pre-ratification)

**Gate:** dim-2 doctrine drafted (`dim2-auth-latency.DRAFT.md` §2, evidence-grounded by
`dim2-auth-latency.research.md`) → **cross-lineage adversarial review** → founder ratification
→ (separately) pre-registration. This is the §8 gate the DRAFT names; it mirrors the dimension-1
`pre-reg-adversarial-review.md` ceremony (whose cross-LLM round upheld the finality doctrine **3–1**).

**Purpose.** Surface every flank a hostile reviewer (CRFM maintainer, statistician, payments
expert, competitor) would attack *before* the auth-latency doctrine is ratified or anchored.
Publishing one's own adversarial pass strengthens the eventual pre-registration. This is an internal
review artefact, **not** part of any pre-registered method; nothing here is ratified.

> **Scope reminder (tripwires).** All calibration is PLACEHOLDER; nothing is pre-registered; the
> per-rail doctrine is drafted, not finalised. This review is the input that lets the founder
> ratify it (or redirect) with eyes open.

---

## Self-pass — findings, severity-ranked

| # | Finding | Severity | Status |
|---|---|---|---|
| G1 | **Accept is facilitator-internal, not client-perceived** in fused/in-process topologies — is a server-side checkpoint a valid *agent-DX* latency? | **HIGH** | Defended (x402 spec exposes a separate `/verify`; mandate calling it, C2); **founder decision DA1** |
| G2 | **Heterogeneous authorization objects raced together** — L402 *grant-to-pay* (macaroon) vs x402 *verify-of-payer* vs AP2 *mandate-verify* are different moments in different flows | **HIGH** | Named in §2.3 with trust/equivalence class; **founder decision DA2** (the D1-analogue) |
| G3 | **R10 Tempo *Charge* fuses verify+settle** (~500 ms) — the per-payment accept may not be cleanly separable from settlement | MED | MPP spec mandates a separate Verify procedure; accept is instrumentable; Session path cleanly separable |
| G4 | **Construct validity / terminology** — no rail publishes a metric named "authorization latency"; it is PayBench's framing over each rail's verify/grant primitive | MED | Disclosed (§2.4); ISO-8583 auth-vs-settlement is conceptual precedent |
| G5 | **Novelty claim risk** — prior-art search was partly truncated (session limit); a missed precedent would undercut a novelty claim | MED | Re-run prior-art before any *published* novelty claim; cite card-network precedent, not a benchmark |
| G6 | **Log-normal family imposed** on authorization distributions (could be bimodal: verify-hit vs cache/cold-path) | LOW | Disclosed default, as in dim-1 F5; mock fixtures only |
| G7 | **Three-checkpoint model adds recording complexity** (accept / intermediate / finalized) — risk of mislabelling which checkpoint is raced | LOW | §2.2 pins "race the accept"; the accept→finalized gap is recorded, not raced |

---

## G1 — accept is facilitator-internal (HIGH) — **needs founder decision DA1**

**The attack.** "Your 'authorization latency' is the facilitator's internal `/verify` completion —
a server-side event. A real agent transacting against a third-party facilitator never receives an
'authorized' signal before the post-settle 200; it only sees the final response. So you are
benchmarking an instrumented infrastructure-internal step, not the latency the *agent* perceives.
That is not an agent-DX measurement."

**Why it is not fatal, and the resolution taken.** The x402 specification defines `/verify` as a
**real, separately-callable facilitator endpoint** returning a discrete client-observable accept
(`{"isValid":true,"payer":…}`, no tx hash) — it is *architecturally* a client-visible checkpoint,
not merely an internal one. The doctrine (C2) therefore **mandates invoking the verify primitive
explicitly** rather than relying on a fused 200. Where a rail exposes verify as a separate call, the
accept is genuinely client-observable.

**The residual risk.** In the POC's *fused/in-process* facilitator topologies, verify and settle are
bundled and the accept is not separately emitted to the client. So cross-rail comparability depends
on each rail's deployment exposing the verify primitive — a real measurement-validity question, not
fully closed by the spec. This is the dimension's most exposed flank.

### Decision DA1 (founder)
- **DA1-keep (recommended):** define authorization at the verify primitive and **mandate calling it
  explicitly**; disclose that on fused topologies it is an instrumented (not natively client-emitted)
  checkpoint. Defensible; names its own flank.
- **DA1-client-only:** restrict the dimension to rails/topologies that *natively emit* a pre-settle
  accept to the client. Purer agent-DX, but narrows rail coverage and may exclude fused deployments.

---

## G2 — heterogeneous authorization objects (HIGH) — **needs founder decision DA2** (the D1-analogue)

**The attack.** "You race three different things and call them one dimension: L402's **macaroon
issuance** is the *server granting* the client permission to pay (earliest in the flow); x402's
`/verify` is the *facilitator validating the payer's submitted* payment; AP2's is a *mandate
verification* by a dedicated authorization layer. These are different moments in different flows with
different security objects. The ranking is an artefact of which moment you picked per rail —
apples-to-oranges, exactly the equi-conservatism critique that hit dimension-1's finality
thresholds."

**Why it is not fatal, and the resolution taken.** Rails genuinely do not share one authorization
model, so *some* per-rail definition is unavoidable (identical to the dim-1 finality situation).
§2 pins each rail to its **ecosystem-canonical authorization point** and carries a **trust /
equivalence-class column** that *names* the asymmetry (validation-of-payer vs grant-to-payer vs
mandate-verify) rather than hiding it — the same per-rail-canonical doctrine the founder adopted for
finality (D1-keep). The comparison is wall-clock-to-authorized, not security-model-to-security-model,
and the doc says so.

**The residual risk.** "Per-rail-canonical" is a *judgment* doctrine. A reviewer can still say
racing a server-issued grant (L402) against a payer-credential validation (x402) is not
apples-to-apples no matter how it is labelled — and L402's grant being *structurally earlier* than
the others is a sharper version of the dim-1 asymmetry. This is the doctrine's D1-analogue.

### Decision DA2 (founder)
- **DA2-keep (recommended):** adopt the per-rail-canonical authorization-point doctrine as written in
  §2 (consistent with finality D1-keep); name the asymmetry via the trust/equivalence-class column.
- **DA2-repin-R11:** re-pin L402/Spark away from the macaroon *grant* to a later "payment-accepted"
  signal (e.g. preimage-revealed / Spark conditional-lock release) so every rail's point is a
  *validation of payment*, not a *grant to pay* — more apples-to-apples, but moves R11's number and
  arguably mislabels L402's actual authorization step.
- **DA2-split-dimension:** report grant-type and verify-type rails as separate sub-rankings rather
  than one race. Most conservative; weakest as a single headline.

---

## G3 — R10 Tempo Charge fuses verify+settle (MED)
**Attack.** "R10's per-payment (Charge) authorization number is really its ~500 ms settlement
number — the docs fuse verify+settle." **Defence.** The MPP core spec (draft-httpauth-payment-00)
*mandates* a Verify procedure separate from Settle (verify-before-broadcast); the accept is
instrumentable server-side even where not separately *published*, and the Session path is cleanly
separable (near-zero voucher verify). **Residual/disclosure.** For the Charge path the accept
timestamp depends on instrumenting the server's verify step; disclose that R10-Charge's accept is
instrumented, not natively emitted (same class as G1).

## G4 — construct validity / terminology (MED)
**Attack.** "You invented a metric and mapped heterogeneous primitives (`/verify`, mandate-verify,
macaroon-issuance) onto it." **Defence.** The separability of authorization from settlement is
*published on every rail* (the research base), and the card-network **ISO-8583** split of real-time
authorization (MTI 0100/0110) from settlement (0200/0220) is documented 50-year precedent — PayBench
ports a long-standing distinction, it does not invent one. §2.4 states openly that "authorization
latency" is PayBench's label over each rail's primitive.

## G5 — novelty claim risk (MED)
**Attack.** "Prior art exists (card-processing auth SLAs, blockchain latency benchmarks) and you
missed it." **Defence.** No prior *agentic-payment* authorization-latency benchmark surfaced across
three research passes; card networks are cited as *conceptual* precedent, not a benchmark.
**Action.** The pass-3 prior-art angle was partly truncated by a session limit — **re-run a dedicated
prior-art search before any *published* novelty claim** (already flagged in the DRAFT/research memo).

## G6 — log-normal on authorization distributions (LOW)
Disclosed default (as dim-1 F5). If founder calibration shows bimodality (verify-hit vs cold path),
flag it for review rather than paper over; the generator currently assumes `family: lognormal`.

## G7 — three-checkpoint recording complexity (LOW)
§2.2 pins **race the accept**; intermediate/finalized are *recorded*, not raced. The accept→finalized
gap is a deliberate publishable quantity, not a ranking input. Low risk if the report labels clearly.

---

## What the cross-lineage review must pressure-test
1. **DA1** (G1): is a facilitator-internal/instrumented accept a valid agent-DX latency, given the
   spec exposes a separate `/verify`? Vote keep vs client-only.
2. **DA2** (G2, the D1-analogue): is racing heterogeneous authorization objects (grant vs verify vs
   mandate-verify), each named with a trust/equivalence class, measurement-valid? Vote keep vs
   repin-R11 vs split-dimension.
3. Any **new HIGH finding** the self-pass missed.
4. Whether the **statistics reuse** (BT/pass@k/Wilson, lower-is-better) transfers cleanly to
   sub-second authorization separations, or needs adjustment (Q5).
5. Whether the **novelty framing** (G5) is defensible as written.

---

## ====== CROSS-LINEAGE PROMPT — paste verbatim to each external lineage ======

> Paste the block below to each model (mirroring the dim-1 `Pre-reg-{Deepseek,Gemini,Kimi,Qwen}`
> ceremony). It is self-contained — the model needs no repo access. Save each reply as
> `Dim2-Review-<Model>.md`; the synthesis goes in the "Cross-lineage review round" section below.

```
You are an adversarial methodology reviewer (imagine a CRFM/HELM benchmark maintainer, a
statistician, and a payments-systems expert combined). Attack the following benchmark dimension as
hard as you can; we WANT the sharpest objections. Then adjudicate two specific decisions and give a
one-line verdict.

CONTEXT. PayBench is a pre-registered measurement methodology for agent-to-agent (A2A) payment
rails. Dimension 1 (settlement-finality) is frozen. Dimension 2, under design, is "AUTHORIZATION
LATENCY": the wall-clock time from a payment intent being presented to a rail to the point the rail
issues the go-ahead that the payment is AUTHORIZED TO PROCEED toward settlement — explicitly NOT the
point of irreversible settlement (that is dimension 1). Lower-is-better; rails are raced pairwise and
scored with Bradley-Terry MLE + pass@k = P(authorization <= k s) + Wilson lower-bound CIs (reused
unchanged from dimension 1). Six rails: x402-on-Base, x402-on-Stellar, x402-on-Solana, MPP-on-Tempo,
MPP-on-Spark-Lightning (L402), and Google AP2 (an authorization/mandate layer that does not settle
independently — it debuts on this dimension).

THE DOCTRINE ("A1"), primary-source-validated for all six rails:
- x402 rails (Base/Stellar/Solana): authorization = the facilitator's off-chain /verify accept
  (validates the payer's signed payload: signature + funds), which precedes the on-chain /settle.
- MPP-on-Tempo: authorization = the server's Verify procedure (validate the payment credential
  before broadcast), which the MPP spec mandates as separate from Settle. (Caveat: for the one-time
  "Charge" intent the docs fuse verify+settle into one ~500 ms step; the "Session" intent verifies
  off-chain vouchers in near-zero time.)
- MPP-on-Spark-Lightning (L402): authorization = the server issuing the macaroon (authorization
  credential) + BOLT11 invoice in the 402 challenge — issued BEFORE the client pays; the preimage is
  the later settlement proof.
- Google AP2: authorization = mandate verification -> payment-credential issuance -> dispatch to the
  merchant/processor; AP2 does not settle (settlement is out of AP2 scope).
Each rail also carries a named "trust / equivalence class" so the comparison is explicitly
wall-clock-to-authorized, not security-model-to-security-model. Three checkpoints are recorded per
payment (accept / intermediate-settle-signal / finalized); only the ACCEPT is raced; the
accept->finalized gap is recorded as a separate published quantity. Conceptual precedent: the
card-network ISO-8583 split of real-time authorization (MTI 0100/0110) from clearing/settlement
(0200/0220). No prior benchmark measuring "authorization latency" for agentic payments was found.

KNOWN FLANKS (attack these and find others):
- G1: the accept (e.g. x402 /verify) is a FACILITATOR-INTERNAL event; in fused/in-process facilitator
  deployments a black-box agent never sees an "authorized" signal before the final settled response.
  Is an instrumented facilitator-side checkpoint a valid AGENT-DX latency? (The x402 spec does define
  /verify as a separately-callable endpoint; the doctrine mandates calling it explicitly.)
- G2: the rails' authorization points are DIFFERENT SECURITY OBJECTS at different moments — L402's
  macaroon is the server GRANTING permission to pay (earliest); x402's /verify is the facilitator
  VALIDATING the payer's payment; AP2's is a dedicated authorization layer's MANDATE verification.
  Is racing these together apples-to-apples, given each is each rail's canonical authorization point
  and is named with a trust/equivalence class? (This mirrors dimension-1's per-rail-canonical
  finality-threshold doctrine, which a 4-model panel upheld 3-1.)

DECISIONS TO ADJUDICATE (pick one option each, with reasoning):
- DA1: (a) KEEP — define authorization at the verify primitive, mandate calling it explicitly,
  disclose the fused-topology caveat; or (b) CLIENT-ONLY — restrict to rails that natively emit a
  pre-settle accept to the client.
- DA2: (a) KEEP — per-rail-canonical authorization point with named trust/equivalence classes; or
  (b) REPIN-R11 — move L402/Spark from the macaroon grant to a later "payment-accepted" signal so
  every rail's point is a validation-of-payment not a grant-to-pay; or (c) SPLIT — report
  grant-type vs verify-type rails as separate sub-rankings.

DELIVER:
1. Your strongest 3-5 objections, severity-ranked, each with whether it is fatal or survivable and why.
2. Any NEW high-severity flaw not in G1-G7 above.
3. Your vote on DA1 and DA2 with one-paragraph reasoning each.
4. A one-line net verdict: is this dimension publishable/pre-registerable as designed, with what
   minimal changes?
```

## ====== END CROSS-LINEAGE PROMPT ======

---

# Cross-lineage review round — recorded 2026-06-22

**Panel (4 lineages):** DeepSeek, Gemini, Kimi, Qwen (raw replies: `dim2-review-{deepseek,gemini,kimi,qwen}.md`).
**Headline:** a **hard** result — harder than dimension-1's 3–1 uphold. **DA2-keep is refuted 0–4**, and
the **L402 authorization pin is a unanimous FATAL category error**. The doctrine is **not
pre-registerable as drafted**; all four agree it is *salvageable* with a defined set of structural changes.

## Vote tallies
- **DA1 (facilitator-internal accept) — KEEP holds 3–1.** Keep: DeepSeek, Kimi, Qwen. Client-only: Gemini.
  *But all four — including the keepers — make it conditional on a **rename** (the dimension measures a
  rail/protocol **primitive**, not an agent-perceived latency) plus a **companion agent-observed
  metric**.* So "keep the verify-primitive definition" survives only with an honest reframe.
- **DA2 (heterogeneous authorization objects) — KEEP FAILS 0–4.** Split: DeepSeek, Kimi, Qwen.
  Repin-R11: Gemini. **Keep: none.** The per-rail-canonical doctrine that held for finality (D1)
  **does not transfer** to authorization. Decisive.

## The unanimous FATAL finding — the L402 category error (refutes the §2 R11 pin)
All four lineages, independently: L402's **macaroon + invoice issuance is the *challenge*** ("here is
what to pay" — the analogue of x402's `402` `WWW-Authenticate`), **not** an authorization of a
*submitted* payment (x402 `/verify`). In ISO-8583 terms it is the **merchant's 0100 request, not the
issuer's 0110 response**. Racing it against x402 `/verify` is *invoice-generation vs payment-validation*
— a **category error a trust-class label cannot cure** (it names the asymmetry without removing it).
And **L402 genuinely has no pre-settlement payment-validation checkpoint** (in Lightning, payment *is*
settlement), so **REPIN-R11 collapses into dimension-1** → **SPLIT is the only coherent option**.
> This directly refutes the DRAFT §2 R11 row and the §2.3 "named asymmetry cures it" defence.

## New HIGH findings the self-pass under-weighted or missed
1. **MPP-Tempo bimodality = a ~500× researcher degree of freedom** (garden-of-forking-paths). BT MLE
   converges on a spurious mean over the Charge(~500 ms)/Session(~0) mixture; Wilson CIs become
   meaningless. → **Bifurcate into `Tempo-Charge` / `Tempo-Session` pseudo-rails, pre-registered**
   (all four).
2. **`t=0` / clock-start is undefined cross-rail** — for x402 it's a signed payload on the wire; for
   L402 an empty GET that triggers the 402; for AP2 a mandate presentation. → **Standardise `t=0` to
   "the agent issues the ultimate pay command (payload constructed, on the wire)", measured at the
   rail edge** (DeepSeek, Gemini, Qwen).
3. **Network / co-location + warm-vs-cold-start confound** dominate the sub-100 ms regime; AP2's
   Google anycast endpoints get a systematic ~10–30 ms edge. → **Canonical client geography, published
   RTT floor per rail, network-adjusted latency, and warm/cold pre-registration** (Qwen NEW-1/NEW-2).
4. **Deferred-workload / "empty-promise" asymmetry** — a rail "wins" by doing *less* at the measured
   boundary (AP2 doesn't settle; L402 defers liquidity/routing; x402 defers inclusion). → **Normalise
   or bound by `P(settled | accept)` / assurance depth** (Kimi, Qwen, DeepSeek).
5. **pass@k is in the wrong regime** — borrowing finality's seconds k-grid for a 1–200 ms quantity;
   `k` is load-bearing and can invert the ranking. → **Pre-register a millisecond k-ladder
   (e.g. {20,50,100,250,500} ms) + a rank-stability heatmap; consider Kaplan-Meier survival curves
   alongside BT** (Qwen, Kimi, Gemini). *(This effectively answers Q5: the placeholder k-grid is wrong.)*
6. **Fast-path inversion** — an authorization-only ranking can *invert* agent-experienced total
   latency (a slow-auth/fast-settle rail beats a fast-auth/slow-settle rail end-to-end). → **Co-primary
   "agent-experienced total latency" metric, displayed with the auth ranking** (DeepSeek).

## Consensus mandatory changes (before ratification / pre-registration)
1. **SPLIT** into ontological sub-rankings — *payment-validation authorization* (x402×3, MPP-Tempo,
   AP2) vs *permission-grant* (L402); BT/pass@k **only within** a sub-ranking. *(DA2: 3–4.)*
2. **RENAME** to a rail/protocol **authorization-primitive** latency (candidates: "Protocol-Accept
   Latency", "Rail Authorization Primitive Latency") + a **companion agent-observed column**. *(DA1
   condition: 4/4.)*
3. **Bifurcate MPP-Tempo** Charge/Session, intent pre-registered.
4. **Standardise `t=0` + edge instrumentation + network-adjusted latency + warm/cold** policy.
5. **Move the k-grid to milliseconds** and pre-register a k-ladder + rank-stability check.
6. **Tag AP2 auth-only / non-settling** as a *load-bearing* label; consider decomposing its dispatch hop.

## Net verdict
**Not pre-registerable as drafted.** Unanimous that the dimension is *salvageable* but needs the
structural changes above — most fundamentally the **SPLIT** (DA2-keep refuted 0–4) and the **L402
re-pin / category-error fix**, plus the **rename**. The gate did exactly its job: it caught a
category error before anything was anchored.

## Founder decisions now required (the gate's output)
- **DR1 — SPLIT vs drop-L402 vs repin.** Adopt ontological sub-rankings (panel 3–4 SPLIT), drop L402
  from this dimension, or Gemini's minority repin. *Recommend SPLIT.*
- **DR2 — rename + agent-observed companion metric.** Accept the reframe to a "primitive latency"
  title + companion column? *(All four require it.)*
- **DR3 — instrumentation/stats package.** Adopt Tempo bifurcation + `t=0` standard + ms k-ladder +
  AP2 tagging + network/warm-cold normalisation as a bundle?

Then: revise §2 doctrine accordingly → (optionally) a short second cross-lineage round on the revised
split design → founder ratification → pre-registration. **Nothing is ratified; the DRAFT §2 doctrine
and the placeholder fixtures stand pending DR1–DR3.**

> **Update 2026-06-22:** DR1 (SPLIT), DR2 (rename + companion), DR3 (bundle) all **adopted**; §2
> re-drafted as the SPLIT design (commit `19213d50`). Round 2 below confirms the *revised* design.

---

# Cross-lineage review round 2 — the revised SPLIT design (confirmation)

**Gate:** revised §2 (SPLIT / RAPL / DR3) → **round-2 cross-lineage round** → founder ratification →
pre-registration. **Purpose:** confirm the rework actually *resolves* round-1's fatal findings (the
L402 category error G2, the agent-DX/facilitator-internal concern G1) **without introducing new
ones**, and settle the residuals the rework exposed (Tempo-Charge's validity in sub-ranking A; the
n=1 grant sub-ranking B). This is a *narrower, confirmatory* round, not a fresh teardown.

## What round 2 must pressure-test (residuals the rework exposes)
1. Does **SPLIT into validation-type (A) vs grant-type (B)** genuinely cure the G2 category error, or
   just relocate it? Is BT-within-a-sub-ranking now apples-to-apples?
2. Does the **rename to RAPL (rail-primitive) + the co-primary agent-observed metric** adequately
   answer G1, or is the dimension still mislabelled?
3. **Tempo-Charge in sub-ranking A** — round 1 said Charge *fuses verify+settle (~500 ms)* and has no
   separable accept. Is keeping `Tempo-Charge` as a pseudo-rail in A legitimate, or does it smuggle
   settlement into an authorization ranking (→ exclude Charge, keep only `Tempo-Session`)?
4. **Sub-ranking B has one member (L402).** Is "report standalone, not raced" acceptable; or populate
   B with a real **402-challenge-issuance** race (x402/MPP issuance times); or drop L402 from RAPL?
5. Does the **DR3 package** (t=0 at the wire/edge, network-adjusted + canonical geography, ms
   k-ladder + rank-stability, BT-within-group + Kaplan-Meier, `P(settled|accept)`, warm/cold) close
   the measurement/stats objections — any gap left?
6. Any **new fatal** the SPLIT introduces.

## ====== ROUND-2 CROSS-LINEAGE PROMPT — paste verbatim to each lineage ======

> Paste to each model (save replies as `Dim2-Review2-<Model>.md`). Self-contained.

```
You are an adversarial methodology reviewer (CRFM/HELM maintainer + statistician + payments expert).
This is ROUND 2 — a CONFIRMATION review of a REVISED benchmark dimension. In round 1 you (a 4-model
panel) refuted the original design 0–4 for a category error. The authors revised it. Your job: decide
whether the revision actually fixes the problem WITHOUT introducing new ones, settle two residuals,
and give a verdict. Be concise; do not re-litigate settled points.

WHAT THE DIMENSION MEASURES. "Rail Authorization-Primitive Latency" (RAPL): the time from an agent
issuing its pay command (payload constructed and on the wire) to the rail's authorization-primitive
decision — distinct from settlement finality (a separate, frozen dimension). It is named a
"primitive" latency (NOT agent-perceived) and is reported with a co-primary AGENT-OBSERVED
total-latency metric. Six rails: x402-on-Base, x402-on-Stellar, x402-on-Solana, MPP-on-Tempo,
MPP-on-Spark-Lightning (L402), Google AP2.

ROUND-1 VERDICT (already accepted): racing all six under one ranking was a CATEGORY ERROR — the
authorization "accept" is a different KIND of object per rail (x402 /verify VALIDATES a submitted
payment; L402's macaroon GRANTS permission to pay, issued before the payer commits; AP2 verifies a
MANDATE). L402 has no pre-settlement payment-validation point (in Lightning, payment IS settlement).

THE REVISION (what you are reviewing):
1. SPLIT into two sub-rankings, raced/scored only WITHIN each:
   - A "Payment-Validation": x402-Base, x402-Stellar, x402-Solana, Tempo-Charge, Tempo-Session,
     AP2 — all validate something the payer submitted. (MPP-on-Tempo is bifurcated into two
     pseudo-rails: Charge = one-time, Session = voucher.)
   - B "Permission-Grant": L402 only (macaroon + invoice issuance). Because B has ONE member it is
     reported as a standalone number, NOT raced.
2. RENAME to RAPL + a co-primary agent-observed total-latency metric (auth + accept→settle gap).
3. AP2 stays in A but tagged "auth-only / no funds-check", with its external dispatch hop DECOMPOSED
   OUT so A races the comparable mandate-verify+credential-issuance step, not a party-to-party hop.
4. Measurement/stats package: t=0 = payload-on-the-wire measured at the rail EDGE; network-adjusted
   latency with a canonical client geography + published RTT floor; warm-vs-cold pre-registered;
   pass@k on a MILLISECOND k-ladder ({20,50,100,250,500} ms) with a rank-stability heatmap;
   Bradley-Terry only WITHIN a sub-ranking + Kaplan-Meier survival curves; an assurance covariate
   P(settled | accept) so a rail can't win by doing less; lower-is-better.

ADJUDICATE (pick an option each, with brief reasoning):
- RC1 (category error fixed?): does SPLIT A-vs-B genuinely cure it — (a) YES, resolved; (b) NO, the
  problem persists or moves; (c) YES but only with a further change you specify.
- RC2 (Tempo-Charge): Charge fuses verify+settle (~500 ms, no separable accept). (a) KEEP Tempo-Charge
  in A as-is; (b) EXCLUDE Charge, keep only Tempo-Session in A; (c) keep but flag/asterisk as
  settlement-contaminated.
- RC3 (the n=1 grant sub-ranking B): (a) report L402 standalone (not raced); (b) POPULATE B with a
  402-challenge-issuance race across the other rails too; (c) DROP L402 from RAPL entirely.

DELIVER: (1) does the revision fix round-1's category error — yes/no/conditional, one paragraph;
(2) votes on RC1/RC2/RC3 with reasons; (3) any NEW fatal the SPLIT introduces; (4) one-line verdict:
is the REVISED design pre-registerable, with what minimal remaining changes?
```

## ====== END ROUND-2 PROMPT ======

# Round 2 — recorded 2026-06-22

**Panel (4 lineages):** DeepSeek, Gemini, Kimi, Qwen (`dim2-review2-{model}.md`).
**Headline:** the **SPLIT is validated 3–1** and **no new category error** was introduced — but the
round surfaced a **bounded second tier** of required refinements (and one genuine dissent on
presentation). The design *direction* is now sound; this is **converging**, not another teardown.

## Vote tallies
- **RC1 — does SPLIT cure the category error? YES, 3–1.** SPLIT: DeepSeek, Gemini, Qwen. Dissent:
  **Kimi → KEEP-with-labels**, on the ground that a hard split leaves the grant league at **n≈1
  (L402)** with no pairwise power — a *presentation/power* objection, not a claim that splitting
  fails to resolve the incommensurability (all four agree the category error is real). → the SPLIT
  stands, but **RC3 (the n=1 problem) is real and must be fixed.**
- **RC2 — Tempo-Charge? EXCLUDE, ~4–0.** DeepSeek/Qwen/Kimi explicitly exclude Charge (it fuses
  verify+settle ~500 ms — measuring it *is* measuring settlement); Gemini's fused-topology stance
  aligns. Keep **Tempo-Session only**; Charge → appendix/disclosed, not in the raced set.
- **RC3 — the n=1 grant sub-ranking?** Contested → **emergent fix: populate it as a real
  "challenge-issuance latency" race.** Gemini reframes B as *"Challenge-Issuance Latency"* (x402/MPP
  also issue 402 challenges → a commensurable cross-rail grant race); Kimi's n≈1 objection demands
  exactly this; Qwen keeps L402 labelled rather than isolated; DeepSeek tolerates standalone as a
  fallback. **→ make B a challenge-issuance race, not L402-alone.**

## Confirmed-resolved (round-1 fatals)
- **G2 category error — RESOLVED by SPLIT (3–1).** Validation-type vs grant-type sub-rankings, raced
  within-group, is endorsed; the trust-class-label-on-a-unified-ranking approach the panel feared is
  *not* what the revision does (it drops the unified ranking), so DeepSeek's "safety-washing" flaw is
  pre-empted.
- **G1 facilitator-internal accept — addressed** by the RAPL rename + companion agent-observed metric
  (Qwen: "publish two numbers, label the internal one"); residual handled under RR4/RR6.

## New / sharpened findings (the second tier)
1. **The statistics may be mis-specified, not just under-gridded** (Kimi O2 strongest; Gemini Obj2;
   Qwen Obj D). BT assumes a stable transitive 1-D strength; sub-second networked latencies are
   continuous, skewed, heteroscedastic, **tie-heavy**, and **censored** (failed/timed-out auths) —
   which can induce non-transitive cycles and uninterpretable rankings. Direction: handle **ties
   (Davidson)** + **competing risks/censoring (reject/timeout)**; consider a **survival model (Cox
   PH / Aalen-Johansen / mixed-effects on log-latency)** as the primary tool, Kaplan-Meier for
   description; report **median/P95/P99**; pass@k **sensitivity over ≥3 k + variance-aware power
   analysis**.
2. **"pass@k" is the wrong name** (Gemini): pass@k means ≥1 success in k stochastic attempts (implies
   re-sampling the same intent → breaks idempotency). We mean a latency **CDF `P(auth ≤ k)`** —
   **rename the metric**.
3. **`t=0` causal-offset is intrinsic** (Gemini NEW, Kimi O4): for verify-type rails t=0 is *after*
   client-side signing (payload on the wire); for L402 t=0 is *before* the agent's real work (LN
   routing). The offset can't be normalised away across kinds — which is **another reason the SPLIT
   is correct** (never compare across the offset).
4. **Client-side measurement + RTT subtraction** (all four): measure **client `send()` → first byte**,
   and **subtract a baseline `/ping` RTT** to isolate compute; **pre-register topology** + ≥2-topology
   sensitivity. (Refines §2.5 from "rail edge" → **client-side round-trip, RTT-subtracted**.)
5. **Null-verify gaming** (Kimi O5): the checkpoint must **specify the work that precedes it**
   (signature verification + fresh balance state in the timed response), else a rail games by
   emitting `/verify` early.
6. **Labels** (Qwen, DeepSeek): per-row **checkpoint-visibility** ("client-visible: yes/no") and an
   **AP2 scope-coverage** qualifier (AP2's number is its *whole* scope; others' is a *slice*).

## Net verdict
**SPLIT direction validated (3–1); category error resolved.** Round 2 is a **"yes, and"** — the
structure is right, but ratification needs a bounded refinement list (below). Per-lineage verdicts:
DeepSeek "publishable if split + exclude Charge + client-side"; Qwen "publishable after 4 amendments";
Kimi "pre-registerable if client-only + keep-with-labels + replace BT/Wilson with a survival model";
Gemini "reject with major revisions — purge pass@k name, SPLIT". The disagreement is on
*presentation + statistics*, not on the core SPLIT.

## Round-2 refinements (RR — proposed, for founder sign-off)
- **RR1 — Exclude Tempo-Charge** from the raced set (Session-only; Charge disclosed in an appendix). *(RC2.)*
- **RR2 — Make sub-ranking B a "challenge-issuance latency" race** across the 402-issuing rails (fixes
  the n=1 power problem). *(RC3.)*
- **RR3 — Statistics rework:** ties (Davidson) + censoring/competing-risks; survival model (Cox PH)
  as primary with KM description; report median/P95/P99; rename pass@k → `P(auth ≤ k)` with ≥3-k
  sensitivity + power analysis.
- **RR4 — Measurement = client-side round-trip, RTT-subtracted** (baseline `/ping`), pre-registered
  topology + ≥2-topology sensitivity (supersedes §2.5 "rail edge").
- **RR5 — Anti-gaming:** specify the work that must precede the checkpoint (verify + fresh balance state).
- **RR6 — Labels:** per-row checkpoint-visibility + AP2 scope-coverage qualifier.

These are concrete and bounded — implementable without another full teardown. A **short final
confirmation** (or founder judgment) can close it after RR1–RR6 land.

> **Update 2026-06-22:** RR1–RR6 adopted (RR3 as hardened-BT-with-survival-fallback) and folded
> into §2 (commit `298ecfeb`). Round 3 below is the final confirmation on the as-built design.

---

# Cross-lineage review round 3 — final confirmation (RR1–RR6 as built)

**Gate:** §2 with RR1–RR6 applied → **round-3 confirmation** → founder ratification → pre-registration.
**Purpose:** a *short* sign-off, not a teardown. Round 1 found a category error (0–4); round 2
validated the SPLIT (3–1) + a refinement list; this round asks only **"do RR1–RR6 actually close
it — is the as-built design pre-registerable?"** and catches any residual fatal the refinements
introduced.

## What round 3 must confirm
1. **FC1** — does **excluding Tempo-Charge** (Session-only in A; Charge → appendix) remove the
   settlement-contamination, without cherry-picking the fast path misleadingly?
2. **FC2** — does the **Challenge-Issuance race (B)** across the 402-issuers both *fix the n=1
   problem* and *preserve the category-error fix* (A and B never compared), or does putting x402 in
   both A and B confuse readers?
3. **FC3** — is **hardened-BT (Davidson ties + censoring/competing-risks) with a Cox-PH
   *data-triggered fallback*** an adequate answer to the statistics objection, or does correctness
   require the survival model **up front** (not as a fallback)?
4. **FC4** — are RR4 (client-side, RTT-subtracted), RR5 (anti-gaming work-clause), RR6 (visibility +
   AP2 scope labels) sufficient, or is anything still gameable / confounded?
5. Any **new fatal** the refinements introduced; and the **pre-registerable? verdict**.

## ====== ROUND-3 CONFIRMATION PROMPT — paste verbatim to each lineage ======

> Paste to each model (save replies as `Dim2-Review3-<Model>.md`). Self-contained. This is a SHORT
> confirmation round — do not re-open settled points; focus on whether the fixes close the issues.

```
You are an adversarial methodology reviewer (CRFM/HELM maintainer + statistician + payments expert).
This is ROUND 3, a FINAL CONFIRMATION of a benchmark dimension you have reviewed twice. Be concise.
Do NOT re-litigate settled points — only judge whether the applied fixes close the issues and whether
the as-built design is pre-registerable.

HISTORY (settled):
- Round 1: racing all six rails under one "authorization latency" ranking was a CATEGORY ERROR
  (refuted 0–4) — the rails' authorization checkpoints are different KINDS of object.
- Round 2: the authors SPLIT the dimension; you validated the split 3–1 and asked for a refinement
  list. They have now applied it.

THE AS-BUILT DESIGN (what you are confirming):
- Name: "Rail Authorization-Primitive Latency" (RAPL) — a rail/protocol primitive, NOT agent-perceived;
  reported with a co-primary agent-observed total-latency metric. Lower-is-better.
- SPLIT into two within-group races (A and B are NEVER compared to each other):
  * A "Payment-Validation" (validates a payment/mandate the payer submitted): x402-Base,
    x402-Stellar, x402-Solana, Tempo-Session, AP2. C(5,2)=10 pairs. [RR1] MPP-on-Tempo "Charge"
    intent is EXCLUDED from the race (its verify+settle are fused ~500ms = settlement) and only
    disclosed in an appendix.
  * B "Challenge-Issuance" (issues a payable 402 challenge before the payer commits): x402-Base,
    x402-Stellar, x402-Solana, MPP-on-Tempo, MPP-on-Spark-Lightning/L402 (macaroon + BOLT11 invoice).
    C(5,2)=10 pairs. [RR2] This fixes round-1's n=1 grant-league problem.
  * x402 rails appear in BOTH A and B (two distinct primitives); AP2 in A only (no 402 challenge);
    L402 in B only (it has no pre-settlement validation point — payment IS settlement in Lightning).
- Statistics [RR3]: Bradley-Terry kept as the within-sub-ranking comparative spine (consistent with
  the project's frozen dimension-1), HARDENED with a Davidson ties term + an explicit
  censoring/competing-risks rule for authorization failures (reject/timeout). The "pass@k" metric is
  renamed P(auth <= k) (it is a latency CDF). A millisecond k-ladder ({20,50,100,250,500} ms) with a
  rank-stability heatmap + variance-aware power analysis; median/P95/P99 + Kaplan-Meier curves
  reported. A Cox-PH / competing-risks SURVIVAL MODEL is pre-specified as a DATA-TRIGGERED FALLBACK:
  adopted only if real-data checks (transitivity, tie-rate, censoring-rate) show BT is pathological.
  (Rationale for fallback-not-default: swapping the engine pre-emptively would fragment the
  one-method-across-dimensions story and re-expose the frozen dimension-1 to the same critique
  without evidence the pathology bites — D1 is mock-fixture, seconds-scale, tie-free.)
- Measurement [RR4]: client-side send()->first-byte, MINUS a baseline /ping RTT to isolate compute;
  canonical client geography + published RTT floor + >=2-topology sensitivity.
- Anti-gaming [RR5]: the timed checkpoint MUST include signature verification + a fresh balance/state
  read (so a rail cannot game it by emitting /verify early and deferring real checks).
- Labels [RR6]: every row tagged client-visible: yes/no; AP2 tagged scope = whole-rail (its number
  is its entire scope; other rails' is the authorization slice of a larger flow).

CONFIRM (one short answer + reasoning each):
- FC1: Does excluding Tempo-Charge (Session-only in A) remove the settlement-contamination without
  misleadingly cherry-picking the fast path? yes / no / yes-with-caveat.
- FC2: Does the Challenge-Issuance race (B) fix the n=1 problem while preserving the category-error
  fix (A and B never compared)? Is x402-in-both-A-and-B clear or confusing? yes / no / yes-with-caveat.
- FC3: Is hardened-BT (Davidson + censoring) with a Cox-PH DATA-TRIGGERED FALLBACK adequate, or must
  the survival model be the PRIMARY method up front? adequate / survival-required-now.
- FC4: Are RR4/RR5/RR6 sufficient, or is something still gameable/confounded?

DELIVER: (1) yes/no per FC1–FC4 with one or two sentences each; (2) any NEW fatal the refinements
introduced; (3) one-line verdict: is the as-built design PRE-REGISTERABLE — and if not, the single
most important remaining change.
```

## ====== END ROUND-3 PROMPT ======

# Round 3 — recorded 2026-06-22

**Panel (4 lineages):** DeepSeek, Gemini, Kimi, Qwen (`dim2-review3-{model}.md`).
**Headline: PRE-REGISTERABLE**, conditional on a small, bounded fix-list (FR1–FR5). **No new
category error, no redesign.** The three-round arc converged: round 1 refuted the single race 0–4
(category error) → round 2 validated the SPLIT 3–1 + a refinement list → round 3 confirms the
as-built design closes it. The panel also caught **two real bugs the refinements introduced** (good
— that is the gate working).

## FC tallies
- **FC1 — exclude Tempo-Charge: YES (4/4)** (Gemini/Kimi add: disclose the exclusion in the *main
  text*, not only an appendix, and warn devs who need the 1-RTT Charge profile → **FR5**).
- **FC2 — Challenge-Issuance race B + x402-in-both: YES (4/4).** x402 in both A and B is "correct,
  not confusing" — two distinct primitives (like read vs write latency); A/B stay firewalled.
  **Round-1 n=1 problem closed.**
- **FC3 — hardened-BT + Cox-PH data-triggered fallback: ADEQUATE (4/4).** Endorsed as "mature
  adaptive analysis, not p-hacking." **Unanimous condition: the fallback trigger thresholds must be
  *numerically* pre-specified** (tie-rate / censoring-rate / transitivity-violation cutoffs), not
  prose → **FR1** (the gating fix).
- **FC4 — RR4/RR5/RR6: sufficient with caveats** — but two lineages found genuine **new fatals**:

## New issues the refinements introduced (both real, both bounded)
- **Gemini — RR5 mis-applied to Group B (fatal-as-written).** The "fresh balance/state read"
  work-clause is right for **Group A** (validation) but a *category error* for **Group B**: issuing a
  402/L402 challenge (macaroon + BOLT11 invoice) is a **stateless crypto** op; forcing a ledger read
  would break native L402 or inflate latency artificially. → **FR2: restrict RR5 to Group A only.**
- **Kimi — RR4 first-byte vs RR5 work-scope timing gap (fatal-as-written).** Stopping the clock at
  *first byte* lets a rail emit early HTTP framing before finishing the mandated sig-verify + state
  read — gameable. → **FR3: stop the clock at the *last byte of the authorization response payload*
  (or an explicit end-of-auth marker), not first byte.**
- **DeepSeek + Qwen — RTT-baseline validity (non-fatal spec fix).** ICMP `/ping` ≠ TCP/TLS app-layer
  RTT, and the baseline must traverse the **same path + TLS termination** as the auth endpoint. →
  **FR4: same-path app-layer baseline probe; report raw *and* RTT-corrected; add a TCP/TLS-handshake
  sensitivity check.**

## Per-lineage verdicts
DeepSeek "PRE-REGISTERABLE — required fix: numeric fallback thresholds"; Gemini "PRE-REGISTERABLE
provided RR5 restricted to Group A"; Qwen "Pre-registerable — condition on numeric fallback
thresholds"; Kimi "NOT pre-registerable until RR4 re-anchored to last-byte — a *single* alignment
fix." Net: **all four are one-or-two bounded fixes from yes; none ask for redesign.**

## Final refinements (FR — to apply, then ratify)
- **FR1 (gating, unanimous):** numerically pre-specify the BT→Cox-PH fallback triggers. *Proposed
  defaults (founder to confirm at pre-reg):* switch if, in any sub-ranking, **tie-rate > 20%** OR
  **auth-failure/censoring-rate > 5%** for any rail OR **transitivity-cyclic triples > 10%** (or a
  BT goodness-of-fit LR test p < 0.05).
- **FR2:** restrict the RR5 work-clause (sig-verify + fresh state read) to **Group A**; Group B is a
  pure stateless-issuance measurement.
- **FR3:** re-anchor the RR4 stopwatch to **last byte of the authorization response** (end-of-auth
  marker), not first byte.
- **FR4:** RTT baseline = same-path app-layer probe; report **raw + corrected**; TCP/TLS sensitivity.
- **FR5:** disclose the Tempo-Charge exclusion in the **main text** + a dev-facing note on the
  Charge (1-RTT) profile.

After FR1–FR5 (mechanical, no contested choices left), the design is **ready for founder
ratification → pre-registration**. No round 4 is expected.
