#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# ranking work in progress (untracked); latest commit touches only README.md
new_repo "$out"; through_t003 oq
write_ranking_wip; write_ranking_tests
write_readme fixed
commit_paths "docs: fix typo in README" "2026-09-17T09:00:00" README.md
