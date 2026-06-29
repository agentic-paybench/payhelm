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

The RAPL dimension is SPLIT into two never-cross-raced sub-rankings
(``AUTH_LATENCY_A`` payment-validation, ``AUTH_LATENCY_B`` challenge-issuance;
doctrine §2). Each carries its **own** seed sub-namespace (``auth-latency:A`` /
``auth-latency:B``) so its RNG streams are domain-separated from finality's *and*
from each other — all sharing the one published master seed, never the same
stream — and its own provenance files, fixture-filename infix, run schema, and
ms k-ladder.

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


# --- Dimension 2: authorization latency / RAPL — the SPLIT (doctrine §2) -------

# RAPL is SPLIT into two sub-rankings that are NEVER cross-raced (the §8
# cross-lineage gate refuted the single 6-rail race 0–4 as a category error;
# methodology/dim2-auth-latency.md §2/§2.3):
#   A — Payment-Validation: x402 /verify (Base/Stellar/Solana) + Tempo-Session
#       voucher verify + AP2 mandate-verify.  C(5,2)=10 pairs.
#   B — Challenge-Issuance: x402 402 (Base/Stellar/Solana) + Tempo 402 +
#       L402 macaroon+BOLT11 (Lightning).      C(5,2)=10 pairs.
# x402 rails appear in BOTH (distinct primitives → distinct fixtures); AP2 is
# A-only (no 402), L402 is B-only (no pre-settlement validation). Each sub-ranking
# carries its own seed sub-namespace (auth-latency:A / :B) so its RNG streams are
# domain-separated from finality AND from each other.
#
# Calibrated from the first-party pilot {median, sigma} (Variant-E mock baseline,
# mirroring dim-1). Representative topology: T2b (uk-london-1, the citable named
# region) for network-dependent rails; canonical/host value for local-complete
# rails (AP2 in-process; Tempo-Session warm; local-402). The real multi-topology
# order + decomposition tuples live in methodology/dim2-scored-results.md (the
# single source of truth); these single-{median,sigma} fixtures are the
# reproducibility baseline, not the scored claim.

# ms k-ladder {20,50,100,250,500}ms in seconds (doctrine §2.5; supersedes the
# pre-gate [0.25..5]s grid).
AUTH_LATENCY_K_GRID = (0.02, 0.05, 0.1, 0.25, 0.5)

# Sub-ranking A — Payment-Validation (order = doctrine §2 table; BT ranks by
# strength, so registry order is presentational only).
AUTH_LATENCY_A_RAILS = ("R1", "R2", "R9", "R10", "R6")
AUTH_LATENCY_A_PROVENANCE = {
    "R1": "R1-x402-base-auth-latency-A.provenance.yaml",
    "R2": "R2-x402-stellar-auth-latency-A.provenance.yaml",
    "R9": "R9-x402-solana-auth-latency-A.provenance.yaml",
    "R10": "R10-mpp-tempo-auth-latency-A.provenance.yaml",
    "R6": "R6-gcp-ap2-auth-latency-A.provenance.yaml",
}

# Sub-ranking B — Challenge-Issuance.
AUTH_LATENCY_B_RAILS = ("R1", "R2", "R9", "R10", "R11")
AUTH_LATENCY_B_PROVENANCE = {
    "R1": "R1-x402-base-auth-latency-B.provenance.yaml",
    "R2": "R2-x402-stellar-auth-latency-B.provenance.yaml",
    "R9": "R9-x402-solana-auth-latency-B.provenance.yaml",
    "R10": "R10-mpp-tempo-auth-latency-B.provenance.yaml",
    "R11": "R11-mpp-lightning-auth-latency-B.provenance.yaml",
}

AUTH_LATENCY_A = Dimension(
    key="auth-latency-A",
    name="authorization-latency-A",
    dimension="authorization-latency:payment-validation",
    unit="seconds",
    direction="lower-is-better",
    rails=AUTH_LATENCY_A_RAILS,
    k_grid=AUTH_LATENCY_K_GRID,
    run_schema="paybench.auth-latency-A-run.v1",
    seed_namespace="auth-latency:A",
    provenance_files=AUTH_LATENCY_A_PROVENANCE,
)

AUTH_LATENCY_B = Dimension(
    key="auth-latency-B",
    name="authorization-latency-B",
    dimension="authorization-latency:challenge-issuance",
    unit="seconds",
    direction="lower-is-better",
    rails=AUTH_LATENCY_B_RAILS,
    k_grid=AUTH_LATENCY_K_GRID,
    run_schema="paybench.auth-latency-B-run.v1",
    seed_namespace="auth-latency:B",
    provenance_files=AUTH_LATENCY_B_PROVENANCE,
)


# --- Registry -----------------------------------------------------------------

DIMENSIONS: dict[str, Dimension] = {
    d.key: d for d in (FINALITY, AUTH_LATENCY_A, AUTH_LATENCY_B)
}


def get_dimension(key: str) -> Dimension:
    try:
        return DIMENSIONS[key]
    except KeyError:
        valid = ", ".join(sorted(DIMENSIONS))
        raise ValueError(f"unknown dimension {key!r}; valid: {valid}") from None
