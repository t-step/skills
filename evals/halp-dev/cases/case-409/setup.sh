#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
ledger_base "$out"
# irrelevant state: README edit, an old branch, a stale unrelated log, an untracked scratch file
printf '\nSee docs/ for more.\n' >> README.md; stamp 202609171400 README.md
tree=$(git rev-parse 'main^{tree}')
c=$(GIT_AUTHOR_DATE="2026-06-02T09:00:00" GIT_COMMITTER_DATE="2026-06-02T09:00:00" git commit-tree "$tree" -p main -m "spike: csv export experiment")
git branch spike/old-csv "$c"
mkdir -p logs; put logs/deploy-2026-06.log <<'J'
2026-06-10 09:00 deploy ok
J
stamp 202606100900 logs/deploy-2026-06.log
put scratch/notes.txt <<'J'
try numpy for rollups?
J
