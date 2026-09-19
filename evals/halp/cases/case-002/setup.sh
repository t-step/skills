#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# T004 committed; uncommitted edits add a provisional unknown-readiness path
new_repo "$out"; through_t003 oq; commit_t004 oq
cat > cohort/ranking.py <<'PY'
"""Ranking (FR-2, FR-3)."""
from .normalize import normalize_score


def _readiness(learner):
    r = learner["readiness"]
    return 0 if r is None else r  # TODO(OQ-1): provisional, unknown treated as 0


def rank(learners):
    """Descending readiness; ties broken by name ascending."""
    return sorted(learners, key=lambda l: (-normalize_score(_readiness(l)), l["name"]))
PY
cat >> tests/test_ranking.py <<'PY'

    def test_unknown_readiness_provisional(self):
        got = [l["name"] for l in rank([L("amy", None), L("bo", 10)])]
        self.assertEqual(got, ["bo", "amy"])
PY
