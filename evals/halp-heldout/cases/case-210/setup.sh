#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# a test log NEWER than the last code change; tree clean apart from the untracked log
new_repo "$out"
put csvmerge/merge.py <<'J'
def merge(a, b, key):
    seen = {}
    for row in a + b:
        seen[row[key]] = row
    return list(seen.values())
J
put tests/test_merge.py <<'J'
from csvmerge.merge import merge


def test_dedupe_keys():
    assert len(merge([{"id": 1}], [{"id": 1}], "id")) == 1
J
put pyproject.toml <<'J'
[tool.pytest.ini_options]
testpaths = ["tests"]
J
commit_all "csvmerge: merge by key" "2026-09-10T09:00:00"
put csvmerge/merge.py <<'J'
def merge(a, b, key):
    out = {}
    for row in a + b:
        out.setdefault(row[key], []).append(row)
    return [r for rows in out.values() for r in rows]
J
commit_all "csvmerge: keep all rows per key" "2026-09-15T16:00:00"
sync_mtimes
mkdir -p logs
put logs/pytest.log <<'J'
============================= test session starts ==============================
collected 11 items

tests/test_merge.py F.                                                   [ 18%]
tests/test_io.py .........                                               [100%]

=================================== FAILURES ===================================
__________________________ test_dedupe_keys ___________________________________
>       assert len(merge([{"id": 1}], [{"id": 1}], "id")) == 1
E       assert 2 == 1
=========================== short test summary info ============================
FAILED tests/test_merge.py::test_dedupe_keys - assert 2 == 1
========================= 1 failed, 10 passed in 0.41s =========================
J
stamp 202609161820 logs/pytest.log
