#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# all six tasks ticked and committed; follow-up item deferred in the task file; clean
new_repo "$out"; through_t003 assumption; commit_t004 assumption
cat > cohort/report.py <<'PY'
"""Ranking report (T005)."""
from .ranking import rank


def render(learners):
    return "\n".join(f"{i}. {l['name']}" for i, l in enumerate(rank(learners), 1))
PY
cat > tests/test_report.py <<'PY'
import unittest

from cohort.report import render


class ReportTests(unittest.TestCase):
    def test_render_numbered(self):
        out = render([{"name": "amy", "readiness": 10}, {"name": "bo", "readiness": 90}])
        self.assertEqual(out, "1. bo\n2. amy")
PY
write_tasks assumption x x x x x .
commit_all "T005: ranking report output" "2026-09-16T18:00:00"
cat > cohort/cli.py <<'PY'
"""CLI entry point (T006)."""
import json
import sys

from .report import render


def main(argv):
    print(render(json.load(open(argv[1]))))
PY
write_tasks assumption x x x x x x
printf '\nT007 (CSV export) is deferred to a follow-up PR and is out of scope for this branch.\n' >> $SPEC/tasks.md
commit_all "T006: CLI entry point" "2026-09-17T10:00:00"
