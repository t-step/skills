#!/usr/bin/env bash
# usage: build.sh <dest> [k13|k37]   (default k37).  Deterministic + idempotent: rebuilds <dest> from scratch each run.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; DEST="${1:?dest}"; VAR="${2:-k37}"
URL=https://github.com/immutable-js/immutable-js.git; SHA=77434b3cbbc8ee21206f4cc6965e1c9b09cc92b6
rm -rf "$DEST"; mkdir -p "$DEST"; DEST="$(cd "$DEST" && pwd)"; cd "$DEST"
git init -q -b base . && git fetch -q --depth 1 "$URL" "$SHA" && git checkout -q FETCH_HEAD   # shallow, no remote configured
git -c user.name=fixture -c user.email=fixture@example.invalid commit -q --allow-empty -m "noop" >/dev/null 2>&1 && git reset -q --hard "$SHA"
printf 'node_modules\ndist\n' >> .git/info/exclude
npm ci --ignore-scripts --no-audit --no-fund >/dev/null 2>&1
[ "$VAR" = base ] || git apply "$HERE/wip-$VAR.patch"   # base = pristine upstream commit, no WIP
echo "built $DEST variant=$VAR head=$(git rev-parse --short HEAD) treehash=$(git diff HEAD | shasum | cut -c1-12)"
