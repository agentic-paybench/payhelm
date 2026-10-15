# Freeze-evidence: paybench-dim1-testnet-prereg-v1 (settlement finality, DIM-01, test-network confirmatory run)

STATUS: PASS

GATE8-GAUNTLET: PASS
GATE9-XDIM: PASS

- **Dimension / manifest:** `dim1-testnet-prereg-manifest.sha256` = `ead93f13d06137e45e34d099a54d32079e0c1ac0d5abd894e4390bc0f7101707`
- **Tag:** `paybench-dim1-testnet-prereg-v1`  ·  **Freeze date:** `2026-10-14`
- **Frozen document:** `dim1-testnet-PRE-REGISTRATION.md` = `016d24f29b0465e89647ac910f0d3fd065fe393ccd9e23039a7e2cbf8c350993`
- **Harness and adapter hashes:** `dim1-testnet-harness-manifest.sha256` = `1a9d1445d5328f2c2408f24929a439c3b4e9f1e2938fd9d6d91dd005b04b3e15` (54 private files by sha256, paths relative to the private repository's `poc/` directory; the code stays private, by ruling of 2026-10-10)

The frozen document is the pre-registration's final revision with only the freeze-time edits: the draft header's instruction paragraph removed, the revision paragraphs kept as the appendix "Revision history", and the freeze markers filled. Values taken over the manifest itself (its hash and the anchor values) are kept out of the document, which the manifest covers.

## Gate 8: pre-freeze adversarial gauntlet (CEREMONY-PREFLIGHT section 8)

The break-it gauntlet ran before any anchor, in nine rounds from 2026-10-11 to 2026-10-14:
- four or five model lineages per round, each reviewer told to break the design, not agree with it;
- the last three rounds narrowed to the scoring tables;
- each round triaged by a disposition sheet into [GAP], [DOC] and [DISC], and every surviving [GAP] cured in a new revision before the next round.

Round 9 found two seams in the outcome table:
- one ruled by the founder: a terminal status-0 receipt takes precedence over unverifiable identifier;
- one cured mechanically: every runner reports by its payment's own primary-clock timeout.

Round 9 also raised wording items, all cured in the final revision. By the founder's ruling of 2026-10-14 there was no round 10. The final check was the founder's own reading of sections 5.3 and 5.5 of the final revision, which found no state claimed by two rows or by none.

- Result files: the nine disposition sheets, held privately beside the draft with the round prompts and every reviewer's output verbatim.
- Surviving GAPs: **none**.

## Gate 9: cross-dimension doctrine consistency (CEREMONY-PREFLIGHT section 9)

- Prior dimensions checked: DIM-01 v1.2 (`paybench-prereg-v1.2`) and DIM-02 RAPL (`paybench-rapl-prereg-v1`), under the split-versus-label rule of ERRATA E1.
- Reconciliation note: held privately beside the draft; its result, point by point:
  - (a) start of clock: a principled difference, stated. The primary start is the first unpaid request on every rail; DIM-02's `t = 0` is this run's companion interval, reported beside the primary.
  - (b) split versus label: consistent. One event kind is raced and the trust class is labelled, as in v1.2.
  - (c) R11's display name: a principled difference from the DIM-02 page, stated. It is "Machine Payments Protocol on Lightning (Spark regtest)", and every rail's name carries its test network.
  - (d) R9's reliance level under Alpenglow: a difference from the v1.2 table, stated. The clock ends at `finalized` as the network reports it, and R9 is a diagnostic outside the races.

## Gates 1 to 7 (CEREMONY-PREFLIGHT sections 1 to 7)

1. **Frozen-set completeness.**
   - `python3 -m dim1.orchestrator plan` on each of the four confirmatory configurations prints the same harness-manifest hash, `1a9d1445…5b04b3e15`, and the same master-schedule hash, `c9f94073…1c4add63`.
   - `sha256sum -c` of the harness hash list in the private `poc/` directory: 54 OK, 0 missing, 0 failed.
   - `sha256sum -c` of this manifest from `paybench/`: 2 OK.
   - The founder re-runs both at the freeze.
2. **Reproduction pinning.**
   - `python3 -m paybench.mockbench.cli run` reproduces the frozen v1.2 `run_hash` `sha256:895f99ed52567421a1d7e9068ab9a0d7147d6381ec137e1b130b805e63b14ee0` byte for byte.
   - The harness test suite passes (69 tests).
   - The founder re-runs both at the freeze.
3. **No dangling references.** Every identifier the document cites resolves in the harness code, its configuration or the pinned SDKs.
4. **Internal consistency.**
   - The SDK versions cited match the lockfiles and the R1 pip freeze.
   - "32-slot rooted" appears only as the quoted frozen v1.2 text.
5. **Required clauses.** The test-network watermark ("no value-bearing funds") and the OSF-independence clause ("independently sufficient") are both present.
6. **Frozen-doc hygiene.**
   - The body carries no status scaffolding and no working commit SHA.
   - Its dates are exploratory-run dates (required registration metadata), source and verification dates, and one decision-confirmed date.
   - The revision history appendix is kept by the gauntlet's round 1 ruling.
   - No em-dash or en-dash anywhere.
7. **Born-clean.** As gate 6.
