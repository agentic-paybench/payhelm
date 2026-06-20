# Dim-2 Authorization Latency — Research Memo (evidence base, not doctrine)

> **Status: RESEARCH INPUT to `dim2-auth-latency.DRAFT.md` — not doctrine, not
> pre-registered.** Captures the adversarially-verified findings from the deep
> research pass run 2026-06-20 (109 agents, 26 sources, 122 claims extracted →
> top-25 verified, 25 confirmed / 0 refuted). Primary-source-strong on x402;
> three rails + a prior-art question were left as gaps and are the subject of a
> **second, focused pass** (see §"Gaps", below — task `wdcd8fxdt`).

## Verdict

The **A1 doctrine** — authorization = an **off-chain facilitator ACCEPT** signal
that occurs **before** on-chain confirmation, recorded as a checkpoint distinct
from `confirmed` and `finalized` — is **validated by primary specifications for
all three x402 rails** (Base/EVM, Stellar/Soroban, Solana at the facilitator
layer). It is **unevidenced** (neither confirmed nor refuted) for AP2 (R6),
MPP-on-Tempo (R10), and MPP-on-Spark-Lightning (R11), and **no prior published
"authorization latency" benchmark** was surfaced.

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

## Gaps — subject of the focused second pass (task `wdcd8fxdt`)

The first pass verified only its top-25 claims (a budget cut that skewed toward
x402/Solana); AP2/Tempo/Lightning claims were extracted but not verified, so these
are **gaps, not refutations**:

- **R6 Google AP2** — mandate-verification vs settlement framing; is there a discrete
  "authorized / ready to dispatch" moment? (AP2 specs were fetched; no verified claim.)
- **R10 MPP-on-Tempo** — authorization/accept checkpoint distinct from Tempo BFT
  settlement? Unevidenced.
- **R11 MPP-on-Spark-Lightning (L402)** — is the L402 challenge / BOLT11 invoice
  issuance an authorization checkpoint distinct from preimage-release settlement?
  Unevidenced (L402 spec fetched, no surviving claim).
- **Prior art / novelty** — no published "authorization latency" benchmark surfaced.
  The dimension *appears novel*, but a dedicated prior-art check (incl. card-network
  ISO-8583 authorization-vs-settlement as conceptual precedent) is needed **before**
  any novelty claim.

## Implications for the doctrine

- **Q2 → confirmable as A1** for the x402 rails (R1/R2/R9), grounded in primary specs.
- **Q3 doctrine** drafts cleanly for R1/R2/R9; R6/R10/R11 rows stay open pending the
  second pass.
- **Validation run refined:** call `/verify` explicitly (C2); record accept /
  settle@confirmed / finalized as three checkpoints (C1); all accept timings are
  first-party (C3).
- Feeds the **cross-lineage adversarial gate** (DRAFT §8) as the grounded evidence base.
