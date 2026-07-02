# PayHELM Dimension-2 (authorization latency / RAPL) — HANDOFF

**Branch:** dim-2 work was cut on `paybench/dim2-auth-latency`, then **merged to `paybench/poc`**
(where it now lives alongside frozen dim-1). The `main` merge is a founder/PR step (main is PR-gated).

> **Status (2026-06-30): RATIFIED, FROZEN, TRIPLE-ANCHORED, OSF-REGISTERED (embargoed), IA-ARCHIVED.**
> This supersedes the earlier "gate-cleared / pre-registerable / founder-must-decide" state. Every item
> on the old decide/do list is done (ratified 2026-06-24; ceremony completed 2026-06-29→30). What remains
> is the **Variant-E-deferred real-rail run**, the **held arXiv submission**, and the **Day-0 release**.
> See "What remains" below.

## The doctrine as ratified (dim-2 v1, 2026-06-24)

- **Metric: RAPL** (Rail Authorization-Primitive Latency), **SPLIT** into two never-cross-compared
  sub-rankings — **A = Payment-Validation** (facilitator/`verify` accept) and **B = Challenge-Issuance**
  (the 402). Racing all six rails as one ranking was the original category error.
- **DR4 — group-and-decompose:** group rails by work-class, report a per-rail decomposition tuple,
  **no single cross-class ordinal**.
- **FR1 numeric fallback triggers (confirmed):** BT → survival/Cox-PH when **tie > 20% / censoring > 5% /
  cyclic-triples > 10% / BT-fit LR p < 0.05**. Set → pre-registered → honoured even if it forces the
  survival model (does not tune to flatter BT).
- **FR4:** **≥ 2 topologies mandatory.**
- Cross-lineage gate arc (DeepSeek/Gemini/Kimi/Qwen): **0–4 (category error) → 3–1 (SPLIT) → 4/4
  (pre-registerable) → round-4 work-type scan 4/4 → DR4.** See `dim2-adversarial-review.md`,
  `dim2-worktype-synthesis.md`.

## The harness — re-aligned to the SPLIT design (DONE)

- `mockbench/dimensions.py` carries the **A/B SPLIT** (`AUTH_LATENCY_A` / `AUTH_LATENCY_B`, 10 pairs each);
  `fixtures.py`/`bench.py`/`cli.py` thread the dimension. **21/21 tests green** (`tests/test_auth_latency.py`).
- **Frozen finality preserved bit-for-bit:** run_hash `sha256:895f99ed…b14ee0`, unperturbed by the dim-2
  generalisation (pinned in CI + `test_finality_artefact_is_unperturbed_by_generalisation`).
- The A/B run_hashes reproduce deterministically. Calibration is now **real first-party pilot data**, not
  placeholder — all six rails instrumented + run-validated (`mblake4u/agentpay`, branch
  `dim2-rapl-instrumentation`). Pilot medians in `dim2-q4-pilot-log.md` (indicative until the real-rail run
  flips them to scored).

```bash
# finality (frozen) — must print run_hash 895f99…b14ee0
python -m paybench.mockbench.cli run
# auth-latency A/B (calibrated pilot fixtures)
python -m paybench.mockbench.cli all -d auth-latency
python -m pytest paybench/mockbench/tests/ --noconftest -c /dev/null -q
```

## The freeze (ceremony completed 2026-06-29 → 30)

- **Manifest** `dim2-prereg-manifest.sha256` = `46a19eab516ef3214270513f718bd07a846e18a4f42d9916fcb829da71dcd388`
  (32 files).
- **Signed tag** `paybench-rapl-prereg-v1` (YubiKey EdDSA, `mblake@everydayai.link`) → freeze commit
  `3dd74caa`.
- **OpenTimestamps** → Bitcoin block **955977**; **cosign** → Rekor **logIndex 2012836917**.
- **OSF** Open-Ended Registration (project `Gv8j7`, RAPL component) — **embargoed to 2026-07-17 (Day-0)**.
- **Internet Archive** item `dim2-auth-latency`.
- Registration record: `dim2-PRE-REGISTRATION.md`; ceremony: `dim2-CEREMONY-RUNBOOK.md`; de-drafted
  doctrine: `dim2-auth-latency.md`; scored-results write-up: `dim2-scored-results.md`.

