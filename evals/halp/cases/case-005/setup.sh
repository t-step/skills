#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# T004 implemented in the working tree, task ticked, nothing committed
new_repo "$out"; through_t003 oq
write_ranking_final; write_ranking_tests; write_tasks oq x x x x . .
