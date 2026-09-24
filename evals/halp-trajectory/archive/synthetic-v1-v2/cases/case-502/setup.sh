#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh <absolute-output-dir> [variant]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:?output dir}"
ledger_t4_vendor "$out"
