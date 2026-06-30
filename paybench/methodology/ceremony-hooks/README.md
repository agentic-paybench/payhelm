# Ceremony hooks — the freeze gate

Machinery that **refuses to publish a `paybench-*prereg*` tag** unless the freeze is accompanied by committed
**freeze-evidence** attesting CEREMONY-PREFLIGHT gates 8 (pre-freeze gauntlet) and 9 (cross-dimension
consistency). A pre-registration freeze is only "real" once the tag is pushed and anchored, so **push** is the
enforced boundary — blocking local `git tag` would also break `git fetch`/`clone` of the existing frozen tags.

## Parts
- `freeze-guard.sh` — the rule, in one place. `freeze-guard.sh <tag> [<commit>]` → exit 0 (PASS/LEGACY) or 1.
- `pre-push` — local hook; refuses to push a prereg tag the guard rejects. Instant feedback. Break-glass:
  `PAYBENCH_FREEZE_OVERRIDE=1 git push …`.
- `install-hooks.sh` — copies `pre-push` into this clone's hooks dir (hooks aren't version-controlled).
- `../../.github/workflows/freeze-guard.yml` — CI backstop; same `freeze-guard.sh` on every pushed prereg tag.
  Server-side, cannot be bypassed locally → make it a **required status check** for full teeth.
- `../freeze-evidence/<tag>.md` — the attestation, one per freeze. `TEMPLATE.md` is the form.

## Install (once per clone)
```
bash paybench/methodology/ceremony-hooks/install-hooks.sh
```

## What it enforces (and what it does NOT)
- **Enforces:** a named, committed attestation exists for every published freeze, and a `STATUS: PASS` freeze
  carries explicit `GATE8-GAUNTLET: PASS` + `GATE9-XDIM: PASS` lines. No silent freeze.
- **Does NOT** verify the gauntlet actually ran or that the doctrines are truly consistent — it forces the
  human sign-off to exist and be part of the anchored byte-set; the operator still must not lie in it. It is a
  checklist gate with cryptographic provenance, not an oracle.
- `STATUS: LEGACY` is the honest escape for freezes that predate the gates (the two existing tags); it is
  allowed so re-pushing historical tags doesn't break, but new freezes should be `PASS`.
