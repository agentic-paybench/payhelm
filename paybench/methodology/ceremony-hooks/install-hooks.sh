#!/usr/bin/env bash
# Installs the freeze-guard pre-push hook into this clone's hooks dir.
# Git hooks are not version-controlled, so each clone runs this once.
set -eu

root="$(git rev-parse --show-toplevel)"
hooks_dir="$(git rev-parse --git-path hooks)"   # honours core.hooksPath + worktrees
src="${root}/paybench/methodology/ceremony-hooks/pre-push"
dest="${hooks_dir}/pre-push"

mkdir -p "$hooks_dir"
if [ -e "$dest" ] && ! grep -q "PAYBENCH_FREEZE_OVERRIDE" "$dest" 2>/dev/null; then
  echo "A pre-push hook already exists and is not ours:"
  echo "  $dest"
  echo "Back it up or chain it manually, then re-run. Aborting to avoid clobbering it." >&2
  exit 1
fi

cp "$src" "$dest"
chmod +x "$dest"
echo "Installed freeze-guard pre-push hook:"
echo "  $dest"
echo "It refuses to push paybench-*prereg* tags without committed freeze-evidence."
