"""Benchmark *dimensions* as first-class, parametric descriptors.

The harness was originally hard-wired to settlement-finality (methodology §3).
A *dimension* is now a first-class parameter so a second dimension —
authorization latency (§8 Resolution B, §11 roadmap), where AP2/R6 debuts — can
reuse the same seeded log-normal fixture machinery, content-addressing, and
BT/pass@k/Wilson stats without forking the code.

**Frozen-finality contract.** The settlement-finality dimension is part of the
pre-registered, Bitcoin-anchored v1.2 artefact: its fixture content-hashes and
its run report ``run_hash`` are frozen and must reproduce *bit-for-bit*. The
``FINALITY`` descriptor below is therefore pinned to the exact strings, seed
domains, schema names, rail set, and k-grid that the original hard-coded harness
used — every value here that feeds a hashed payload (``dimension``, ``unit``,
the ``fixture:<rail>`` / ``pair:<a>:<b>`` seed domains, the fixture/run schema
strings, the k-grid, the rail order) is identical to the pre-refactor constant.
Generalising the harness must not perturb a single byte of the finality path; the
``test_reproducibility`` suite asserts this.

The new ``AUTH_LATENCY`` descriptor carries its **own** seed namespace
(``auth-latency``) so its RNG streams are domain-separated from finality's — two
dimensions sharing the one published master seed, never the same stream — and its
own provenance files, fixture-filename infix, run schema, and k-grid.

Pure stdlib; no third-party deps (consistent with the rest of the harness).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from . import K_GRID_SECONDS, SETTLING_RAILS
from .paths import FIXTURES_DIR, PROVENANCE_DIR, RAIL_PROVENANCE, RUNS_DIR

# Shared fixture-payload schema (dimension-agnostic; the payload's ``dimension``
# field is what distinguishes a finality fixture from an auth-latency one).
FIXTURE_SCHEMA = "paybench.fixture.v1"


@dataclass(frozen=True)
class Dimension:
    """One benchmarked dimension: its identity, rail set, units, and provenance.

    ``key`` is the internal/filename id (``finality`` / ``auth-latency``).
    ``dimension`` is the value written into every hashed fixture payload and run
    report — for finality it MUST stay ``"settlement-finality"``. ``direction``
    records that *lower is better* for both dimensions (the race semantics in
    ``bench.race_pair`` — lower wins — are therefore identical and reused as-is).
    ``seed_namespace`` is prepended to the RNG seed domains; ``""`` for finality
    (so its domains stay ``fixture:<rail>`` / ``pair:<a>:<b>``), a real namespace
    for every other dimension so their streams never collide with finality's.
    """

    key: str
    name: str
    dimension: str
    unit: str
    direction: str
    rails: tuple[str, ...]
    k_grid: tuple[float, ...]
    run_schema: str
    seed_namespace: str
    provenance_files: dict[str, str]
    fixture_schema: str = FIXTURE_SCHEMA

    # --- seed domains (domain-separated from the single master seed, §6) ------

    def _ns(self) -> str:
        return f"{self.seed_namespace}:" if self.seed_namespace else ""

    def fixture_seed_domain(self, rail_id: str) -> str:
        """Per-rail fixture-sampling seed domain (``fixture:<rail>`` for finality)."""
        return f"fixture:{self._ns()}{rail_id}"

    def pair_seed_domain(self, a: str, b: str) -> str:
        """Per-pair race seed domain (``pair:<a>:<b>`` for finality)."""
        return f"pair:{self._ns()}{a}:{b}"

    # --- filesystem layout ----------------------------------------------------

    def provenance_path(self, rail_id: str) -> Path:
        return PROVENANCE_DIR / self.provenance_files[rail_id]

    def fixture_path(self, rail_id: str) -> Path:
        return FIXTURES_DIR / f"{rail_id}-{self.key}.fixture.json"

    def run_path(self) -> Path:
        return RUNS_DIR / f"{self.key}-run.json"


# --- Dimension 1: settlement-finality (FROZEN v1.2 — do not perturb) ----------

# Every field is pinned to the original hard-coded harness so the finality
# fixtures and run report reproduce bit-for-bit. ``key="finality"`` reproduces
# the ``<rail>-finality.fixture.json`` / ``finality-run.json`` names; the empty
# seed namespace reproduces the ``fixture:<rail>`` / ``pair:<a>:<b>`` domains.
FINALITY = Dimension(
    key="finality",
    name="settlement-finality",
    dimension="settlement-finality",
    unit="seconds",
    direction="lower-is-better",
    rails=tuple(SETTLING_RAILS),
    k_grid=tuple(K_GRID_SECONDS),
    run_schema="paybench.finality-run.v1",
    seed_namespace="",
    provenance_files=dict(RAIL_PROVENANCE),
)


# --- Dimension 2: authorization latency (§8 Resolution B; §11 Day-30) ---------

# The auth-latency rail set is the 5 settling rails + R6 (AP2), which debuts here
# (§8). C(6,2)=15 pairs. PLACEHOLDER calibration only — real numbers are a
# founder step (see the auth-latency provenance files + dim2 DRAFT addendum).
AUTH_LATENCY_RAILS = ("R1", "R2", "R9", "R10", "R11", "R6")

AUTH_LATENCY_PROVENANCE = {
    "R1": "R1-x402-base-auth-latency.provenance.yaml",
    "R2": "R2-x402-stellar-auth-latency.provenance.yaml",
    "R9": "R9-x402-solana-auth-latency.provenance.yaml",
    "R10": "R10-mpp-tempo-auth-latency.provenance.yaml",
    "R11": "R11-mpp-lightning-auth-latency.provenance.yaml",
    "R6": "R6-gcp-ap2-auth-latency.provenance.yaml",
}

# Authorization latency is sub-second-to-a-few-seconds (mandate verify / 402
# challenge-response / credential check), faster than finality — so the pass@k
# grid is finer and tighter than finality's [2..20]s. PLACEHOLDER grid pending
# founder ratification at pre-registration.
AUTH_LATENCY_K_GRID = (0.25, 0.5, 1, 2, 3, 5)

AUTH_LATENCY = Dimension(
    key="auth-latency",
    name="authorization-latency",
    dimension="authorization-latency",
    unit="seconds",
    direction="lower-is-better",
    rails=AUTH_LATENCY_RAILS,
    k_grid=AUTH_LATENCY_K_GRID,
    run_schema="paybench.auth-latency-run.v1",
    seed_namespace="auth-latency",
    provenance_files=AUTH_LATENCY_PROVENANCE,
)


# --- Registry -----------------------------------------------------------------

DIMENSIONS: dict[str, Dimension] = {d.key: d for d in (FINALITY, AUTH_LATENCY)}


def get_dimension(key: str) -> Dimension:
    try:
        return DIMENSIONS[key]
    except KeyError:
        valid = ", ".join(sorted(DIMENSIONS))
        raise ValueError(f"unknown dimension {key!r}; valid: {valid}") from None
