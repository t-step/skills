#!/usr/bin/env bash
# usage: build.sh <dest> [k13|base]   (default k13).  Deterministic + idempotent: rebuilds <dest> from scratch each run.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; DEST="${1:?dest}"; VAR="${2:-k13}"
URL=https://github.com/axios/axios.git; SHA=c6cce43cd94489f655f4488c5a50ecaf781c94f2
rm -rf "$DEST"; mkdir -p "$DEST"; DEST="$(cd "$DEST" && pwd)"; cd "$DEST"
git init -q -b base . && git fetch -q --depth 1 "$URL" "$SHA" && git checkout -q FETCH_HEAD   # shallow, no remote configured
printf 'node_modules\n' >> .git/info/exclude
npm ci --ignore-scripts --no-audit --no-fund >/dev/null 2>&1
[ "$VAR" = base ] || git apply "$HERE/wip-$VAR.patch"   # base = pristine upstream commit, no WIP
echo "built $DEST variant=$VAR head=$(git rev-parse --short HEAD) treehash=$(git diff HEAD | shasum | cut -c1-12)"
