#!/usr/bin/env bash
# Usage: build.sh <dest>   -- deterministic, idempotent (rebuilds <dest> from scratch). Needs: git, uv, network.
# Result: <dest> is a git repo, HEAD (detached) = upstream base commit, no remote, WIP applied as uncommitted change,
#         deps in <dest>/.venv (Python 3.8, pinned by requirements.lock), .venv/caches excluded via .git/info/exclude.
set -euo pipefail
DEST="${1:?usage: build.sh <dest>}"; HERE="$(cd "$(dirname "$0")" && pwd)"
URL=https://github.com/pytest-dev/pytest.git; BASE=e856638ba086fcf5bebf1bebea32d5cf78de87b4; PYV=3.8
rm -rf "$DEST"; mkdir -p "$DEST"; DEST="$(cd "$DEST" && pwd)"; cd "$DEST"
git init -q; git fetch -q --depth 300 "$URL" "$BASE"; git checkout -q --detach FETCH_HEAD
printf '%s\n' '.venv/' '.pytest_cache/' '__pycache__/' '*.egg-info/' '*.pyc' >> .git/info/exclude
uv venv -q --python "$PYV" .venv
uv pip install -q --python .venv/bin/python -r "$HERE/requirements.lock"
# no tags in the fetched history: pin the version setuptools_scm would have produced (tox.ini requires minversion 2.0)
SETUPTOOLS_SCM_PRETEND_VERSION=5.2.4.dev6+ge856638ba uv pip install -q --python .venv/bin/python --no-deps -e .
git apply "$HERE/wip.patch"
git status --short
