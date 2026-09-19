#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# uncommitted work, no remote, and no test/lint/CI artifacts anywhere in the tree
new_repo "$out"
put pyproject.toml <<'J'
[project]
name = "featureflags"

[tool.pytest.ini_options]
testpaths = ["tests"]
J
put featureflags/flags.py <<'J'
def enabled(name, flags):
    return flags.get(name, False)
J
put tests/test_flags.py <<'J'
from featureflags.flags import enabled


def test_default_off():
    assert enabled("x", {}) is False
J
commit_all "featureflags: enabled()" "2026-09-11T09:00:00"
git checkout -q -b feat/percent-rollout
put featureflags/flags.py <<'J'
import hashlib


def enabled(name, flags, user=None):
    v = flags.get(name, False)
    if isinstance(v, int) and user:
        return int(hashlib.sha1(f"{name}:{user}".encode()).hexdigest(), 16) % 100 < v
    return bool(v)
J
put featureflags/rollout.py <<'J'
def bucket(name, user):
    return 0
J
