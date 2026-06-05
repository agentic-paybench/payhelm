"""Known-answer + property tests for the statistical layer (methodology §5)."""

from __future__ import annotations

import math

from paybench.mockbench.stats import (
    bradley_terry_mle,
    pass_at_k,
    wilson_interval,
)


def test_wilson_known_answer():
    # Reference: 50/100 successes, 95% Wilson (z=1.95996) ~ [0.4038, 0.5962].
    ci = wilson_interval(50, 100)
    assert abs(ci.phat - 0.5) < 1e-12
    assert abs(ci.lower - 0.4038) < 1e-3
    assert abs(ci.upper - 0.5962) < 1e-3
    # Symmetric around 0.5 at phat=0.5.
    assert abs((ci.lower + ci.upper) - 1.0) < 1e-9


def test_wilson_clamped_and_ordered():
    ci = wilson_interval(500, 500)  # phat = 1.0
    assert ci.phat == 1.0
    assert ci.lower < 1.0  # lower bound strictly below 1
    assert ci.upper == 1.0  # clamped
    zero = wilson_interval(0, 500)
    assert zero.lower < 1e-9  # analytically 0 at 0 successes (float residue only)
    assert 0.0 < zero.upper < 1.0
    empty = wilson_interval(0, 0)
    assert (empty.phat, empty.lower, empty.upper, empty.n) == (0.0, 0.0, 0.0, 0)


def test_wilson_accepts_fractional_successes():
    # Ties contribute half-wins; the interval must accept fractional successes.
    ci = wilson_interval(250.5, 500)
    assert abs(ci.phat - 0.501) < 1e-12


def test_pass_at_k_monotone_in_k():
    samples = [1.0, 2.0, 3.0, 4.0, 5.0]
    p2 = pass_at_k(samples, 2.0).interval.phat
    p3 = pass_at_k(samples, 3.0).interval.phat
    assert p2 == 0.4  # {1,2} <= 2
    assert p3 == 0.6  # {1,2,3} <= 3
    assert p3 >= p2  # pass@k is non-decreasing in k


def test_bradley_terry_two_item_ranking_and_convergence():
    # i beats j 400/500; j beats i 100/500. i should outrank j and converge.
    items = ["i", "j"]
    wins = {("i", "j"): 400.0, ("j", "i"): 100.0}
    comps = {("i", "j"): 500.0, ("j", "i"): 500.0}
    bt = bradley_terry_mle(items, wins, comps, prior=1.0)
    assert bt.converged
    assert bt.ranking == ["i", "j"]
    assert bt.strengths["i"] > bt.strengths["j"]
    assert abs(sum(bt.strengths.values()) - 1.0) < 1e-9


def test_bradley_terry_smoothing_prevents_separation_divergence():
    # Complete separation: i beats j every time. Unregularised MLE diverges;
    # the smoothing prior must yield a finite, convergent, correctly-ordered fit.
    items = ["i", "j"]
    wins = {("i", "j"): 500.0, ("j", "i"): 0.0}
    comps = {("i", "j"): 500.0, ("j", "i"): 500.0}
    bt = bradley_terry_mle(items, wins, comps, prior=1.0)
    assert bt.converged
    assert bt.ranking == ["i", "j"]
    assert math.isfinite(bt.strengths["j"]) and bt.strengths["j"] >= 0.0
    assert bt.strengths["i"] > bt.strengths["j"]


def test_bradley_terry_transitive_chain():
    # a >> b >> c by construction; BT must reconcile to a > b > c.
    items = ["a", "b", "c"]
    wins = {
        ("a", "b"): 450.0, ("b", "a"): 50.0,
        ("b", "c"): 450.0, ("c", "b"): 50.0,
        ("a", "c"): 490.0, ("c", "a"): 10.0,
    }
    comps = {k: 500.0 for k in wins}
    bt = bradley_terry_mle(items, wins, comps, prior=1.0)
    assert bt.converged
    assert bt.ranking == ["a", "b", "c"]
