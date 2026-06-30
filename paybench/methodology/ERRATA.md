# PayBench methodology — errata & clarifications (public, append-only)

The pre-registered methodology of record is **frozen and cryptographically anchored** per dimension and is
never edited in place — that immutability is the point of the freeze. Corrections and clarifications that
arise *after* a freeze are therefore published here, as a dated additive layer that references (but does not
alter) the anchored byte-set. Each entry states what was anchored, what the issue is, the resolution, and any
follow-on artefact. This file is itself not part of any frozen manifest.

**Anchored baselines referenced below**
- **Dimension 1 — settlement-finality (v1.2).** Manifest `prereg-manifest.sha256` =
  `a5f6feb46819dc3926012a8a38ac519cd0d5df33c20734516dca4b32d30d3a6f`; signed tag `paybench-prereg-v1.2`;
  Bitcoin block 952636; Rekor logIndex 1740328355.
- **Dimension 2 — authorization latency / RAPL.** Manifest `dim2-prereg-manifest.sha256` =
  `46a19eab516ef3214270513f718bd07a846e18a4f42d9916fcb829da71dcd388`; signed tag `paybench-rapl-prereg-v1`;
  Bitcoin block 955977; Rekor logIndex 2012836917.

---

## E1 (2026-06-30) — Reconciling the finality single-race with the RAPL split doctrine

**Where it arises.** `methodology.md` §3 (settlement-finality) races all rails in one Bradley-Terry model and
distinguishes their differing security models with a **trust / equivalence-class** label. `dim2-auth-latency.md`
§2.3 argues that for authorization a label "names a category error without removing it" and therefore *splits*
the authorization primitives into separate sub-rankings rather than labelling them. Read side by side these can
appear to contradict: *if a label is insufficient in dimension 2, why is it sufficient in dimension 1?*

**Resolution — the two doctrines key on different axes, and both are correct as written.** The RAPL split
criterion is a difference in the **kind of event/object being timed**, not a difference in security strength.
Per `dim2-auth-latency.md` §2.3, sub-ranking A times *validation of something the payer has already submitted*
("is this payment/mandate valid?") while sub-ranking B times the server *issuing a payable challenge before the
payer has committed anything* ("here is what to pay") — in ISO-8583 terms a `0100` request versus an earlier
protocol step. These are **different checkpoints in the protocol**: racing them in one model would compare
unlike events, which a label cannot cure, so they are split.

Settlement-finality presents no such event-kind difference. Every rail's finality figure measures the **same
event** — the single point of payment irreversibility / reliance — and the rails differ only in the **trust
class** (security strength) of that one checkpoint. A label is the correct instrument for a *trust-class* axis
and was never claimed to cure an *event-kind* difference; there is no event-kind difference in finality to
split on. The governing rule, stated uniformly: **split when the timed events differ in kind; label when the
same event differs in trust class.** Under that rule §3 and §2.3 are consistent, not contradictory.

**Residual concern, separately addressed.** A real and already-disclosed edge remains (`methodology.md` §3,
"this dimension's most exposed flank"): because each rail is pinned to its *own* ecosystem-canonical reliance
level, the thresholds are not equi-conservative, so a rail can place well partly by having a laxer canonical
bar — e.g. pass@2 admits optimistic-soft-commit Base (~2 s) while excluding `finalized` Solana (~14.6 s). The
per-rail-canonical doctrine is the right *agent-DX* default (it measures the moment each rail tells an agent it
may act) and is retained as **primary**. To let any reader see the order *without* the canonical-bar asymmetry,
a **uniform-reliance secondary cut** will be published alongside the primary at the next revision: the same
rails raced at a single common bar (uniform-irreversibility — Base hard-L1 vs Solana `finalized`, etc.). The
secondary does not replace the primary; it removes the "win bought with a laxer bar" reading by construction.

**Disposition.** Errata + reconciliation (this entry) now; the uniform-reliance secondary cut is a published
addition, not a re-freeze of the anchored finality byte-set. The governing split-vs-label rule above is added
to the cross-dimension consistency gate in `CEREMONY-PREFLIGHT.md` so the two dimensions cannot drift again.
Internal tracking: `gauntlet-r1-disposition-sheet.md` row **G-F1**.
