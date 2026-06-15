# Session 1 — PayHELM Dimension-2 (authorization latency) — HANDOFF

**Branch:** `paybench/dim2-auth-latency` (cut from `paybench/poc`). **Not** PR'd —
that is a later founder step, once the dimension is calibrated + pre-registered.

## What this session built (mechanical, autonomous)

1. **Dimension-parametric harness.** `paybench/mockbench/dimensions.py` adds a
   first-class `Dimension` descriptor; `fixtures.py`, `bench.py`, `cli.py` now
   thread `dim=FINALITY` by default. CLI gained `--dimension {finality,auth-latency}`.
2. **Auth-latency dimension.** 6 rails (R1, R2, R9, R10, R11, **+ R6/AP2 — debuts
   here**, §8 Resolution B) → C(6,2) = 15 pairs → 7,500 trials. Seeded log-normal
   fixtures, content-addressed, provenance written back.
3. **Tests.** `tests/test_auth_latency.py` mirrors the finality suite + adds
   cross-dimension RNG-isolation and a frozen-finality-hash pin. **21/21 green.**
4. **DRAFT methodology** `methodology/dim2-auth-latency.DRAFT.md` (proposed, not
   adopted).

## Frozen-finality guarantee (verified)

The dimension-1 settlement-finality artefact is **bit-for-bit unchanged**:
- run_hash `sha256:895f99ed…b14ee0` (unchanged), ranking `R10, R1, R2, R9, R11`;
- `cli verify` passes; no git diff on `paybench/{runs,fixtures,calibration/provenance}`
  finality files;
- pinned in CI (`.github/workflows/paybench-reproducibility.yml`) **and** in
  `test_auth_latency.py::test_finality_artefact_is_unperturbed_by_generalisation`.

## Reproduce

```bash
# finality (frozen) — must print run_hash 895f99…b14ee0
python -m paybench.mockbench.cli run
# auth-latency (placeholder) — 15 pairs / 7,500 trials
python -m paybench.mockbench.cli generate -d auth-latency
python -m paybench.mockbench.cli verify   -d auth-latency
python -m paybench.mockbench.cli run      -d auth-latency
# tests (isolated from HELM's root conftest)
python -m pytest paybench/mockbench/tests/ --noconftest -c /dev/null -q
```

## ⚠️ Everything calibration is PLACEHOLDER

Every `calibration/provenance/<rail>-auth-latency.provenance.yaml` is marked
**"PLACEHOLDER — pending founder calibration"**. The `{median_s, sigma_log}` are
illustrative, NOT measured. The auth-latency `run_hash`/ranking are deterministic
functions of those placeholders — they are not a result, only a working pipeline.

## What a founder must DECIDE / CALIBRATE next

| # | Decision (see DRAFT §6) | Why it's a founder call |
|---|---|---|
| Q1 | **AP2 (R6) scope** — time mandate-verify only, or verify + orchestration to first underlying-rail dispatch? | Defines what R6 means on this dimension |
| Q2 | **Solana authorization point** — is `confirmed`-level (~2.27s, captured in the D1 run, deliberately *withheld* from the placeholder) the right signal? | §3 disavows `confirmed` for *finality*; authorization is a different question |
| Q3 | **Ratify the per-rail authorization-point doctrine** (DRAFT §2 table), incl. the trust/equivalence-class column + named asymmetry | The D1 reliance-level analogue; doctrine, not mechanics |
| Q4 | **Real calibration** — first-party measure isolating the *authorize* leg from *settle*, per rail (+ doc/telemetry spread), replacing every placeholder | Judgment + first-party sourcing (Hybrid-C) |
| Q5 | **k-grid + BT prior** for sub-second separations | Pre-registered scoring constants |

## Then (NOT this session — tripwires)

- Fold the ratified doctrine into `methodology.md` as a real section (not a DRAFT).
- Run the **pre-registration ceremony** (OSF / cosign / OpenTimestamps / signed
  tag) for the dimension-2 design — a founder ceremony.
- **PR `paybench/dim2-auth-latency` → `paybench/poc`** (CI from Session 4 already
  guards finality on that PR).

## Tripwires honoured

No frozen v1.2 artefact touched; nothing pre-registered; per-rail doctrine left as
DRAFT for founder decision; no real calibration numbers committed (placeholders
only, the Solana real figure intentionally withheld). One-writer discipline: all
work on a single machine on this branch.

## Commits on this branch

1. `make MockBench dimension-parametric (finality frozen bit-for-bit)`
2. `auth-latency dimension fixtures + PLACEHOLDER provenance + report`
3. `auth-latency tests + DRAFT methodology addendum + handoff`
