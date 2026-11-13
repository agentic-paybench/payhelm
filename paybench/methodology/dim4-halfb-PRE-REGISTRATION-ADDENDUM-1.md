# Addendum 1 to the DIM-04 Half B test-network data pre-registration

Pre-registration: `dim4-halfb-PRE-REGISTRATION.md` on this branch, tag `paybench-dim4-halfb-prereg-v1`, OSF DOI 10.17605/OSF.IO/BMT8P (https://doi.org/10.17605/OSF.IO/BMT8P), called "the registration" below. This addendum is a new file; no frozen file is edited.

Dated 2026-11-12, written by Everyday AI Ltd (the company, below) after the confirmatory run of 2026-11-12 and before publication of any of its results. It records facts about the run and about the company's instrument. It changes nothing in the registration: no rule, K value, reason entry, scorer file or outcome is changed, and no record is re-scored.

Every time below is UTC on 2026-11-12. Rails are named by the display names of the registration's section 11. The run's files are named by the rail labels of the registration's section 3: R11 is Machine Payments Protocol on Lightning (Spark regtest), R10 Machine Payments Protocol on Tempo (Moderato testnet), R1 x402 on Base (Sepolia), R9 x402 on Solana (devnet, Alpenglow) and R2 x402 on Stellar (testnet). The harness code and the run's records are private; they are identified here by sha256, with paths relative to the private repository's `poc/dim4-half-b/` directory, as in the registration's harness manifest.

## 1. The refused start and the restart

**What the registration says.** Section 7.1: "the five rails run their blocks at the same time on the one vantage, each rail starting its second block when its first ends". Section 16.1: the seed is the hash of Bitcoin block 975500, "read before block 1 starts from two independent sources, https://mempool.space/api and https://blockstream.info/api, which must return the same hash, with at least six confirmations on both". Section 7.2 provides for a block stopped on the funds rule. The registration provides no rule for a start refused before any payment.

**What happened.**
- The launcher started block 1 of Machine Payments Protocol on Lightning at 01:42:01 and of x402 on Base at 01:42:00. Each driver begins with the seed read. For both rails, https://mempool.space/api answered `GET /api/block-height/975500` with HTTP 502. The driver read each source once, with no retry, and stopped. At 01:42:02 the launcher recorded both stops (`R11/launcher-output.txt` and `R1/launcher-output.txt`, line 19 of each).
- The driver stops before it takes the rail's lock or creates a block folder. No payment was made, and no record was written, for either rail.
- The other three rails read the seed from both sources (the same hash, 8 confirmations on each) and started block 1 between 01:42:04.91 and 01:42:04.97.
- The company's founder decided at 03:21:54 to restart the two rails with the same frozen code, the same seed and the same block schedules, launched one after the other so that their seed reads did not coincide. The decision also required the report to state the cause, both start times and the offset.
- Block 1 of Machine Payments Protocol on Lightning started at 03:22:55.63 and block 1 of x402 on Base at 03:22:36.36. Each read the same seed from both sources, with 16 confirmations on each, and each driver checked its rail's frozen configuration value (Machine Payments Protocol on Lightning 476889e5380146d3d74e7d2da73b8076c1e3650168eabd5a74694b06e5fa8b65, x402 on Base dd339644b1dbd27e282f848d8248822eab54c1e0f601eae641c9087b0d529b36) and the frozen harness value c45f5c1145f010e52a0e78736b8a0c5de8a6d2a5ba826bad420f90e646c7b170 before any repetition, as at every confirmatory start. Their offsets from the first block start of the other three rails are 1 h 40 min 51 s for Machine Payments Protocol on Lightning and 1 h 40 min 31 s for x402 on Base.

**The wait.** The time between the refused start and the decision was the wait for that decision; in it no code, configuration or file of the two stopped rails was changed, and only the three running rails wrote their records. The sources:
- The run's command log: its last entry before the decision, at 01:42:52, records the stop. The decision of 03:21:54 was received at 03:22:15; the next command ran at 03:22:23 and the first restart command at 03:22:29.
- The private repository's history: no commit on any branch between 01:42:03 and 03:22:30. The public payhelm repository's history has none either.
- File modification times in the private working tree: between 01:42:03 and 03:22:30 only files under the run folders of the three running rails changed (`R10/`, `R9/` and `R2/`). No file under `R11/` or `R1/` has a last change in that interval: each rail's `launcher-output.txt` was written at 01:42:02 and next appended at the restart.
- The records the drivers write carry no outcome. Outcomes are computed from the records by the report tool after the run, and during the run the drivers scored records only in memory, to decide replacements. No outcome of any rail had been displayed or written when the restart was decided.

**Consequence.** For Machine Payments Protocol on Lightning and x402 on Base, the run did not meet the design of section 7.1 that all five rails run their blocks at the same time: their hours of the day differ from those of the other three rails. For these two rails an effect of the time of day cannot be excluded. The report gives the start and end times of every block and the number of rails running in each stretch.

**The fault.** The seed read is the company's instrument (`halfb/seed.py`, sha256 in the registration's harness manifest). It makes one request per source with no retry. The registration's retry rule (section 5.2) covers reads of each rail's settlement and death evidence, not the seed read, so the instrument matched the registered text. It nevertheless let a single HTTP 502 answer from one source stop the start of two rails. This is a fault in the company's instrument, not in any network or source.

