#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# T004 code and tests in the working tree, plus a test over the upstream sample export
new_repo "$out"; WITH_SAMPLE_DATA=1 through_t003 assumption
write_ranking_final; write_ranking_tests; write_sample_data_test
