# PayHELM Dimension-2 (authorization latency / RAPL) — HANDOFF

**Branch:** `paybench/dim2-auth-latency` (cut from `paybench/poc`). **Not** PR'd — that is a founder
step, once the dimension is ratified + pre-registered.

> **Status (2026-06-22): doctrine GATE-CLEARED and PRE-REGISTERABLE.** The dimension went through
> three cross-lineage adversarial rounds (**0–4 → 3–1 → 4/4**); see "How we got here". What remains
> is founder/credentialed work: confirm the FR1 thresholds, run the Q4 validation/calibration,
> ratify, pre-register, PR.

## The harness (mechanical, autonomous — built session 1)

1. **Dimension-parametric harness.** `mockbench/dimensions.py` adds a first-class `Dimension`
   descriptor; `fixtures.py`/`bench.py`/`cli.py` thread `dim=FINALITY` by default. CLI gained
   `--dimension {finality,auth-latency}`. **21/21 tests green** (`tests/test_auth_latency.py`).
2. **Frozen finality preserved bit-for-bit:** run_hash `sha256:895f99ed…b14ee0`, ranking
   `R10,R1,R2,R9,R11`; pinned in CI + `test_finality_artefact_is_unperturbed_by_generalisation`.

> ⚠️ **The harness still runs the *pre-gate* single 6-rail / 15-pair placeholder race.** The doctrine
> has since been redesigned (SPLIT, below); **re-aligning the harness** (two sub-rankings,
> Tempo-Session-only, ms k-ladder, hardened-BT) is a **post-ratification** task — deliberately not
> built against an un-ratified design. The harness's auth-latency numbers are a *working pipeline*,
> **not a result** (all calibration is PLACEHOLDER).

```bash
# finality (frozen) — must print run_hash 895f99…b14ee0
python -m paybench.mockbench.cli run
# auth-latency (PLACEHOLDER, pre-gate single-race pipeline)
python -m paybench.mockbench.cli all -d auth-latency
python -m pytest paybench/mockbench/tests/ --noconftest -c /dev/null -q
```

## How we got here (the methodology arc — the substantive work)

- **Research (3 passes):** all six rails' authorization checkpoints are **primary-source-validated**
  (`dim2-auth-latency.research.md`); ISO-8583 auth-vs-settlement is conceptual precedent; no prior
  "authorization latency" benchmark surfaced (novelty plausible — *re-check before publishing*).
- **Cross-lineage gate (`dim2-adversarial-review.md`):**
  - **Round 1 — refuted 0–4.** Racing all six rails as one ranking was a **category error** (L402's
    macaroon is a *grant-to-pay*, not a validation of payment).
  - **Round 2 — SPLIT validated 3–1**, + a refinement list (RR1–RR6).
  - **Round 3 — PRE-REGISTERABLE 4/4**, conditional on fixes (FR1–FR5); the panel caught two real
    bugs (RR5-on-Group-B, first-byte gaming) — both fixed.
- **The doctrine now (`dim2-auth-latency.DRAFT.md` §2), renamed _Rail Authorization-Primitive
  Latency_ (RAPL):** two within-group races — **A Payment-Validation** (x402×3, Tempo-Session, AP2;
  Tempo-Charge excluded) and **B Challenge-Issuance** (x402×3, Tempo, L402); hardened-BT (Davidson
  ties + censoring) with a **Cox-PH data-triggered fallback**; metric renamed `P(auth ≤ k)`; ms
  k-ladder; client-side last-byte RTT-subtracted measurement; anti-gaming + visibility/scope labels.

## What the founder must DECIDE / DO next (in order)

| # | Step | Notes |
|---|---|---|
| 1 | **Confirm the FR1 fallback thresholds** | Numeric BT→Cox-PH triggers (proposed: tie>20% / censoring>5% / cyclic-triples>10%) — a statistician's call; **best set from the Q4 pilot** (below) |
| 2 | **Run the Q4 validation/calibration** (credentialed) | Plan: `dim2-validation-run-plan.md`. Pilots FR1 + the power analysis **and** replaces PLACEHOLDER fixtures with real `{median,sigma}`. **Runs *before* pre-registration** (mirrors D1 calibrate-before-freeze). Needs a thin `/verify` route + RTT endpoint added to the POC adapters (`mblake4u/agentpay`). |
| 3 | **Ratify the doctrine** | Fold the gate-cleared §2 into `methodology.md` as a real section (not DRAFT) |
| 4 | **Pre-registration ceremony** | OSF / cosign / OpenTimestamps / signed tag — a founder ceremony, as for D1 |
| 5 | **Harness re-alignment** | Re-build the harness to the SPLIT design (two sub-rankings, ms ladder, hardened-BT) |
| 6 | **PR → `paybench/poc`** | Session-4 reproducibility CI already guards finality on the PR |
| — | **Prior-art novelty re-check** | The round-3 prior-art pass was partly truncated; confirm before any *published* novelty claim |

## Discipline for Q4 → FR1 (don't undo the gate)
The Q4 pilot **informs** principled FR1 thresholds; it must **not tune** them to flatter BT on the
data that will be scored (that re-creates the post-hoc method-switching the panel rejected). Set →
pre-register → honour the trigger even if it forces the survival model.

## Tripwires honoured this session
No frozen v1.2 artefact touched (finality bit-for-bit); **nothing ratified or pre-registered**;
doctrine remains DRAFT; **no real calibration committed** (placeholders only; the real Solana figure
withheld); no adapters modified / nothing run against testnets. One-writer discipline maintained
(one Syncthing index-desync incident this session, recovered via `git reset`, no data loss).

## Key artefacts
`dim2-auth-latency.DRAFT.md` (doctrine) · `dim2-auth-latency.research.md` (evidence) ·
`dim2-adversarial-review.md` (3 gate rounds + verdicts) · `dim2-review{,2,3}-{model}.md` (raw
replies) · `dim2-validation-run-plan.md` (Q4 plan) · `dimension-design-lessons.md` (cross-dimension
knock-on + new-dimension checklist).
