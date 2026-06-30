# Freeze-evidence — <TAG-NAME>

Copy this file to `freeze-evidence/<exact-tag-name>.md`, fill it in, **commit it in the same commit you tag**,
then create + push the tag. The `freeze-guard` pre-push hook and CI both refuse to publish a `paybench-*prereg*`
tag unless this file exists and attests the gates below. The guard checks the `STATUS:` line and (for PASS) the
two `GATE…:` lines — keep those lines machine-readable; prose around them is free.

STATUS: PASS

GATE8-GAUNTLET: PASS
GATE9-XDIM: PASS

- **Dimension / manifest:** `<dim>-prereg-manifest.sha256` = `<sha256>`
- **Tag:** `<tag-name>`  ·  **Freeze date:** `<YYYY-MM-DD>`

## Gate 8 — pre-freeze adversarial gauntlet (CEREMONY-PREFLIGHT §8)
Ran the break-it gauntlet over the to-be-frozen design *before* anchoring. Record: who/what ran it, how many
adversaries, and the triage. **Pass bar: no surviving `[GAP]`-tier attack** (only disclosed `[DISC]` remain).
- Result file(s): `<path to gauntlet result / disposition sheet>`
- Surviving GAPs: **none** (list must be empty to mark PASS).

## Gate 9 — cross-dimension doctrine consistency (CEREMONY-PREFLIGHT §9)
Diffed this dimension's load-bearing doctrines against every already-frozen dimension under the split-vs-label
rule (split on event-*kind*; label on trust-*class*). **Pass bar: rule applied identically; no contradiction.**
- Prior dimensions checked: `<list>`
- Diff / reconciliation note: `<path, e.g. ERRATA.md entry>`