## 2. Five places where the frozen instrument and the frozen document disagree

None of the five changes any outcome, any valid repetition or whether any cell is complete. The only value that differs between the two outputs of section 3 is the K of two cells (2.1).

**2.1 The report tool and the K table file.**
- The registration: section 6.1 enters the K table from `evidence/freeze-values-2026-11-08-v09-freeze.json`. Section 6 says "the report tool refuses a K table whose pin differs from the scorer it runs".
- The code: `halfb/report.py` loads the file named by `--k-table` whole and passes it to `build()`. That function reads each cell's K as `k_table.get(cell, 10)` and the pin as `k_table.get("_scorer_sha256")`. The file holds the table, pin included, one level down, under the key `k_table`; its top-level keys are `cost_per_payment`, `folder_sha256_files`, `k_rows`, `k_table`, `scorer_sha256` and `scorer_version`.
- The effect: given the file, the tool printed K = 10 for every cell and did not run the pin check. Given the table under `k_table`, with no frozen file changed, the tool's `build()` function gives K = 20 for checks 6a and 6c on Machine Payments Protocol on Tempo, as section 6.1 enters them, and runs the pin check, which passes. No cell's completeness differs between the two outputs; the report gives the counts. The same fault was found in the seed tool at the freeze preparation and corrected there (registration, revision table "Confirmatory order (2026-11-09)"); the report tool was not corrected.

**2.2 The scorer's fingerprint.**
- The registration: section 6.1 names the scorer's fingerprint from before the freeze preparation, bfd23d11a912d6a4935625136f3e59000c1276feb33643be30d232523b878c5d, in the same paragraph that records its change. Section 16.5 names the frozen value, 52f53699f0b958699680efb39eea61c4289a7879b260b2d5f3370e0478e1a3c9.
- The code: the four scorer files hash to 52f53699f0b958699680efb39eea61c4289a7879b260b2d5f3370e0478e1a3c9, and the K table pins the same value.
- The effect: none. Every count comes from the frozen scorer.

**2.3 The evidence-limit text of the report tool.**
- The registration: section 10 requires, beside every result on Machine Payments Protocol on Lightning, its evidence limit (section 9.5) and "the unexplained wallet movements of section 12". Section 12 records one such movement: a rise of 408 sats during the hold-invoice sequence.
- The code: the tool's evidence-limit text (`R11_EVIDENCE_LIMIT` in `halfb/report.py`) cites section 12 for two movements. The second is from the company's exploratory records of the stage 3 shakedown's check 6 re-run of 2026-11-05 (folder `shakedown/2026-11-05-c6`), which section 12 declares; section 12 does not carry this movement.
- The effect: none on any count. The report states the limit in its own words and cites the registration only for what it carries.

**2.4 The kinds of five cells.**
- The registration: section 4.9 names checks 6a and 6c on Machine Payments Protocol on Tempo, and check 1a on x402 on Base, x402 on Solana and x402 on Stellar, as network-enforcement detectors.
- The code: `halfb/cells.py` omits these five cells from its list of network-enforcement detectors. Their records and the tool's output therefore label them "library or service behaviour".
- The effect: none. The scorer reads a cell's kind only to tell descriptive cells from the others, and these five cells are not descriptive under either label. The report gives the registration's kind.

**2.5 The cause text of NOT EXERCISED.**
- The registration: section 5.6 attributes a refusal by matching its recorded text against the frozen reason entries: "Each reason entry is a full phrase or a typed code copied verbatim from a recorded response, matched case-sensitively, with the record that showed it cited" and "Only VERIFIED entries attribute a refusal".
- The code: when no entry matches, the scorer records the cause as "refusal reason does not name the replay mechanism", followed by the recorded text.
- The effect: none on any count. That wording reads as a judgement of what the text means, whereas the scorer found that no frozen entry matched. The report words the cause from section 5.6: a refusal text not among the registration's reason entries.

