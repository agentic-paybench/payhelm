# Cross-dimensional knock-on + new-dimension checklist (from the D2 gate)

> Internal note, not pre-registered. Triggered by the dimension-2 cross-lineage gate
> (`dim2-adversarial-review.md`, 2026-06-22), which refuted the single-race authorization
> doctrine 0–4. Purpose: check whether D2's findings ripple into **frozen D1 (finality)** or the
> **future dimensions**, and distil the transferable lessons so the next dimension does not repeat
> the category error.

## 1. Knock-on to Dimension 1 (settlement-finality) — **FROZEN v1.2: no invalidation; vindicated**

No change to the anchored artefact is needed or permitted (it is OTS/Rekor/signed-tag frozen).
Specifically:

- **The L402 category error is authorization-specific.** D1 measures L402's *finality* (preimage
  release / Spark ceremony), a well-defined settlement point — not its authorization. No D1 error.
- **Finality is genuinely ONE shared concept** (irreversibility) across all rails. The D2 panel
  *explicitly* contrasted: finality has a shared cross-rail meaning, authorization does not. So D1's
  **per-rail-canonical reliance-level doctrine (D1-keep) is *vindicated* by the contrast**, not
  weakened — the per-rail approach is valid precisely *because* the underlying concept is shared.
- **D2's live-measurement critiques (t=0, network RTT, warm/cold, co-location) do not bite frozen
  D1.** D1 ships as **calibrated mock fixtures** (Variant E) — Monte-Carlo draws, *not* live network
  variance (§5.3 caveat) — so those run-time confounds are out of scope for the frozen methodology.
  D1 also already discloses the bundled `request → agent-perceived-finality` unit (F4), BT
  degeneracy under cluster separation (F6), and the log-normal default (F5).
- **Forward note (not a change):** when D1 is eventually run against **real rails** (the Q3 HELD
  residual), that *real-rail* run should adopt the §2-checklist below — but that is its own future
  pre-registration, separate from and not altering the frozen v1.2 methodology.

## 2. Knock-on to Day-60 **Fee Predictability** (future, not drafted) — **the real one**

Apply the **concept-unity check (below) BEFORE drafting**, because "fee" is a prime candidate for
the same trap: it may be **non-commensurable across rails** — gas fee (Base/Solana), ledger fee
(Stellar), routing/liquidity fee (Lightning), PSP/interchange fee (Tempo/Stripe), and AP2
(orchestration cost, no settlement fee). Racing these in one ranking could be the dimension-2
category error again. Likely outcome: a **SPLIT / sub-rankings** by fee *kind*, plus a standardised
definition of *what counts as the fee* (gross vs net, which legs included). Decide this up front.

## 3. Knock-on to Tier-2 factual lookups (fees/assets/custody/capability) — low

Not ranked, so the category-error risk is low; but the **fee-definition** standardisation overlaps
with Day-60 — define "fee" once, consistently, for both.

## 4. Reusable new-dimension checklist (distilled from the D2 gate)

Run this **before** drafting any new ranked dimension; it is what the D2 self-pass missed:

1. **Concept unity.** Is the measured quantity *one shared object* across all rails, or *multiple
   ontological kinds*? If multiple → **split into commensurable sub-rankings**; do **not** race them
   together under a trust/equivalence-class label (a label names a category error without curing it).
2. **Agent-perceived vs protocol-primitive.** Name which the metric is. If it is a protocol
   primitive (not what the agent experiences), say so in the title and add a **companion
   agent-observed metric** (and watch for fast-path inversion).
3. **Boundary standardisation (`t=0`).** Define the measured interval *identically* across rails
   (e.g. command-on-the-wire → checkpoint, measured at the rail edge), so no rail is advantaged by
   excluded work or network RTT.
4. **Real-rail measurement hygiene** (for the live run, not the mock harness): canonical client
   geography, published RTT floor, network-adjusted latency, warm-vs-cold pre-registration.
5. **Statistics fit the shape.** BT only *within* commensurable groups; **survival curves** for
   heterogeneous generative processes; k-grid in the **right magnitude regime**; an **assurance /
   quality covariate** (e.g. `P(settled | accept)`) so a rail cannot win by *doing less*.
6. **Gate it.** Cross-lineage adversarial review **before** ratification/pre-registration — D2 shows
   the self-pass alone misses category errors (the gate caught one the author defended).

## 5. Process / ceremony lessons (distilled from the D2 freeze + gauntlet)

These are not design lessons — they are about the *order and enforcement* of the freeze ceremony.
D2's ceremony went well but exposed an ordering gap worth not repeating:

1. **Gauntlet BEFORE freeze, not after.** The break-it gauntlet (round 1) ran *after* the D2 freeze,
   so its evidence can only honestly be marked **`STATUS: LEGACY`**, never `PASS` — the freeze
   pre-dates the adversarial pass that was supposed to harden it. This is the exact gap
   **`CEREMONY-PREFLIGHT` gate 8 (pre-freeze gauntlet)** now closes; the real-rail re-registration
   runs it in the right order and can legitimately mark `STATUS: PASS`. Freeze-order is: draft →
   gauntlet → disposition → freeze → anchor, not freeze → anchor → gauntlet.
2. **Check cross-dimension consistency at the gate.** The gauntlet caught **G-F1** — a finality↔RAPL
   split-vs-label inconsistency — reconciled in `ERRATA.md` E1 (split-on-KIND / label-on-CLASS). Hence
   **gate 9 (cross-dimension split-vs-label consistency)**: a new dimension's grouping/labelling must
   be checked against every already-frozen dimension, not just internally.
3. **Freeze the classifier, and enforce the freeze mechanically.** A committed
   `freeze-evidence/<tag>.md` attestation is enforced by a **pre-push hook + tag-immutability ruleset +
   freeze-guard CI** — so a `*-prereg-*` tag cannot be published without its gate-8&9 evidence. Trust a
   mechanical guard over ceremony discipline.

## 6. Workflow / knowledge-hygiene lessons (surfaced completing D2)

Not about the method at all — about how the work is recorded so the *next* session inherits reality.

1. **Launch sessions from the repo root.** The bulk of D2 ran with `claude` launched from the
   `dim2-auth-latency/` subdirectory, which Claude Code slugs to a **separate project** (its own
   transcripts, its own — here absent — memory dir), invisible to repo-root sessions. A mid-session
   `cd` does not fix it: the project key is fixed at launch. Launch from
   `agentic-paybench/payhelm/` so transcripts and memory land in the one project.
2. **When a dimension's status changes, update the in-repo status doc — don't rely on memory alone.**
   D2's completion facts propagated into per-project memory, but `SESSION-1-HANDOFF.md` was left saying
   "pre-registerable / founder-must-decide" for ~a week, so a fresh session reading the repo got a stale
   story. Status belongs in the repo (handoff + methodology); memory is a pointer, not the record. Close
   the loop on the doc at ratification/freeze.
3. **Per-project memory does not cross repos.** dim-1's arXiv work (done in the `mblake4u/agentpay`
   project) was invisible to `payhelm` sessions and got re-discovered. Cross-project ceremony knowledge
   lives in Notion (the "Pre-registration anchor ceremony" cheat sheet); check it + prior session logs
   before re-deriving a step.
4. **`main` is PR-gated.** Land `main` changes via PR; dimension work lands on `paybench/poc` first.
