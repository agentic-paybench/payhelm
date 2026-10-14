"""Tests for the threshold-check report emitter."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from paybench.mockbench import K_GRID_SECONDS, N_FIXTURE_SAMPLES, SETTLING_RAILS
from paybench.mockbench.fixtures import load_fixture
from paybench.mockbench.stats import pass_at_k
from paybench.w3c_report import emit

EXPECTED = json.loads((Path(emit.__file__).with_name("EXPECTED.json")).read_text(encoding="utf-8"))


def _report() -> dict:
    return emit.build_report()


def test_report_is_byte_reproducible_and_matches_expected_digests():
    report = _report()
    data = emit.serialise(report)
    assert data == emit.serialise(_report())
    assert hashlib.sha256(data).hexdigest() == EXPECTED["report-sha256"]
    assert len(data) == EXPECTED["report-bytes"]
    assert report["check-set"]["sha256"] == EXPECTED["check-set-sha256"]
    assert report["roll-up"]["declared"] == EXPECTED["declared"]


def test_counts_equal_the_frozen_pass_at_k_predicate_per_rail_and_threshold():
    report = _report()
    by_rail_threshold: dict[tuple[str, int], int] = {}
    for check in report["checks"]:
        # identifier shape: finality-le-<k>s/<rail>/<index>
        head, rail, *rest = check["check"].split("/")
        if not rest:
            continue  # the not-exercised rail has no draw index
        threshold = int(head[len("finality-le-") : -1])
        if check["state"] == "pass":
            by_rail_threshold[(rail, threshold)] = by_rail_threshold.get((rail, threshold), 0) + 1
    for rail in SETTLING_RAILS:
        samples = [float(s) for s in load_fixture(rail)["samples"]]
        for k in K_GRID_SECONDS:
            expected = round(pass_at_k(samples, k).interval.phat * len(samples))
            assert by_rail_threshold.get((rail, int(k)), 0) == expected


def test_listing_is_alphabetical_by_rail_name_and_rollup_is_consistent():
    report = _report()
    rails_in_order: list[str] = []
    for check in report["checks"]:
        rail = check["check"].split("/")[1]
        if not rails_in_order or rails_in_order[-1] != rail:
            rails_in_order.append(rail)
    assert len(rails_in_order) == len(set(rails_in_order)) == len(SETTLING_RAILS) + 1
    names = {rail: load_fixture(rail)["rail_name"] for rail in SETTLING_RAILS}
    unexercised = json.loads(
        (emit.FIXTURES_DIR / emit.UNEXERCISED_FIXTURE).read_text(encoding="utf-8")
    )
    names[emit.UNEXERCISED_RAIL] = unexercised["rail_name"]
    assert [names[r] for r in rails_in_order] == sorted(names.values())
    rollup = report["roll-up"]
    states = [c["state"] for c in report["checks"]]
    assert rollup["declared"] == len(states) == len(SETTLING_RAILS) * N_FIXTURE_SAMPLES * len(K_GRID_SECONDS) + len(K_GRID_SECONDS)
    assert rollup["pass"] == states.count("pass")
    assert rollup["fail"] == states.count("fail")
    assert rollup["not-exercised"] == states.count("not-exercised") == len(K_GRID_SECONDS)
    assert rollup["negative-capable"] == {"kind": "shown-by-run"}


def test_report_carries_no_comparison_content():
    text = emit.serialise(_report()).decode("ascii").lower()
    for forbidden in ("bradley", "win_rate", "wilson", "ranking", "strength", "race"):
        assert forbidden not in text.replace("no ordering implies a best buy", "")
    assert emit.ORDERING_SENTENCE in _report()["domain"]["description"]
    assert emit.PROTOCOL_SENTENCE in _report()["domain"]["description"]
    assert emit.MEASUREMENT_SENTENCE in _report()["domain"]["description"]
    assert "before any run" not in text and "before any measurement" not in text


def test_every_number_is_a_safe_integer():
    limit = 2**53
    for check in _report()["checks"]:
        for value in check.get("annotations", {}).values():
            assert isinstance(value, int) and not isinstance(value, bool) and abs(value) < limit
