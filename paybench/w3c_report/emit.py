"""Emit a v0.1 per-check report from the MockBench settlement-finality fixtures.

The unit is one threshold check per fixture draw per threshold. For each of the
five settling rails, each of the 5,000 calibrated draws in the rail's fixture is
checked against each threshold on the frozen threshold grid
(``paybench.mockbench.K_GRID_SECONDS``: 2, 3, 5, 10, 15 and 20 seconds). The
state is ``pass`` when the draw is at or below the threshold and ``fail``
otherwise, which is the predicate ``pass_at_k`` in ``paybench/mockbench/stats.py``
applies to the same draws.

What is NOT emitted, on purpose: no race records, no Bradley-Terry strengths or
ranking, no win rates, no interval estimates, no score. A threshold check has a
verdict of its own; a race between two rails does not, and a ranking would be a
merit ordering. Rails are listed alphabetically by rail name; that ordering is
fixed and carries no performance meaning.

This is a mock replay of calibrated fixtures, not a live-rail measurement.

The output is deterministic: the same fixtures and the same code write the same
bytes. There is no clock, no randomness and no environment input.

Usage, from the repository root::

    python3 -m paybench.w3c_report.emit --out finality-threshold-report.level1.json --verify

The run prints the byte count, the SHA-256 of the file and the check-set root, and
compares them with ``EXPECTED.json`` beside this module.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

from paybench.mockbench import K_GRID_SECONDS, SETTLING_RAILS
from paybench.mockbench.fixtures import load_fixture
from paybench.mockbench.paths import FIXTURES_DIR

FORMAT = "public-agent-conformance/report/v0.1"
TREE_SHAPE = "flat"
DIGEST_ENCODING = "jcs-sha256"
DOMAIN_ID = "d-mockbench-finality-thresholds"
MICROSECONDS = 10**6

#: The rail with no settlement-finality fixture: it is measured on
#: authorization latency, not finality, so its finality checks are not exercised.
UNEXERCISED_RAIL = "R6"
UNEXERCISED_FIXTURE = "R6-auth-latency-A.fixture.json"

ORDERING_SENTENCE = (
    "Rails are listed alphabetically by rail name. That ordering is fixed and "
    "carries no performance meaning."
)
PROTOCOL_SENTENCE = "The same measurement protocol was applied identically to every rail."
PROTOCOL_SCOPE_SENTENCE = (
    "The protocol referred to is the threshold check applied to every fixture draw; the "
    "calibration runs from which the fixtures were built carry the limitations disclosed and pre-registered "
    "in section 7 of the methodology (paybench/methodology/methodology.md): the R2 fixture is "
    "a manual-path lower bound that omits the facilitator round trip, the R11 fixture was "
    "measured on a hosted regtest, the R10 fixture was measured on a testnet and is an "
    "optimistic bound, and the R9 tail is partly documentation-derived."
)
ORDERING_DISCLOSURE = (
    "The frozen and anchored finality pre-registration this report points at (signed tag "
    "paybench-prereg-v1.2; OSF DOI 10.17605/OSF.IO/XGFUJ) pins a run record "
    "(runs/finality-run.json) whose pairwise-model output contains a statement ordering the "
    "five rails on this dimension. That statement is part of the frozen record and was fixed "
    "before this report existed. This report does not assert any ordering: the rails are "
    "listed alphabetically, the order carries no performance meaning, and nothing here is a "
    "recommendation to use any rail."
)
REPLY_SENTENCE = (
    "Any operator of a rail or facilitator named here may respond through the structured "
    "right-of-reply channel at https://reply.agentic-paybench.dev/."
)

MEASUREMENT_SENTENCE = (
    "These figures are a measurement, not a recommendation: no rail is endorsed, no "
    "ordering implies a best buy, and no rail is being suggested for use."
)

DOMAIN_DESCRIPTION = (
    "A mock replay of calibrated fixtures, not a live-rail measurement. Each fixture is a "
    "population of 5,000 settlement-finality draws, in seconds, generated from a log-normal "
    "distribution calibrated to a rail's provenance record: first-party test-network runs "
    "(for one rail combined with published documentation for its tail) made before the "
    "measurement method was frozen and externally anchored. The method and its analysis "
    "plan were frozen and externally anchored (signed tag paybench-prereg-v1.2, OSF DOI "
    "10.17605/OSF.IO/XGFUJ) after those calibration runs and before publication of any "
    "result. One check is emitted per draw per threshold; its state is pass when the draw "
    "is at or below the threshold and fail otherwise, and a check is not a conformance "
    "requirement on any rail. "
    + MEASUREMENT_SENTENCE
    + " "
    + ORDERING_SENTENCE
    + " "
    + PROTOCOL_SENTENCE
    + " "
    + PROTOCOL_SCOPE_SENTENCE
    + " "
    + ORDERING_DISCLOSURE
    + " "
    + REPLY_SENTENCE
)

CROSSWALK = {
    "pass": "the fixture draw is at or below the threshold named in the check identifier",
    "fail": "the fixture draw is above the threshold named in the check identifier",
    "not-exercised": (
        "the rail has no settlement-finality fixture (it is measured on authorization "
        "latency, not finality), so the check was never run; cause not_applicable"
    ),
    "inconclusive": "never emitted; every fixture draw has a verdict",
    "void": "never emitted; every fixture is content-hash verified before it is read",
    "observed-us": "the fixture draw in whole microseconds (the fixture is quantised to 6 decimal places)",
}


def _check_id(threshold_s: int, rail_id: str, index: int | None) -> str:
    base = f"finality-le-{threshold_s}s/{rail_id}"
    return base if index is None else f"{base}/{index:05d}"


def _micros(sample: str) -> int:
    """A fixture sample (a fixed-format decimal string of seconds) as integer microseconds.

    The fixture is quantised to six decimal places, so the conversion is exact; a
    sample with more places would not be, and is refused rather than rounded.
    """
    whole, _, frac = sample.partition(".")
    if len(frac) > 6 or not whole.isdigit() or (frac and not frac.isdigit()):
        raise ValueError(f"sample {sample!r} is not a decimal with at most six places")
    return int(whole) * MICROSECONDS + int((frac + "000000")[:6])


def _rail_name(fixture: dict[str, Any]) -> str:
    return str(fixture["rail_name"])


def build_report() -> dict[str, Any]:
    """The v0.1 report, as a dict, from the committed fixtures."""
    fixtures = {rail: load_fixture(rail) for rail in SETTLING_RAILS}
    unexercised_path = FIXTURES_DIR / UNEXERCISED_FIXTURE
    unexercised_name = _rail_name(json.loads(unexercised_path.read_text(encoding="utf-8")))

    # (rail name, rail id, fixture or None), alphabetical by rail name.
    listing: list[tuple[str, str, dict[str, Any] | None]] = [
        (_rail_name(fx), rail, fx) for rail, fx in fixtures.items()
    ]
    listing.append((unexercised_name, UNEXERCISED_RAIL, None))
    listing.sort(key=lambda entry: entry[0])

    checks: list[dict[str, Any]] = []
    for _name, rail, fixture in listing:
        for threshold in K_GRID_SECONDS:
            threshold_us = int(threshold) * MICROSECONDS
            if fixture is None:
                checks.append(
                    {
                        "cause": {
                            "code": "not_applicable",
                            "detail": "no settlement-finality fixture; measured on authorization latency",
                        },
                        "check": _check_id(int(threshold), rail, None),
                        "state": "not-exercised",
                    }
                )
                continue
            for index, sample in enumerate(fixture["samples"]):
                observed_us = _micros(sample)
                # The frozen predicate, as stats.pass_at_k applies it: s <= k on the float.
                assert (float(sample) <= threshold) == (observed_us <= threshold_us)
                checks.append(
                    {
                        "annotations": {"observed-us": observed_us},
                        "check": _check_id(int(threshold), rail, index),
                        "state": "pass" if observed_us <= threshold_us else "fail",
                    }
                )

    counts = {
        "declared": len(checks),
        "exercised": sum(1 for c in checks if c["state"] != "not-exercised"),
        "fail": sum(1 for c in checks if c["state"] == "fail"),
        "inconclusive": 0,
        "not-exercised": sum(1 for c in checks if c["state"] == "not-exercised"),
        "pass": sum(1 for c in checks if c["state"] == "pass"),
        "void": 0,
    }
    rollup: dict[str, Any] = dict(counts)
    rollup["carried"] = 0
    rollup["referenced"] = 0
    rollup["negative-capable"] = {"kind": "shown-by-run" if counts["fail"] >= 1 else "nothing"}

    return {
        "check-set": {
            "digest-encoding": DIGEST_ENCODING,
            "leaf-count": len(checks),
            "sha256": check_set_root(checks),
            "tree-shape": TREE_SHAPE,
        },
        "checks": checks,
        "crosswalk": CROSSWALK,
        "domain": {"description": DOMAIN_DESCRIPTION, "id": DOMAIN_ID},
        "evidence": [],
        "format": FORMAT,
        "roll-up": rollup,
        "source": {
            "dimension": "settlement-finality",
            "fixture-content-hashes": {
                rail: fixtures[rail]["content_hash"] for rail in sorted(fixtures)
            },
            "kind": "mock replay of calibrated fixtures",
            "rails": [{"id": rail, "name": name} for name, rail, _fx in listing],
            "threshold-seconds": [int(k) for k in K_GRID_SECONDS],
        },
    }


def _leaf_bytes(check: dict[str, Any]) -> bytes:
    """The jcs-sha256 bytes of one check.

    For the values this emitter writes (ASCII strings with no quotation mark,
    backslash or control character, and integers of magnitude below 2**53) the
    RFC 8785 form is the compact, sorted-key JSON. The assertion keeps that true.
    """
    text = json.dumps(check, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    assert text.isascii() and "\\" not in text
    return text.encode("ascii")


def check_set_root(checks: list[dict[str, Any]]) -> str:
    """The flat root: SHA-256 over the concatenated SHA-256 of each leaf, in order."""
    digest = hashlib.sha256()
    for check in checks:
        digest.update(hashlib.sha256(_leaf_bytes(check)).digest())
    return digest.hexdigest()


def serialise(report: dict[str, Any]) -> bytes:
    """The bytes written: compact, sorted-key, ASCII JSON and one trailing newline."""
    text = json.dumps(report, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return (text + "\n").encode("ascii")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m paybench.w3c_report.emit",
        description="Emit a v0.1 per-check report of threshold checks from the finality fixtures.",
    )
    parser.add_argument("--out", required=True, help="path to write the report to")
    parser.add_argument(
        "--verify",
        action="store_true",
        help="also build the report a second time and fail unless the bytes are identical",
    )
    parser.add_argument(
        "--expected",
        default=str(Path(__file__).with_name("EXPECTED.json")),
        help="a file of expected digests to compare against (default: EXPECTED.json beside this module)",
    )
    args = parser.parse_args(argv)

    report = build_report()
    data = serialise(report)
    if args.verify and serialise(build_report()) != data:
        print("FAIL: two builds produced different bytes", file=sys.stderr)
        return 1
    Path(args.out).write_bytes(data)
    exit_code = 0
    expected_path = Path(args.expected)
    if expected_path.is_file():
        expected = json.loads(expected_path.read_text(encoding="utf-8"))
        observed = {
            "report-sha256": hashlib.sha256(data).hexdigest(),
            "check-set-sha256": report["check-set"]["sha256"],
            "report-bytes": len(data),
            "declared": report["roll-up"]["declared"],
        }
        mismatched = [k for k, v in observed.items() if expected.get(k) != v]
        if mismatched:
            print(f"MISMATCH against {expected_path}: {', '.join(mismatched)}", file=sys.stderr)
            exit_code = 1
        else:
            print(f"matches {expected_path}")

    rollup = report["roll-up"]
    print(f"wrote {args.out}")
    print(f"bytes: {len(data)}")
    print(f"gzip -9 bytes: {len(gzip.compress(data, 9, mtime=0))}")
    print(f"sha256: {hashlib.sha256(data).hexdigest()}")
    print(f"check-set sha256 ({TREE_SHAPE}): {report['check-set']['sha256']}")
    print(
        "declared {declared} exercised {exercised} pass {pass} fail {fail} "
        "not-exercised {not-exercised}".format(**rollup)
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
