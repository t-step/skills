#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
ledger_base "$out"
make_origin "git@github.com:acme/ledgerkit.git" main feat/monthly-rollup
git branch -q -u origin/feat/monthly-rollup
gh_open "$out"
