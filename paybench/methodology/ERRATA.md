# PayBench methodology — errata & clarifications (public, append-only)

The pre-registered methodology of record is **frozen and cryptographically anchored** per dimension and is
never edited in place — that immutability is the point of the freeze. Corrections and clarifications that
arise *after* a freeze are therefore published here, as a dated additive layer that references (but does not
alter) the anchored byte-set. Each entry states what was anchored, what the issue is, the resolution, and any
follow-on artefact. This file is itself not part of any frozen manifest.

**Anchored baselines referenced below**
- **Dimension 1 — settlement-finality (v1.2).** Manifest `prereg-manifest.sha256` =
  `a5f6feb46819dc3926012a8a38ac519cd0d5df33c20734516dca4b32d30d3a6f`; signed tag `paybench-prereg-v1.2`;
  Bitcoin block 952636; Rekor logIndex 1740328355; OSF registration DOI
  <https://doi.org/10.17605/OSF.IO/XGFUJ> (public since 2026-07-17).
- **Dimension 2 — authorization latency / RAPL.** Manifest `dim2-prereg-manifest.sha256` =
  `46a19eab516ef3214270513f718bd07a846e18a4f42d9916fcb829da71dcd388`; signed tag `paybench-rapl-prereg-v1`;
  Bitcoin block 955977; Rekor logIndex 2012836917; OSF registration DOI
  <https://doi.org/10.17605/OSF.IO/UFQG5> (public since 2026-07-17).

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

**Specification of the uniform-reliance cut (populated at the real-rail run).** The secondary race fixes one
common reliance target — **irreversibility** (value cannot be reversed), the strongest semantic shared by all
settling rails — and races every rail at *that* target instead of its own ecosystem-canonical bar. Mapping:
- x402-Base (R1): **hard L1 finality** (~minutes; the bridging/withdrawal threshold §3 excludes from the
  primary) — **not in the mock calibration; the real-rail run measures it.**
- x402-Solana (R9): **`finalized`** (already the primary bar; measured).
- x402-Stellar (R2): **ledger close** (deterministic ⇒ irreversible at close; already canonical).
- MPP-Tempo (R10): **BFT block finality** (deterministic; already canonical).
- MPP-Spark-Lightning (R11): **preimage release** (HTLC claim is irreversible; already canonical).
- AP2 (R6): excluded — does not settle independently.

Only Base has a distinct *softer* canonical bar, so the cut's effect is concentrated there: at
uniform-irreversibility Base moves from optimistic-soft (~2 s) to hard-L1 (~minutes), removing the "win bought
with a laxer bar" reading by construction (Base would rank last, not first). The cut is populated when the
real-rail run captures Base hard-L1; until then dim-1 publishes no rankings (Variant-E), so there is nothing
for it to mislead in the interim. The primary (per-rail-canonical) ranking is retained as the agent-DX default.

**Disposition.** Errata + reconciliation (this entry) now; the uniform-reliance secondary cut is a published
addition, not a re-freeze of the anchored finality byte-set. The governing split-vs-label rule above is added
to the cross-dimension consistency gate in `CEREMONY-PREFLIGHT.md` so the two dimensions cannot drift again.
Internal tracking: `gauntlet-r1-disposition-sheet.md` row **G-F1**.

---

## E2 (2026-06-30) — Network-latency results are "rail+facilitator-as-deployed", not rail-in-isolation

The scored network-group order in `dim2-scored-results.md` is produced with each rail pinned to a *different*
facilitator operator (Solana → x402.org, Stellar → OZ, Base → a Base-Sepolia-RPC-backed facilitator), and all
three topologies (T1 devbox / T2a Codespaces / T2b OCI) reach that **same pinned backend**. The within-group
order is therefore a property of **rail + facilitator as deployed**, not of the rail protocol in isolation, and
"robust across 3 topologies" means robust across three *agent vantages onto one fixed backend*, not across
backends. Read the order accordingly. The real-rail run will vary the backing-service leg (≥2 independent RPC
providers; self-hosted vs hosted) to separate rail from facilitator. Tracking: `gauntlet-r1…` **G-R3**.

