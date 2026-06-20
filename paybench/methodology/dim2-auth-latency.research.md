# Dim-2 Authorization Latency — Research Memo (evidence base, not doctrine)

> **Status: RESEARCH INPUT to `dim2-auth-latency.DRAFT.md` — not doctrine, not
> pre-registered.** Captures adversarially-verified findings from three deep-research
> passes on 2026-06-20: **Pass 1** (`wxhbthfbs`, x402 rails), **Pass 2** (`wdcd8fxdt`,
> AP2 + Tempo-MPP), **Pass 3** (`w2x1qieos`, L402/Spark + prior-art). **All six rails
> now carry a primary-source-validated authorization checkpoint distinct from
> settlement.** (Pass 3's final synthesis was truncated by a session token limit, but
> its 23 claims were verified 3-0 individually; the two card-network sub-claims that
> abstained are noted under Gap B.)

## Verdict (per rail)

The **A1 doctrine** — authorization = an authorization-layer **ACCEPT/verify** signal
that occurs **before** settlement, recorded as a checkpoint distinct from
`confirmed`/`finalized` — now stands as:

| Rail | A1 evidenced? | By |
|---|---|---|
| R1 Base / R2 Stellar / R9 Solana (x402) | ✅ primary spec | Pass 1 — x402 `/verify` vs `/settle` |
| R6 Google AP2 | ✅ primary spec | Pass 2 — mandate-verify → credential → dispatch, settlement out of scope |
| R10 MPP-on-Tempo | ✅ primary spec (with a Charge/Session nuance) | Pass 2 — MPP normative Verify vs Settle procedures |
| R11 MPP-on-Spark-Lightning (L402) | ✅ primary spec | Pass 3 — L402 macaroon+invoice (auth) vs preimage (settle); Spark conditional-lock vs SSP finalize |
| Prior-art / novelty | ✅ precedent found; novelty plausible | Pass 3 — ISO-8583 MTI 0100/0110 vs 0200/0220 = documented *conceptual* precedent; no prior "authorization-latency" benchmark surfaced |

## Verified findings (primary sources; 3-0 adversarial votes)

1. **x402 normatively separates `/verify` (off-chain) from `/settle` (on-chain).**
   `/verify` "verifies a payment authorization without executing the transaction
   on the blockchain"; `/settle` "submit[s] validated payments to the blockchain
   and monitor[s] for confirmation." The resource server fulfils work only after a
   valid verify → **verify-before-settle ordering is normative.**
   *Sources:* github.com/coinbase/x402; docs.x402.org/core-concepts/facilitator;
   docs.cdp.coinbase.com/x402/core-concepts/facilitator.

2. **The `/verify` response is a discrete, separately-observable accept signal.**
   Spec §7.1 shows the success response as `{"isValid": true, "payer": "0x…"}` with
   **no transaction field**; the tx hash appears **only** in `/settle`'s
   `SettlementResponse`. So the accept checkpoint is timeable strictly before any
   settlement tx exists.
   *Sources:* coinbase/x402 specs/x402-specification-v1.md; CDP docs.
   *Caveat:* the high-level CDP overview page collapses verify+settle into one
   sentence — the boundary must be cited from the facilitator API spec, not marketing.

3. **x402-on-Base (EVM "exact" scheme): verification is a distinct off-chain
   phase** (signature recovery to `authorization.from`, balance, parameter/validity
   checks, `eth_call` simulation) **before** the on-chain
   `transferWithAuthorization` (EIP-3009) settle call. EIP-3009's gasless design
   makes the signed authorization an off-chain artifact submitted on-chain later.
   *Source:* coinbase/x402 specs/schemes/exact/scheme_exact_evm.md.

4. **x402-on-Stellar (Soroban): same verify-vs-settle split on a non-EVM chain.**
   Facilitator exposes standard `/verify`, `/settle`, `/supported`; verify is
   off-chain (decode XDR, confirm amount/recipient, check Soroban auth-entry
   signatures, simulate) and **precedes** submission via the OpenZeppelin Relayer.
   Authorization is carried by signed **Soroban authorization entries** (not
   pre-signed transactions).
   *Sources:* developers.stellar.org/docs/build/agentic-payments/x402 (+ /built-on-stellar);
   docs.openzeppelin.com/relayer/.../stellar-x402-facilitator-guide.

5. **Solana commitment ladder validates the confirmed-vs-finalized split.**
   processed → confirmed → finalized. `confirmed` = 66%+ stake voted, **reversible**
   (~5% drop risk; the recommended RPC default); `finalized` = +31 confirmed blocks,
   effectively irreversible.
   *Sources:* docs.anza.xyz/consensus/commitments; solana.com/developers/guides/advanced/confirmation.