**A note on the report, outside the five.** The registration's section 4.10 defines the core-draft invariant count over both Machine Payments Protocol rails together. The report gives it per rail, by the same counting rule applied to each rail's records separately, because the registration's section 10 admits no statistic that combines rails. This is a departure of the report from a registered definition, not a disagreement between the instrument and the document.

## 3. The analysis invocation

The registration does not print a command line for the report tool. The tool's own usage line, in `halfb/report.py`, is `python3 -m halfb.report <block_folder> [<block_folder> ...] --k-table <k.json> [--out <file>]`. Both commands below were run from `poc/dim4-half-b/` with Python 3.12.3. Each was re-run on 2026-11-12 after the first runs, and each reproduced its output byte for byte.

**A. The tool as given, with the K table file of section 6.1:**

```
/usr/bin/python3 -m halfb.report confirmatory/975500/R1/block1 confirmatory/975500/R1/block2 confirmatory/975500/R10/block1 confirmatory/975500/R10/block2 confirmatory/975500/R11/block1 confirmatory/975500/R11/block2 confirmatory/975500/R2/block1 confirmatory/975500/R2/block2 confirmatory/975500/R9/block1 confirmatory/975500/R9/block2 --k-table evidence/freeze-values-2026-11-08-v09-freeze.json --out report-tool-output-975500.json
```

Output A: `report-tool-output-975500.json`, sha256 04ad7e5dfa5cb258c069967f222820dd0ff3f7e175f74936303dac6f03cd13c7.

**B. The same frozen function, given the table under `k_table`. This invocation produced the published counts:**

```
/usr/bin/python3 -c 'import json,sys; from halfb import report; out=report.build(sys.argv[2:], json.load(open(sys.argv[1]))["k_table"]); sys.stdout.write(json.dumps(out, indent=2, sort_keys=False, default=str) + "\n")' evidence/freeze-values-2026-11-08-v09-freeze.json confirmatory/975500/R1/block1 confirmatory/975500/R1/block2 confirmatory/975500/R10/block1 confirmatory/975500/R10/block2 confirmatory/975500/R11/block1 confirmatory/975500/R11/block2 confirmatory/975500/R2/block1 confirmatory/975500/R2/block2 confirmatory/975500/R9/block1 confirmatory/975500/R9/block2 > report-tool-output-975500-frozen-k-table.json
```

It serialises the result exactly as the tool's `--out` does. Output B: `report-tool-output-975500-frozen-k-table.json`, sha256 b5fd66e86ed1b2976c9cb289d70c88f172edd4a685b14e1703c6116ad1bbbc57.

**How the two outputs differ.** In exactly two fields: `K` of cell `6a-R10` and `K` of cell `6c-R10` are 10 in output A and 20 in output B. Every other field of all 47 cells, and every top-level field, is equal. The equal fields include `scorer_sha256`: the tool prints the hash it computes whether or not it checked the pin, so neither output shows by itself whether the pin was checked.

**The inputs, by sha256.** The tool and the scorer files are those of the registration's harness manifest (`dim4-halfb-harness-manifest.sha256`, sha256 c45f5c1145f010e52a0e78736b8a0c5de8a6d2a5ba826bad420f90e646c7b170). Its 45 files were checked against it on 2026-11-12, and all 45 matched. The K table file is not in that manifest; its sha256 is pinned in `halfb/confirmatory.py`, which is.