## E3 (2026-06-30) — AP2 is timed under a lighter work-clause; not a topology-invariance control

AP2 (R6) is measured in-process via capture-replay with expiry/time-claim enforcement no-op'd, so its timed
window is offline signature verification and **excludes** the network credential/delegation-status resolution
that the anti-gaming work-clause (RR5) requires of the other Group-A rails (a fresh network state read). AP2's
Group-A figure is thus a thinner slice than its tablemates', and its apparent topology-invariance is an artefact
of the measurement boundary deleting the network — so **AP2 must not be cited as the FR4 topology-invariance
control.** The real-rail run will either apply RR5 symmetrically (include a fresh credential-status resolution)
or measure AP2 in its real sidecar topology. Tracking: `gauntlet-r1…` **G-R6**.

## E4 (2026-06-30) — The novelty claim is subject-level, not a new statistical method

The contribution is most accurately stated as **the first open, pre-registered benchmark *design* and instrument
for agent-to-agent payment rails** — not a novel statistical method. Every method primitive (Bradley-Terry,
pass@k, Wilson intervals, OSF/cosign/OpenTimestamps, content-addressing) is off-the-shelf; the doctrines
(reliance-level, the authorization split, group-and-decompose) are domain partitioning/labelling conventions,
and the split *ports* the ISO-8583 0100/0110 distinction rather than inventing it. The prior-art search backing
the "no prior comparative, pre-registered A2A-rail benchmark" claim will be committed (queries, sources, dates)
into the next manifest so the negative claim is auditable. The paper's "methodological contribution" framing is
aligned to this at the next recompile. Tracking: `gauntlet-r1…` **G-P1/P2**.

## E5 (2026-06-30) — The authorization split does not sum a rail's full cost

Because authorization is split into sub-rankings A and B that are never cross-raced, no scored number sums all
the legs a rail actually pays (e.g. x402 incurs B *then* A; the companion end-to-end metric is recorded but not
scored). A summed **end-to-end** ranking — pay-command → first reliance-grant, summing each rail's required
legs, with A/B retained as the decomposition — will be published as a co-reported secondary cut at the real-rail
run. Until then the split order should not be read as a rail's *total* authorization latency. Tracking:
`gauntlet-r1…` **G-R1**.

## E6 (2026-06-30) — What the mock harness validates (and what it does not)

The calibrated mock validates the **statistics layer** (Bradley-Terry / pass@k / Wilson over seeded populations)
and reproduction determinism — **not** the rail-adapter layer that extracts a timing number from a real rail
response (last-byte stopwatch, same-path RTT subtraction, the work-clause). Read "validated pipeline" as
"validated statistics layer." Golden-transcript adapter tests (recorded raw response → adapter → assert against
a hand-labelled timestamp — the pattern AP2 already uses via capture-replay) are deferred to the real-rail run,
when the adapters are final. A check of the pilot artefacts (2026-06-30) confirmed the T1/T2a/T2b runs logged
only *derived* samples (`accept_raw_s`, `challenge_raw_s`, `rtt_floor_s`, …), not the raw rail responses — so
golden-transcript tests cannot be backfilled from existing data, and the real-rail harness must additionally
**log raw rail transcripts** for that backfill to become possible. (AP2 is the one rail with replayable raw
captures today.) Tracking: `gauntlet-r1…` **G-P4**.

## E7 (2026-07-03): Freeze provenance clarifications (ceremony machinery, not methodology)

This entry records three process/provenance facts about the anchored freezes. None changes any methodology of
record or any anchored byte-set; all three were confirmed on 2026-07-03 by re-verifying against the tags with
`paybench/methodology/verify-freeze.sh` (byte-set, self-hash, OTS + Rekor digests all match for both dimensions).