6. **Solana `finalized` lags `confirmed` by ≥32 slots ≈ ~13s** (slot ≈ 400ms).
   Concrete confirmed↔finalized separation for checkpoint timing.
   *Source:* solana.com/developers/guides/advanced/confirmation.
   *Time-sensitivity:* this is the Tower-BFT figure; it collapses to ~150ms if
   **Alpenglow** reaches mainnet (NOT live as of 2026-06-20) — a disclosed limitation.

## Load-bearing caveats (carry into the doctrine)

- **C1 — Solana "accept" mis-map risk.** Solana's three commitment levels are all
  **on-chain**; **do not** equate Solana `processed` with the A1 off-chain accept.
  The accept for x402-on-Solana belongs to the **facilitator `/verify`**, not Solana
  consensus. (This confirms our POC-scoping catch: the ~2.27s `confirmed_s` is the
  settle-at-confirmed checkpoint, not the accept.)
- **C2 — Practical timeability (instrumentation).** Some integrations call **only**
  `/settle` (which internally verifies before broadcasting), so the accept is not
  always emitted as a separate HTTP response even though the protocol defines it as
  distinct. **The benchmark must invoke `/verify` explicitly** to capture the accept
  checkpoint. → This *resolves* the "facilitator-internal vs client-perceived"
  tension in A1's favour: the spec exposes a client-observable accept endpoint; we
  must call it rather than rely on the fused 200.
- **C3 — Ordering, not wall-clock.** The x402 specs establish *ordering* and
  *separability*, but publish **no per-step wall-clock latencies.** The only
  quantitative figure in the corpus is Solana's ~13s confirmed↔finalized gap. All
  per-rail accept timings must be **first-party measured** (the validation run).

## Pass-2 verified findings (2026-06-20, task `wdcd8fxdt`)

