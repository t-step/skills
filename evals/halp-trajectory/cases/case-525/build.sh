#!/usr/bin/env bash
# Usage: build.sh <dest>   -- deterministic, idempotent (rebuilds <dest> from scratch). Needs: git, uv, network.
# Result: <dest> is a git repo, HEAD (detached) = upstream base commit, no remote, WIP applied as uncommitted change,
#         deps in <dest>/.venv (Python 3.9, pinned by requirements.lock), .venv/caches excluded via .git/info/exclude.
set -euo pipefail
DEST="${1:?usage: build.sh <dest>}"; HERE="$(cd "$(dirname "$0")" && pwd)"
URL=https://github.com/mwaskom/seaborn.git; BASE=22cdfb0c93f8ec78492d87edb810f10cb7f57a31; PYV=3.9
rm -rf "$DEST"; mkdir -p "$DEST"; DEST="$(cd "$DEST" && pwd)"; cd "$DEST"
git init -q; git fetch -q --depth 1 "$URL" "$BASE"; git checkout -q --detach FETCH_HEAD
printf '%s\n' '.venv/' '.pytest_cache/' '__pycache__/' '*.egg-info/' '*.pyc' >> .git/info/exclude
uv venv -q --python "$PYV" .venv
uv pip install -q --python .venv/bin/python -r "$HERE/requirements.lock"
uv pip install -q --python .venv/bin/python --no-deps -e .
git apply "$HERE/wip.patch"
git status --short
