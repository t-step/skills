#!/usr/bin/env bash
# Deterministic, idempotent fixture build. Usage: build.sh <dest>
# Produces <dest>: a git repo at upstream base commit 6fd65310fa3167b9626c38a5487e171ca407d988 (depth-1 history, no remote left),
# the WIP applied as an UNCOMMITTED working-tree change, and a project-local .venv (git-excluded).
set -euo pipefail
DEST="${1:?usage: build.sh <dest>}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_URL="https://github.com/sympy/sympy.git"; BASE="6fd65310fa3167b9626c38a5487e171ca407d988"; PYVER="3.9"
mkdir -p "$DEST"; DEST="$(cd "$DEST" && pwd)"
cd "$DEST"
[ -d .git ] || git init -q .
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"
git fetch -q --depth 1 origin "$BASE"
git checkout -q -f --detach "$BASE"
git reset -q --hard "$BASE"
git clean -qfd                      # drops untracked files, keeps git-ignored .venv
git remote remove origin            # fixture must not carry a remote
mkdir -p .git/info
grep -qx '.venv/' .git/info/exclude 2>/dev/null || echo '.venv/' >> .git/info/exclude
if [ ! -x .venv/bin/python ]; then uv venv -q --python "$PYVER" .venv; fi
uv pip install -q --python .venv/bin/python "mpmath==1.3.0"
git apply --whitespace=nowarn "$HERE/wip.patch"
# tree fingerprint: HEAD + tracked diff + untracked file names/contents (excluding ignored)
FP=$( { git rev-parse HEAD; git diff HEAD --binary; git ls-files -o --exclude-standard -z | xargs -0 -I{} sh -c 'echo {}; cat "{}"'; } | shasum -a 256 | cut -d' ' -f1)
echo "BUILD_OK dest=$DEST head=$(git rev-parse --short HEAD) fingerprint=$FP"