**(a) The dim-1 and dim-2 freezes predate the gate-8/9 freeze-guard, so the guard reports LEGACY / BLOCKED.**
Both tags were anchored (`paybench-prereg-v1.2` on 2026-06-06; `paybench-rapl-prereg-v1` on 2026-06-29) before the
CEREMONY-PREFLIGHT gate-8 (pre-freeze gauntlet) and gate-9 (cross-dimension) attestation machinery existed (added
2026-06-30). Their `freeze-evidence/*.md` files were authored afterward and are `STATUS: LEGACY`; because the
evidence is not inside the tagged commit, `freeze-guard.sh` blocks the tags. This is honest, not a defect: neither
freeze can claim gate-8/9 PASS because the gauntlet post-dates it. Re-pushing either tag uses the documented
`PAYBENCH_FREEZE_OVERRIDE=1` path, and the freeze-guard CI job must NOT be a required status check while these
legacy tags exist or it will block legitimately. Every freeze from dim-3 onward commits its filled gate-8/9
evidence before tagging, so the guard passes without override.

**(b) The tagged freeze commits are now preserved on protected append-only frozen branches.** After later branch
rebases, the tagged commits were held only by their tags (`aeab0640` survived on `paybench/dim2-auth-latency`;
`3dd74caa` was on no branch at all). Append-only branches `paybench/dim1-frozen` (at `paybench-prereg-v1.2`) and
`paybench/dim2-frozen` (at `paybench-rapl-prereg-v1`) now pin the exact anchored commits and must never be rebased
or force-pushed.

**(c) The dim-1 signed-tag message carries a truncated manifest hash.** The `paybench-prereg-v1.2` tag message
records the manifest hash elided as `a5f6feb4…d3a6f`, not the full 64-hex digest; the dim-2 tag correctly records
the full `sha256:46a19eab…388`. The full dim-1 digest of record is
`a5f6feb46819dc3926012a8a38ac519cd0d5df33c20734516dca4b32d30d3a6f`; the manifest self-hash and both the
OpenTimestamps and Rekor proofs bind that full value, so only the human-readable tag message is abbreviated.
Future tag messages carry the full hash with no ellipsis.

**Disposition.** Provenance clarifications only; no re-freeze and no change to any anchored byte-set. Verify any
freeze from its tag alone with `paybench/methodology/verify-freeze.sh <tag>`.

**Update (2026-07-03, commit `5b84621e`).** The two grandfathered tags are now exempted by EXACT name at the top
of `ceremony-hooks/freeze-guard.sh`, so the local pre-push hook, the manual self-check, and `verify-freeze.sh`
allow them without `PAYBENCH_FREEZE_OVERRIDE=1` (this supersedes the override note in (a) above). New prereg tags
stay fully gated. The freeze-guard workflow can therefore be promoted to a required tag-ruleset workflow once
DIM-03 freezes with its gate-8/9 evidence committed in-tag; that promotion is intentionally not wired yet.

## E8 (2026-07-21): anchor robustness; the OSF leg is corroborating, not load-bearing

Each dimension's pre-registration is anchored three independent ways (the OSF registration DOI, an
OpenTimestamps attestation in the Bitcoin blockchain, and a cosign signature in the Rekor transparency
log), plus a signed git tag. These legs do not depend on each other: the Bitcoin and Rekor anchors commit
to the same manifest hash and are independently sufficient to prove the freeze date and byte-set even if
the OSF platform were unavailable, renamed, or discontinued. The frozen documents themselves cannot cite
their own DOIs (the DOI is minted at registration, after the byte-set is fixed, and an OSF registration
is immutable from submission), so the DOI-to-manifest linkage is published here and in the anchored
baselines above rather than inside any frozen file. Both registrations exited their planned Day-0
embargo on 2026-07-17 and are public; an independent copy of the dimension-1 attachments, including the
self-verifying `.ots` and `.cosign.bundle` proofs, is held at the Internet Archive
(<https://archive.org/details/methodology_202606>).
