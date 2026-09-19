#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
export LEDGER_TASK3_NOTE=$'\n  - OQ-1 (open): month key format. Option A: "YYYY-MM" strings (what the code does now). Option B: (year, month) tuples. Not decided.'
ledger_base "$out"