| File | sha256 |
|---|---|
| `evidence/freeze-values-2026-11-08-v09-freeze.json` (the K table file) | cd460ac3d99e6a27616e913f06379488481bf725756d031c246fa83e46102fba |
| `halfb/outcomes.py` (scorer) | f8f5dbfe36a7726d4cabeec80648a170eb9f530d221abf8dbd6fba24a1415fa9 |
| `halfb/reasons.py` (scorer) | fa839575d1add4d5c7681b05ea9b9367f181f9aeb8b7f2d75af1e63f01c56f10 |
| `halfb/cells.py` (scorer) | b3939a77b19dc8e251f1ed5ad1dd9347491c2d0addce561513ed6b0d20668800 |
| `halfb/versions.py` (scorer) | 1b62033653c01869f9f8a064ce3217316c87535887e42c4e6261aa4860bee0e3 |
| `halfb/report.py` (the report tool) | e7657b9eda082d65d3985a04208e88b0bcda57a0533bc9f6a2b968dd93ab8810 |
| `halfb/invariants.py` | e4c1adf4c1baf4444cd2999107830721f7c39160f34dbb1c6b6dead12ebb5577 |
| `halfb/records.py` | 0837a8a691497595a381566d71470b79d83f8cec6e8da16821dd45f40b6f8194 |
| `confirmatory/975500/R11/block1/records.jsonl` | 573a23414a310f1923aafabd36def4abe75fdb692af69be89be1f644363fa027 |
| `confirmatory/975500/R11/block2/records.jsonl` | 45e031555c958b4c45c75aaf1a21bca07a26d9f1bafc64af73b2d5a4e8891409 |
| `confirmatory/975500/R10/block1/records.jsonl` | 22283d67ef420c075ec018601e591b5c03394fa8e1938ad5ffd938a150927d74 |
| `confirmatory/975500/R10/block2/records.jsonl` | 88cd17df99a6d335e71bf3389865fdf37492e234e8af3de530edee447cc6f99a |
| `confirmatory/975500/R1/block1/records.jsonl` | fd3fd960577ac8abc769de2dc97da83a2b13aa7f7fd689b6dddcdf5d70c0c9ca |
| `confirmatory/975500/R1/block2/records.jsonl` | 361694dd7f0e41b66418f7673e2aceecd7f3141c82ecabd3999f46962a1802b2 |
| `confirmatory/975500/R9/block1/records.jsonl` | 7a652128dbf74ff3c7296efee29d0f036cf33455d26dc18ebe87e75cdbe8c5e1 |
| `confirmatory/975500/R9/block2/records.jsonl` | 7e604d8b1c782bcf26f4f4385fa090a49e6af421547a50d5b098b95fd8b55e83 |
| `confirmatory/975500/R2/block1/records.jsonl` | 72983b3735cb4b89cc52a0eadbaf31fd19e084429a0729160fd6e64085ed2f66 |
| `confirmatory/975500/R2/block2/records.jsonl` | c04eeff6cf5379066a54a275c31aede70ae38072f49dce47816cadbd4c4d0731 |
| `confirmatory/975500/R11/block1/sweep.jsonl` | b0d26441e0f09f214439aa53a48075ed45fc2a0793a2a0ab106af36fa8252ea6 |
| `confirmatory/975500/R11/block2/sweep.jsonl` | b5866ddbda1a01b01124ef8d4fc9a67a1d9469bbcb6815ddeb545ec4eb089591 |
| `confirmatory/975500/R10/block1/sweep.jsonl` | a2072eb95fc66000c0e8d8551d2784f720ec882386fde75b1bb41d85f1682893 |
| `confirmatory/975500/R10/block2/sweep.jsonl` | 3358fc5c9ccb041ef267ae95823d864d9cd3def264e3d677813451bdee876781 |
| `confirmatory/975500/R1/block1/sweep.jsonl` | f86a632baa36099339a06b047ba316d08c46efe21a591748549a441129f2f536 |
| `confirmatory/975500/R1/block2/sweep.jsonl` | 4f3627174b414424b7a68479f30e31a7d0c9726a553470e1194a972625aa5530 |
| `confirmatory/975500/R9/block1/sweep.jsonl` | 0d6367f1c8d187d801ae0deeb1d05097429e2aa9f8f8ca0db0692e86b736635a |
| `confirmatory/975500/R9/block2/sweep.jsonl` | eb940220acb6c96c66da2ce0dea37bc48eac4c13f048dc17555515a87afa3eda |
| `confirmatory/975500/R2/block1/sweep.jsonl` | 95047ea45e40bbc952c6e49ceb9b2541fd2e0c31bce0f8ded7398e327210a7c8 |
| `confirmatory/975500/R2/block2/sweep.jsonl` | 7e7931b6496b5c39e48c5c7e0f9a65b9e2bab24b74de8f359fe5f1b579e55e89 |

Both outputs are kept unaltered by the company and are available on request; any copy can be checked against its sha256 above.

## 4. Check 2b on Machine Payments Protocol on Tempo

The registration's section 16.6 holds one replay entry for check 2b on Machine Payments Protocol on Tempo, `ExpiringNonceReplay`, VERIFIED from the exploratory record `R10/block1/2b-R10#1` of 2026-11-04. Under section 5.6 a refusal text that matches no frozen entry makes the attempt NOT EXERCISED; no entry is added after the confirmatory run (section 5 below). The report states every attempt of this check with the refusal text and node version recorded.

## 5. What is not done

- No block, cell or attempt is re-run.
- No reason entry is added. Section 5.6 freezes the entries before any confirmatory run.
- No scorer, report tool or harness file is changed, and no record is re-scored.
- No frozen file of the registration is edited.

The published counts are those of output B.
