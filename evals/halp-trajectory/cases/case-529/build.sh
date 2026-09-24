#!/usr/bin/env bash
# build.sh <dest>  -- preact ref-cleanup fixture. Deterministic; re-running wipes and rebuilds <dest>.
# Needs: git, node>=20, npm, network (github + npm registry). Tests additionally need Chrome (see test.sh).
set -euo pipefail
DEST="${1:?usage: build.sh <dest>}"; HERE="$(cd "$(dirname "$0")" && pwd)"
BASE=db0f4f2e7a2338ea40050f623f05505a798fc1a4
rm -rf "$DEST"; mkdir -p "$DEST"; DEST="$(cd "$DEST" && pwd)"; cd "$DEST"
git init -q . && git remote add origin https://github.com/preactjs/preact.git
git fetch -q --depth 1 origin "$BASE" && git -c advice.detachedHead=false checkout -q FETCH_HEAD
git remote remove origin
git config user.name fixture; git config user.email fixture@example.invalid
printf 'node_modules/\n' >> .git/info/exclude
npm ci --ignore-scripts --no-audit --no-fund >/dev/null 2>&1
npm i --no-save --no-package-lock --ignore-scripts --no-audit --no-fund jsdom@24.1.3 >/dev/null 2>&1
git apply "$HERE/wip.patch"                    # WIP = uncommitted working-tree change
echo "HEAD=$(git rev-parse HEAD)"
echo "TREE_HASH=$( (git diff --binary; git ls-files -o --exclude-standard) | shasum -a 256 | cut -c1-16)"
git status --short
