#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# mixed staged / unstaged / untracked state
new_repo "$out"; through_t003 oq
write_ranking_wip; write_ranking_tests
mkdir -p scratch; echo 'print("debug")' > scratch/debug_ranking.py
git add tests/test_ranking.py
echo "" >> $SPEC/plan.md; echo "Note: tie-break is by name, per FR-3." >> $SPEC/plan.md
