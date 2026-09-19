#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# feat branch, T001-T003 committed; ranking module and its tests are new and uncommitted
new_repo "$out"; through_t003 oq
write_ranking_wip; write_ranking_tests
