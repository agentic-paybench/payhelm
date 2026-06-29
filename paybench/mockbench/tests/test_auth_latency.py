"""Dimension-2 (authorization-latency / RAPL) tests — mirror of test_reproducibility.

Covers the SPLIT RAPL dimension end-to-end (determinism, content-addressing,
calibration fidelity, reproducible runs, rankings) AND the cross-dimension
invariants the generalisation must hold:

* RAPL is SPLIT into two never-cross-raced sub-rankings — A (Payment-Validation)
  and B (Challenge-Issuance), C(5,2)=10 pairs each (doctrine §2; supersedes the
  pre-gate single 6-rail / 15-pair race the cross-lineage gate refuted 0–4);
* finality, RAPL-A and RAPL-B are mutually RNG-domain-separated (same rail, same
  master seed → different streams, different fixture hashes); and
* generalising the harness did not perturb the frozen finality artefact (an
  explicit pin on the v1.2 run_hash, complementing the CI guard).

RAPL fixtures are CALIBRATED from the first-party pilot {median, sigma} (the
Variant-E mock baseline, representative topology per fixture); these tests assert
harness *behaviour* + the doctrine's within-group order, not an absolute latency.
"""

from __future__ import annotations

import math
import statistics

from paybench.mockbench import N_FIXTURE_SAMPLES, TRIALS_PER_PAIR
from paybench.mockbench.bench import run_benchmark
from paybench.mockbench.dimensions import AUTH_LATENCY_A, AUTH_LATENCY_B, FINALITY
from paybench.mockbench.fixtures import (
    build_payload,
    content_hash,
    load_calibration,
    sample_finalities,
)

# Deterministic outputs of the calibrated RAPL fixtures. These pin the harness's
# reproducibility (regenerating the calibrated fixtures unchanged must reproduce
# them bit-for-bit) AND the doctrine's within-group order.
#
# A — Payment-Validation: AP2 (DPC, local crypto) < Tempo-Session (local) <
#     Solana < Stellar < Base (network facilitator). Local ≪ network.
EXPECTED_AUTH_A_RANKING = ["R6", "R10", "R9", "R2", "R1"]
EXPECTED_AUTH_A_RUN_HASH = (
    "sha256:7487c278aecc3586937b1903fc9fdd56cdce842b39560f0d9abb6041d122072b"
)
# B — Challenge-Issuance: local-402 (Stellar/Solana/Tempo/Base, ~ms) ≪ Lightning
#     (BOLT11 invoice mint, ~0.5 s).
EXPECTED_AUTH_B_RANKING = ["R2", "R9", "R10", "R1", "R11"]
EXPECTED_AUTH_B_RUN_HASH = (
    "sha256:19b91c8df32f73fca84615ed44f3c00455c81f8a1df39ac2e9ff9314b4dd7c71"
)
# The frozen, pre-registered v1.2 settlement-finality run hash (§9). Must never
# change — the whole point of the dimension-parametric refactor.
FROZEN_FINALITY_RUN_HASH = (
    "sha256:895f99ed52567421a1d7e9068ab9a0d7147d6381ec137e1b130b805e63b14ee0"
)

SUBRANKINGS = (AUTH_LATENCY_A, AUTH_LATENCY_B)


def test_auth_sampling_is_deterministic():
    for dim in SUBRANKINGS:
        cal = load_calibration(dim.rails[0], dim)
        a = sample_finalities(cal, dim)
        b = sample_finalities(cal, dim)
        assert a == b
        assert len(a) == N_FIXTURE_SAMPLES


def test_auth_content_hash_is_stable():
    for dim in SUBRANKINGS:
        cal = load_calibration("R10", dim)
        samples = sample_finalities(cal, dim)
        h1 = content_hash(build_payload(cal, samples, dim))
        h2 = content_hash(build_payload(cal, samples, dim))
        assert h1 == h2
        assert h1.startswith("sha256:")


def test_auth_content_hash_changes_with_parameters():
    # Different rails differ within a sub-ranking...
    r1 = load_calibration("R1", AUTH_LATENCY_A)
    r6 = load_calibration("R6", AUTH_LATENCY_A)
    h_r1 = content_hash(build_payload(r1, sample_finalities(r1, AUTH_LATENCY_A), AUTH_LATENCY_A))
    h_r6 = content_hash(build_payload(r6, sample_finalities(r6, AUTH_LATENCY_A), AUTH_LATENCY_A))
    assert h_r1 != h_r6
    # ...and the SAME rail differs between sub-rankings A and B (distinct
    # primitives → distinct fixtures → distinct streams + hashes).
    a = load_calibration("R1", AUTH_LATENCY_A)
    b = load_calibration("R1", AUTH_LATENCY_B)
    h_a = content_hash(build_payload(a, sample_finalities(a, AUTH_LATENCY_A), AUTH_LATENCY_A))
    h_b = content_hash(build_payload(b, sample_finalities(b, AUTH_LATENCY_B), AUTH_LATENCY_B))
    assert h_a != h_b


