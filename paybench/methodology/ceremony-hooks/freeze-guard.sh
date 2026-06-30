#!/usr/bin/env bash
# freeze-guard.sh — single source of truth for the pre-registration freeze gate.
#
# Refuses to bless a `paybench-*prereg*` tag unless a committed freeze-evidence file
# attests that CEREMONY-PREFLIGHT gates 8 (pre-freeze gauntlet) and 9 (cross-dimension
# consistency) passed. Called by BOTH the local pre-push hook and the freeze-guard CI job,
# and runnable by hand as a pre-freeze self-check.
#
# Usage:  freeze-guard.sh <tag-name> [<commit-ish, default HEAD>]
# Exit:   0 = OK / allowed (PASS or LEGACY) · 1 = blocked · 2 = usage/repo error
#
# Evidence file (committed in the tagged commit):
#   paybench/methodology/freeze-evidence/<tag-name>.md
# Required machine-checkable lines:
#   STATUS: PASS        -> also requires  GATE8-GAUNTLET: PASS  and  GATE9-XDIM: PASS
#   STATUS: LEGACY      -> allowed (freeze predates the gates; gaps tracked in ERRATA.md)

set -u

TAG="${1:-}"
COMMIT="${2:-HEAD}"
[ -n "$TAG" ] || { echo "freeze-guard: usage: freeze-guard.sh <tag-name> [<commit>]" >&2; exit 2; }

REL="paybench/methodology/freeze-evidence/${TAG}.md"

cobj="$(git rev-parse --verify --quiet "${COMMIT}^{commit}")" || {
  echo "freeze-guard: cannot resolve commit '${COMMIT}'" >&2; exit 2; }

if ! git cat-file -e "${cobj}:${REL}" 2>/dev/null; then
  echo "FREEZE-GUARD: BLOCKED — no freeze-evidence committed for tag '${TAG}'." >&2
  echo "  expected (in the tagged commit): ${REL}" >&2
  echo "  CEREMONY-PREFLIGHT gates 8 (gauntlet) + 9 (cross-dimension) must be attested before a" >&2
  echo "  *-prereg-* tag is published. Copy freeze-evidence/TEMPLATE.md, fill it, commit, then tag." >&2
  exit 1
fi

body="$(git cat-file -p "${cobj}:${REL}")"
status="$(printf '%s\n' "$body" | grep -iE '^STATUS:' | head -1 | sed -E 's/^STATUS:[[:space:]]*//I' | tr -d '[:space:]')"
status_uc="$(printf '%s' "$status" | tr '[:lower:]' '[:upper:]')"

case "$status_uc" in
  PASS)
    if printf '%s\n' "$body" | grep -qiE '^GATE8-GAUNTLET:[[:space:]]*PASS' \
    && printf '%s\n' "$body" | grep -qiE '^GATE9-XDIM:[[:space:]]*PASS'; then
      echo "FREEZE-GUARD: OK — '${TAG}' attests gate 8 (gauntlet) + gate 9 (cross-dimension) PASS."
      exit 0
    fi
    echo "FREEZE-GUARD: BLOCKED — '${TAG}' is STATUS: PASS but is missing a" >&2
    echo "  'GATE8-GAUNTLET: PASS' and/or 'GATE9-XDIM: PASS' line." >&2
    exit 1 ;;
  LEGACY)
    echo "FREEZE-GUARD: ALLOW (legacy) — '${TAG}' predates the gates; gaps tracked in ERRATA.md."
    exit 0 ;;
  "")
    echo "FREEZE-GUARD: BLOCKED — '${TAG}' evidence has no 'STATUS:' line (need PASS or LEGACY)." >&2
    exit 1 ;;
  *)
    echo "FREEZE-GUARD: BLOCKED — '${TAG}' has unrecognised STATUS '${status}' (need PASS or LEGACY)." >&2
    exit 1 ;;
esac
