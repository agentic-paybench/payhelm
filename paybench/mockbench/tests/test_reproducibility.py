"""Reproducibility + calibration-fidelity tests (methodology §5.4 item 6, §6–§7)."""

from __future__ import annotations

import math
import statistics

from paybench.mockbench import N_FIXTURE_SAMPLES, SETTLING_RAILS
from paybench.mockbench.bench import run_benchmark
from paybench.mockbench.fixtures import (
    build_payload,
    content_hash,
    load_calibration,
    sample_finalities,
)


def test_sampling_is_deterministic():
    # Same rail, same master seed -> identical sample sequence, every time.
    cal = load_calibration("R1")
    a = sample_finalities(cal)
    b = sample_finalities(cal)
    assert a == b
    assert len(a) == N_FIXTURE_SAMPLES


def test_content_hash_is_stable():
    cal = load_calibration("R10")
    samples = sample_finalities(cal)
    h1 = content_hash(build_payload(cal, samples))
    h2 = content_hash(build_payload(cal, samples))
    assert h1 == h2
    assert h1.startswith("sha256:")


def test_content_hash_changes_with_parameters():
    # A different calibration must produce a different fixture hash (pre-reg
    # integrity: the hash is coupled to the literal provenance parameters).
    r1 = load_calibration("R1")
    r9 = load_calibration("R9")
    h_r1 = content_hash(build_payload(r1, sample_finalities(r1)))
    h_r9 = content_hash(build_payload(r9, sample_finalities(r9)))
    assert h_r1 != h_r9


def test_samples_track_calibrated_lognormal():
    # The generated population must actually match the calibrated distribution:
    # empirical median ~ median_s and stdev(log samples) ~ sigma_log.
    for rail in SETTLING_RAILS:
        cal = load_calibration(rail)
        xs = [float(s) for s in sample_finalities(cal)]
        emp_median = statistics.median(xs)
        emp_sigma_log = statistics.pstdev([math.log(x) for x in xs])
        target_median = float(cal.median_s)
        target_sigma = float(cal.sigma_log)
        assert abs(emp_median - target_median) / target_median < 0.03, rail
        assert abs(emp_sigma_log - target_sigma) < 0.01, rail


def test_run_is_bit_for_bit_reproducible():
    r1 = run_benchmark()
    r2 = run_benchmark()
    assert r1["run_hash"] == r2["run_hash"]
    assert r1["config"]["total_trials"] == 5000
    assert r1["config"]["n_pairs"] == 10


def test_ranking_matches_finality_order():
    # Fastest calibrated median should top the BT ranking; slowest should be last.
    report = run_benchmark()
    ranking = report["bradley_terry"]["ranking"]
    # Medians: R10 1.75 < R1 2.05 < R2 2.74 < R9 14.63 < R11 16.52
    assert ranking[0] == "R10"
    assert ranking[-1] == "R11"
    assert ranking == ["R10", "R1", "R2", "R9", "R11"]
    assert report["bradley_terry"]["converged"] is True
