<!-- posture-class: level1-measurement -->
# Threshold-check report (v0.1 per-check format)

This directory writes a report in the v0.1 per-check format of the W3C Agent Conformance and Benchmarking Community Group from the MockBench settlement-finality fixtures in this repository.

## What it is

A mock replay of calibrated fixtures, not a live-rail measurement. Each fixture in `paybench/fixtures/` is a population of 5,000 settlement-finality draws, in seconds, for one rail, generated from a log-normal distribution calibrated to that rail's provenance record. The provenance records are in `paybench/calibration/provenance/`.

The emitter reads the five settlement-finality fixtures only. One rail in the published rail set is measured on authorization latency and has no settlement-finality fixture; its six checks are written as `not-exercised` with cause `not_applicable`, which says something about the design of the benchmark and nothing about that rail.

## The unit

One check per fixture draw per threshold. The thresholds are the frozen threshold grid, `K_GRID_SECONDS` in `paybench/mockbench/__init__.py`.

| threshold | in microseconds |
|---|---|
| 2 s | 2000000 |
| 3 s | 3000000 |
| 5 s | 5000000 |
| 10 s | 10000000 |
| 15 s | 15000000 |
| 20 s | 20000000 |

The state of a check is `pass` when the draw is at or below the threshold and `fail` otherwise. That is the predicate `pass_at_k` in `paybench/mockbench/stats.py` applies to the same draws. A threshold here is a reporting threshold; it is not a requirement on any rail, and a `fail` is not a conformance verdict about a rail.

The report lists each rail's id beside its name under `source.rails`, in alphabetical order by rail name, and the checks follow that order.

Check identifiers are `finality-le-<threshold>s/<rail id>/<draw index>`, with the draw index being the position in the fixture's `samples` list, zero padded to five digits. Each check carries one annotation, `observed-us`, the draw in whole microseconds. The fixtures are quantised to six decimal places, so the conversion is exact, and the digests are taken under `jcs-sha256`, which admits integers only.

## What it does not contain

No race records, no strengths or ordering from the pairwise model, no win rates, no interval estimates and no score. The pairwise races and the model fitted to them are outside this report on purpose: a race between two rails has no pass or fail state of its own, and an ordering would be a comparison of rails that this report does not make.

## Provenance and the posture of the figures

The fixtures were calibrated from first-party test-network runs (for one rail combined with published documentation for its tail) made before the method was frozen and externally anchored. The method and its analysis plan were frozen and externally anchored after those calibration runs and before publication of any result: signed tag `paybench-prereg-v1.2`, OSF DOI 10.17605/OSF.IO/XGFUJ. The figures are calibration evidence replayed from fixtures.

These figures are a measurement, not a recommendation: no rail is endorsed, no ordering implies a best buy, and no rail is being suggested for use.

Rails are listed alphabetically by rail name. That ordering is fixed and carries no performance meaning.

The same measurement protocol was applied identically to every rail.

The protocol referred to is the threshold check applied to every fixture draw; the calibration runs from which the fixtures were built carry the limitations disclosed and pre-registered in section 7 of the methodology (`paybench/methodology/methodology.md`): the R2 fixture is a manual-path lower bound that omits the facilitator round trip, the R11 fixture was measured on a hosted regtest, the R10 fixture was measured on a testnet and is an optimistic bound, and the R9 tail is partly documentation-derived.

The frozen and anchored finality pre-registration this report points at (signed tag `paybench-prereg-v1.2`; OSF DOI 10.17605/OSF.IO/XGFUJ) pins a run record (`runs/finality-run.json`) whose pairwise-model output contains a statement ordering the five rails on this dimension. That statement is part of the frozen record and was fixed before this report existed. This report does not assert any ordering: the rails are listed alphabetically, the order carries no performance meaning, and nothing here is a recommendation to use any rail.

## Corrections and right of reply

Any operator of a rail or facilitator named here may respond through the structured right-of-reply channel at https://reply.agentic-paybench.dev/.

## Rerun

From the repository root, with Python 3.9 or later and nothing installed:

```
python3 -m paybench.w3c_report.emit --out finality-threshold-report.level1.json --verify
```

The run writes the report, builds it a second time and fails unless the two builds are byte-identical, then prints the byte count, the SHA-256 of the file and the check-set root, and compares them with `EXPECTED.json`. It exits non-zero on any mismatch. There is no clock, no randomness and no network access.

The report is about 13.5 megabytes written compactly and about 1.1 megabytes compressed, which is why it is regenerated rather than committed.

## Check the report with another reader

The check-set root is a flat tree over each check's `jcs-sha256` bytes, as `check-set` declares. The reference reader in the `agent-evidence-vectors` package (`w3creport.rejections` and `w3creport.shape_errors`) accepts the report with no shape error and no rejection row.

## Tests

```
python3 -m pytest paybench/w3c_report/tests
```
