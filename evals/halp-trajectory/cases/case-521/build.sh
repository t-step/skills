#!/bin/bash
# Deterministic, idempotent fixture builder.  usage: build.sh <dest>
# Result: <dest> = git repo at upstream base commit (branch main, no remote, shallow) + the WIP applied as an
# UNCOMMITTED working-tree change (wip.patch = tracked edits, untracked/ = scratch files the agent had created) + .venv (git-excluded).
# Needs: git, uv, network (GitHub + PyPI). Python 3.10 is fetched by uv if absent.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
URL=https://github.com/django/django.git
SHA=6efc35b4fe3009666e56a60af0675d7d532bf4ff
[ $# -eq 1 ] || { echo "usage: $0 <dest>" >&2; exit 2; }
dest=$1
if [ -e "$dest" ]; then
  [ -f "$dest/.git/halp-fixture" ] || { echo "refusing to overwrite $dest (not a fixture built by this script)" >&2; exit 2; }
  rm -rf "$dest"
fi
mkdir -p "$dest"; dest=$(cd "$dest" && pwd); cd "$dest"
git init -q .
git remote add origin "$URL"
git fetch -q --depth 1 origin "$SHA"
git checkout -q -b main FETCH_HEAD
git remote remove origin
: > .git/halp-fixture
printf '.venv/\n' >> .git/info/exclude
uv venv -q --python 3.10 .venv
uv pip install -q --python .venv/bin/python -e . asgiref==3.7.2 pytz==2023.3 sqlparse==0.4.4
git apply --whitespace=nowarn "$here/wip.patch"
[ -d "$here/untracked" ] && cp -R "$here/untracked/." "$dest/"
echo "built $dest @ $(git rev-parse --short HEAD)"
git status --short