> ⚠️ **freeze-evidence STATUS = LEGACY, not PASS.** The break-it gauntlet (round 1) ran *after* this freeze,
> so it cannot honestly be marked PASS — that ordering is exactly the gap `CEREMONY-PREFLIGHT` gates 8 & 9
> (added 2026-06-30) now close. The structural `[GAP]` items ride the planned real-rail re-registration,
> which will run gates 8 & 9 and should mark STATUS: PASS. See `freeze-evidence/paybench-rapl-prereg-v1.md`.

## Multi-topology (FR4) — status

- **T1 devbox** — pilot baseline (all six rails).
- **T2a GitHub Codespaces (Azure)** — **PASSED**: A order held (Solana < Stellar < Base), B heterogeneity
  held; finding — **local rails host-sensitive, network rails path-sensitive**.
- **T2b OCI uk-london-1** — Stellar full-N re-run **40/40, 0 censoring, ≈289 ms** (the earlier ~13% was a
  harness-classifier artefact, since fixed). Paid VM terminated after the run.
- Raw samples curated into `paybench/evidence/dim2-topology/` (+ README + SHA256SUMS).

## Post-freeze hardening (2026-06-28 → 30)

- **Defense dossier + gauntlet round 1** (`DEFENSE-DOSSIER.md`, `gauntlet-r1-disposition-sheet.md`):
  **G-F1** (finality↔RAPL split contradiction) ratified as **errata** (split-on-KIND / label-on-CLASS;
  uniform-reliance secondary cut spec'd, rides the real-rail run). `[DISC]` disclosures landed as
  `ERRATA.md` E2–E6; E1 tightens the uniform-reliance spec.
- **Process gates:** `CEREMONY-PREFLIGHT` gained gate **8** (pre-freeze gauntlet) + gate **9**
  (cross-dimension split-vs-label consistency) + freeze-the-classifier.
- **freeze-guard:** committed `freeze-evidence/<tag>.md` attestation enforced by a **pre-push hook** +
  the **"Guard frozen prereg tags"** tag-immutability ruleset + a **freeze-guard CI** workflow
  (PR #1 → merged to `main`).

## What remains (the real "next")

| # | Step | Notes |
|---|---|---|
| 1 | **arXiv** (held) | On `cs.CR` endorsement `3666MT`: recompile combined two-dimension paper (Overleaf; incl. COI paragraph; +`cs.PF`), update held submission, write the arXiv id back into `CEREMONY-RUNBOOK.md`. Backup endorser draft ready. |
| 2 | **Day-0 (2026-07-17)** | OSF DOI release, Wayback the now-public GitHub URLs, snapshot the OSF page. On Google Calendar + Notion Filing & Publishing Calendar. |
| 3 | **Real-rail run** (Variant-E deferred) | Re-registration pass that folds in the gauntlet residuals — G-R4/R8 (classifier + censoring bound), G-R2 (grouping threshold), G-F2 (adjacent-pair CIs), G-R3 (vary backing-service leg), G-R6 (AP2 sidecar); produces the **uniform-reliance cut**, the summed E2E (G-R1), golden adapter tests + raw transcripts (G-P4). Runs gates 8 & 9 → marks `freeze-evidence STATUS: PASS`. |
| 4 | **Gauntlet round 2** | Held; auto-triggers at the real-rail pre-freeze via gate 8. |
| ✅ | Ratify · calibrate · freeze · pre-register · re-align harness · PR→poc · prior-art re-check | All **done** (2026-06-22 → 30). |

## Tripwires honoured
Frozen finality v1.2 artefact untouched throughout (bit-for-bit). Real-rail rankings remain deferred
(Variant E). One-writer discipline; agentpay RAPL work safe on `origin/dim2-rapl-instrumentation`.

## Key artefacts
`dim2-auth-latency.md` (ratified doctrine) · `dim2-PRE-REGISTRATION.md` · `dim2-scored-results.md` ·
`dim2-prereg-manifest.sha256`(+`.ots`/`.cosign.bundle`) · `dim2-CEREMONY-RUNBOOK.md` ·
`CEREMONY-PREFLIGHT.md` (gates 8–9) · `DEFENSE-DOSSIER.md` · `gauntlet-r1-disposition-sheet.md` ·
`ERRATA.md` · `COMPETING-INTERESTS.md` · `freeze-evidence/paybench-rapl-prereg-v1.md` ·
`dim2-q4-pilot-log.md` · `dim2-topology2-run-plan.md` · `dimension-design-lessons.md` ·
`paybench/evidence/dim2-topology/`.
