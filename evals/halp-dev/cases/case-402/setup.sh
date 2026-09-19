#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
ledger_base "$out"
mkdir -p logs
put logs/pytest.log <<'J'
============================= test session starts ==============================
collected 3 items

tests/test_parse.py .                                                    [ 33%]
tests/test_totals.py .                                                   [ 66%]
tests/test_report.py .                                                   [100%]

============================== 3 passed in 0.08s ===============================
J
stamp 202609171700 logs/pytest.log
