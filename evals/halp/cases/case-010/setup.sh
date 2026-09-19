#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# T004 committed with a ranking implementation and its tests
new_repo "$out"; through_t003 assumption
write_ranking_no_tiebreak; write_ranking_tests_weak; write_tasks assumption x x x x . .
commit_all "T004: rank learners by readiness with tie-break tests (FR-2, FR-3)" "2026-09-16T16:20:00"
