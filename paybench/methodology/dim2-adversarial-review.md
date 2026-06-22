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

# Cross-lineage review round — recorded <YYYY-MM-DD> (TO FILL after running)

> Synthesis of the external lineages' replies (`Dim2-Review-<Model>.md`), mirroring the dim-1
> "Cross-LLM review round" format: per-decision vote tally (e.g. "DA2 — keep HOLDS 3–1"), any new
> HIGH findings, consensus prose fixes (zero-regen), defer-to-calibration items, and the net verdict
> that gates founder ratification. **Empty until the founder runs the prompt above.**
