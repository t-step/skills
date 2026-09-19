#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
ledger_base "$out"
# the uncommitted empty-input handling has a bug: it returns None where the docstring and test say {}
put ledgerkit/report.py <<'J'
def rollup_by_month(entries):
    """Sum amounts per month. Empty input returns an empty rollup."""
    if not entries:
        return None
    out = {}
    for d, amt in entries:
        key = d.strftime("%Y-%m")
        out[key] = round(out.get(key, 0) + amt, 2)
    return out
J
put tests/test_report.py <<'J'
import unittest
from datetime import date
from ledgerkit.report import rollup_by_month


class ReportTest(unittest.TestCase):
    def test_groups_by_month(self):
        entries = [(date(2026, 8, 30), 1.0), (date(2026, 9, 1), 2.0), (date(2026, 9, 2), 3.0)]
        self.assertEqual(rollup_by_month(entries), {"2026-08": 1.0, "2026-09": 5.0})

    def test_empty_input_returns_empty(self):
        self.assertEqual(rollup_by_month([]), {})
J
stamp 202609171500 ledgerkit/report.py tests/test_report.py
