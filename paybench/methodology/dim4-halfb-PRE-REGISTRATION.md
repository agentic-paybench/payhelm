# PayBench DIM-04 Half B: conformance checks on five test-network rails, data pre-registration

**Version:** 1.0 (data pre-registration; the draft revisions 0.2 to 0.9, the freeze preparation and the founder's ruling on the confirmatory order are recorded in Appendix C; scorer version 0.9) · **Method:** binary conformance checks against documented per-rail bounds, reported as counts only: k of K valid repetitions, with the VOID and NOT EXERCISED counts by cause and whether each cell is complete; no interval is computed (founder ruling 2026-11-04); a fresh compliance read precedes any publication · **Frozen:** at the signed tag `paybench-dim4-halfb-prereg-v1` · **Manifest:** `paybench/methodology/dim4-halfb-prereg-manifest.sha256` (its sha256, the value the anchors commit to, is carried in the signed tag's message; it cannot appear in this document, which the manifest covers)

## 1. What this document registers

This document fixes, before the confirmatory run executes, the seven checks of the DIM-04 structural profile's measured annexes (Half B: six conformance checks and one descriptive observation, check 3, which is outside the conformance count), four recorded invariants (section 4.10), the rails each check runs on, the exact procedure of each check, the rule that turns each repetition into one binary outcome, the void rules, the number of repetitions, the analysis plan and the display rule.

Each check executes one or more cells of the DIM-04 structural profile, revision 4 (Half A), which states from vendor documentation what each rail's documents say about outcome certainty. Half A measures nothing; every one of its cells is labelled documentation-derived. Half B tests a subset of those documented statements by running payments on test networks, so that a cell can carry a measured label where the checks executing it support one (section 10), and so that any divergence between a document and a rail's observed behaviour is found and reported as a finding of divergence between the specification and the behaviour, not as a rank event.

What it measures is the behaviour of five pinned test deployments and service paths, with Everyday AI Ltd's own payer, payee, sellers and (where named) facilitators (the company, below), not of the rails in production. Every check title and outcome below is a statement about that pinned test deployment and the company's own stack (section 7.6), never about a rail in general, a production deployment, a public facilitator or another implementation.

The design of this run is to be fixed and externally anchored after the exploratory runs listed in section 12 and before the confirmatory run or any publication. The data of those exploratory runs is not reused as outcome data in any result of this run; it sets only the per-cell K by the rule of section 6.

## 2. Watermark

Test-network tokens only, obtained from faucets or test operators and carrying no monetary value; no value-bearing funds are moved; nothing is sent to or read from any mainnet; the company is the only payer and the only payee of every payment; no third party's endpoint is the subject of any fault; no ranking of rails is published, and no comparison of one rail with another is made.

## 3. Rails, networks and pinned software

The five settling rails, in R-number order. Software is pinned by lockfile at stage 2 and content-addressed in the manifest (section 16); the versions below are the versions the company's existing adapters pin today, read from their installed packages on 2026-10-29.

| Rail | Network | Payment path | Pinned client software (today) |
|---|---|---|---|
| R1 x402-Base | Base Sepolia (eip155:84532) | x402 exact, EIP-3009 `transferWithAuthorization` | x402 2.12.0 (Python), web3 7.16.0 |
| R2 x402-Stellar | Stellar Testnet | x402 exact, Soroban authorization entries | @x402/stellar 2.14.0, @x402/core 2.14.0, @x402/extensions 2.14.0 |
| R9 x402-Solana | Solana devnet | x402 exact, SVM | @x402/svm 2.12.0, @x402/core 2.12.0, @x402/extensions 2.12.0 |
| R10 Machine Payments Protocol on Tempo | Tempo Moderato testnet (chain 42431) | pure-Tempo charge, TIP-20 pathUSD; the Stripe-mediated acceptance leg is not used | mppx 0.6.30, viem 2.52.2 |
| R11 Machine Payments Protocol on Lightning | Spark hosted regtest | BOLT11 invoice paid by a Spark wallet; preimage as credential | @buildonspark/spark-sdk 0.7.17, @buildonspark/lightning-mpp-sdk 0.1.4 |

**R6 GCP+AP2** is not measured by any check (section 9.1): AP2 settles nothing, and its double-spend rule binds the paying agent's own code, for which the POC has no test counterparty.

Every record names its test network: `base-sepolia`, `stellar-testnet`, `solana-devnet`, `tempo-moderato-42431` or `spark-regtest`. No record names a mainnet.

## 4. The seven checks

Each check below carries: the Half A cell it executes (quoted from revision 4, section 2.1 or 2.2), the rail-specific documented claim it tests (quoted from the vendor source, with the URL and the date the quotation was checked as an exact substring of the raw text), the procedure, the binary outcome rule, the voids specific to the check (the voids common to every check are in section 5.3), and the statements of ignorance for rails out of scope. Sub-checks are lettered; each sub-check on each rail is one **cell** of the run, with its own K (section 6).

Unless stated otherwise, every quotation below was checked on **2026-10-29** as an exact substring of the raw text fetched that day (whitespace normalised; HTML pages reduced to text). The two Solana cookbook pages answered HTTP 429 on 2026-10-29; their quotations are cited from the raw text saved on **2026-10-09** (sha256 `8f0a529d65539113b82c081043711a480df37680c7975bffdaba299634691e8b` for `confirmation.md`, `be66bcbcd0ef27bc4fab2a43c7ac8056a191c3c2ac8905b3ebfaf7556df0c2cd` for `retry.md`) and are re-read before the freeze.

### 4.1 Check 1: an identical resubmission cannot settle twice (x402 rails: R1, R2, R9)

**Half A cells executed (RetrySafety).** R1: "Identical resubmit cannot move value twice; a fresh signature within the window is not prevented (documentation-derived)". R2: "Nonce is consumed, so the same entry cannot apply twice; a fresh entry within the window is not prevented (documentation-derived)". R9: "The identical transaction cannot execute twice; a fresh signature over the same payment while the original blockhash is still valid can move value twice, stated by the vendor (documentation-derived)".

**Documented claims tested.**
- R1: EIP-3009 nonces are "randomly generated 32-byte data unique to the authorizer's" address, and `authorizationState` returns "True if the nonce is used". https://raw.githubusercontent.com/ethereum/ERCs/master/ERCS/erc-3009.md (checked 2026-10-29; the same text as https://eips.ethereum.org/EIPS/eip-3009).
- R2: the authorization entry's nonce is "an arbitrary value that is unique for all the signatures performed by address until signatureExpirationLedger", https://developers.stellar.org/docs/learn/fundamentals/contract-development/contract-interactions/stellar-transaction ; and "Replay protection is also implemented in the host", https://developers.stellar.org/docs/learn/fundamentals/contract-development/authorization (both checked 2026-10-29).
- R9: "Although Solana's transaction deduplication ensures the transfer only executes once on-chain", while "the facilitator could return `success` to each caller", https://raw.githubusercontent.com/x402-foundation/x402/main/specs/schemes/exact/scheme_exact_svm.md (checked 2026-10-29).

**Procedure.** One repetition: the payer requests the company's seller's resource, receives the challenge, signs one payment payload, and presents it; the precondition is that this first payment reaches the rail's settled state (section 5.1). Then:
- **1a, through the seller.** The payer presents the byte-identical payment header a second time to the same resource.
- **1b, direct to the network.** The same signed artefact is submitted a second time below the seller: on R1, the copied facilitator calls `transferWithAuthorization` again with the same signed authorization; on R2, the same signed authorization entry is wrapped in a new transaction by the company's self-hosted facilitator signer and submitted; on R9, the byte-identical signed raw transaction is sent again to the devnet RPC.
Reads after the second presentation: the rail's settlement evidence for the payer-to-payee transfer over the window from the first presentation to 120 seconds after the second (R1 ERC-20 `Transfer` logs and `authorizationState`; R2 Horizon operations of the payer's account; R9 the payer's token-account signatures; section 5.2).

**Outcome.** HELD if exactly one transfer of the payment amount from the payer to the payee is found for that payload. VIOLATED if two or more are found. The seller's or facilitator's HTTP answer to the second presentation is recorded beside the outcome (on R9 the scheme text above expects that a duplicate may be answered `success`); it does not decide the outcome.

**Ignorance.** R10 and R11 are covered by check 2. R6: section 9.1.

### 4.2 Check 2: an identical resubmission cannot settle twice (Machine Payments Protocol rails: R10, R11)

**Half A cells executed (RetrySafety).** R10: "Single-use proof semantics are a MUST at the protocol layer; nonce consumption prevents same-chain replay; a fresh signature inside the window, or a second broadcast in push mode, is not addressed (documentation-derived)". R11: "Proof is single-use at the protocol layer; the wallet layer's retry ID is OPTIONAL and its effect unstated; BOLT 4 permits a recipient to accept a second payment on an already-paid hash (documentation-derived)".

**Documented claims tested.**
- R10 and R11 (protocol layer): "A payment proof MUST be usable exactly once; subsequent attempts to use the same proof MUST be rejected by the payment method infrastructure." https://raw.githubusercontent.com/tempoxyz/mpp-specs/main/specs/core/draft-httpauth-payment-01.md (checked 2026-10-29).
- R10: "Nonce consumption prevents same-chain replay", https://raw.githubusercontent.com/tempoxyz/mpp-specs/main/specs/methods/tempo/draft-tempo-charge-00.md ; in expiring-nonce mode, an unexpired seen hash is rejected ("reject as replay"), https://tempo.xyz/developers/docs/protocol/tips/tip-1009.md (both checked 2026-10-29).
- R11: "a challenge that has been marked consumed MUST NOT be accepted again, even if the resource delivery subsequently fails." https://raw.githubusercontent.com/tempoxyz/mpp-specs/main/specs/methods/lightning/draft-lightning-charge-00.md ; at the routing layer a final node "MAY succeed in accepting the HTLC." for an already-paid hash, https://raw.githubusercontent.com/lightning/bolts/master/04-onion-routing.md ; at the wallet layer, "Reuse the same ID and payment parameters when retrying; do not generate a new ID for each attempt." https://docs.spark.money/api-reference/wallet/pay-lightning-invoice.md (all checked 2026-10-29).

**Procedure.** Precondition as check 1 (the first payment settled). Then:
- **2a, the credential presented again.** The payer presents the byte-identical credential to the same resource a second time (R10: the same signed-transaction credential; R11: the same preimage credential).
- **2b, the payment repeated below the seller.** R10: the byte-identical signed transaction is sent again to the Tempo Moderato RPC with `eth_sendRawTransaction`. R11: the payer's wallet calls `payLightningInvoice` a second time for the same invoice with the same `transferId` and the same payment parameters, after the first send reached `TRANSFER_COMPLETED`.
Reads: R10 receipts and TIP-20 `Transfer` logs from payer to payee over the window; R11 the payer's and the payee's wallet transfer lists and balances (section 5.2).

**Outcome.** 2a: HELD if the second presentation is refused (no 2xx, no `Payment-Receipt`, no resource) and no second transfer is found; VIOLATED if any 2xx or any delivery of the resource answers the second presentation of the same credential, or a second transfer is found. 2b on R10: HELD if exactly one transfer is found; VIOLATED if two are found. 2b on R11 is a descriptive cell (section 4.9), scored on one observable event, **SECOND TRANSFER** (yes or no) after a same-`transferId` retry of a completed payment, against the operator's retry guidance quoted above; the request identity the wallet returns is recorded; it never scores VIOLATED, because BOLT 4 permits a second payment on an already-paid hash and the operator does not state what a repeated `transferId` does.

**R11 and hold invoices.** Check 2 on R11 uses ordinary invoices and needs no hold invoice; no check of the confirmatory run uses a hold invoice (section 8).

**Ignorance.** R6: section 9.1.

### 4.3 Check 3 (descriptive, outside the conformance count): a fresh signature inside the validity window (all five settling rails)

**Half A cells executed (RetrySafety).** The second halves of the five cells quoted in checks 1 and 2: on R1, R2 and R10 a fresh signature or entry inside the window "is not prevented" or "is not addressed"; on R9 it "can move value twice, stated by the vendor"; on R11, "BOLT 4 permits a recipient to accept a second payment on an already-paid hash".

**Documented claims tested.**
- R9: "If the initial blockhash is still valid, it is possible for both transactions to be accepted by the network." https://solana.com/developers/cookbook/transactions/retry.md (retrieved 2026-10-09; re-read before freeze).
- R1, R2, R9: the x402 mitigation for the re-sign case is optional: "The `payment-identifier` extension enables clients to provide an `id` that serves as an idempotency key." https://raw.githubusercontent.com/x402-foundation/x402/main/specs/extensions/payment_identifier.md (checked 2026-10-29). Check 3 runs WITHOUT the extension; no check runs with it (section 4.5).
- R10: "Validity windows limit temporal replay windows", draft-tempo-charge-00 (URL above, checked 2026-10-29); neither draft addresses a fresh signature inside one challenge.
- R11: "Each BOLT11 invoice MUST use a freshly generated random payment hash." draft-lightning-charge-00 (checked 2026-10-29); the operator's procedure is "Do not create a second payment just because the first call threw", https://docs.spark.money/wallets/withdraw-to-lightning.md (checked 2026-10-29).

**Procedure.** One repetition: the payer receives one challenge and makes two distinct payments against it, the second after the first has settled and while the challenge and the first artefact's validity window are still open. R1: two EIP-3009 authorizations with distinct random nonces. R2: two authorization entries with distinct nonces. R9: two transactions with distinct memo nonces against the same requirements, the second signed while the first's blockhash is still valid. R10: two transactions with distinct nonces against one challenge before its `expires`. R11: a second `payLightningInvoice` for the same invoice with a NEW `transferId`, after the first send reached `TRANSFER_COMPLETED` and before the invoice's expiry.

**Outcome.** This check has no documented bound to hold or violate on four rails: the documents leave the case unaddressed (R1, R2, R10) or permit it (R11 by BOLT 4). Each repetition is therefore scored on one observable event, **SECOND SETTLED** (yes or no): yes if a second transfer of the payment amount from the payer to the payee is found for the second artefact. On R9 the vendor states that both "it is possible" to be accepted, so neither answer violates the document. The report gives k of K for "second settled" per rail, beside the rail's documented statement, and names any rail where the observed answer is the one the documents rule out (none of the five documents rules out either answer, so this check can produce no divergence finding). Its result carries the label "measured, observed" (section 10) and never moves the label of a Half A cell, which stays documentation-derived on the second halves quoted above; no interval is shown for it. Where the second payment settles, the company's seller also served the resource twice; that is recorded.

**What the check measures, stated plainly.** On R1, R2 and R9 the second payment passes through the company's own facilitator, which settles any valid fresh authorization by design. The check therefore measures whether the rail stack as the company runs it (protocol, pinned facilitator software, chain) prevents the second settlement, not whether a third-party facilitator would.

**Ignorance.** R6: section 9.1.

### 4.4 Check 4: an artefact presented after its deadline fails conclusively, and its death is observable to the payer (all five settling rails)

**Half A cells executed (AmbiguityWindow and TerminalSignal).**
- R1: "Bounded by the authorization's own deadline"; terminal: "Authorization consumed, or deadline passed with it unconsumed".
- R2: "Bounded by the signed authorization entry's expiration ledger"; terminal: "Synchronous submission result, with a timeout that is explicitly not a failure signal".
- R9: "Bounded by blockhash expiry, and the bound must be computed by the client"; terminal: "Signature confirmed at the pinned commitment, or observed block height past the transaction's last valid block height with the signature unseen, conditional on the observing node".
- R10: "Bounded by the transaction's expiration timestamp, which the protocol requires to sit inside the challenge's own expiry"; terminal: "A receipt header on success; failure arrives as an HTTP status and a problem document, with no defined definitive-failure signal".
- R11: AmbiguityWindow "Bounded, but composite and per-route"; terminal: "Success is the preimage; definitive failure is not defined".

