#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# feature branch mid-merge of main, one conflicted file
new_repo "$out"; through_t003 oq; commit_t004 oq
git checkout -q main
mkdir -p cohort
cat > cohort/ranking.py <<'PY'
"""Shared ranking helper."""


def rank(items, key):
    return sorted(items, key=key)
PY
commit_all "Add shared ranking helper" "2026-09-16T09:00:00"
git checkout -q feat/cohort-ranking
GIT_AUTHOR_DATE="2026-09-17T09:00:00" GIT_COMMITTER_DATE="2026-09-17T09:00:00" \
  git merge main --no-edit >/dev/null 2>&1 || true