**R6 — Google AP2 (validates the Q1 framing).**
- AP2 is **explicitly an authorization/mandate layer that does not settle**;
  settlement is delegated to a separate **Merchant Payment Processor** role + the
  underlying rail, and is **out of AP2 scope** ("AP2 operates as a security feature
  within a Commerce Protocol … outside the scope of AP2").
- **Discrete, normatively-ordered authorization checkpoint:** chained signed
  **Intent → Cart/Checkout → Payment** mandates; the Shopping Agent forwards the
  Payment Mandate to the **Credential Provider** (and possibly the Network) for
  **verification**; **only upon successful verification is a payment credential
  released**, which is **then dispatched to the Merchant**, who initiates payment
  with the processor. MUST-ordering: "Credential Provider MUST receive a Payment
  Mandate before returning a payment credential."
- This is exactly the **Q1 "verify + orchestration → dispatchable"** structure:
  mandate-verify → credential issuance → dispatch-to-rail, published and discrete.
- **No latency figures** — the spec frames discrete *steps*, not timed moments →
  AP2 calibration is first-party/placeholder.
- *Sources:* ap2-protocol.org/specification (+ /ap2/specification, /ap2/flows);
  Google Cloud AP2 announcement.

**R10 — MPP-on-Tempo (verify/settle split is normative; a Charge/Session nuance).**
- MPP defines an **HTTP-native handshake** — 402 + `WWW-Authenticate: Payment`
  challenge → client retries with `Authorization: Payment` credential → server
  verifies → `Payment-Receipt`. The MPP core spec (draft-httpauth-payment-00, Tempo
  Labs + Stripe) **requires every method to define BOTH a "Verification Procedure"
  and a separate "Settlement Procedure"** — verify-before-settle is normative (same
  shape as x402).
- **Pull path:** server MUST verify (deserialize the RLP tx, check call/amount/
  recipient) **before broadcasting** — accept provably precedes on-chain submission.
- **Nuance for calibration:** for the one-time **Charge** intent the docs present
  verify+settle as **one combined ~500ms step** (the only *published* timing is the
  ~500ms Simplex-BFT confirmation), so the accept is **instrumentable but not
  separately published** for Charge. For the **Session** intent, per-payment
  authorization is an off-chain **signed-voucher** check (**microseconds / near-zero**),
  clearly earlier than the two-tx batched settlement.
- *Sources:* github.com/tempoxyz/mpp-specs; mpp.dev/protocol/http-402 (+ /intents/charge,
  /payment-methods/tempo); docs.tempo.xyz; tempo.xyz/blog/mpp-sessions.

**Terminology caveat (carry into the doctrine + the cross-lineage gate).** Neither
AP2 nor MPP uses the literal word *"authorization latency"*: MPP calls the accept
step **"verification"**, AP2 calls it **"mandate verification / credential issuance"**.
The *separability* from settlement is genuine and published, but **our
"authorization" label is our framing over their verify/verify-mandate primitive**,
and **no rail publishes a metric named "authorization latency"** or an
authorization-step latency number for the per-transaction path. State this openly.

## Pass-3 verified findings (2026-06-20, task `w2x1qieos`)

**R11 — MPP-on-Spark-Lightning / L402 (authorization checkpoint confirmed).**
- The L402 **402 challenge** carries **BOTH a macaroon and a BOLT11 invoice** in the
  `WWW-Authenticate` header (both REQUIRED). The **macaroon is the authorization
  credential**; the **preimage is the proof-of-payment / settlement proof**. The full
  credential is literally `macaroon:preimage`.
- The **macaroon is minted and issued by the server *before* payment** (at the
  challenge); the **preimage is obtained only afterwards by paying the invoice** — so
  the **authorization grant (macaroon + invoice issuance) is a distinct, earlier step
  than preimage-release settlement.** LSAT makes this explicit: a *"partial"* token is
  issued at the 402 (pre-payment); it becomes a *"complete"* token only after payment
  reveals the preimage.
- **Spark path specifically:** the Spark Lightning send flow has a **conditional
  authorization step** (the agent agrees to conditionally transfer leaves; the Spark
  Entity *locks* leaves until a deadline) that is distinct from and earlier than
  **settlement** (the SSP supplies the Lightning proof-of-payment/preimage; the SE
  finalizes the leaf transfer atomically). So the ~16.5s Spark FROST+SSP ceremony is
  the *settlement* event, downstream of the conditional-lock authorization.
- *Sources:* lightninglabs/L402 protocol-specification.md (+ introduction);
  docs.lightning.engineering L402; lightning.engineering L402-for-agents (2026-03);
  docs.spark.money/learn/lightning; spark.money lightning-invoice.
- *Caveat:* one Spark *marketing* article documents neither HODL invoices nor the
  auth-vs-settlement split nor any latency figures — the structure is in the L402 spec
  + docs.spark.money, not the overview pages.

**Prior art / novelty.**
- **Conceptual precedent confirmed:** ISO 8583 (Worldpay reference guide) defines
  **distinct message-type identifiers for real-time authorization (0100 request /
  0110 reply, 0120/0130 advice) vs settlement-bearing financial messages (0200/0210,
  0220/0230)** — authorization and settlement are *separate, separately-coded message
  classes*. This is **documented conceptual precedent**: PayBench's authorization
  dimension ports a 50-year-old card-network distinction (real-time auth vs batch
  clearing/settlement) to agentic rails — a framing asset, not a weakness.
- **Novelty plausible:** across all three passes, **no prior academic / HELM-style /
  vendor benchmark that defines or measures "authorization latency" as a dimension
  separate from settlement finality was surfaced.** *Honest caveat:* Pass 3's
  prior-art angle was **partly truncated** by a session token limit (two card-network
  sub-claims about a bounded auth *response-time SLA* abstained rather than confirmed,
  due to verifier errors — not a refutation). The core MTI separation is solid (3-0);
  the "auth-latency-as-a-measured-metric SLA" sub-point is not nailed down. A defensible
  novelty claim can stand, framed as *"no prior benchmark, conceptual precedent in
  card networks."*

## Cross-rail conclusion (all six rails)

**Every rail in the set separates an authorization/accept grant from settlement** —
x402 (`/verify` vs `/settle`), AP2 (mandate-verify → credential → dispatch; settlement
out of scope), MPP-Tempo (Verify vs Settle procedures), and L402/Spark (macaroon +
invoice vs preimage). This is a strong, primary-source-grounded vindication of both the
**dimension's validity** (it is a real, published checkpoint on every rail, not an
artifact we imposed) and the **A1 doctrine**. It is the evidence base the §8
cross-lineage gate attacks.

## Implications for the doctrine

- **Q2 → confirmable as A1** for the x402 rails (R1/R2/R9), grounded in primary specs.
- **Q3 doctrine** drafts cleanly for R1/R2/R9; R6/R10/R11 rows stay open pending the
  second pass.
- **Validation run refined:** call `/verify` explicitly (C2); record accept /
  settle@confirmed / finalized as three checkpoints (C1); all accept timings are
  first-party (C3).
- Feeds the **cross-lineage adversarial gate** (DRAFT §8) as the grounded evidence base.