**Documented claims tested.**
- R1: `validBefore` is "The time before which this is valid (unix time)", erc-3009.md (checked 2026-10-29).
- R2: "Signature is still considered valid on signatureExpirationLedger, but it is no longer valid on signatureExpirationLedger + 1.", stellar-transaction page (checked 2026-10-29); the x402 scheme caps it: "The auth entry expiration ledger MUST NOT exceed `currentLedger + ceil(maxTimeoutSeconds / estimatedLedgerSeconds)`." https://raw.githubusercontent.com/x402-foundation/x402/main/specs/schemes/exact/scheme_exact_stellar.md (checked 2026-10-29).
- R9: the client polls `getBlockHeight` "with the `confirmed` commitment level until it returns a block height greater than the previously returned last valid block height.", https://solana.com/developers/cookbook/transactions/confirmation.md ; "a dropped transaction can be safely discarded once the blockhash it references is older than the `lastValidBlockHeight` received from `getLatestBlockhash`.", retry.md (both retrieved 2026-10-09; re-read before freeze).
- R10: `valid_before` is the "Transaction expiration timestamp (seconds)", https://tempo.xyz/developers/docs/protocol/transactions/spec-tempo-transaction.md ; in the expiring-nonce mode the pinned client uses, "Transactions with `validBefore` in the past or more than 30 seconds in the future are rejected.", https://tempo.xyz/developers/docs/protocol/tips/tip-1009.md (checked against the text fetched 2026-10-29); the client signs "with `validBefore` no later than the challenge `expires` auth-param.", draft-tempo-charge-00; "Expiring-nonce transactions can now set `validBefore` up to five minutes ahead, instead of 30 seconds.", https://tempo.xyz/developers/docs/protocol/upgrades/t11.md (all checked 2026-10-29).
- R11: "Servers MUST NOT accept credentials for expired invoices", draft-lightning-charge-00; BOLT 11's default expiry is "3600 (1 hour) if not specified", https://raw.githubusercontent.com/lightning/bolts/master/11-payment-encoding.md (both checked 2026-10-29).

