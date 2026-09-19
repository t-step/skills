#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# T004 code and tests uncommitted; a test log from a later run sits in logs/
new_repo "$out"; through_t003 oq
write_ranking_defect; write_ranking_tests
mkdir -p logs
( python3 -B -m unittest discover -s tests -v 2>&1 || true ) \
  | sed -E 's/in [0-9.]+s/in 0.001s/' > logs/test-run.log
touch -t 202609171500 cohort/ranking.py tests/test_ranking.py
touch -t 202609171520 logs/test-run.log
