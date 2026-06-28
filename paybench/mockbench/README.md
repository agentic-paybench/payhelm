# PayBench MockBench harness

Pure-stdlib Python harness for the **settlement-finality** benchmark (N16 MockBench).
It generates calibrated, content-addressed fixtures from each settling rail's empirical
log-normal finality distribution and scores the pairwise finality races with Bradley-Terry
MLE + pass@k + Wilson lower-bound CIs.

> Instantiates the closed decisions: **N16 MockBench architecture**, **N6 hybrid-tiered
> schema** (Tier-1 settlement-finality only), and the **first-benchmark-scope / Resolution B**
> design. See `../methodology/methodology.md` §5–§8 and `../calibration/calibration-plan.md`.

## Usage

```bash
# from the payhelm repo root
python -m paybench.mockbench.cli generate   # gen fixtures + write provenance fixture_content_hash
python -m paybench.mockbench.cli verify     # re-verify fixture hashes vs provenance
python -m paybench.mockbench.cli run        # run the 5,000-trial finality benchmark
python -m paybench.mockbench.cli all        # generate then run
```

No third-party dependencies (no numpy/scipy). Python 3.9+.

## Dimensions

The harness is **dimension-parametric** (`mockbench/dimensions.py`). Every
subcommand takes `--dimension {finality,auth-latency}` (`-d`), defaulting to
`finality`:

- **`finality`** (default) — the frozen, pre-registered v1.2 settlement-finality
  benchmark: 5 settling rails → C(5,2) = 10 pairs → 5,000 trials. Its fixture
  hashes and `run_hash` are frozen and reproduce bit-for-bit (the `FINALITY`
  descriptor is pinned to the original constants; CI + tests guard it).
- **`auth-latency`** — the Day-30 authorization-latency dimension (§11), where
  **AP2/R6 debuts** (§8 Resolution B): 6 rails → C(6,2) = 15 pairs → 7,500 trials.
  Calibration is **PLACEHOLDER** pending founder sourcing — see
  `../methodology/dim2-auth-latency.DRAFT.md` and `../SESSION-1-HANDOFF.md`.

```bash
python -m paybench.mockbench.cli all -d auth-latency   # generate + run the auth-latency dimension
```

Dimensions share the one published master seed but are RNG-domain-separated
(`fixture:<rail>` vs `fixture:auth-latency:<rail>`), so neither perturbs the
other's streams.

## What it does

1. **Fixture generation** (`fixtures.py`). For each of the 5 settling rails (R1, R2, R9, R10,
   R11) it reads `{median_s, sigma_log}` from the rail's calibration provenance and draws
   `N_FIXTURE_SAMPLES` (5,000) seeded log-normal finality samples. Samples are quantised to 6 dp
   and serialised as fixed-format decimal strings so the canonical bytes are byte-stable.
2. **Content-addressing**. Each fixture is sha256-hashed over its payload (calibration + seed +
   samples); the hash is written into the fixture file *and* back into the rail's provenance
   `fixture_content_hash` (a surgical, comment-preserving line edit — no YAML round-trip).
3. **Benchmark** (`bench.py`). 5 rails → C(5,2) = **10 pairs** → **500 trials/pair = 5,000
   trials**. Each trial is a finality race: draw one sample for each rail from its fixture
   population; lower finality wins (ties split 0.5/0.5). Loading a fixture re-verifies its content
   hash, so the run records and checks the exact fixture bytes it consumes.
4. **Scoring** (`stats.py`). Bradley-Terry MLE (relative ranking) + pass@k = P(finality ≤ k)
   over the calibrated population (absolute thresholds) + Wilson 95% lower-bound CIs on every
   proportion.

## Reproducibility (methodology §5.4 item 6, §6)

A **single published master seed** (`MASTER_SEED = 20260717`) drives every stochastic step,
domain-separated per stream via `sha256(f"{seed}:{domain}")`. Same seed + same fixtures →
bit-for-bit identical fixture hashes **and** an identical run report (`run_hash`). The run
report carries no wall-clock, so it is byte-stable across executions.

## Design notes / honest caveats

- **BT smoothing prior.** Widely-separated rails (a ~2 s rail vs a ~16 s rail) win ~100 % of
  their races — *complete separation* — under which the unregularised BT MLE diverges to the
  boundary and never converges. `bradley_terry_mle` applies a symmetric additive (Beta) prior
  (`prior=1.0` pseudo-win per pair-direction), standard BT regularisation; with 500 real
  trials/pair it is a negligible pull on the well-identified estimates but guarantees a finite,
  convergent fit. Recorded as `smoothing_prior` in the run report.
- **BT vs pass@k.** When rails are far apart in finality, BT strengths collapse toward 0 for the
  slow rails — *correct* BT behaviour, and exactly why the methodology pairs the relative BT
  ranking with the absolute, interpretable pass@k. Read them together.
- **Calibrated mock, not real-rail.** Per Variant E, this harness exercises the full
  measurement + statistics pipeline against *calibrated mock fixtures*. Real-rail rankings are
  the Q3 HELD residual and are not produced here.

## Layout

```
paybench/mockbench/
  __init__.py     pre-registered design constants (seed, rails, N, trials, k-grid, z)
  paths.py        filesystem layout + rail→provenance/fixture mapping
  fixtures.py     calibration parsing, seeded sampling, content-addressing, provenance write-back
  stats.py        Bradley-Terry MLE, pass@k, Wilson LB
  bench.py        the 10-pair / 5,000-trial harness + report
  cli.py          generate / verify / run / all
  tests/          reproducibility + known-answer stats tests
paybench/fixtures/  generated fixture JSON (content-addressed)   [committable]
paybench/runs/      generated run report (deterministic)          [committable]
```
