"""Dimension-2 (authorization-latency) tests — mirror of test_reproducibility.

Covers the new dimension end-to-end (determinism, content-addressing,
calibration fidelity, reproducible run, ranking) AND the two cross-dimension
invariants the generalisation must hold:

* the finality and auth-latency dimensions are RNG-domain-separated (same rail,
  same master seed → different streams, different fixture hashes), and
* generalising the harness did not perturb the frozen finality artefact (an
  explicit pin on the v1.2 run_hash, complementing the CI guard).

All auth-latency calibration is PLACEHOLDER (see the provenance files); these
tests assert harness *behaviour*, not any real-world latency claim.
"""

from __future__ import annotations

import math
import statistics

from paybench.mockbench import N_FIXTURE_SAMPLES, TRIALS_PER_PAIR
from paybench.mockbench.bench import run_benchmark
from paybench.mockbench.dimensions import AUTH_LATENCY, FINALITY
from paybench.mockbench.fixtures import (
    build_payload,
    content_hash,
    load_calibration,
    sample_finalities,
)

# The deterministic outputs of the PLACEHOLDER auth-latency fixtures. These pin
# the harness's reproducibility, not a latency claim — regenerating the
# placeholder fixtures unchanged must reproduce them bit-for-bit.
EXPECTED_AUTH_RANKING = ["R10", "R1", "R2", "R11", "R9", "R6"]
EXPECTED_AUTH_RUN_HASH = (
    "sha256:a6802f13067efc3ab3f90363620c3a48770052557ae72528b929db8d4ae62873"
)
# The frozen, pre-registered v1.2 settlement-finality run hash (§9). Must never
# change — the whole point of the dimension-parametric refactor.
FROZEN_FINALITY_RUN_HASH = (
    "sha256:895f99ed52567421a1d7e9068ab9a0d7147d6381ec137e1b130b805e63b14ee0"
)


def test_auth_sampling_is_deterministic():
    cal = load_calibration("R6", AUTH_LATENCY)
    a = sample_finalities(cal, AUTH_LATENCY)
    b = sample_finalities(cal, AUTH_LATENCY)
    assert a == b
    assert len(a) == N_FIXTURE_SAMPLES


def test_auth_content_hash_is_stable():
    cal = load_calibration("R10", AUTH_LATENCY)
    samples = sample_finalities(cal, AUTH_LATENCY)
    h1 = content_hash(build_payload(cal, samples, AUTH_LATENCY))
    h2 = content_hash(build_payload(cal, samples, AUTH_LATENCY))
    assert h1 == h2
    assert h1.startswith("sha256:")


def test_auth_content_hash_changes_with_parameters():
    r1 = load_calibration("R1", AUTH_LATENCY)
    r6 = load_calibration("R6", AUTH_LATENCY)
    h_r1 = content_hash(build_payload(r1, sample_finalities(r1, AUTH_LATENCY), AUTH_LATENCY))
    h_r6 = content_hash(build_payload(r6, sample_finalities(r6, AUTH_LATENCY), AUTH_LATENCY))
    assert h_r1 != h_r6


def test_auth_samples_track_calibrated_lognormal():
    for rail in AUTH_LATENCY.rails:
        cal = load_calibration(rail, AUTH_LATENCY)
        xs = [float(s) for s in sample_finalities(cal, AUTH_LATENCY)]
        emp_median = statistics.median(xs)
        emp_sigma_log = statistics.pstdev([math.log(x) for x in xs])
        target_median = float(cal.median_s)
        target_sigma = float(cal.sigma_log)
        assert abs(emp_median - target_median) / target_median < 0.03, rail
        assert abs(emp_sigma_log - target_sigma) < 0.01, rail


def test_auth_run_is_bit_for_bit_reproducible():
    r1 = run_benchmark(AUTH_LATENCY)
    r2 = run_benchmark(AUTH_LATENCY)
    assert r1["run_hash"] == r2["run_hash"] == EXPECTED_AUTH_RUN_HASH
    # 6 rails -> C(6,2) = 15 pairs -> 15 * 500 = 7,500 trials (§8 Resolution B).
    assert r1["config"]["n_pairs"] == 15
    assert r1["config"]["total_trials"] == 15 * TRIALS_PER_PAIR == 7500
    assert r1["dimension"] == "authorization-latency"
    assert r1["schema"] == "paybench.auth-latency-run.v1"


def test_auth_ranking_tracks_placeholder_medians():
    report = run_benchmark(AUTH_LATENCY)
    # Placeholder medians: R10 0.30 < R1 0.45 < R2 0.55 < R11 0.70 < R9 0.90 < R6 1.30.
    assert report["bradley_terry"]["ranking"] == EXPECTED_AUTH_RANKING
    assert report["bradley_terry"]["converged"] is True
    # AP2 (R6) debuts here and is the slowest-authorizing rail under the placeholder.
    assert report["bradley_terry"]["ranking"][-1] == "R6"
    assert "R6" in report["config"]["rails"]


def test_dimensions_are_rng_domain_separated():
    # Same rail + same master seed, different dimension -> different seed domain,
    # different sample stream, different fixture content hash. This is what keeps
    # auth-latency from silently reusing finality's RNG stream.
    assert FINALITY.fixture_seed_domain("R1") == "fixture:R1"
    assert AUTH_LATENCY.fixture_seed_domain("R1") == "fixture:auth-latency:R1"
    assert FINALITY.pair_seed_domain("R1", "R2") == "pair:R1:R2"
    assert AUTH_LATENCY.pair_seed_domain("R1", "R2") == "pair:auth-latency:R1:R2"

    fin = load_calibration("R1", FINALITY)
    aut = load_calibration("R1", AUTH_LATENCY)
    fin_stream = sample_finalities(fin, FINALITY)
    aut_stream = sample_finalities(aut, AUTH_LATENCY)
    assert fin_stream != aut_stream
    assert content_hash(build_payload(fin, fin_stream, FINALITY)) != content_hash(
        build_payload(aut, aut_stream, AUTH_LATENCY)
    )


def test_finality_artefact_is_unperturbed_by_generalisation():
    # The dimension-parametric refactor must leave the frozen v1.2 finality run
    # byte-identical. Pinning the absolute run_hash here makes the guarantee a
    # local unit test, not only a CI assertion.
    report = run_benchmark(FINALITY)
    assert report["run_hash"] == FROZEN_FINALITY_RUN_HASH
    assert report["dimension"] == "settlement-finality"
    assert report["bradley_terry"]["ranking"] == ["R10", "R1", "R2", "R9", "R11"]