**Procedure.** The company's seller issues challenges with a short validity window (a configuration value fixed in section 16, one that passed the rail's positive control in every shakedown block run at that value, and never shorter than the network's own minimum); the payer signs the payment artefact and HOLDS it, presenting nothing. The payer then reads the network until its state is past the artefact's deadline by the rail's own clock, never the host's: R1 the latest block's timestamp greater than `validBefore`; R2 the latest closed ledger sequence greater than `signatureExpirationLedger`; R9 `getBlockHeight` at `confirmed` greater than `lastValidBlockHeight`; R10 the latest block's timestamp greater than `valid_before`; R11 the invoice's expiry passed both by the payer's read of the Spark service time (the HTTP `Date` header of the response to the operator's regtest block-height endpoint named in section 16.3; the body is not read) and by the seller host's clock, each by at least 5 seconds, each recorded (section 5.2). Every repetition records that its late presentation was made after the deadline by the rail's own clock, with the reading that showed it (`late_by_rail_clock`); a repetition without that record is NOT EXERCISED (section 5.6). Each block also carries the positive control of section 5.6: a sibling artefact built the same way and presented before its deadline must settle. Then:
- **4a, through the seller.** The held artefact is presented to the resource. On R11 the payment is made before the invoice's expiry (the precondition, not the outcome) and the preimage credential is held and presented to the seller after the invoice's expiry.
- **4b, direct to the network.** R1: the copied facilitator calls `transferWithAuthorization` with the held authorization. R2: the self-hosted facilitator submits a transaction carrying the held entry. R9: the held signed transaction is sent to the devnet RPC. R10: the held signed transaction is sent to the Moderato RPC. R11: the payer's wallet calls `payLightningInvoice` on the expired invoice.

**Outcome.** 4a on R11 is scored on the seller's answer, not on transfers: HELD if the seller refuses the preimage credential presented after the invoice's expiry (no 2xx, no receipt, no resource); VIOLATED if it serves the resource. On 4a on R1, R2, R9 and R10, a held artefact presented after its deadline by the rail's own clock and served (any 2xx or any delivery of the resource) is VIOLATED, and it is violation evidence ahead of the voids (section 5.3). Every other cell of check 4: HELD if both hold: (i) no transfer for the held artefact is found, in the read window of 120 seconds after presentation or in the assurance sweep (section 5.4); and (ii) the artefact's death is observable to the payer at the first read after presentation: R1 `authorizationState(payer, nonce)` false with the latest block timestamp past `validBefore`; R2 no successful transaction carrying the entry with the latest closed ledger past the expiration ledger; R9 `getSignatureStatuses` returning no status for the signature (searching the transaction history, not only the recent cache) with the confirmed height past `lastValidBlockHeight`; R10 no receipt for the transaction hash with the latest block timestamp past `valid_before`; R11 (4b) the wallet's refusal, or a send request status other than `TRANSFER_COMPLETED` that stays so through the window, with no transfer in the payee's list. On R1, R2 and R9 that read is the death signal their documents state. On R10 and R11, whose documents define no definitive failure signal, it is a MEASURED death observation the company defines, never a documented signal, and is reported as such. VIOLATED if a transfer for the held artefact is found at any time. A transaction that landed on the network and failed, with no transfer, is a death observation on every rail (R9 a signature status carrying an error; R10 a receipt whose status is not success; R1 an authorization still unused). If (i) holds and (ii) cannot be read, the repetition is VOID (section 5.3), never held; if (i) holds and the first read after presentation shows a readable state that is not yet a death, the repetition is VOID with that cause, never VIOLATED and never HELD.

The HTTP answer to 4a is recorded; on R10 and R11 a refusal of an expired challenge by the server library tests the library's challenge check, which the record says, and is never counted as the chain's or wallet's own expiry.

**Ignorance.** R6: section 9.1. R11: the HTLC expiry or accumulated CLTV of a route is not exposed by the profiled path (Half A named gap G10), so check 4 on R11 tests the invoice's expiry, not the route's.

### 4.5 Check 5: a duplicate nonce cannot settle twice (5a nonce: R1, R2, R10; 5b payment identifier: a statement of ignorance)

**Half A cells executed (RetrySafety).** R1: "Identical resubmit cannot move value twice" (by nonce); R2: "Nonce is consumed, so the same entry cannot apply twice"; R10: "nonce consumption prevents same-chain replay". The payment-identifier extension that Half A section 2.2 records for R1, R2 and R9 ("For the re-sign case, x402 also defines an optional idempotency key") is a statement of ignorance here (5b, below).

**Documented claims tested.**
- 5a. R1: `authorizationState` returns "True if the nonce is used", erc-3009.md. R2: the nonce "has to be unique among all the non-expired signatures of the address", authorization page. R10: "Nonce consumption prevents same-chain replay", draft-tempo-charge-00 (all checked 2026-10-29).
- 5b, not tested: the extension's response table, "| Same `id`, different payload | Return 409 Conflict |" (payment_identifier.md, checked 2026-10-29), is what no pinned library implements.

**Procedure.**
- **5a.** The payer signs below the client kit, choosing the nonce: two DIFFERENT artefacts (different amount or different resource) carrying the SAME nonce, both presented, the second after the first has settled. R1: two EIP-3009 authorizations with one nonce. R2: two authorization entries with one nonce, inside one expiration window. R10: two Tempo transactions in the 2D nonce lane (`nonceKey` other than the expiring-nonce value) with the same `nonce_key` and `nonce`. On R10 the pinned client signs with expiring nonces (read in the DIM-01 pre-registration's section 6.7); check 5a on R10 deliberately uses the 2D lane, which the Tempo charge draft names for payment transactions, and the record says so.
**Outcome.** 5a: HELD if at most one transfer is found for the nonce; VIOLATED if two are found.

**5b, a statement of ignorance.** 5b is a statement of ignorance on R1, R2 and R9: no pinned library implements the extension's deduplication, so the only implementation available to test would be the company's own. The evidence, read from the pinned packages on 2026-10-30: the pinned Python `x402` 2.12.0 (R1), in `x402/extensions/payment_identifier/__init__.py`, shows the deduplication as the server's own code in its usage example ("cached = await idempotency_store.get(id)"; "return cached  # Return cached response") and exports only helpers to declare, extract and validate the identifier; the pinned `@x402/extensions` 2.14.0 (R2) and 2.12.0 (R9) `payment-identifier` modules export only declare, extract, validate and generate functions, with no 409, conflict or fingerprint handling. The specification itself places the duty on the implementer: "Resource servers and facilitators should bind each `id` to a normalized request fingerprint before returning a cached result." (payment_identifier.md, checked 2026-10-29). No seller in this run advertises the extension.

**R10's nonce modes, stated plainly.** The pinned client signs in TIP-1009's expiring-nonce mode, so check 2b on R10, which rebroadcasts the pinned client's own transaction byte for byte, is the run's test of TIP-1009's identical-hash replay rule. Check 5a on R10 uses the 2D nonce lane, a configuration the pinned client does not use; it is a supplemental check of the Tempo charge draft's lane, labelled as such in every record.

**Ignorance.** 5a is not applicable to R9 (a Solana transaction has no account nonce in the x402 exact scheme; uniqueness is the blockhash and memo, covered by checks 1 and 3) or to R11 (a payment hash is the only identifier; covered by checks 2 and 3). 5b is a statement of ignorance on R1, R2 and R9 (above) and not applicable to R10 and R11 (the extension is x402's). R6: section 9.1.

### 4.6 Check 6: an interrupted flow resolves to a terminal state readable by the payer, and value never moves twice (all five settling rails; R11 by 6a only)

**Half A cells executed (CertaintyEpistemics and TerminalSignal).** R1: "the facilitator may report a broadcast it cannot confirm as non-terminal"; R2: "Synchronous submission result, with a timeout that is explicitly not a failure signal"; R9: "Signature confirmed at the pinned commitment, or observed block height past the transaction's last valid block height with the signature unseen"; R10: "failure arrives as an HTTP status and a problem document, with no defined definitive-failure signal"; R11: "the operator states a failed call is not proof that no transfer started".

**Documented claims tested.**
- R1: the `settlement_pending` code requires the hash "so the caller can reconcile on chain before deciding whether to retry", https://raw.githubusercontent.com/x402-foundation/x402/main/specs/x402-specification-v2.md (checked 2026-10-29).
- R2: "You can try again knowing you won't accidentally, say, duplicate a payment.", https://stellar.org/blog/developers/transaction-submission-timeouts-and-dynamic-fees-faq (checked 2026-10-29).
- R11: "A failed call does not guarantee that no transfer started or that funds are immediately spendable.", pay-lightning-invoice.md (checked 2026-10-29).

**Procedure.** One fault per repetition, from these classes:
- **6a, the client drops after sending** (all five rails): the payer process is killed after its payment request is written to the socket and before any response is read; a fresh payer process then reads the rail's terminal signal (R11: a fresh wallet session reads the send request's status).
- **6b, the facilitator drops before broadcast** (R1, R2, R9; the company's facilitators): the facilitator accepts `/settle`, closes the connection without broadcasting, and logs the fault.
- **6c, the facilitator (or, on R10, the company's seller in pull mode) drops after broadcast** (R1, R2, R9, R10): the transaction is broadcast, then the connection to the seller (R10: to the payer) is closed with no answer.
- **6d, the facilitator pauses past the seller's timeout** (R1, R2, R9): the facilitator waits, after broadcast, longer than the seller's settle timeout, then answers.

After each fault, the payer follows the pre-registered recovery procedure and nothing else: it reconciles on the chain or ledger, or reads the wallet's status, and makes NO new payment for that challenge until a terminal state is read or the artefact's deadline has passed with the death read of check 4 observed; then it requests the resource once more and pays a fresh challenge if one is issued. A re-payment the harness makes because the seller issued a fresh challenge is recorded as such. On every rail the transfers of the original artefact and of the re-payment are each counted by that payment's own identifier (R1 the authorization nonce, R2 the authorization entry's nonce, R9 the transaction signature, R10 the transaction hash, R11 the invoice's payment hash); both identifiers and both counts are recorded, and the outcome below reads the two counts directly. A bound count that cannot be read makes the repetition VOID (V2, section 5.3); it is never replaced by a window proxy. The two bound counts must sum to the window count, or the repetition is VOID (an internal inconsistency, section 5.3); a re-payment bound count of one or more in a record that records no re-payment is VOID for the same reason. The assurance sweep re-counts the read window, and the original artefact's count there is the window count less the re-payment's bound count as the live record bound it. Records written before the bound counts existed (before version 0.5) are scored with a fallback: the re-payment counts one transfer whenever the harness paid again, whether or not the resource was obtained, and the original artefact's count is the rest. The fallback serves only records that carry no original artefact's identifier (`original_id`): it is never used for a record that binds the counts, and in the confirmatory run a check 6 record without that identifier is VOID (V2).

**Outcome.** Two outcomes, each reported, and both recorded whatever the other is. **Safety:** HELD if at most one transfer moves value for the original artefact and no terminal state read is later contradicted; VIOLATED if the original artefact moves value twice, or a terminal state is read and later contradicted. A re-payment the harness makes because the seller issued a fresh challenge is recorded as a recovery cost (yes or no, with its transfer), reported beside the recovery outcome, and never counted toward safety. A payment for the challenge that moves value (the original artefact's or the re-payment's own identifier-bound transfer count is one or more) while the resource is not obtained is reported as a named line beside the cell, "paid, resource not obtained" (the founder's ruling of 2026-11-08 on gauntlet round 4 question 2); the trigger reads the two bound counts, never the runner's record that it paid again. The line gives the number of such repetitions, zero included, and for each its block and attempt, which payment moved (the original, the re-payment, or both), the original payment's and the re-payment's identifiers, both bound transfer counts and the window count as the record holds them (a count that could not be read is printed as not read, never as a fallback value), the void cause where the repetition is VOID, and, where the re-payment moved, the seller's answer to the re-payment as the runner records it (`repayment_status`, the seller's HTTP status; an answer reporting that the payment failed, while the network shows the re-payment's transfer, is the seller's report disagreeing with the network on value). Where only the original moved there is no re-payment to answer, and the seller's answer to the follow-up request is not a recorded field. It is reported whatever the cell's k, never counted toward safety, and never folded unnamed into the recovery outcome: such a repetition carries its own recovery state. An original that moved value with no re-payment moving is the named line on every rail, never a scored failure: on R11 the runner asks again for the resource with a plain request and never presents the original's preimage, so the sentence quoted below is not engaged for the original. Whether a re-payment that moved value fails the repetition depends on whether a quoted sentence of the rail's specification bounds the seller's answer (the founder's ruling of 2026-11-06 on gauntlet round 3 question 1; the source texts read verbatim and committed with their sha256s in `paybench/dim4-half-b/sources/2026-11-06/`, fetched 2026-11-06):
- R11: recovery is VIOLATED, and the repetition with it, when the seller rejects with 402 the preimage credential of a re-payment that moved value, presented before both its challenge's and its invoice's expiry (the runner records both expiries and the presentation time). The bound: "The server MUST atomically mark the challenge as consumed and deliver the resource." (draft-lightning-charge-00 line 332, https://raw.githubusercontent.com/tempoxyz/mpp-specs/main/specs/methods/lightning/draft-lightning-charge-00.md). An error such as a 500 after the challenge is consumed is the text's own case and stays the named line: "If resource delivery fails after the challenge is consumed, the server MUST return an appropriate HTTP error (e.g., 500) and MUST NOT reissue the same challenge. The client MUST treat such a response as a payment loss and MAY retry with a new payment." (lines 337 to 340). Any other error the seller returns to such a presentation is read as the text's own "appropriate HTTP error" after a consumed challenge, a payment loss the text allows (lines 337 to 340), and stays the named line; 402 alone is the text's answer for rejecting a credential: "When rejecting a credential, the server MUST return HTTP 402 (Payment Required) with a fresh `WWW-Authenticate: Payment` challenge per {{I-D.httpauth-payment}}." (lines 405 to 407; the founder's ruling of 2026-11-08 on gauntlet round 4 question 1). A rejection after either expiry is what the text requires ("Servers MUST NOT accept credentials for expired invoices.", lines 464 to 465) and stays the named line. This rule is a row of the outcome table (section 5.7): a void reached first pre-empts it, and the named line, collected from void repetitions too, is the floor; a 402 whose presentation's expiry was not recorded is VOID (V2). The presentation time and both expiries are read on the harness host's clock. Safety is reported on its own, as before.
- R1, R2 and R9: no sentence of the x402 specification (https://raw.githubusercontent.com/x402-foundation/x402/main/specs/x402-specification-v2.md), its exact scheme or its HTTP transport obliges a server to serve once value has moved, and the exact scheme anticipates the case: "Under `upfront` the payment commits first, so a handler failure leaves the client charged with nothing delivered; this specification defines no refund, and any remedy is the resource server's own arrangement." (https://raw.githubusercontent.com/x402-foundation/x402/main/specs/schemes/exact/scheme_exact.md line 20). The event is the named line, never a scored failure.
- R10: the Tempo charge draft (https://raw.githubusercontent.com/tempoxyz/mpp-specs/main/specs/methods/tempo/draft-tempo-charge-00.md) bears two readings and does not decide between them. It says "Upon successful settlement, servers MUST return a `Payment-Receipt` header per {{I-D.httpauth-payment}}." (lines 700 to 702), and its pull-mode steps are "3. Server broadcasts transaction to Tempo", "4. Transaction included in block with immediate finality (~500ms)" and "5. Server returns a receipt whose `reference` field is the transaction digest" (lines 615 to 617). Read as settlement on the chain, a transaction that landed obliges the receipt; read as what the server itself observed, a server whose broadcast call returned an error has not settled. The text is silent on a server whose broadcast call errors while the transaction lands, which is the case section 12 records. The event is the named line, never a scored failure (founder, 2026-11-06).
- On every rail, no answer at all to the re-payment is the named line.
A check 6 cell whose report carries one or more such repetitions can never give its Half A cell "measured, held" (section 10).

On R11, where the terminal read is the operator's view and no documented signal, a terminal state read and later contradicted is VOID with cause (an instrument finding), reported beside the cell. On R10 a dead read later contradicted by a receipt is VIOLATED when the receipt's block timestamp is later than the artefact's `valid_before` (the chain included an expired transaction), and VOID with cause (read lag) when it is not; the runner records the receipt's block timestamp and the artefact's `valid_before`, and a contradiction recorded without them is VOID with cause (an instrument finding); this rule reads a dead read only, and any other contradicted terminal read on R10 is VOID with cause (an instrument finding). On R1, R2 and R9 a contradicted terminal read is VIOLATED only when the contradicting read is at the finalized level, and a contradicting read below it is VOID with cause (read lag). A dead read in a record whose own bound count finds the original artefact's transfer is a contradicted read too, whether or not the runner flagged it, and is decided by the same rules; its contradicting read's level is not recorded, so live it is VOID with cause, and the sweep's re-read at the final level decides it. The assurance sweep (section 5.4) also re-reads a payment read as dead: on R1, R2 and R9 a transfer of the original artefact found there is a contradiction at the finalized level; on R10 the sweep records each transfer's block timestamp and transaction hash, and the original artefact's transfer (the re-payment's excluded by its hash) is decided by the same `valid_before` rule; on R11 it is VOID with cause (an instrument finding). **Recovery:** whether the original payment reached a terminal state readable by the payer, settled (the evidence of section 5.2) or dead (the death read of check 4), by the artefact's deadline plus the read margin, and whether the resource was obtained. If no terminal state can be read because the reads fail, the repetition is VOID (section 5.3). If the reads succeed and still show neither state: on R1, R2 and R9, read at the network's finalized level (R1 `finalized`, R9 `finalized`, R2 a closed ledger), that is VIOLATED and recorded as an indeterminate terminal state, a recovery failure (the recovery outcome is VIOLATED, and safety is read, as always, from the original artefact's count), and it is violation evidence ahead of the voids (section 5.3), decided whether or not the window count was read; read below the finalized level it is never decided and the repetition is VOID with cause (section 5.2); on R10 and R11, whose documents define no definitive failure signal, it is reported as a confirmation of the documented gap, never as VIOLATED.

**Ignorance.** 6b, 6c (facilitator side) and 6d are not applicable to R10 and R11, which have no facilitator in the profiled path. A held Lightning payment (a hold invoice the payee never settles) is not a confirmatory cell: section 8. R6: section 9.1.

### 4.7 Check 7: a settlement outcome reported after a settle that cannot succeed agrees with the network on value (R1: a genuine on-network failure; R2, R9 and R10 in pull mode: the pinned facilitator's or seller's refusal before broadcast)

**Half A cells executed (CertaintyEpistemics).** R1: "Mediated at submission, trustless at the arbiter; the facilitator may report a broadcast it cannot confirm as non-terminal"; R2 and R9: "Mediated at submission, trustless at the arbiter"; R10: "Mediated at the protocol layer, trustless at the chain arbiter, with a public receipt read documented".

**Documented claims tested.**
- R1, R2, R9: "Settlement is performed via the facilitator calling the `transferWithAuthorization` function" (R1), https://raw.githubusercontent.com/x402-foundation/x402/main/specs/schemes/exact/scheme_exact_evm.md ; the non-terminal case "The settlement transaction was broadcast but its confirmation could not be established", x402-specification-v2.md (both checked 2026-10-29).
- R10: in push mode "servers MUST fetch the transaction receipt and verify that it indicates successful execution", draft-tempo-charge-00 (checked 2026-10-29); in pull mode the server broadcasts.

**Procedure.** The company's facilitator (R1, R2, R9) or the company's seller in pull mode (R10) pauses between a successful verify and its settle; during the pause the payer moves its whole balance of the payment token to a second firm wallet, so that the settlement genuinely fails on the network. The facilitator or seller then settles and reports what it observes. The same fault class (balance drained during the pause) is used on every rail of the check. On R1 the failure reaches the network: the facilitator broadcasts and the transaction fails there. On these rails the pinned facilitator verifies again at settle, so after the drain it refuses before broadcasting; the cell tests that the seller's report after that refusal agrees with the network on value (R2, R9 and R10). Every repetition records whether the settle reached the network (`broadcast`).

**Outcome.** HELD if the report agrees with the network: reported failed and no transfer found; reported `settlement_pending` with a hash that the payer's reconciliation resolves to no transfer; reported pending and reconciliation finds exactly one transfer (HELD with an annotation); or reported success with exactly one transfer found. VIOLATED if the report says failed while a transfer is found, success while none is found, or any report while more than one transfer is found. A report that disagrees with the network on value is violation evidence ahead of the voids, live and in the assurance sweep (section 5.3). A repetition with no seller report while every read answered, or with a pending report whose hash the payer's reconciliation resolves to no transfer while one transfer is found, is VOID with cause (an internal inconsistency, section 5.3). Any other combination is scored by the exhaustive rule of section 5.7. If the balance move itself does not land before settle (read from the network), and the report agrees with the network, the repetition is VOID, because the fault was not injected (section 5.3).

**Ignorance.** R11 (no facilitator or verify step in the profiled path) and R10 in push mode (the payer broadcasts) are not covered. R6: section 9.1.

### 4.8 Cell census

| Check | R1 | R2 | R9 | R10 | R11 |
|---|---|---|---|---|---|
| 1a, 1b | yes | yes | yes | n/a (check 2) | n/a (check 2) |
| 2a, 2b | n/a (check 1) | n/a (check 1) | n/a (check 1) | yes | yes |
| 3 | yes | yes | yes | yes | yes |
| 4a, 4b | yes | yes | yes | yes | yes |
| 5a | yes | yes | n/a | yes | n/a |
| 5b | ignorance (section 4.5) | ignorance (section 4.5) | ignorance (section 4.5) | n/a | n/a |
| 6a | yes | yes | yes | yes | yes |
| 6b, 6d | yes | yes | yes | n/a | n/a |
| 6c | yes | yes | yes | yes (seller) | n/a |
| 7 | yes | yes | yes | yes (pull) | n/a |

A held Lightning payment on R11 is a statement of ignorance, not a cell (section 8).

Cells: 1a and 1b on three rails (6); 2a and 2b on two (4); 3 on five (5); 4a and 4b on five (10); 5a on three (3); 6a on five (5); 6b, 6c and 6d on three (9) plus 6c on R10 (1); 7 on four (4). Total 47 cells, all unconditional. Of the 47, six are descriptive and outside the conformance count (the five cells of check 3, and 2b on R11, section 4.2); 41 are in the conformance count.

### 4.9 What each cell can detect

Each cell is one of three kinds, and every record and any published presentation names the kind beside the result:
- **Network-enforcement detector**, which can be VIOLATED only if the test network diverges from its own documented rule: 1a and 1b on R1, R2 and R9 (1a is scored on transfers only; the seller's answer is recorded and decides nothing); 2b on R10; 4b on R1, R2, R9 and R10; 5a on R1, R2 and R10; 6a and 6c on R10 (VIOLATED only by the original artefact moving value twice or by the chain including an expired transaction; a paid re-payment without the resource is the named line there, section 4.6).
- **Library or service behaviour**, genuinely open on the stack the company runs: 2a; 4a (a served late presentation is VIOLATED, section 4.4); 4b on R11; 6a to 6d on R1, R2 and R9; 6a on R11 (a paid re-payment rejected within its expiry is VIOLATED, section 4.6); 7.
- **Descriptive observation**, with no documented bound to hold or violate: 3 on every rail; 2b on R11.
A HELD result from a network-enforcement detector confirms the documented rule on that test network; it is expected, and it is reported as a confirmation, not as a discovery.

### 4.10 Recorded invariants

Four quoted requirements are checkable from records the run produces anyway. Each is checked over every relevant record of the confirmatory run, reported as a count of records that hold and that do not, with no interval and no cell label. They are not cells and do not count toward any K.
- R11: "Each BOLT11 invoice MUST use a freshly generated random payment hash." (draft-lightning-charge-00, checked 2026-10-29): over every invoice the company's R11 seller issues, the count of payment hashes that repeat an earlier one.
- R2: "The auth entry expiration ledger MUST NOT exceed `currentLedger + ceil(maxTimeoutSeconds / estimatedLedgerSeconds)`." (scheme_exact_stellar.md, checked 2026-10-29): over the subject entry of every R2 record, the count that exceed the cap, computed from the challenge's `maxTimeoutSeconds`, the ledger at signing and `estimatedLedgerSeconds` (its value and source entered in section 16). The pinned facilitator tolerates the cap plus 2 ledgers; that tolerance is stated beside the count.
- R10: the client signs "with `validBefore` no later than the challenge `expires` auth-param." (draft-tempo-charge-00, checked 2026-10-29): over every R10 transaction, the count whose `validBefore` is later than its challenge's `expires`.
- The Machine Payments Protocol core draft: servers "MUST return 402 with a fresh challenge and appropriate problem type when payment verification fails" (draft-httpauth-payment-01, checked 2026-10-29): over every R10 and R11 presentation the seller refuses at verification, the count answered otherwise.
Two of the four (the R10 `validBefore` rule and the R2 cap) test the company's own client and the pinned scheme library, not a network or an operator; the report says so beside them.

## 5. Measurement protocol (identical on every rail)

The same measurement protocol was applied identically to every rail. Identically means: the same outcome and void rules, the same repetition rule, the same records and the same reads of each rail's own evidence were applied in every cell; which fault classes apply to a rail, the component at which a fault is injected, and the mechanism each check exercises differ by rail, are listed cell by cell in section 4.8, and make counts across rails not comparable.

The mechanisms, by rail: an EIP-3009 authorization nonce and `validBefore` on Base Sepolia, a Soroban authorization entry nonce and expiration ledger on Stellar testnet, a transaction blockhash, memo and last valid block height on Solana devnet, a Tempo transaction nonce and `valid_before` on Moderato, and a BOLT11 invoice payment hash and expiry on Spark regtest.

### 5.1 Precondition

Where a check needs a first, legitimate payment (checks 1, 2, 3, 5 and 7's verify), that payment must reach the rail's settled state, read as in section 5.2, before the check's action. If it does not within 120 seconds, the repetition is VOID with cause "precondition not settled", and the observation is kept and reported (the legibility pilot's observed sporadic facilitator refusals are this case).

### 5.2 Reads

Each rail's settlement and death evidence is read by the payer from the network, never from the seller's answer: R1 `authorizationState` and ERC-20 `Transfer` logs on the public Base Sepolia RPC, at `latest` for the live read and covered by `finalized` in the sweep; R2 Horizon transaction and operation records of the payer's account; R9 `getSignatureStatuses` and the payer's token-account signatures at `confirmed` for the live read and `finalized` in the sweep; R10 `eth_getTransactionReceipt` and TIP-20 `Transfer` logs on the Moderato RPC; R11 the payer's and payee's Spark transfer lists and send request statuses. Log reads span at most 100 blocks per request (the legibility pilot observed the public Base Sepolia RPC refusing a read over 200 blocks with HTTP 413). Each read is retried up to three times at 2, 4 and 8 seconds on a connection failure, a 413, a 429 or a 5xx; the retries are recorded. The read margin after a deadline is one read interval past the first network state beyond it: one block on R1, R9 and R10, one ledger on R2, and for R11 the first status read after the invoice's expiry. An indeterminate terminal state (check 6) is never decided at that margin: on R1, R2 and R9 it is decided only at the network's finalized level.

### 5.3 Voids

Violation evidence wins: any read, live or in the sweep, that shows a transfer the outcome rule forbids, a second or late presentation that was served (2a on R10 and R11; 4a on every rail, when the presentation was made after the deadline by the rail's own clock), a check 7 report that disagrees with the network on value, a check 6 terminal read contradicted at the finalized level on R1, R2 or R9, a check 6 dead read on R10 contradicted by a transfer in a block after the artefact's `valid_before` (section 4.6), or a check 6 terminal state still indeterminate at the finalized level on R1, R2 or R9, scores the repetition VIOLATED, whatever void trigger also fired. Otherwise, a repetition is VOID, never HELD and never VIOLATED, when (V2 is tested before V3, because a corroboration derived from a failed read means nothing):
- V1, the precondition payment did not settle (section 5.1);
- V2, a read needed to decide the outcome failed after its retries (a refused, unanswered or dropped read; the legibility pilot observed all three), including a check 6 bound count that could not be read, a check 6 record of the confirmatory run without the original artefact's identifier, and on R11 a 402 to a paid re-payment whose presentation's expiry was not recorded (section 4.6);
- V3, the fault was not shown injected as specified: on 6b, 6c and 6d the facilitator's or seller's own fsynced fault log and a read from outside the component that logged it (an RPC response, a network read, the other party's log) must both show the fault fired; the repetition is VOID when the log says it did not fire, when the log and the outside read disagree in either direction (for example a drop-after-broadcast hook that logged firing with no broadcast seen), or when either is missing; on 6a the fault is the harness's own kill of the payer, recorded by the harness; on check 7, the balance move not landing before settle;
- V4, the payer's or facilitator's test balance could not cover the repetition (the funds rule, section 7.4, normally stops cleanly before this);
- V5, a network's software version changed during the repetition, defined per rail as the version string each rail's endpoint reports (R1 and R10 `web3_clientVersion`, R9 `getVersion`, R2 Horizon's root `horizon_version` and `core_version`, R11 the SDK's reported service version where exposed, else V5 does not apply on R11), read at each repetition's start and end (which of these reads each public endpoint actually answers is NOT VERIFIED; stage 2 confirms each and enters the result before the freeze);
- V6, action not delivered: the check's action has no recorded response (no HTTP answer to a presentation, no RPC accept or reject for a direct submission, no server access-log entry for a 6a request);
- check 4's positive control (section 5.6) failed in the block, or is not recorded for the block;
- check 4, a readable state at the first read after presentation that is not yet a death (section 4.4);
- check 6, a terminal state undecided below the finalized level on R1, R2 or R9 (section 5.2), a terminal state read as neither with its commitment level not recorded (V2), or a contradicted terminal read as section 4.6 voids it (an instrument finding on R11, on R10 without the receipt's block timestamp and on R10 for any contradicted read that is not a dead read; read lag on R10 at or before `valid_before`, and below the finalized level on R1, R2 and R9; a dead read whose record's own bound count finds the original artefact's transfer included);
- an internal inconsistency the harness cannot honestly produce: no transfer found after a settled precondition (checks 1, 2, 3 and 5a); no seller report while every read answered (check 7); the original artefact's and the re-payment's bound counts not summing to the window count (check 6); a re-payment bound count of one or more in a record that records no re-payment (check 6); a pending report whose hash resolves to no transfer while one transfer is found (check 7);
- a descriptive cell with no second-transfer reading.
A repetition that is VOID or NOT EXERCISED (section 5.6) is replaced by a further attempt at the end of its block. A cell is complete only with K valid repetitions (HELD or VIOLATED, or for a descriptive cell an observed yes or no) within at most 2K attempts; otherwise the cell is INCOMPLETE, reported with every attempt, and its Half A cell is not labelled measured. Voids and NOT EXERCISED repetitions are counted and reported per cell with their causes.

Every VOID trigger above is exercised before the pre-run commit in the exact call shape the live run uses, with a positive control that must fire and a negative control that must stay silent, the outputs committed with the pre-run record (section 13).

Transfer counting, disclosed: on R2, R9, R10 and R11 a repetition counts the payer-to-payee transfers inside its read window, not transfers bound to the artefact's own identifier (R1 binds each transfer to the artefact's nonce); check 6 is the exception, counting each payment by its own identifier on every rail (section 4.6). Each rail's repetitions run one after another on wallets only the harness uses, and the assurance sweep (section 5.4) re-counts no sooner than two hours later. A stray transfer into the window would be counted; that error can only move a repetition toward VIOLATED, which is visible and investigated, never toward HELD. In the stage 3 shakedown (section 12) the live count and the sweep's re-count were equal on all 639 records that carried a live count; the other 19 were VOID with no live count (18 R10 records for funds, 1 R2 record for an action not delivered), and the sweep found no transfer for any of them.

### 5.4 Assurance sweep

No sooner than two hours after the last repetition of each block, every repetition's evidence is re-read: R1 receipts covered by the `finalized` tag; R2 Horizon `successful`; R9 `finalized` with no error; R10 receipts on the finalized chain; R11 transfer lists. The sweep re-reads every repetition that is not VIOLATED, voids included; a HELD, void or NOT EXERCISED repetition whose sweep evidence shows a forbidden transfer is reclassified VIOLATED and reported as a sweep reclassification; nothing is reclassified the other way. A check 6 sweep may also make a repetition VOID with cause (section 4.6: the R11 instrument finding, and on R10 a dead read's original transfer in a block at or before `valid_before`); it is counted as a sweep reclassification too. A repetition whose sweep re-read failed is counted per cell as "sweep not read". Every VIOLATED carries the sweep's count beside it, and one whose sweep evidence differs from its live evidence is annotated as such in the report. The report tool refuses a block without its sweep file.

### 5.5 Records

One record per repetition, append-only and fsynced, in the format fixed at stage 2: the cell, the repetition number, every request and response with timestamps, every network read with its result and retries, the fault log entries, the terminal signal read, the outcome (HELD, VIOLATED, VOID with cause, NOT EXERCISED with the recorded reason, or for a descriptive cell the observed yes or no), the cell's kind (section 4.9), and the network name. Each block writes an end marker only when it has run to its end; the report tool refuses to run on a block without one.

### 5.6 Attribution and exercise

A refusal counts toward HELD only when its recorded reason names the mechanism the check exercises (nonce or authorization used, replay, expiry); a refusal for any other recorded reason is NOT EXERCISED, reported and not counted toward K. Each reason entry is a full phrase or a typed code copied verbatim from a recorded response, matched case-sensitively, with the record that showed it cited; an entry carrying a per-request value (an identifier, a timestamp) is a regular expression around the verbatim words; no entry is a single generic word. Only VERIFIED entries attribute a refusal; an entry never seen in a recorded response stays NOT VERIFIED and attributes nothing. The scorer records which entry carried each HELD, and refuses to score a cell that needs attribution and has no mechanism in its cell index. The entries, from the stage 3 shakedown's records, are entered in section 16 and frozen with the K table, before any confirmatory run.

On R2 and R9 the pinned facilitator's answer names no mechanism; the recorded reason for a seller refusal there is that answer followed by the facilitator's own verify message, which is the network's simulation error as transcribed by the company's facilitator, and is disclosed as such beside every result of cells 1a and 4a on those rails. Beside each block's result of 1a and 4a on R2 and R9, the report states whether the matching below-seller cell recorded the network's own reason naming the same mechanism.

In checks 1, 2, 3 and 5 the second submission is made while the artefact's own validity window is still open by the network's clock, and that is recorded; otherwise the repetition is NOT EXERCISED (on check 3, a descriptive cell, the second payment must be made inside the challenge's and the first artefact's window, as section 4.3 states). Check 4 adds a positive control per block: a sibling artefact built the same way and presented before its deadline must settle, or that block's check 4 repetitions are VOID; a block whose control is not recorded is treated the same way. In check 4 the late presentation must be recorded as made after the deadline by the rail's own clock (section 4.4); otherwise the repetition is NOT EXERCISED.

### 5.7 Exhaustive outcomes

Each check carries a complete table of observed states to HELD, VIOLATED, VOID or NOT EXERCISED (for descriptive cells, to the observed yes or no, or VOID), fixed in the scorer and listed in section 16 before the freeze; a state not in the table scores VIOLATED (unclassified) and is reported as unclassified, counted apart from the divergences of section 10, never as a divergence.

## 6. Repetitions (K)

**K = 10 valid repetitions per cell.** The exploratory shakedown (section 12) runs each cell before the freeze. Where a cell's first ten exploratory repetitions are not unanimous, that cell's confirmatory K is **20**. Unanimity is judged over the first ten VALID exploratory repetitions of one named shakedown folder, whose file hashes are committed before any of its outcomes is read for K; a cell with fewer than ten valid exploratory repetitions in its folder takes K = 20, however many attempts it had; no further exploratory repetition may change a cell's K. A check 6 cell carries two outcomes (safety and recovery, section 4.6); its first ten are unanimous only when all ten agree on both. This rule, and every doubling it produces, is fixed after the declared exploratory runs and before the confirmatory run; it is not fixed before the exploratory data, which its authors will have seen. The per-cell K table, with the shakedown outcome behind each doubling, is entered in section 6.1 at the freeze.

What K buys: a count. Each cell is reported as k of K valid repetitions with its VOID and NOT EXERCISED counts by cause; no interval is computed or shown for any cell or invariant (founder ruling 2026-11-04). The repetitions are not independent draws (one host, shared wallets, shared public endpoints, one seeded order), and a count describes the repetitions of this run on this test deployment; it carries no claim of a rate, a frequency or a probability of any event on any network, test or production.

The scorer that judges a repetition valid is pinned: the K table carries the sha256 of the scorer files (`outcomes.py`, `reasons.py`, `cells.py` and `versions.py`, which decides V5), and the report tool refuses a K table whose pin differs from the scorer it runs. If a cell's scoring logic changes after the shakedown, that cell's shakedown repetitions are re-run under the new logic, the new folder's file hashes are committed before any of its outcomes is read, and its K is judged on that folder alone. Where a scoring change needs only fields the shakedown records already carry, the records are re-scored under the new scorer rather than re-run (the founder's ruling of 2026-11-04 as applied in version 0.5: re-scored rather than re-run, unless a record lacks a field the new rule needs, in which case the cell is named in the stage report and its repetitions re-run). One exception, by the founder's ruling of 2026-11-06 on gauntlet round 3 question 1: the two check 6 records that need the new field `repayment_status` and lack it (6a-R10 block 2 attempt 2; 6c-R10 block 2 attempt 3, folder `2026-11-05-c6`) are not re-run; they stay valid with their own recovery state ("paid, resource not obtained: original and re-payment moved value; the seller's answer to the re-payment not recorded", so worded from version 0.9), so neither cell's first ten is unanimous and both keep K = 20. Re-running them would put the eleventh repetition into the first ten and drop both cells to K = 10 on a folder chosen after its data was seen. A control (`tests/test_v08.py`, `test_two_unrecorded_records_keep_k_twenty`) and two scorer mutants (scoring them VOID; judging unanimity on the outcome alone) hold this.

Expected size: 47 cells at K = 10 is 470 confirmatory repetitions (plus replacements for void and NOT EXERCISED repetitions, and cells doubled to K = 20); at the K table of section 6.1 it is 490; a repetition makes one to three test payments.

### 6.1 Per-cell K

Entered 2026-11-06 by `poc/dim4-half-b/halfb/freeze_values.py`, output `poc/dim4-half-b/evidence/freeze-values-2026-11-06.json`, re-entered for version 0.8 the same day from `poc/dim4-half-b/evidence/freeze-values-2026-11-06-v08.json` (scorer version 0.8; the K table is unchanged), and re-entered for version 0.9 on 2026-11-08 from `poc/dim4-half-b/evidence/freeze-values-2026-11-08-v09.json` (scorer version 0.9; the K table and the costs per payment are unchanged), and re-entered at the freeze preparation the same day from `poc/dim4-half-b/evidence/freeze-values-2026-11-08-v09-freeze.json` (a citation in two comments of `outcomes.py` corrected, so the scorer pin changed; nothing else in the file changed). Each cell is judged on one named folder of section 12: the latest that holds the cell, so a cell re-run after a logic change is judged on the re-run folder alone. Each folder's files were checked against its committed hash list before any record was read. Every record was re-scored through the one scorer (version 0.9; `_scorer_sha256` bfd23d11a912d6a4935625136f3e59000c1276feb33643be30d232523b878c5d, the sha256 the report tool computes over `outcomes.py`, `reasons.py`, `cells.py` and `versions.py`), in block then attempt order. Re-scored under version 0.8, no shakedown record changed outcome; the two records below changed only their recovery state, as the founder's ruling on round 3 question 1 requires. Re-scored under version 0.9, no record of the four folders (809) changed its outcome, safety, cause or rule; the same two records changed only the wording of their recovery state, which now carries the line's name of version 0.9 and says which payments moved (both the original and the re-payment), and they stay the only entries on the named line.

Result: 45 cells at K = 10 and 2 cells at K = 20 (6a-R10 and 6c-R10), 490 confirmatory valid repetitions in all. The two doublings are on the recovery outcome: in one repetition of each (block 2, attempt 2 of 6a-R10; block 2, attempt 3 of 6c-R10) the harness's re-payment after the seller's fresh challenge moved value (one transfer bound to the re-payment's own transaction hash) and the seller answered it 402 "Payment verification failed.", so the resource was not obtained; the other nine of each obtained it. Safety was HELD in all ten of both. Those two records predate the field `repayment_status` (section 4.6) and are not re-run, by the founder's ruling of 2026-11-06 on round 3 question 1, which sets aside the re-run rule of section 6 for these two records only: they stay valid with their own recovery state ("paid, resource not obtained: original and re-payment moved value; the seller's answer to the re-payment not recorded", so worded from version 0.9), neither cell's first ten is unanimous, and both keep K = 20. The control `test_two_unrecorded_records_keep_k_twenty` (`poc/dim4-half-b/tests/test_v08.py`) and two scorer mutants (scoring such a record VOID; judging unanimity on the outcome alone) hold it. On R10 that event is the named line of section 4.6 and never a scored failure, so neither cell can carry "measured, held" (section 10).

Cells judged on a later folder (gauntlet round 3, R3-11), with the K their earlier folder would have given under scorer 0.8 and why the later folder exists: the ten check 4 cells (4a and 4b on every rail) had 0 valid repetitions on `2026-11-04` (K 20 there), because version 0.5 added the rail-clock lateness record that those records lack; they are judged on `2026-11-04-v05` (10 valid each, K 10). 5a-R10 had 5 valid of 15 attempts on `2026-11-04` and 7-R10 had 7 of 15 (K 20 there), through a harness gas defect and a drained payer; both are judged on `2026-11-04-v05-r10` (10 valid each, K 10). The 15 check 6 cells had 10 valid each on `2026-11-04` (K 10 there, 6a-R10 and 6c-R10 included), and are judged on `2026-11-05-c6`, the re-run after check 6 began counting each payment by its own identifier (revision 0.6), where 6a-R10 and 6c-R10 take K 20. The latest-folder rule therefore lowered K for 12 cells and raised it for 2; every later folder was committed with its hash list before any of its outcomes was read.

| Cell | K | Folder | Attempts | Valid | The first ten valid repetitions | Attempts not valid, by cause |
|---|---|---|---|---|---|---|
| 1a-R1 | 10 | `2026-11-04` | 20 | 20 | all HELD | none |
| 1a-R2 | 10 | `2026-11-04` | 10 | 10 | all HELD | none |
| 1a-R9 | 10 | `2026-11-04` | 14 | 10 | all HELD | 4: NOT EXERCISED (refusal reason does not name the replay mechanism: 'transaction_simula...) |
| 1b-R1 | 10 | `2026-11-04` | 10 | 10 | all HELD | none |
| 1b-R2 | 10 | `2026-11-04` | 10 | 10 | all HELD | none |
| 1b-R9 | 10 | `2026-11-04` | 14 | 10 | all HELD | 4: NOT EXERCISED (refusal reason does not name the replay mechanism: 'Transaction simula...) |
| 2a-R10 | 10 | `2026-11-04` | 10 | 10 | all HELD | none |
| 2a-R11 | 10 | `2026-11-04` | 10 | 10 | all HELD | none |
| 2b-R10 | 10 | `2026-11-04` | 10 | 10 | all HELD | none |
| 2b-R11 | 10 | `2026-11-04` | 10 | 10 | all no | none |
| 3-R1 | 10 | `2026-11-04` | 10 | 10 | all yes | none |
| 3-R2 | 10 | `2026-11-04` | 10 | 10 | all yes | none |
| 3-R9 | 10 | `2026-11-04` | 10 | 10 | all yes | none |
| 3-R10 | 10 | `2026-11-04` | 10 | 10 | all yes | none |
| 3-R11 | 10 | `2026-11-04` | 10 | 10 | all no | none |
| 4a-R1 | 10 | `2026-11-04-v05` | 10 | 10 | all HELD | none |
| 4a-R2 | 10 | `2026-11-04-v05` | 10 | 10 | all HELD | none |
| 4a-R9 | 10 | `2026-11-04-v05` | 11 | 10 | all HELD | 1: NOT EXERCISED (refusal reason does not name the expiry mechanism: 'transaction_simula...) |
| 4a-R10 | 10 | `2026-11-04-v05` | 10 | 10 | all HELD | none |
| 4a-R11 | 10 | `2026-11-04-v05` | 10 | 10 | all HELD | none |
| 4b-R1 | 10 | `2026-11-04-v05` | 10 | 10 | all HELD | none |
| 4b-R2 | 10 | `2026-11-04-v05` | 10 | 10 | all HELD | none |
| 4b-R9 | 10 | `2026-11-04-v05` | 10 | 10 | all HELD | none |
| 4b-R10 | 10 | `2026-11-04-v05` | 10 | 10 | all HELD | none |
| 4b-R11 | 10 | `2026-11-04-v05` | 10 | 10 | all HELD | none |
| 5a-R1 | 10 | `2026-11-04` | 10 | 10 | all HELD | none |
| 5a-R2 | 10 | `2026-11-04` | 10 | 10 | all HELD | none |
| 5a-R10 | 10 | `2026-11-04-v05-r10` | 10 | 10 | all HELD | none |
| 6a-R1 | 10 | `2026-11-05-c6` | 11 | 10 | all HELD (recovery: terminal settled; resource obtained) | 1: VOID (V6 action not delivered) |
| 6a-R2 | 10 | `2026-11-05-c6` | 10 | 10 | all HELD (recovery: terminal settled; resource obtained) | none |
| 6a-R9 | 10 | `2026-11-05-c6` | 10 | 10 | all HELD (recovery: terminal settled; resource obtained) | none |
| 6a-R10 | 20 | `2026-11-05-c6` | 10 | 10 | NOT unanimous: HELD (recovery: terminal settled; paid, resource not obtained: original and re-payment moved value; the seller's answer to the re-payment not recorded); HELD (recovery: terminal settled; resource obtained) | none |
| 6a-R11 | 10 | `2026-11-05-c6` | 10 | 10 | all HELD (recovery: terminal settled; resource obtained) | none |
| 6b-R1 | 10 | `2026-11-05-c6` | 10 | 10 | all HELD (recovery: terminal dead; resource obtained) | none |
| 6b-R2 | 10 | `2026-11-05-c6` | 10 | 10 | all HELD (recovery: terminal dead; resource obtained) | none |
| 6b-R9 | 10 | `2026-11-05-c6` | 10 | 10 | all HELD (recovery: terminal dead; resource obtained) | none |
| 6c-R1 | 10 | `2026-11-05-c6` | 10 | 10 | all HELD (recovery: terminal settled; resource obtained) | none |
| 6c-R2 | 10 | `2026-11-05-c6` | 10 | 10 | all HELD (recovery: terminal settled; resource obtained) | none |
| 6c-R9 | 10 | `2026-11-05-c6` | 10 | 10 | all HELD (recovery: terminal settled; resource obtained) | none |
| 6c-R10 | 20 | `2026-11-05-c6` | 10 | 10 | NOT unanimous: HELD (recovery: terminal settled; paid, resource not obtained: original and re-payment moved value; the seller's answer to the re-payment not recorded); HELD (recovery: terminal settled; resource obtained) | none |
| 6d-R1 | 10 | `2026-11-05-c6` | 10 | 10 | all HELD (recovery: terminal settled; resource obtained) | none |
| 6d-R2 | 10 | `2026-11-05-c6` | 10 | 10 | all HELD (recovery: terminal settled; resource obtained) | none |
| 6d-R9 | 10 | `2026-11-05-c6` | 10 | 10 | all HELD (recovery: terminal settled; resource obtained) | none |
| 7-R1 | 10 | `2026-11-04` | 10 | 10 | all HELD | none |
| 7-R2 | 10 | `2026-11-04` | 10 | 10 | all HELD | none |
| 7-R9 | 10 | `2026-11-04` | 10 | 10 | all HELD | none |
| 7-R10 | 10 | `2026-11-04-v05-r10` | 10 | 10 | all HELD | none |


## 7. Run configuration

### 7.1 Order

Within each block of each rail, the repetitions of that rail's cells are placed in one order drawn by a seeded shuffle (seed fixed in section 16, never the seed of the exploratory runs), and the five rails run their blocks at the same time on the one vantage, each rail starting its second block when its first ends, as in the stage 3 shakedown, so that time of day cannot systematically favour a rail or a check. Check 4's waits for a deadline (on R9 about 150 blocks) run concurrently with other repetitions on other rails only when the waiting repetition holds no open connection and the other repetition uses different wallets; otherwise the order waits.

### 7.2 Blocks

Two blocks per rail, each holding half of the repetitions of every cell of that rail, run one after the other on the one vantage. A rail whose block stops on the funds rule (section 7.4) resumes alone after the top-up while the other rails continue; each rail's blocks are driven independently, as in the stage 3 shakedown, in which no block stopped on the funds rule (the rule was built on 2026-11-06). The first repetition of each block is scored like every other; a first-repetition failure the harness causes is VOID and replaced under the completion rule.

### 7.3 Vantage

One vantage: the company's devbox (label `T1-devbox`), an LXC container on a Proxmox VE host, 4 visible vCPU of an Intel Xeon E5640 at 2.67 GHz, 16 GB of memory, Ubuntu 24.04, kernel 6.17.9-1-pve (read on the host on 2026-10-29), whose network path originates in South Africa. The checks are binary, not timing, so a second vantage would buy nothing; the read margins of section 5.2 are counted in network blocks and ledgers, not in seconds, so no outcome depends on the vantage's round trip. During each block no other measurement workload runs on the container or its host.

### 7.4 Funds

Each wallet's test balance is read at block start and at every twentieth repetition; before each repetition, if any wallet it uses cannot cover it at a fixed conservative cost per payment (fixed in section 16 from the shakedown, plus 15 percent), the block stops cleanly at that boundary and resumes after a top-up made by the founder's hand from the faucet.

As built (draft 0.8, the founder's ruling of 2026-11-06 to apply the funds rule after gauntlet round 3; `poc/dim4-half-b/halfb/funds.py`, called by the orchestrator before every attempt): the readings are those of `halfb/balances.py`, written to the block's `funds.jsonl`; between readings the gate projects each wallet forward, so a reading must cover the attempts made since it plus this one, each at three payments (the most a repetition makes, section 6) at the wallet's cost of section 16.2. Every wallet with a cost is gated, the fee wallets included (the R1, R2 and R9 facilitator signers, and R10's AlphaUSD, which pays check 7's drain fee); the drain wallets, the R1 payer's gas for the drain and R10's AlphaUSD are gated for check 7 only, the only check that uses them. A balance that cannot be read stops the block, as a shortfall does; the stop writes no record for the attempt and no end marker, so the report tool refuses the block until it resumes and ends. A confirmatory block whose configuration does not name the funds rule is refused. A fee shortfall that reached the network anyway would be refused with a fee reason, which names no mechanism and is NOT EXERCISED (section 5.6), never HELD; a control shows it (section 13).

### 7.5 Wallets

Fresh keys on every rail for Half B only, never the DIM-01 wallets: a payer, a payee, a drain wallet for check 7, and a facilitator signer on R1, R2 and R9. Keys are generated at stage 2 and held only in the company's private secrets store, never in a repository. They are funded from faucets by the founder's hand. On R10 the adapter's faucet method is called directly; `setup-accounts.ts` is never re-run. Test funds only; low value; nothing on any mainnet; no paid public endpoint is called.

### 7.6 Counterparties

The company's own sellers on every rail, configured with the short validity window in check 4 only; no seller advertises the payment-identifier extension and no payer sends an `id` (section 4.5). The company's own facilitators where a fault is injected below the seller: on R1 a COPY of the DIM-01 in-process facilitator (`InProcessFacilitatorClient` in `poc/rail-x402-base/seller_server.py`, taken from the revision whose 54 files match the anchored DIM-01 harness manifest, sha256 `1a9d1445d5328f2c2408f24929a439c3b4e9f1e2938fd9d6d91dd005b04b3e15`, verified 2026-10-29), never the frozen file itself; on R2 a self-hosted facilitator built on the `ExactStellarScheme` facilitator class of the pinned `@x402/stellar` 2.14.0 (operated in every R2 block of the stage 3 shakedown, section 12); on R9 a self-hosted facilitator on the `@x402/svm` 2.12.0 facilitator code, paying devnet fees from the Half B facilitator signer (the public x402.org facilitator's rate limit, observed in the DIM-01 exploratory runs, makes it unsuitable as a test counterparty). R10 and R11 run their protocol paths as the company's adapters drive them. No third party's endpoint is ever the subject of a fault; the networks' public RPC, Horizon and Spark operator services are read and submitted to as any client would.

## 8. R11 and hold invoices: a statement of ignorance

**The rule.** No cell of the confirmatory run uses a hold invoice. What a held Lightning payment does on the profiled path (a payee that never provides the preimage; a second payment while the first is held; how and when the payer's funds return) is not measured by this run, because hold invoices are undocumented by the operator, so there is no documented behaviour to check. The exploratory shakedown (section 12) still attempts the hold-invoice sequence (create a hold invoice with a short expiry; pay it; withhold the preimage; attempt a second payment of the same invoice while the first is held; read the send status and the balances until the invoice expires) and reports every observation as an exploratory finding, adverse or not; none enters a result of this run.

**What was checked on 2026-10-29, without moving any funds.** The pinned `@buildonspark/spark-sdk` 0.7.17 declares and implements `createLightningHodlInvoice`, documented in its type declarations as "Creates a Lightning Hodl invoice with a user-provided payment hash. Hodl invoices allow the receiver to hold the HTLC until they decide to settle or fail it." Its implementation validates the payment hash and creates the invoice through the same path as an ordinary invoice, with a default expiry of 30 days. The SDK exposes `providePreimage`, by which the receiver settles a held payment. It exposes no method to fail or cancel a held payment, so a held payment that is never settled resolves only by expiry. Spark's public documentation does not mention hold invoices on any page of its index (https://docs.spark.money/llms.txt, read 2026-10-29), so the feature is undocumented by the operator. The `@buildonspark/lightning-mpp-sdk` 0.1.4 server creates ordinary invoices only.

**What that settles.** Check 2 on R11 and case 6a on R11 need no hold invoice (sections 4.2 and 4.6), and run.

## 9. Statements of ignorance

### 9.1 R6 GCP+AP2, on every check

AP2 is an authorization and evidence layer and settles nothing; its double-spend rule binds the paying agent's own code ("The non-deterministic portion of the Shopping Agent MUST avoid signing multiple, overlapping closed Mandates for the same open Mandate without receiving Receipts rejecting the previously released Mandates", Half A section 2.2), and the POC has no test counterparty that receives a Payment Mandate. No check of this run says anything about R6.

### 9.2 Mainnet

No check runs on, or says anything about, any mainnet. How often any of these faults occurs on any network, test or production, is not measured.

### 9.3 Third-party facilitators and production services

On R1, R2 and R9 every fault below the seller is injected at the company's own facilitator; nothing here describes the behaviour of any public or production facilitator. On R11 the hosted regtest simulates Lightning routing. A VIOLATED result identifies a divergence of this controlled deployment from a quoted requirement only where that requirement applies to the component the check exercised; it does not establish nonconformance of a rail, a vendor, a public facilitator or a production deployment.

### 9.4 Cells of Half A no check measures

OfflineVerifiability on every rail; R11's route-level ambiguity window (named gap G10); R10's second client broadcast in push mode; R11's held-payment behaviour (section 8); the payment-identifier half of the RetrySafety cells on R1, R2 and R9, because no pinned library implements the extension's deduplication (section 4.5, with the evidence). The Machine Payments Protocol core draft's requirement that servers "MUST return 402 with a fresh challenge and appropriate problem type when payment verification fails" is scored by no check; it is a recorded invariant (section 4.10).

### 9.5 Evidence limits per rail

R11's settlement and death evidence is the hosted operator's wallet and service views (transfer lists, send request statuses, balances); they are the only evidence available on this path and do not independently prove route-level settlement, HTLC resolution or the absence of state outside the service. R11's payee is the operator's hosted wallet software; nothing here describes another Lightning implementation. A check 6 safety HELD says the same thing on every rail, and only that: no more than one transfer bound to the original artefact's identifier moved value, and no terminal state read was later contradicted. It does not say which component kept a second transfer from moving: on R1, R2, R9 and R10 the original artefact is a signed payment whose second submission the network, the facilitator or the seller could each have refused, and the check does not tell them apart; on R11 the evidence is the operator's views named above (gauntlet round 4, R4-19). R9's death read assumes the devnet RPC retains the transaction history the read searches; the retention it offers is recorded at the freeze. The public RPC, Horizon and Spark endpoints are named in section 16; a change in their behaviour during the run is not otherwise controlled.

## 10. Analysis plan

Per cell: the number of attempts and of valid repetitions, k (HELD; for a descriptive cell, the observed yes), the VOID and NOT EXERCISED counts by cause, the unclassified VIOLATED count apart from the divergences, whether the cell is complete or INCOMPLETE (section 5.3), the sweep reclassifications and their annotations; for check 6, both outcomes, the recovery cost, the safety and recovery totals, the "paid, resource not obtained" line of section 4.6 with its count, its identifiers and which payment moved, the count of repetitions whose sweep re-read failed, and the count of V6 voids in which the payment settled (the 6a access-log wait of section 16.1); beside every R11 result, R11's evidence limit (section 9.5) and the unexplained wallet movements of section 12; for 1a and 4a on R2 and R9, the disclosure and the below-seller annotation of section 5.6; for section 4.10, the counts. No interval is computed. One scorer entry point serves the run and any re-score, pinned by sha256 in the K table (section 6).

No statistic combines rails. No rail is compared with another. No cell is pooled across rails or checks.

A VIOLATED repetition decided by a row of section 4 is a finding of divergence between the specification and the behaviour on that rail's test deployment, reported with its raw records, whatever k is. An unclassified VIOLATED (section 5.7) is reported as an unclassified state with its raw records, not as a divergence.

Mapping to the Half A profile: after the report, a Half A cell may carry one of two measured labels where every conformance cell executing it is complete (K valid repetitions within 2K attempts): "measured, held" where every such cell held in every valid repetition, and "measured, diverged" where any repetition was VIOLATED; the label names the checks, k of K and the test network. A third label, "measured, observed", belongs to descriptive cells only (check 3; 2b on R11) and never moves a Half A cell's label. A cell that is INCOMPLETE moves nothing. A check 6 cell whose report carries one or more "paid, resource not obtained" repetitions can never give its Half A cell "measured, held" (the founder's rulings of 2026-11-06 on round 3 question 1 and of 2026-11-08 on round 4 question 2, which widened the line to any payment for the challenge); where it would otherwise have held, the report labels it "measured, not held: paid, resource not obtained reported", which moves no Half A label. The count of measured cells over the profile's 30 is computed for the company's own use and is never published as a column or figure.

## 11. Display rule

Any artefact that presents results of this run lists rails alphabetically by these display names, and only in that order: "Machine Payments Protocol on Lightning (Spark regtest)", "Machine Payments Protocol on Tempo (Moderato testnet)", "x402 on Base (Sepolia)", "x402 on Solana (devnet, Alpenglow)", "x402 on Stellar (testnet)". It carries the sentences "Rails are listed alphabetically by rail name. That ordering is fixed and carries no performance meaning." and "The same measurement protocol was applied identically to every rail." followed by the qualifying sentence of section 5, and "These figures are a measurement, not a recommendation: no rail is endorsed, no ordering implies a best buy, and no rail is being suggested for use.", and "Each cell tests a different documented bound on a different software stack, so counts across rails are not the same measurement and are not to be compared.", and every other statement the company's section 21 Level 1 rules require at the time of publication. Beside any presentation that sits near the published DIM-02 authorization-latency table, it carries: "These conformance checks are a different kind of measurement from the DIM-02 authorization-latency figures: each result here is a count of binary outcomes for one rail under one fault, and none is comparable with, or to be combined with, any figure in that table." This document makes no commitment to publish.

The happy-path latency of these rails is not measured by this run. The test-network settlement finality of the same five deployments is the subject of the DIM-01 test-network confirmatory run (pre-registration at tag `paybench-dim1-testnet-prereg-v1`, OSF DOI https://doi.org/10.17605/OSF.IO/UETFW); any latency statement accompanying these results cites that run and states no second figure.

## 12. Exploratory runs that informed this document

One: the stage 3 shakedown of 2026-11-04, with its check 6 re-run of 2026-11-05, under the ExploratoryPilotTransacted partition (`transacted: true`, test networks only, the company's own low-value test funds on the Half B wallets, a separate research store, never the collector's store). Its data is never reused as outcome data in any result of this run, and every run folder is kept and committed.

| Folder (under `poc/dim4-half-b/shakedown/`) | What it holds | Records |
|---|---|---|
| `2026-11-04` | every cell on all five rails in two blocks, scored under version 0.4 live and re-scored under version 0.5; the R11 hold-invoice sequence (`R11-hold/`) | 537 (R1 120, R2 130, R9 117, R10 110, R11 60), plus 80 hold-sequence observations |
| `2026-11-04-v05` | check 4 re-run on all five rails after version 0.5 changed its logic (the rail-clock lateness record; the R11 margin of section 4.4); R2 with a 60 second window after 30 seconds failed the positive control | 101 |
| `2026-11-04-v05-r10` | R10 5a and 7 re-run under version 0.5, the originals having fallen short of ten valid repetitions through a harness gas defect and a drained payer | 20 |
| `2026-11-05-c6` | every check 6 cell (15) re-run after check 6 began counting the original payment's and the re-payment's transfers each by its own identifier (revision 0.6) | 151 |

What it informed: the verbatim refusal reason entries of section 5.6 (every entry VERIFIED from a shakedown record; the six R2 entries corrected or dropped); the V5 version reads of section 5.3 (every public endpoint answered; none changed within a repetition; R11 exposes none); the check 4 windows of section 16 (R1 30 s, R9 20 s, R10 20 s and R11 30 s confirmed by their positive controls; R2 overturned at 30 s and passing at 60 s); the R11 kill delay (2000 ms); the per-cell K of section 6.1 (45 cells at K = 10; 6a-R10 and 6c-R10 at K = 20, not unanimous on the recovery outcome); the answer that the R2 public testnet RPC returns diagnostic events for a failed transaction; and the gauntlet round 2 repairs that version 0.5 carries. In the check 6 re-run every cell's first ten valid repetitions were HELD on safety; on R10, in one repetition each of 6a and 6c, the harness's re-payment moved value and the seller refused it 402 "Payment verification failed.", so the resource was not obtained (recovery outcome). The cause, read on 2026-11-06 from the seller's logs and the network: each re-payment landed about one second after its paid request (Moderato blocks 42656511 and 42656942, status 1), but the pinned mppx 0.6.30 server's broadcast call (`eth_sendRawTransactionSync` through viem 2.52.2) returned about 61 seconds later with the node's refusal of the same transaction, "'valid_before' 1793857312 is too close to current time (min allowed: 1793857351)", raised through viem's retry layer (`withRetry`); mppx treats that error as a verification failure and answered 402 without reading the transaction's receipt, so its report disagreed with the network on value. The same happened to the original artefact of 6c-R10 attempt 3 (block 42656829, landed; the seller's fault log recorded `broadcast: false`, a field that meant only that the send call returned without an error, renamed `send_call_returned` in version 0.8 (gauntlet round 3, R3-18); the repetition's fault is corroborated by the network, which shows the transaction, so it is HELD by section 5.3's evidence standard, not VOID). All three fall within one five-minute stretch of block 2; no other R10 seller broadcast in the four folders failed this way, and no check 6 record of the folder `2026-11-04` shows a paid re-payment without the resource. Why the first submission's answer did not come back in time is not in the logs; in all 151 records the original payment's and the re-payment's identifier-bound counts summed to the window count (version 0.8 makes that a scored check, section 5.3, and the re-score confirms it); one R1 6a attempt was VOID under V6 (no seller access-log entry one second after the send, although the payment settled) and was replaced under the completion rule. No cell recorded VIOLATED. The hold-invoice sequence (section 8) is reported as exploratory findings: the held payment stayed `LIGHTNING_PAYMENT_INITIATED`, and the payee's incoming transfer `TRANSFER_STATUS_SENDER_KEY_TWEAK_PENDING`, for 30 minutes past the invoice's expiry; a second payment of the same invoice was refused `ALREADY_EXISTS`; the payer's available balance rose by 408 sats unexplained; the 100 sats remain held, since the preimage was never stored. R2's check 4 window, an exploratory finding about the company's own stack (gauntlet round 3, R3-16): at 30 seconds the company's R2 seller path refused an in-window sibling payment in both blocks of `2026-11-04` (402, no settlement) while the same artefact submitted directly to the network settled; at 60 seconds both paths settled in both blocks of `2026-11-04-v05`. The cause on the seller path was not isolated. The two records of 6a-R10 and 6c-R10 that lack the field `repayment_status` are not re-run (section 6.1, the founder's ruling of 2026-11-06 on round 3 question 1). The folders' file hashes enter section 16's frozen set.

## 13. Instrument-build controls (before the pre-run commit)

Every VOID trigger of section 5.3, every exclusion and every terminal-signal read is exercised in the exact call shape the live run uses, with a positive control that must fire and a negative control that must stay silent; every scoring rule has a scorer mutant (a copy of the harness with that rule removed) that the controls must catch (`poc/dim4-half-b/tests/scorer_mutants.py`); every rail's cell logic has runner mutants (a copy of the rail's runner with one rule removed) that the rail's offline controls must catch, each rail's mutants in a committed script (`poc/dim4-half-b/tests/r1_runner_mutants.py`, `r2_runner_mutants.py`, `r9_runner_mutants.py`, `r10_runner_mutants.py`, `r11_runner_mutants.py`), re-run whenever that rail's runner changes, with the output committed with the change; each rail's live read path is proved by a positive control (the block-start control payments found) and a negative control (none in a quiet window) (`poc/dim4-half-b/tests/sweep_controls.py`); version 0.8's rules (the founder's rulings on the round 3 questions, the funds rule of section 7.4, the seed of section 16.1 and the confirmed round 3 repairs) carry their positive and negative controls in `poc/dim4-half-b/tests/test_v08.py` and the runner suites, and their scorer and runner mutants in the scripts above (outputs `tests/scorer-mutants-2026-11-06-v08-output.txt` and `tests/r<n>-runner-controls-2026-11-06-v08-output.txt`); R2's runner mutants run on the shared mutant runner, unmutated copy first (R3-20); version 0.9's rules (the founder's rulings on the round 4 questions and the round 4 fixes) carry their controls in `poc/dim4-half-b/tests/test_v09.py` and their scorer mutants in the script above (output `tests/scorer-mutants-2026-11-08-v09-output.txt`), and every rail's runner mutants are re-run against scorer 0.9 (outputs `tests/r<n>-runner-controls-2026-11-08-v09-output.txt`); from version 0.9 a mutant counts as caught only when a test fails by an assertion, never by a crash or an import failure in the mutated copy; the confirmatory start's checks (the runners inside the harness hash, the frozen configuration hash, the seed read against block H, the block number, the confirmatory driver's own refusals, and the ten per-rail block schedules the seed tool hashes, each the order the driver executes) carry their positive and negative controls in `poc/dim4-half-b/tests/test_freeze_prep.py` and their mutants in the scorer mutant script (outputs `tests/scorer-mutants-2026-11-08-freeze-output.txt` and, after the order ruling of 2026-11-09, `tests/scorer-mutants-2026-11-09-order-output.txt`); the run and any re-score call one scorer entry point; the pre-run runsheet lists each trigger and its exercised status; the outputs are committed with the pre-run record.

## 14. What this run does not say

- It does not compare any rail with any other, rank them, or recommend one.
- It states no latency figure.
- It says nothing about any mainnet, any production facilitator or any production service.
- It states no rate or frequency of any event.
- It says nothing about R6 GCP+AP2.
- No result is claimed to have been fixed before any run: the claim is that the design was frozen and anchored after the declared exploratory runs and before the confirmatory run or any publication.

## 15. Anchors

The manifest (section 16) is to be anchored four ways under the founder's hand: an OpenTimestamps proof committed to a Bitcoin block; a cosign keyless signature recorded in the Rekor transparency log; a hardware-signed annotated git tag whose message carries the manifest's sha256; and an OSF registration of this document with the manifest attached (the PayBench project, node gv8j7, Open-Ended Registration). The anchor values are recorded beside the manifest and in the registration, not in this document. This run is independently sufficient as a pre-registration: its manifest is anchored by OpenTimestamps, a Rekor transparency-log entry and a hardware-signed git tag, so its date is provable even if the OSF registration were unavailable.

## 16. Frozen set

This document; the harness code under `poc/dim4-half-b/`; each rail's lockfile and seller and facilitator source; the settlement asset of each rail (the R1 EIP-3009 token contract address and its verified source, the R2 asset and issuer, the R9 SPL mint and token program, the R10 TIP-20 pathUSD contract, the R11 regtest operator configuration as the SDK names it); the public RPC, Horizon and Spark endpoint URLs; the run configuration (the check 4 short-window values, the seller's settle timeout and the facilitator and seller pause durations of checks 6c, 6d and 7, the R10 submission mode for every R10 cell, the cost per payment, the seed's Bitcoin block height) and, per rail, the sha256 of its frozen part: every field of the confirmatory configuration as `poc/dim4-half-b/halfb/confirmatory.py` builds it, except the seed, the block number and the run folder, which cannot be known at the freeze or differ between the two blocks; the refusal reason entries of section 5.6 (verbatim, each with the record that showed it), the outcome tables of section 5.7 and the V5 version reads of section 5.3; the R2 `estimatedLedgerSeconds` value and its source (section 4.10); the R11 check 4 margin of 5 seconds (section 4.4); the scorer files' sha256 pinned in the K table (section 6); the per-cell K table of section 6.1 and the shakedown summary behind it, with the named shakedown folder's file hashes; the seed rule of section 16.1 (the Bitcoin block height, the two sources and the confirmation count); the harness manifest (every file under `poc/dim4-half-b/halfb/` and `poc/dim4-half-b/runners/`) and its sha256. The seed and the sha256 of the ten block schedules (one per rail and block) are not in the frozen set: both are read and drawn after the freeze, before block 1, and recorded in the pre-run commit (the founder's ruling of 2026-11-06 on round 3 question 5). The confirmatory run executes only when the hashes it computes on the measuring host equal the anchored values. It is started only through `halfb/confirmatory.py`, which builds each rail's configuration from the frozen values alone (the K table file is refused unless its sha256 and its scorer pin are the frozen ones), reads the seed, and refuses without both anchored values; the orchestrator refuses a confirmatory block whose number is not 1 or 2, whose configuration names no seed height, or whose seed is not the hash of block H as read from both sources at that block's start.

Values entered on 2026-11-06, read from the committed code at that date and from the shakedown; the scorer pin of section 16.5 and H of section 16.1 re-entered on 2026-11-08 for version 0.9. Two hashes are not entered here and cannot be: this document's own sha256 and the harness manifest's sha256 are computed at the freeze over the committed files (the drafting notes removed) and recorded beside the manifest, since a document cannot carry its own hash. The frozen configuration sha256 per rail, read on 2026-11-08 from `python3 -m halfb.confirmatory configs`: R1 dd339644b1dbd27e282f848d8248822eab54c1e0f601eae641c9087b0d529b36; R2 8f5062d67095748b273da9ced2a24d90e9752a9f8ba9ad781bf8a12e71fd2e83; R9 4e39dafd80bc46fa13266b72c7aa6bbe10446b3abe1a1d026b554e0d8d857140; R10 364437a01a3d41b8b68f3b6bba3156c49c40a2288233bb95c8d507badc4e8496; R11 476889e5380146d3d74e7d2da73b8076c1e3650168eabd5a74694b06e5fa8b65. The block schedules' sha256 is recorded in the pre-run commit with the seed (section 16.1).

### 16.1 Run configuration

| Value | R1 | R2 | R9 | R10 | R11 | Where it is set |
|---|---|---|---|---|---|---|
| Check 4 short window | 30 s (`maxTimeoutSeconds`) | 60 s (`maxTimeoutSeconds`) | 20 s (`maxTimeoutSeconds`) | 20 s (challenge expiry) | 30 s (invoice expiry) | each `runners/<rail>/runner.py`, the short-window default |
| R11 check 4 margin (section 4.4) | | | | | 5 s, by both clocks | `runners/r11/cells.mts`, `LATE_MARGIN_S` |
| Seller settle timeout (checks 6d, 7) | 30 s | 30 s | 30 s | not used (the seller broadcasts in pull mode; no 6d cell) | not used (no 6d cell) | `HALFB_SETTLE_TIMEOUT_S` default in each seller |
| Check 6c fault | drop after broadcast | drop after broadcast | drop after broadcast | drop after broadcast | no 6c cell | each runner's 6c |
| Check 6d fault | the facilitator's answer held for the settle timeout plus 10 s | the seller stops waiting at the settle timeout and drops; the facilitator's settle runs on | as R2 | no 6d cell | no 6d cell | each seller's `pause_past_timeout` |
| Check 7 pause between verify and settle | 300 s | 300 s | 300 s | 300 s | no check 7 cell | each runner's check 7 (`pause_s`) |
| Check 6a kill | the harness drops the connection after the send | as R1 | as R1 | as R1 | the paying process killed 2000 ms after it announces the call | `runners/r11/cells.mts`, `KILL_AFTER_MS` |
| R10 submission mode | | | | pull mode for every cell (the pinned client signs, the seller broadcasts); below the seller, 2b rebroadcasts the pinned client's bytes to the RPC, 4b sends the late transaction to the RPC, and 5a sends its second artefact to the RPC in the 2D nonce lane | | `runners/r10/cells.mts` header |
| Read window after the action; precondition wait | 120 s; 120 s | 120 s; 120 s | 120 s; 120 s | 120 s; 120 s | 120 s; 120 s | `HALFB_READ_WINDOW_S`, `HALFB_PRECONDITION_S` |
| Wait guard on a deadline; finalized wait | 900 s; 3600 s | 900 s; none | 900 s; 3600 s | 900 s; none | 900 s; none | `HALFB_DEATH_WAIT_S`, `HALFB_FINALIZED_WAIT_S` |
| Price per payment | 0.001 test USDC | 0.001 test USDC | 0.001 test USDC | 0.001 pathUSD | 100 sats | each seller's price default |
| Seed of the confirmatory order (section 7.1) | the hash of the Bitcoin block at height H, one seed for all rails; H is entered here at the freeze, at least 144 blocks above the Bitcoin tip read at the freeze: H = 975500, entered 2026-11-08 when the tip read from both sources at 09:26 UTC was 975044 (456 blocks below H); the freeze is made only while the tip read at the freeze is at most 975356 (H less 144), and otherwise H is re-entered before the freeze; read before block 1 starts from two independent sources, https://mempool.space/api and https://blockstream.info/api, which must return the same hash, with at least six confirmations on both; the seed and the sha256 of the ten block schedules it draws (one per rail and block, each over that rail's cells at the K of section 6.1, and of the ten together) are recorded in the pre-run commit before block 1 (the founder's ruling of 2026-11-06 on round 3 question 5); the exploratory seed was `shakedown-2026-11-04`; the string `halfb-confirmatory-2026-11-06` of version 0.7 is withdrawn, and no order was drawn under it | | | | | `halfb/seed.py` (proved against both live sources on 2026-11-06: block 974798, the same hash from both, 11 confirmations); `halfb/confirmatory.py`, `SEED_HEIGHT` |
| Check 6a access-log wait (V6) | 1 s after the send, then the seller's access log is read | as R1 | as R1 | as R1 | not used (the fresh wallet session's send request is the delivery evidence) | each runner's 6a (gauntlet round 3, R3-23) |
| Check 4 short windows tried in the stage 3 shakedown | 30 s | 30 s (positive control failed in both blocks), then 60 s (passed) | 20 s | 20 s | 30 s | section 12 (gauntlet round 3, R3-16) |

### 16.2 Cost per payment (section 7.4)

For each wallet and asset, the largest per-payment fall over the two blocks of the full shakedown folder `2026-11-04` (the wallet's fall in a block divided by the payments the block made: the payee's rise divided by the price, or on R11, whose payee is the operator's hosted wallet, the transfers the block's records count plus the two block-start control payments), plus 15 percent, rounded up. A wallet whose balance did not fall has no entry. Output: `poc/dim4-half-b/evidence/freeze-values-2026-11-06.json`.

| Rail | Wallet | Asset | Cost per payment, plus 15 percent |
|---|---|---|---|
| R1 | payer | test USDC | 1150 units (0.00115) |
| R1 | facilitator | test ETH | 693370907824 wei |
| R1 | payer | test ETH | 29535604486 wei (check 7's drain) |
| R1 | drain | test ETH | 29529425383 wei (check 7's return) |
| R2 | payer | test USDC | 0.0011501 |
| R2 | facilitator | test XLM | 0.0017167 |
| R2 | payer | test XLM | 0.000001 |
| R2 | drain | test XLM | 0.000001 |
| R9 | payer | test USDC | 1150 units (0.00115) |
| R9 | facilitator | test SOL | 11502 lamports |
| R9 | payer | test SOL | 548 lamports |
| R9 | drain | test SOL | 548 lamports |
| R10 | payer | pathUSD | 1201 units (the price and the fee) |
| R10 | payer | AlphaUSD (check 7's drain fee) | 32 units: 27 units per drain, read 2026-11-06 from the payer's AlphaUSD balance either side of two shakedown drain transactions (Moderato blocks 42573189 and 42574076), plus 15 percent; `halfb/balances.py` reads it from version 0.8 |
| R11 | payer | sats | 136 |

### 16.3 Settlement assets and endpoints

| Rail | Settlement asset | Public endpoints |
|---|---|---|
| R1 | test USDC, the EIP-3009 token at `0x036CbD53842c5426634e7929541eC2318f3dCF7e` on Base Sepolia, a `FiatTokenProxy` (EIP-1967) whose implementation is `FiatTokenV2_2` at `0xd74cc5d436923b8ba2c179b4bCA2841D8A52C5B5`, both verified (compiler 0.6.12); the verified sources, fetched 2026-11-06 from https://base-sepolia.blockscout.com/api/v2/smart-contracts/, are committed in `paybench/dim4-half-b/sources/2026-11-06/` with their sha256s | `https://sepolia.base.org` |
| R2 | test USDC, issuer `GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5`, contract `CBIELTK6YBZJU5UP2WWQEUCYKLPU6AUNZ2BQ4WWFEIE3USCIHMXQDAMA` (`USDC_TESTNET_ADDRESS` of the pinned `@x402/stellar` 2.14.0, read 2026-11-06; the identifier every R2 shakedown record carries) | Soroban RPC `https://soroban-testnet.stellar.org`; Horizon `https://horizon-testnet.stellar.org` |
| R9 | test USDC, SPL mint `4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU`, the SPL Token program | `https://api.devnet.solana.com` |
| R10 | pathUSD, TIP-20 at `0x20c0000000000000000000000000000000000000` (check 7's drain fee in AlphaUSD, `0x20c0000000000000000000000000000000000001`) | `https://rpc.moderato.tempo.xyz` |
| R11 | sats on Spark hosted regtest (SDK network `regtest`) | the Spark service the SDK names for `regtest`; the clock read: the HTTP `Date` header of the response to `https://regtest-mempool.us-west-2.sparkinfra.net/api/blocks/tip/height` (the body, a block height, is not read) |

R2 `estimatedLedgerSeconds` (section 4.10): 5, read in all 189 R2 shakedown records that carry it, from the pinned `@x402/stellar` 2.14.0 `getEstimatedLedgerCloseTimeSeconds` for the Stellar testnet.

### 16.4 Lockfiles (sha256 on 2026-11-06)

The rail adapters sit in the repository's `poc/` directory, outside the harness folder; the harness loads their installed packages.

| Rail | File | sha256 |
|---|---|---|
| R1 | `poc/rail-x402-base/requirements.lock`, a hash-pinned lock of all 68 installed packages, generated 2026-11-06 from the virtual environment's exact versions; every installed version equals its pin (gauntlet round 3, R3-13; the requirements file `requirements.txt`, a3d4e910488b305596601b8091ab7400801b2429332d0e100d66c2074ea7a54f, stays as the adapter's own) | b9b708aac51e96142b7bf3b5e2418618d404a15f4f678ef67d8a6176b1d10a9b |
| R2 | `poc/rail-stellar-x402/package-lock.json` | 5c40daeff5c3f8ccf0e5a598c7672cec4db4c11101ca8ecf5c09e173ca68aaf7 |
| R9 | `poc/rail-solana-x402/package-lock.json` | ec7f55e93c2a7f26827c2e38efaeac7afc2046f3817cf19c06f66f56c2642421 |
| R10 | `poc/rail-tempo-mpp/package-lock.json` | b0a6d3d196409f47d6be48f7d41d41370d910821c9fc17d92127ae4d6c8bcafb |
| R11 | `poc/rail-lightning-mpp/package-lock.json` | 012ce5b9c6e5b3579b5899efb88d4399687b4a568b94c03bec10ccb6c5d8794f |

### 16.5 The scorer, the K table and the shakedown folders

- Scorer version 0.9, `_scorer_sha256` 52f53699f0b958699680efb39eea61c4289a7879b260b2d5f3370e0478e1a3c9 over four files (`outcomes.py` f8f5dbfe36a7726d4cabeec80648a170eb9f530d221abf8dbd6fba24a1415fa9, `reasons.py` fa839575d1add4d5c7681b05ea9b9367f181f9aeb8b7f2d75af1e63f01c56f10, `cells.py` b3939a77b19dc8e251f1ed5ad1dd9347491c2d0addce561513ed6b0d20668800, `versions.py` 1b62033653c01869f9f8a064ce3217316c87535887e42c4e6261aa4860bee0e3; `versions.py`, which decides V5, joined the pin in version 0.8, gauntlet round 3, R3-06; version 0.9 changed `outcomes.py` only, and the freeze preparation corrected a line citation in two of its comments). Each folder's hash check also refuses a file under the folder that its hash list does not name (R3-26).
- The K table: section 6.1.
- Each shakedown folder's committed hash list, by its own sha256: `2026-11-04.sha256` (124 files) c2cf9557c2daaae802af7216a18fc16b69fd40aaa61bbbfeb5f3d3595b20dde5; `2026-11-04-v05.sha256` (105 files) 8c776ace9481270ea015819b221cc2f3a78fe27f3f414f5a29e43b7cdab7f9c7; `2026-11-04-v05-r10.sha256` (21 files) 66a1f0d48c368cc615bf1dc24dcb7065feed1c9f95504b8bdbad69a07d17999c; `2026-11-05-c6.sha256` (110 files) d3e94af719fb58c2f9607ab9f559096d6960db5054aed10451e00dcec4df9878.

### 16.6 Refusal reason entries (section 5.6)

Each entry is copied verbatim from the recorded response cited; matched case-sensitively; a pattern surrounds a per-request value only. Source: `poc/dim4-half-b/halfb/reasons.py`. 20 entries VERIFIED, 1 NOT VERIFIED (which attributes nothing).

| Rail | Mechanism | Entry | Status | The record that showed it |
|---|---|---|---|---|
| R1 | expiry | `invalid_exact_evm_payload_authorization_valid_before` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R1/block1/4a-R1#1 (the facilitator's verify answer at the seller) |
| R1 | expiry | `FiatTokenV2: authorization is expired` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R1/block1/4b-R1#1 (the token's revert, below the seller); also eth_call, evidence/r1-reason-strings-ethcall-2026-10-30.jsonl |
| R1 | nonce | `FiatTokenV2: authorization is used or canceled` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R1/block1/5a-R1#1 |
| R1 | replay | `invalid_exact_evm_nonce_already_used` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R1/block1/1a-R1#1 (the facilitator's verify answer at the seller) |
| R1 | replay | `FiatTokenV2: authorization is used or canceled` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R1/block1/1b-R1#1 (the token's revert, below the seller); also eth_call, evidence/r1-reason-strings-ethcall-2026-10-30.jsonl |
| R10 | expiry | pattern `Payment expired at \d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z\.` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R10/block1/4a-R10#1 (the mppx server's challenge expiry) |
| R10 | expiry | pattern `'valid_before' \d+ is too close to current time \(min allowed: \d+\)` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R10/block1/4b-R10#1 (the node's validBefore check; the deadline had passed by the chain clock before submission). The node gives this text in three circumstances: a deadline already past, a deadline inside the minimum lead time, and a resubmission of a transaction that has already landed (section 12); on 4b-R10 it attributes only with `late_by_rail_clock` recorded, so the artefact was past its deadline by the chain's clock (gauntlet round 3, R3-17) |
| R10 | nonce | `nonce too low: next nonce` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R10/block2/5a-R10#1 (the node) |
| R10 | replay | `Transaction hash has already been used` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R10/block1/2a-R10#1 (the mppx 0.6.30 server's pre-broadcast dedup, dist/tempo/server/Charge.js:270) |
| R10 | replay | `ExpiringNonceReplay` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R10/block1/2b-R10#1 (the node's nonce manager, a typed error) |
| R11 | expiry | `Lightning invoice has expired` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R11/block1/4a-R11#1 (the seller's copied verify, seller.mts line 72) |
| R11 | expiry | pattern `Invoice for lightning send request [0-9a-f-]+ has expired` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R11/block1/4b-R11#1 (Spark's RequestLightningSend, InvalidInputException) |
| R11 | replay | `Preimage already consumed for payment` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R11/block1/2a-R11#1 (the mppx Lightning server) |
| R2 | expiry | `signature has expired` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R2/block1/4a-R2#1 (Error(Auth, InvalidInput), facilitator simulation) and R2/block1/4b-R2#1 (Error(sceAuth, scecInvalidInput), network diagnostics) |
| R2 | nonce | `nonce already exists for address` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R2/block1/5a-R2#1 (Error(sceAuth, scecExistingValue), network diagnostics) |
| R2 | replay | `nonce already exists for address` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R2/block1/1a-R2#1 (Error(Auth, ExistingValue), facilitator simulation) and R2/block1/1b-R2#1 (Error(sceAuth, scecExistingValue), network diagnostics) |
| R9 | expiry | `Simulation failed: "BlockhashNotFound"` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R9/block1/4a-R9#6 (facilitator simulation) |
| R9 | expiry | `Blockhash not found` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R9/block1/4b-R9#5 (RPC simulation, code 7050008) |
| R9 | replay | `Simulation failed: "AlreadyProcessed"` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R9/block1/1a-R9#5 (facilitator simulation) |
| R9 | replay | `This transaction has already been processed` | VERIFIED | shakedown 2026-11-04 (ExploratoryPilotTransacted), R9/block1/1b-R9#5 (RPC simulation, code 7050007) |
| R9 | replay | `duplicate_settlement` | NOT VERIFIED | none |

The V5 version reads (section 5.3): `poc/dim4-half-b/evidence/v5-version-reads-2026-10-30.jsonl`, with `version_start` and `version_end` on every shakedown record; R1 `reth/v2.5.2-7134be3/x86_64-unknown-linux-gnu/base/v1.5.0`, R2 Horizon `30.0.0`, R9 `solana-core` `4.4.0-beta.1`, R10 `tempo/v1.17.0-55a96ba/x86_64-unknown-linux-gnu`; R1 and R10 answer only to curl (the first, urllib read of 2026-10-30 was refused 403); R11 exposes none.

Observed for the R2 check 4 short window in the stage 3 shakedown (section 12), stated as observation only: at 30 seconds the positive control failed in both blocks of `2026-11-04` (the sibling artefact presented through the company's seller was answered 402 and did not settle, while the sibling submitted directly to the network settled); at 60 seconds it passed in both blocks of `2026-11-04-v05`, through the seller and directly.

## Appendix A: sources read for this draft

Saved raw texts of 2026-10-29 (31 files, manifest sha256 `6992d65a07dc18b922e8a4785069a3aa477982c79d5d54b25e0f48e98188c4aa`) in the registrant's private data store, folder `halfb-spec-2026-10-29/`; every quotation in section 4 was checked against them by `tools/quotecheck.py` (35 quotations, 0 missing). The Solana cookbook pages: the 2026-10-09 saved texts, by the sha256 values in section 4.

## Appendix C: revision 0.2 (2026-10-30), the gauntlet round 1 delta

Applied after the cross-lineage review round 1 (five reviewers; their texts are kept unedited in the company's records). Each change names the review surface that caused it; the surfaces are defined in the round 1 disposition. Changes that alter what a check measures or how a repetition is scored were NOT applied and await a ruling.

| Change | Where | Surface |
|---|---|---|
| Scope sentence: every check is about the pinned test deployment and the company's own stack | section 1 | S16-ScopeOverclaim |
| Exploratory data "not reused as outcome data"; what it sets | section 1 | S32-ExploratoryReuseWording |
| TIP-1009's expiry-rejection sentence quoted for R10 | section 4.4 | S21-R10ExpiryQuote |
| "is ever found" replaced by the read window and the sweep | section 4.4 | S29-SweepAsymmetry (wording only) |
| R1 5b decided from package source, never exploratory outcome; R10 nonce modes stated | section 4.5 | S20-CensusCount; S12-R10NonceLane |
| The core draft's 402 requirement removed from check 6's claims; listed as not scored | sections 4.6, 9.4 | S23-Check6QuoteNotExercised |
| Check 7 retitled to what it tests | section 4.7 | S22-Check7TitleClaim |
| Census count corrected to 49 unconditional and 2 conditional (superseded: 47, all unconditional, at revision 0.4) | section 4.8 | S20-CensusCount |
| Each cell's kind named (network-enforcement detector; library or service behaviour; descriptive) | section 4.9 | S04-ByConstructionCells |
| K rule disclosed as fixed after the exploratory data; per-cell K table at freeze; interval described, not a rate | section 6, 6.1 | S14-KDoublingForkingPath (wording); S02-WilsonVersusNoRate |
| Payment-identifier extension advertised in check 5b only | section 7.6 | S19-ExtensionConfigContradiction |
| Formal limitation on what a VIOLATED result establishes; per-rail evidence limits | sections 9.3, 9.5 | S16-ScopeOverclaim; S30-R9HistoryRetention; S31-R11WalletViews |
| A cross-rail non-comparison sentence added to the display rule | section 11 | S15-RankingLeakage (one sentence; founder veto not exercised) |
| Frozen set lists settlement assets, endpoints and the run's timing and mode values | section 16 | S18-FrozenSetOmissions |

### Revision 0.3 (2026-10-30), the nine round 1 rulings

Each change names the ruling (founder, 2026-10-30) and the review surfaces it answers.

| Change | Where | Ruling | Surfaces |
|---|---|---|---|
| Version line | header | all | |
| Seven checks stated as six conformance checks and one descriptive (check 3); five recorded invariants named; "measured" points at section 10's labels | section 1 | 4, 9 | S03, S17, S24 |
| Exploratory data sets only K (6e's conditional scope removed) | section 1 | 5 | S13 |
| 2a: any 2xx or delivery on the second presentation is VIOLATED; 2b on R11 descriptive (SECOND TRANSFER), never VIOLATED; no confirmatory hold invoice | section 4.2 | 3 (f), 5 (a) | S07, S11 |
| Check 3 marked descriptive, outside the conformance count; "measured, observed"; no interval; never moves a Half A label | section 4.3 | 4, 6 | S03, S17, S02 |
| Check 4 retitled; positive control per block; 4a on R11 scored on the seller's refusal of the late credential; R10 and R11 death reads MEASURED, never documented | section 4.4 | 3 (e), 3 (h), 5 (b) | S06, S09, S10 |
| 5b: a third same-payload presentation; two outcomes, value and response (409) | section 4.5 | 3 (g), 9 | S08, S24 |
| Check 6 retitled; 6e removed; pre-registered recovery procedure; safety outcome (at most one transfer) and recovery outcome; harness re-payment recorded; indeterminate state VIOLATED on R1, R2, R9 only at the finalized level, a confirmation of the documented gap on R10 and R11 | section 4.6 | 3 (h), 3 (j), 5 (c) | S09, S13, S25 |
| Check 7: reported success with a transfer is HELD; other combinations by section 5.7 | section 4.7 | 3 (f) | S07 |
| Census 50 cells, 49 unconditional, 1 conditional (5b on R1); 6e a statement of ignorance (superseded: 47, all unconditional, at revision 0.4) | section 4.8 | 5 (c) | S13, S20 |
| Cell kinds: 2b on R11 descriptive; 6e removed | section 4.9 | 4, 5 (a) | S04, S11 |
| New section 4.10, five recorded invariants, counts only | section 4.10 | 9 | S24 |
| Identical-protocol qualifier replaced by one stating what is identical and what is not, verbatim; the gate sentence kept verbatim; the mechanism list kept as its own sentence | section 5 | 2 | S01 |
| Indeterminate state never decided at the one-block margin | section 5.2 | 3 (h) | S09 |
| Violation evidence wins; V3 corroborated; V5 defined per rail (NOT VERIFIED until stage 2); V6 action not delivered; replacement attempts and the 2K completion rule (the re-run-once rule is superseded by it) | section 5.3 | 3 (a), 3 (c), 3 (i), 3 (k) | S05, S06, S17, S26 |
| The sweep re-reads every non-VIOLATED repetition, voids included; live-versus-final annotation | section 5.4 | 3 (b), 3 (l) | S05, S29 |
| Records carry NOT EXERCISED and the cell kind | section 5.5 | 3 (d) | S06 |
| New section 5.6, attribution (reason strings NOT VERIFIED until stage 2) and window open | section 5.6 | 3 (d), 3 (e) | S06, S27 |
| New section 5.7, exhaustive outcome tables, unclassified states VIOLATED | section 5.7 | 3 (f) | S07 |
| K rule tightened, wording verbatim; no interval on descriptive cells or invariants | section 6 | 6, 7 | S14, S02 |
| Section 8 rewritten as a statement of ignorance; the shakedown still attempts the hold-invoice sequence and reports it | section 8 | 5 (c) | S13 |
| Held payments and the 402 rule (now a recorded invariant) in the unmeasured list | section 9.4 | 5 (c), 9 | S13, S23, S24 |
| Analysis plan reports attempts, NOT EXERCISED, completeness and both outcomes of 5b and check 6; the three measured labels | section 10 | 3, 4 | S17 |
| Display rule: the qualifier reference shortened; no layout rule added (ruling 8: the layout left to the publication decision) | section 11 | 2, 8 | S01, S15 |
| Shakedown in one named folder; the hold-invoice sequence attempted and reported | section 12 | 5 (c), 7 | S13, S14 |
| Frozen set: reason strings, outcome tables, V5 reads, the shakedown folder's hashes; 6e values removed | section 16 | 3, 5 (c), 7 | S06, S07, S13, S14, S26 |

### Revision 0.4 (2026-10-30), the stage 2 ruling on check 5b

Ruling (founder, 2026-10-30, accepting the recommendation on the stage 2 interim report's decision 1): check 5b becomes a statement of ignorance on R1, R2 and R9, with the draft sentence verbatim; the section 4.10 cached-response invariant is removed; 47 cells, all unconditional; no payment-identifier configuration in any seller. Surface: S04 (a check of the company's own code is a check by construction), raised by the stage 2 build.

| Change | Where |
|---|---|
| Version line; four recorded invariants | header, section 1 |
| Check 3 note: no check runs with the extension | section 4.3 |
| Check 5 retitled; the executed cells and claims for 5b removed; 5b a statement of ignorance with the evidence from the pinned packages and the specification quoted | section 4.5 |
| Census 47 cells, all unconditional | section 4.8 |
| 5b removed from the library-behaviour kind | section 4.9 |
| The cached-response invariant removed; four invariants | section 4.10 |
| "payment identifier" removed from the attribution mechanisms | section 5.6 |
| Expected size 470 repetitions | section 6 |
| No seller advertises the extension | section 7.6 |
| The payment-identifier half of RetrySafety listed as unmeasured | section 9.4 |
| 5b removed from the analysis plan and the frozen set | sections 10, 16 |

### Revision 0.5 (2026-11-04), the gauntlet round 2 repairs and the founder's rulings of 2026-11-04

Rulings (founder, 2026-11-04): counts only, no interval (question 5); the four other round 2 questions ruled as recommended (check 6 safety numerator; check 7 per rail; the facilitator verify message disclosed; three table rows); question 6, a terminal state read on R10 or R11 and later contradicted is VOID with cause; question 7, R11 lateness read by both the payer's and the seller's clock with a margin of 5 seconds; question 8, the below-seller cell's reason stated beside each result of 1a and 4a on R2 and R9 as an annotation, not a gate. Repairs: the round 2 disposition (`paybench/dim4-half-b/gauntlet/r2/disposition-r2.md`), labels R2-A1 to R2-A15 and surfaces F, G, I, J, K and M, each checked against the code.

| Change | Where | Ruling or repair |
|---|---|---|
| Version line; method counts only, with a fresh compliance read before publication | header | 5 |
| R11 lateness by both clocks with a 5 second margin; the lateness record; NOT EXERCISED without it | section 4.4 | 7; R2-A12, I |
| Landed-and-failed with no transfer is a death observation on every rail; a not-yet-dead first read is VOID | section 4.4 | 4 |
| Safety counts the original artefact only; re-payment a recovery cost; both outcomes always recorded; contradicted reads VOID on R10 and R11, VIOLATED on R1, R2 and R9 only at the finalized level; the sweep re-reads dead reads; undecided below finalized VOID | section 4.6 | 1, 6; R2-A1, R2-A3 |
| Per-rail sentence; success with exactly one transfer HELD, more than one VIOLATED; pending then one transfer HELD with an annotation; disagreement is violation evidence ahead of the voids; no report VOID; broadcast recorded | section 4.7 | 2, 4; R2-A4, R2-A5, R2-A7 |
| Six descriptive cells, 41 in the conformance count | section 4.8 | census of the cells (gauntlet round 2) |
| R2 cap counted over the subject entry of every record; `estimatedLedgerSeconds` to section 16; the cap plus 2 ledgers tolerance beside the count | section 4.10 | F |
| Violation evidence widened; V2 before V3; V3 needs log and outside read to agree; new voids (control missing, not yet dead, undecided, contradicted, internal inconsistency, descriptive reading missing) | section 5.3 | 4, 6; R2-A1, R2-A2, R2-A7, R2-A11, R2-A14 |
| Every VIOLATED carries the sweep count; no report without a sweep | section 5.4 | R2-A9 |
| Reason entries verbatim, case-sensitive, VERIFIED only, the carrying entry recorded; a cell without a mechanism refused; the disclosure and the below-seller annotation; check 4 control missing and lateness | section 5.6 | 3, 8; R2-A12, R2-A13, R2-A14, R2-A15, K |
| Unclassified reported apart from divergences | sections 5.7, 10 | M |
| No interval; the scorer pinned in the K table; the re-run discipline after a logic change | section 6 | 5; G |
| The warmup payment disclosed as not built | section 7.2 | M |
| Analysis plan counts only, with recovery cost, disclosure and annotation | section 10 | 1, 3, 5, 8 |
| Scorer mutants and the per-rail read-path control named | section 13 | J; the read-path proof |
| Reason entries, `estimatedLedgerSeconds`, the R11 margin and the scorer pin in the frozen set | section 16 | 7; F, G, K |
| Superseded census counts marked in this appendix | Appendix C | M |

Not applied in revision 0.5, and stated in the stage report: R2-A10 (binding each counted transfer to the artefact's own identifier on R2, R9, R10 and R11, and recording the identifiers) changes every runner's read interface; the windowed count with the per-rail sweep stands until then. Ruled in revision 0.6 (founder, 2026-11-05, ruled against the recommendation: the windowed count stays, with a disclosure, and check 6 counts by identifier).

### Revision 0.6 (2026-11-05), the founder's rulings on the stage 3 shakedown report

Rulings (founder, 2026-11-05): first, the check 4 short window is one that passed the rail's positive control in every shakedown block run at that value, with an observation-only R2 sentence in section 16; second, the warmup payment removed and the first repetition scored like every other; third, the windowed transfer count kept with a disclosure, and the re-payment's transfers recorded by their own identifier on check 6 once the check 6 re-run was costed; then, on the cost, the check 6 re-run approved. The scorer stays at version 0.5; the check 6 runner logic changed on all five rails (below).

| Change | Where | Ruling |
|---|---|---|
| Version line | header | 1, 2, 3 |
| The short window is one that passed the rail's positive control in every shakedown block run at that value, not "the shortest each pinned server accepts" | section 4.4 | 1 |
| The window-count disclosure: R2, R9, R10 and R11 count transfers inside the read window, with the sweep's re-count | section 5.3 | 3 |
| The warmup payment removed; the first repetition scored like every other | section 7.2 | 2 |
| The R2 check 4 window observation, observation only | section 16 | 1 |
| Every rail's runner mutants in a committed script, re-run whenever that rail's runner changes | section 13 | the founder's ruling of 2026-11-06 to restore the R1, R10 and R11 runner mutants into committed scripts and re-run them against the current runners, section 13 requiring every rail's runner mutants to be committed scripts, re-run whenever a runner changes |
| Check 6 counts the original artefact's and the re-payment's transfers each by its own identifier on every rail, records both, and reads both directly; an unreadable bound count is VOID | sections 4.6, 5.3 | 3; the founder's follow-on of 2026-11-05 approving the check 6 re-run and asking that the same change record the original payment's transfers by its own identifier on every rail where one exists, so the scorer reads both counts directly |

Filled on 2026-11-06 (no ruling changes a cell): section 6.1's per-cell K table and section 16's values (run configuration, cost per payment, assets and endpoints, lockfiles, the scorer pin and folder hashes, the reason entries), computed by `poc/dim4-half-b/halfb/freeze_values.py`; section 6 states that a check 6 cell is unanimous only when its ten agree on both outcomes, the reading under which 6a-R10 and 6c-R10 take K = 20; section 12's "K = 10 throughout" corrected accordingly.

The check 6 change alters the check 6 runner logic on all five rails, so under the re-run rule every check 6 cell (15 cells) is re-run before the freeze; the scorer is unchanged, since it already read both counts when a record carried them. Every rail has an identifier, R11 included (the payee's completed transfer carries its invoice's payment hash, verified read-only against the ten check 6 records of the shakedown).

### Revision 0.7 (2026-11-06), the founder's rulings on the filled sections 6.1 and 16

Rulings (founder, 2026-11-06): ruling 1 keeps section 6's reading (a check 6 cell is unanimous only when its ten agree on both outcomes; 6a-R10 and 6c-R10 at K = 20), with the two R10 no-resource repetitions read to their cause from the seller logs before the freeze and the draft stating how a paid re-payment with no resource is reported; ruling 2 builds section 7.4's funds rule as written, after gauntlet round 3. Gauntlet round 3 runs on version 0.6 (`paybench/dim4-half-b/gauntlet/r3-prompt.md`, sha256 fd6a59077a9181f5ba0343669bc3b565e32a5c19ffaa7bf76006dce57707a93c).

| Change | Where | Ruling |
|---|---|---|
| Version line | header | 1 |
| The "paid re-payment, resource not obtained" line: counted, named, with the seller's answer and the network's read, never toward safety | sections 4.6, 10; `halfb/report.py`, with a positive and a negative control (`tests/test_v05.py`, PaidRepaymentNoResource) and a scorer mutant | 1 |
| The cause of the two R10 no-resource repetitions, from the seller logs and the network | section 12 | 1 |

The report line changes no fault, procedure, cell or scoring rule (the scorer files and their pin are unchanged), so no shakedown cell is re-run.

### Revision 0.8 (2026-11-06), the founder's rulings on the gauntlet round 3 questions and the confirmed round 3 repairs

Rulings (founder, 2026-11-06, accepting the recommendations, the R10 question included): question 2 (R3-02), a contradicted dead read on R10 is decided by the receipt's block timestamp; question 3 (R3-05), a served presentation on 2a and 4a is violation evidence ahead of the voids, with the row stating per rail what the quoted sentence bounds; question 4 (R3-03 and R3-25), the two internal-inconsistency voids added; question 5 (R3-15), the Bitcoin block seed; question 1 (R3-01), conditional on a verbatim read of the specification texts, then per rail: on R11 a paid re-payment that does not obtain the resource within the invoice's expiry fails the repetition, and on R1, R2, R9 and R10 it is the named line under the label rule and never fails it. Repairs: the round 3 disposition (`paybench/dim4-half-b/gauntlet/r3/disposition-r3.md`), items R3-04, R3-06, R3-07, R3-09, R3-12, R3-13, R3-14, R3-16, R3-17, R3-18, R3-19, R3-20, R3-22, R3-23, R3-24, R3-26 and R3-28, each with its control and mutant where it touches code; section 7.4 built (ruling 2 of 2026-11-06). Scorer version 0.8.

| Change | Where | Ruling or repair |
|---|---|---|
| Version line | header | all |
| The R11 clock is the `Date` header of the block-height endpoint's response | sections 4.4, 16.3 | R3-09 |
| A served late presentation on 4a is VIOLATED and is violation evidence | sections 4.4, 5.3 | question 3 |
| A paid re-payment without the resource: the seller's answer recorded; per rail, R11 VIOLATED within expiry (line 332 quoted), R1, R2, R9 and R10 the named line and the label rule, with the source sentences quoted and both readings of the Tempo text stated | sections 4.6, 10; `halfb/outcomes.py`, `halfb/report.py`, every runner | question 1 |
| A contradicted dead read on R10 decided by the receipt's block timestamp, live and in the sweep; R11 keeps VOID | sections 4.6, 5.3; `outcomes.py`, `runners/r10/cells.mts`, `halfb/sweep.py` | question 2 |
| An unreadable bound count is V2, never a window proxy; the pre-0.5 fallback counts a paid re-payment whether or not served | section 4.6; `outcomes.py` | R3-04 |
| Two internal-inconsistency voids: check 6 counts not summing; check 7 pending resolving to none while one is found | sections 4.6, 4.7, 5.3; `outcomes.py` | question 4 |
| Check 7's title restated per rail | section 4.7 | R3-07 |
| Cell kinds relabelled: 1a on R1, R2, R9 and 6a, 6c on R10 network-enforcement; 4a and 6a on R11 library or service behaviour | section 4.9 | R3-24 |
| The window gate names check 3 | section 5.6 | R3-28 |
| A neither read without its level is V2, not "undecided below finalized" | section 5.3; `outcomes.py` | R3-28 |
| K text matches the code (fewer than ten valid takes K = 20 whatever the attempts); `versions.py` in the scorer pin; the re-score-not-re-run rule and the two-record exception | sections 6, 16.5; `report.py` | R3-12, R3-06, question 1 |
| Every cell judged on a later folder named with its earlier folder's K | section 6.1 | R3-11 |
| The funds rule built: readings, projection, fee wallets, a check 7 drain scope, unread balances stop, a confirmatory block refused without it | section 7.4; `halfb/funds.py`, `halfb/orchestrator.py`, `halfb/balances.py` | ruling 2 of 2026-11-06; R3-08 |
| The R2 facilitator stated as operated | section 7.6 | R3-28 |
| R11's evidence limit beside every R11 result; V6 voids with a settled payment counted | section 10; `report.py` | R3-22, R3-23 |
| The R2 30 second window episode as an exploratory finding; the fault log field renamed `send_call_returned` | section 12; `runners/r10/seller.mts` | R3-16, R3-18 |
| Controls and mutants for every rule above; R2's runner mutants on the shared runner, unmutated copy first; the R11 two-clock rule, the margin and identifier binding on R2, R9 and R11 mutated | section 13; `tests/test_v08.py`, the runner suites and mutant scripts | R3-19, R3-20 |
| The seed is a Bitcoin block hash read from two sources with six confirmations; the schedules' hash moves to the pre-run commit | sections 16, 16.1; `halfb/seed.py` | question 5 |
| The 6a access-log wait and the check 4 windows tried entered | section 16.1 | R3-23, R3-16 |
| R10's AlphaUSD cost entered and read | section 16.2 | R3-08 |
| The R1 token's verified source and the R2 asset's contract identifier entered; the folder hash check refuses an unlisted file | sections 16.3, 16.5; `halfb/freeze_values.py` | R3-14, R3-26 |
| R1 hash-pinned lock | section 16.4; `poc/rail-x402-base/requirements.lock` | R3-13 |
| The R10 expiry entry's three circumstances | section 16.6 | R3-17 |

Not changed, as the disposition proposed: R3-10 (follows question 1), R3-21 (ruling 8 of 2026-11-04 stands), R3-27 (the qualifier stays beside every presentation), R3-29 (re-verified at the freeze), and the refuted R3-30 to R3-34. No shakedown cell is re-run: every record carries the fields the version 0.8 rules read, except the two of question 1, which the founder's ruling keeps as they are; the re-score under scorer 0.8 changes no outcome.

### Revision 0.9 (2026-11-08), the founder's rulings on the gauntlet round 4 questions and the round 4 fixes

Rulings (founder, 2026-11-08, both round 4 questions ruled as recommended): round 4 question 1 (R4-01), keep the 402-only failure on R11 and say why; round 4 question 2 (R4-02), widen the named line to any payment for the challenge that moved value while the resource was not obtained, keyed on the bound counts, named "paid, resource not obtained", with the section 10 label rule following. Fixes: the round 4 disposition (`paybench/dim4-half-b/gauntlet/r4/disposition-r4.md`), items R4-03 to R4-13, and R4-14's internal inconsistency (a re-payment count with no re-payment recorded), each with its controls and scorer mutants; the repair list of 2026-11-08 (the R11 contradiction mutant caught by an assertion). Scorer version 0.9.

| Change | Where | Ruling or fix |
|---|---|---|
| Version line | header | all |
| On R11 only a 402 to a paid, in-expiry re-payment fails the repetition; any other error is the text's own payment-loss path and the named line (lines 337 to 340 and 405 to 407 quoted) | section 4.6; `halfb/outcomes.py` (`REJECTION_STATUS`) | round 4 question 1 |
| The named line "paid, resource not obtained": any payment for the challenge with a bound count of one or more and the resource not obtained, keyed on the counts, each entry naming which payment moved; the label rule follows | sections 4.6, 6, 6.1, 10; `outcomes.py` (`paid_no_resource`), `halfb/report.py` | round 4 question 2 |
| The R10 timestamp rule reads a dead read only | sections 4.6, 5.3; `outcomes.py` | R4-03 |
| The indeterminate state is a recovery failure (safety HELD, recovery VIOLATED), decided without a window count | section 4.6; `outcomes.py` | R4-04 |
| No fallback count for a record that binds the counts; the line prints the counts as recorded | section 4.6; `outcomes.py`, `report.py` | R4-05 |
| A sweep VOID is counted as a sweep reclassification | section 5.4; `outcomes.py` | R4-06 |
| A dead read whose record finds the original's transfer is a contradicted read, flagged or not | sections 4.6, 5.3; `outcomes.py` | R4-07 |
| A confirmatory check 6 record without `original_id` is V2 | sections 4.6, 5.3; `outcomes.py` | R4-08 |
| On R11 a 402 whose presentation's expiry was not recorded is V2 | sections 4.6, 5.3; `outcomes.py` | R4-09 |
| R10 sweep hashes compared case-insensitively | `outcomes.py` | R4-10 |
| "sweep not read" counted per cell | sections 5.4, 10; `report.py` | R4-11 |
| Safety and recovery totals per check 6 row; void cause and counts on each line entry | sections 4.6, 10; `report.py` | R4-12 |
| The R11 rule is an outcome-table row pre-empted by a void; the harness host's clock; docstrings; the sweep subtraction wording | section 4.6; `outcomes.py`, `report.py` | R4-13 |
| A re-payment count with no re-payment recorded is an internal inconsistency | sections 4.6, 5.3; `outcomes.py` | R4-14 |
| The R11 contradiction mutant caught by an assertion; a mutant counts as caught only by a failing assertion | section 13; `outcomes.py` (`FINALIZED_LEVEL.get`), `tests/scorer_mutants.py`, `tests/runner_mutant_copy.py`, `tests/r9_runner_mutants.py` | repair list of 2026-11-08 |
| Controls and mutants for every rule above | section 13; `tests/test_v09.py`, `tests/scorer_mutants.py` | all |
| The K table re-entered under scorer 0.9 (unchanged); the scorer pin; H entered | sections 6.1, 16, 16.1, 16.5; `evidence/freeze-values-2026-11-08-v09.json` | all |

Not changed: R4-15 (confined by R4-08), R4-16 and R4-17 (refuted), R4-18 (already ruled), R4-20 (agrees with the draft). R4-19 was held for a word, since the go named R4-03 to R4-13, and is applied at the freeze preparation below. No shakedown cell is re-run: every rule reads fields the records already carry; the re-score under scorer 0.9 changes no outcome, safety, cause or rule of any of the 809 records, and the K table is unchanged.

### Freeze preparation (2026-11-08)

A drafting decision of 2026-11-08, not a founder ruling, on three gaps found while preparing the freeze, and on R4-19. None changes a measurement or a scoring rule.

| Change | Where | Item |
|---|---|---|
| Version line | header | all |
| What a check 6 safety HELD observes on each rail, and what it does not separate | section 9.5 | R4-19 |
| The per-rail runners inside the anchored harness hash: a runner edited after the freeze refuses a confirmatory start | section 16; `halfb/orchestrator.py` (`HARNESS_DIRS`) | F1 |
| The anchored configuration hash covers the configuration's frozen part (every field except the seed, the block number and the run folder); a confirmatory block is block 1 or 2, names the seed's block height, and its seed must be that block's hash as read from both sources at its start | sections 16, 16.1; `orchestrator.py` (`frozen_config_sha256`) | F2 |
| A confirmatory driver that builds each rail's configuration from the frozen values alone and refuses without both anchored values; built and tested, never run | section 16; `halfb/confirmatory.py` | F3 |
| The frozen configuration sha256 per rail entered | section 16 | F2, F3 |
| The line citation "405 to 406" corrected to "405 to 407" in two comments of `outcomes.py`; the K table re-entered under the new scorer pin (unchanged) | sections 6.1, 16.5; `evidence/freeze-values-2026-11-08-v09-freeze.json` | the freeze-preparation check of 2026-11-08 |
| Controls and mutants for F1 to F3 | section 13; `tests/test_freeze_prep.py`, `tests/scorer_mutants.py` | F1 to F3 |
| The OSF-independence sentence, as in the DIM-01 and DIM-02 pre-registrations | section 15 | the freeze preflight, gate 5 |

### Confirmatory order (2026-11-09)

The founder's ruling of 2026-11-09 on the confirmatory order. The draft's single order over all cells did not match the harness, which executes one rail per run; the ruling keeps the harness's shape, the shakedown's. None changes a measurement or a scoring rule.

| Change | Where | Item |
|---|---|---|
| Version line | header | all |
| One seeded order per rail and block, the five rails running their blocks at the same time, each rail's second block starting when its first ends | section 7.1 | the founder's ruling of 2026-11-09 on the confirmatory order |
| Two blocks per rail; a rail stopped by the funds rule resumes alone while the others continue | section 7.2 | the founder's ruling of 2026-11-09 on the confirmatory order |
| The seed tool draws and hashes the ten per-rail block schedules the driver executes, the K values read by cell from the frozen K table (it had read the file's top-level keys, so every cell would have defaulted to K 10); a table that does not name every cell and nothing else is refused | sections 13, 16, 16.1; `halfb/seed.py` | the freeze-preparation check of 2026-11-08 |
| Controls and mutants for the per-rail schedules | section 13; `tests/test_freeze_prep.py`, `tests/scorer_mutants.py` | the founder's ruling of 2026-11-09 on the confirmatory order |
