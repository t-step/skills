#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
export LEDGER_ADRS=1 LEDGER_TASK3_NOTE=$'; keys are ISO month strings such as "2026-09" (see ADR-0002)'
ledger_base "$out"