def test_auth_samples_track_calibrated_lognormal():
    for dim in SUBRANKINGS:
        for rail in dim.rails:
            cal = load_calibration(rail, dim)
            xs = [float(s) for s in sample_finalities(cal, dim)]
            emp_median = statistics.median(xs)
            emp_sigma_log = statistics.pstdev([math.log(x) for x in xs])
            target_median = float(cal.median_s)
            target_sigma = float(cal.sigma_log)
            assert abs(emp_median - target_median) / target_median < 0.03, (dim.key, rail)
            assert abs(emp_sigma_log - target_sigma) < 0.01, (dim.key, rail)


def test_auth_runs_are_bit_for_bit_reproducible():
    for dim, exp_hash, schema in (
        (AUTH_LATENCY_A, EXPECTED_AUTH_A_RUN_HASH, "paybench.auth-latency-A-run.v1"),
        (AUTH_LATENCY_B, EXPECTED_AUTH_B_RUN_HASH, "paybench.auth-latency-B-run.v1"),
    ):
        r1 = run_benchmark(dim)
        r2 = run_benchmark(dim)
        assert r1["run_hash"] == r2["run_hash"] == exp_hash, dim.key
        # SPLIT: 5 rails -> C(5,2) = 10 pairs -> 10 * 500 = 5,000 trials.
        assert r1["config"]["n_pairs"] == 10, dim.key
        assert r1["config"]["total_trials"] == 10 * TRIALS_PER_PAIR == 5000, dim.key
        assert r1["schema"] == schema
    assert run_benchmark(AUTH_LATENCY_A)["dimension"] == "authorization-latency:payment-validation"
    assert run_benchmark(AUTH_LATENCY_B)["dimension"] == "authorization-latency:challenge-issuance"


def test_auth_rankings_track_doctrine_within_group_order():
    a = run_benchmark(AUTH_LATENCY_A)
    b = run_benchmark(AUTH_LATENCY_B)
    # A: local crypto (AP2, Tempo-Session) ≪ network facilitator (Solana<Stellar<Base).
    assert a["bradley_terry"]["ranking"] == EXPECTED_AUTH_A_RANKING
    assert a["bradley_terry"]["converged"] is True
    assert a["bradley_terry"]["ranking"][0] == "R6"   # AP2 fastest-authorizing
    assert a["bradley_terry"]["ranking"][-1] == "R1"  # Base slowest in A
    # B: local-402 ≪ Lightning invoice-mint (slowest).
    assert b["bradley_terry"]["ranking"] == EXPECTED_AUTH_B_RANKING
    assert b["bradley_terry"]["ranking"][-1] == "R11"
    # The SPLIT invariant: AP2 is A-only, Lightning is B-only.
    assert "R6" in a["config"]["rails"] and "R6" not in b["config"]["rails"]
    assert "R11" in b["config"]["rails"] and "R11" not in a["config"]["rails"]


def test_dimensions_are_rng_domain_separated():
    # Same rail + same master seed, different (sub-)dimension -> different seed
    # domain, different sample stream, different fixture content hash. Keeps
    # finality / RAPL-A / RAPL-B from silently reusing each other's RNG stream.
    assert FINALITY.fixture_seed_domain("R1") == "fixture:R1"
    assert AUTH_LATENCY_A.fixture_seed_domain("R1") == "fixture:auth-latency:A:R1"
    assert AUTH_LATENCY_B.fixture_seed_domain("R1") == "fixture:auth-latency:B:R1"
    assert FINALITY.pair_seed_domain("R1", "R2") == "pair:R1:R2"
    assert AUTH_LATENCY_A.pair_seed_domain("R1", "R2") == "pair:auth-latency:A:R1:R2"
    assert AUTH_LATENCY_B.pair_seed_domain("R1", "R2") == "pair:auth-latency:B:R1:R2"

    streams = {}
    for tag, dim in (("fin", FINALITY), ("A", AUTH_LATENCY_A), ("B", AUTH_LATENCY_B)):
        cal = load_calibration("R1", dim)
        streams[tag] = sample_finalities(cal, dim)
    # all three R1 streams are mutually distinct
    assert streams["fin"] != streams["A"]
    assert streams["A"] != streams["B"]
    assert streams["fin"] != streams["B"]


def test_finality_artefact_is_unperturbed_by_generalisation():
    # The dimension-parametric refactor (incl. the RAPL SPLIT) must leave the
    # frozen v1.2 finality run byte-identical. Pinning the absolute run_hash here
    # makes the guarantee a local unit test, not only a CI assertion.
    report = run_benchmark(FINALITY)
    assert report["run_hash"] == FROZEN_FINALITY_RUN_HASH
    assert report["dimension"] == "settlement-finality"
    assert report["bradley_terry"]["ranking"] == ["R10", "R1", "R2", "R9", "R11"]
