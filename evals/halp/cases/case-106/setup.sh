#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# single-commit branch that only touches README.md; clean
new_repo "$out"; scaffold_main assumption
git checkout -q -b docs/readme-typo
write_readme fixed
commit_all "Fix typo in README" "2026-09-17T09:00:00"
