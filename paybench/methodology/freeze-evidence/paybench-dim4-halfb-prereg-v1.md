# Freeze-evidence: paybench-dim4-halfb-prereg-v1 (DIM-04 Half B, conformance checks on five test-network rails)

STATUS: PASS

GATE8-GAUNTLET: PASS
GATE9-XDIM: PASS

- **Dimension / manifest:** `dim4-halfb-prereg-manifest.sha256` = `4c47841f943c4a8356cdc65ef79c3ebd19db0d7005e1a62b7f5851762995babb`
- **Tag:** `paybench-dim4-halfb-prereg-v1`
- **Frozen document:** `dim4-halfb-PRE-REGISTRATION.md` = `a6164fffafdab67911ae1c0d890d2fd085901c4a08c246233da86e5ade7128eb`
- **Harness hashes:** `dim4-halfb-harness-manifest.sha256` = `c45f5c1145f010e52a0e78736b8a0c5de8a6d2a5ba826bad420f90e646c7b170` (45 private files by sha256, paths relative to the private repository's `poc/dim4-half-b/` directory; the code stays private)
- **Values a confirmatory start checks:** the harness sha256 above; the frozen configuration sha256 per rail, R1 `dd339644b1dbd27e282f848d8248822eab54c1e0f601eae641c9087b0d529b36`; R2 `8f5062d67095748b273da9ced2a24d90e9752a9f8ba9ad781bf8a12e71fd2e83`; R9 `4e39dafd80bc46fa13266b72c7aa6bbe10446b3abe1a1d026b554e0d8d857140`; R10 `364437a01a3d41b8b68f3b6bba3156c49c40a2288233bb95c8d507badc4e8496`; R11 `476889e5380146d3d74e7d2da73b8076c1e3650168eabd5a74694b06e5fa8b65`; the seed's Bitcoin block height 975500

The frozen document is the pre-registration's final draft with only the freeze-time edits: the header's draft status replaced by the frozen status, and the drafting notes removed with the one body reference to them reworded. Values taken over the manifest itself (its hash and the anchor values) are kept out of the document, which the manifest covers.

## Gate 8: pre-freeze adversarial gauntlet (CEREMONY-PREFLIGHT section 8)

The break-it gauntlet ran before any anchor, in four rounds from 2026-10-30 to 2026-11-08:
- each reviewer told to break the design, not agree with it, across model lineages;
- the fourth round narrowed to check 6, the one check whose rules were still moving;
- each round triaged by a disposition sheet that checked every claim against the committed scorer, report tool, runners, source texts and shakedown records, and every confirmed item either cured in a new revision with its controls and mutants, or put to the founder and ruled.

Round 4's two reviewers differed (one "freeze after named fixes", one "do not freeze"); the disposition found that each blocking claim rested on a record state no runner can produce, or on a position the founder had ruled. The founder ruled the two open questions and the named fixes were applied in revision 0.9, with three freeze-preparation hardenings of the confirmatory start. The founder then ruled the confirmatory order (one seeded order per rail and block, the five rails running at the same time, the stage 3 shakedown's shape), and the seed tool was corrected to draw and hash the ten per-rail block schedules the driver executes, with its controls and mutants.

- Result files: the four disposition sheets, held privately beside the draft with the round prompts and every reviewer's output verbatim.
- Surviving confirmed items: **none**.

## Gate 9: cross-dimension doctrine consistency (CEREMONY-PREFLIGHT section 9)

- Prior dimensions checked: DIM-01 v1.2 (`paybench-prereg-v1.2`), DIM-02 RAPL (`paybench-rapl-prereg-v1`) and the DIM-01 test-network data pre-registration (`paybench-dim1-testnet-prereg-v1`), under the split-versus-label rule of ERRATA E1.
- Reconciliation note: held privately beside the draft; its result, point by point:
  - (a) split versus label: not engaged. Half B times nothing and races nothing; each cell is one rail's documented bound, reported as k of K, and no count is set beside another rail's as the same measurement.
  - (b) display names and order: consistent. The five rails carry the DIM-01 test-network display names, each with its test network, in the same fixed alphabetical order, with the ordering sentence and the same-protocol sentence the section 21 Level 1 gate requires.
  - (c) R9's reliance level: consistent. Half B's terminal read on R9 is `finalized` as the network reports it, as in the DIM-01 test-network run.
  - (d) the accurate claim: consistent. The design is frozen and anchored after declared exploratory runs and before the confirmatory run or any publication, the claim of every prior freeze.

## Gates 1 to 7 (CEREMONY-PREFLIGHT sections 1 to 7)

1. **Frozen-set completeness.** `sha256sum -c` of the harness hash list in the private `poc/dim4-half-b/` directory: 45 OK; `sha256sum -c` of this manifest from `paybench/`: 2 OK; `python3 -m halfb.confirmatory configs` prints the harness and configuration values above. The founder re-runs all three at the freeze.
2. **Reproduction pinning.** `python3 -m paybench.mockbench.cli run` reproduces the frozen v1.2 `run_hash` byte for byte (no payhelm code changes in this freeze); the harness suites pass, and every scorer and runner mutant is caught by a failing assertion. The founder re-runs the first at the freeze.
3. **No dangling references.** Every repository path the document cites resolves in the private repository at the freeze.
4. **Internal consistency.** The lockfile hashes of section 16.4, the scorer pin of section 16.5 and the frozen configuration values of section 16 equal the committed files.
5. **Required clauses.** The test-network watermark ("no value-bearing funds") and the OSF-independence clause ("independently sufficient") are both present.
6. **Frozen-doc hygiene.** No status scaffolding; no working commit SHA in prose; dates are run, source, verification and ruling dates; no em-dash or en-dash anywhere.
7. **Born-clean.** As gate 6.
