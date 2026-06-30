# Freeze-evidence — paybench-rapl-prereg-v1 (authorization latency / RAPL, dim-2)

STATUS: LEGACY

- **Manifest:** `dim2-prereg-manifest.sha256` = `46a19eab516ef3214270513f718bd07a846e18a4f42d9916fcb829da71dcd388`
- **Tag:** `paybench-rapl-prereg-v1`  ·  Bitcoin block 955977 · Rekor logIndex 2012836917

**Why LEGACY.** This freeze predates CEREMONY-PREFLIGHT gates 8 & 9 (added 2026-06-30). The break-it gauntlet
(round 1) ran *after* this freeze, so it cannot honestly be marked PASS — that ordering is exactly the gap
gate 8 now closes.

- **Gate 8 (gauntlet):** ran post-freeze (round 1, Opus-lineage). Surviving attacks and their dispositions are
  in `gauntlet-r1-disposition-sheet.md`; the structural `[GAP]` items ride the planned real-rail
  re-registration (which will itself run gates 8 & 9 and should mark STATUS: PASS).
- **Gate 9 (cross-dimension):** the finality↔RAPL split-vs-label consistency is reconciled in `ERRATA.md` E1.
