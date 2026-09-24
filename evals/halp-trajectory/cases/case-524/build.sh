#!/usr/bin/env bash
# Usage: build.sh <dest>   -- deterministic, idempotent (rebuilds <dest> from scratch). Needs: git, uv, network.
# Result: <dest> is a git repo, HEAD (detached) = upstream base commit, no remote, WIP applied as uncommitted change,
#         deps in <dest>/.venv (Python 3.11, pinned by requirements.lock), .venv/caches excluded via .git/info/exclude.
set -euo pipefail
DEST="${1:?usage: build.sh <dest>}"; HERE="$(cd "$(dirname "$0")" && pwd)"
URL=https://github.com/pylint-dev/pylint.git; BASE=1f8c4d9eb185c16a2c1d881c054f015e1c2eb334; PYV=3.11
rm -rf "$DEST"; mkdir -p "$DEST"; DEST="$(cd "$DEST" && pwd)"; cd "$DEST"
git init -q; git fetch -q --depth 1 "$URL" "$BASE"; git checkout -q --detach FETCH_HEAD
printf '%s\n' '.venv/' '.pytest_cache/' '__pycache__/' '*.egg-info/' '*.pyc' >> .git/info/exclude
uv venv -q --python "$PYV" .venv
uv pip install -q --python .venv/bin/python -r "$HERE/requirements.lock"
uv pip install -q --python .venv/bin/python --no-deps -e .
git apply "$HERE/wip.patch"
git status --short
