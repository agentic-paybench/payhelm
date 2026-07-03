# Dim-2 (RAPL) validation/calibration run — plan (read-only scoping; NOT yet run)

> Internal plan, not pre-registered. Scopes the **Q4 first-party measurement** for the gate-cleared
> RAPL design (`dim2-auth-latency.DRAFT.md` §2, post FR1–FR5). **Nothing here has been built or run**
> — the POC adapters are untouched. Running it is a **founder/credentialed step** (testnet keys,
> external calls) and needs explicit go-ahead per the session tripwires.

## 1. Why this runs *before* FR1 is finalised + pre-registration (sequencing)

The numeric BT→Cox-PH fallback triggers (FR1: tie-rate / censoring-rate / transitivity cutoffs) are
**live-measurement** quantities. They cannot be observed on the *mock* fixtures (Monte-Carlo
log-normals don't tie, don't censor, are transitive), so this validation run is the **first and only
place** their real behaviour appears. Therefore the run is a **pilot** that informs FR1 (and the
variance-aware power analysis) *before* the method is frozen — mirroring dimension-1's established
pattern of running first-party n≈30 calibration **before** freezing the methodology.

> **Sequence:** Q4 validation/calibration run → *principled, pilot-informed* FR1 thresholds + power
> analysis → founder ratification → pre-registration → (later) real-rail scored run applies the
> pre-registered rule.

**Discipline (load-bearing).** The pilot **informs** threshold choice (and confirms whether the
fallback is even relevant); it must **not tune** thresholds to flatter BT on the data that will be
scored. Set thresholds on principled grounds (where does Davidson-BT actually lose validity at the
observed tie/censor rates?), pre-register them, and pre-commit to honouring the trigger even if it
forces the switch to Cox-PH. The pilot and the scored set are **separate data** (the scored set is
the mock Monte-Carlo now, a fresh real-rail run later) — so this is non-circular.

## 2. What the run must capture (per the gate-cleared design)

Two primitives, measured **client-side `send()` → last byte of the response** (FR3), each minus a
**same-path app-layer (TCP/TLS) RTT baseline** (FR4); report **raw + corrected**:

- **Sub-ranking A — Payment-Validation accept** (x402×3, Tempo-Session, AP2): time an **explicit
  `/verify`** call carrying the signed payload → the Verification Response (`{isValid, payer}`). The
  timed response **must include** signature verification + a **fresh balance/state read** (RR5/FR2
  work-clause — Group A only).
- **Sub-ranking B — Challenge-Issuance** (x402×3, Tempo, L402): time the initial request → the
  **`402` challenge** (payment requirements; for L402 the **macaroon + BOLT11 invoice**). **No**
  state-read clause here (FR2 — issuance is stateless).
- **Checkpoints recorded alongside** (not raced): `confirmed`/intermediate + `finalized`, to compute
  the **accept→finalized gap** and the **companion agent-observed total latency** (DR2).
- **Failures** (reject/timeout) recorded as **censored** events (feeds FR1 + competing-risks).

## 3. Instrumentation gap (the key finding)

**The POC servers expose only the fused `/resource` (or `/data`) route** — the facilitator
`verify()`/`settle()` are *in-process* middleware calls (`rail-x402-base/seller_server.py:126–130`;
the TS rails' `paymentMiddleware`), **not standalone HTTP endpoints**. So a client cannot currently
time the `/verify` accept as a round-trip. To measure Group A client-side, each adapter needs:

1. **A thin standalone `/verify` route** on the seller server that calls `facilitator.verify(payload,
   requirements)` and returns the Verification Response — enabling a client-side `send()→last-byte`
   timing of the accept. (Small, local server change; or point at a facilitator that already exposes
   `/verify`, e.g. the CDP-hosted x402 facilitator, and time that HTTP call.)
2. **A same-path RTT-baseline endpoint** (a trivial authenticated no-op over the same host/TLS), timed
   identically and subtracted (FR4). An ICMP `/ping` is **not** valid (wrong path + no TLS handshake).
3. **Group B** is already partially exercised — the client receives a `402` first; instrument
   `send()→last-byte` of that `402` (+ RTT baseline). For L402/Spark this includes BOLT11 invoice
   generation.
4. **Per-rail harnesses to extend:** `rail-x402-base/measure_finality.py` (Python),
   `rail-{solana,stellar,tempo,lightning}-*/src/measure-finality*.ts` (TS). They currently time the
   fused request→200 (+ Solana already splits `confirmed_s`/`finality_s`); add the explicit-verify
   accept timing + the challenge-issuance timing + RTT baseline + failure/censoring capture.

## 4. What the run feeds back

- **Real calibration** `{median, sigma_log}` per rail per sub-ranking → **replaces the PLACEHOLDER
  provenance/fixtures** (Q4's primary purpose); written back via the existing content-addressing path.
- **FR1 pilot inputs:** observed **tie-rate, censoring/auth-failure-rate, transitivity** (cyclic
  triples), and **distribution shapes** (is it log-normal? bimodal? heavy-tailed?) — to set principled
  thresholds + the **min-n-per-pair power analysis** (variance-aware, RR3).
- **Fallback-relevance check:** if ties/censoring are negligible at the chosen resolution, the Cox-PH
  fallback stays dormant (BT-hardened suffices); if they're material, FR1 fires and we adopt the
  survival model — *decided by the pre-registered rule, not by preference.*

## 5. Scope / tripwires

- **Founder/credentialed step.** Real testnet runs (keys, external calls) — **needs explicit
  go-ahead**; not an autonomous action.
- The server changes (a `/verify` route + RTT endpoint) are **adapter edits in `agentpay`**,
  a *different repo* from this HELM fork — to be done there, on one machine (one-writer discipline).
- This document changes nothing and runs nothing; it is the ready-to-execute plan.
