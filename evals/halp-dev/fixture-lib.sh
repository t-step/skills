#!/usr/bin/env bash
# Shared deterministic builders for the halp development/property suite.
# All cases derive from ONE small project (ledgerkit) via ledger_base, so a
# paired case differs from its twin by exactly one fact, applied by its own
# setup.sh after the shared base. Fixed dates and content; mtimes are stamped
# explicitly so chronology is part of the fixture, not an accident of "now".
set -euo pipefail

put() { mkdir -p "$(dirname "$1")"; cat > "$1"; }
new_repo() { rm -rf "$1"; mkdir -p "$1"; cd "$1"; git init -q -b main
  git config commit.gpgsign false; git config user.name "Fixture Author"; git config user.email "fixture@example.invalid"; }
commit_all() { git add -A; GIT_AUTHOR_DATE="$2" GIT_COMMITTER_DATE="$2" git commit -q -m "$1"; }
stamp() { local t="$1"; shift; touch -t "$t" "$@"; }
sync_mtimes() { local f t; git ls-files | while read -r f; do
  t=$(git log -1 --format=%cd --date=format:%Y%m%d%H%M -- "$f"); touch -t "$t" "$f"; done; }
make_origin() { local url="$1"; shift; local bare; bare="$(pwd).origin"; rm -rf "$bare"; git init -q --bare "$bare"
  git remote add origin "$bare"; for b in "$@"; do git push -q origin "$b"; done; git remote set-url origin "$url"; }
gh_open() { mkdir -p "$(dirname "$1")/bin"; printf '#!/bin/sh\necho "#12 OPEN review=none https://github.com/acme/ledgerkit/pull/12"\n' > "$(dirname "$1")/bin/gh"
  chmod +x "$(dirname "$1")/bin/gh"; }

# ledger_base <abs-dir>
# State left behind (the shared "obvious mid-task" situation):
#   branch feat/monthly-rollup, no remote. tasks.md: T001, T002 ticked; T003 (monthly rollup) NOT ticked; T004 open.
#   Committed: T001, T002, and the FIRST half of T003 (grouping by month, string keys "YYYY-MM", one test).
#   Uncommitted (1 tracked file modified): report.py gains empty-input handling (no test covers it yet).
#   .gitignore covers logs/ and __pycache__/. The dirty file is stamped 2026-09-17 15:00.
# Env knobs, each used by one case (committed with the scaffold): LEDGER_TASK3_NOTE (extra text after the T003 line),
# LEDGER_ADRS (accepted ADR-0002 in the scaffold; a later accepted ADR-0005 that supersedes it, committed after the plan text).
ledger_base() {
  new_repo "$1"
  put .gitignore <<'J'
logs/
__pycache__/
J
  put README.md <<'J'
# ledgerkit
Small helpers for summarising ledger CSV lines.
J
  put ledgerkit/__init__.py </dev/null
  put tests/__init__.py </dev/null
  put tasks.md <<J
# Tasks
- [ ] T001 parse ledger lines (ledgerkit/parse.py)
- [ ] T002 compute totals (ledgerkit/totals.py)
- [ ] T003 monthly rollup (ledgerkit/report.py): group entries by month, handle empty input${LEDGER_TASK3_NOTE:-}
- [ ] T004 CSV export of the rollup
J
  if [ -n "${LEDGER_ADRS:-}" ]; then
    put docs/adr/0002-month-keys.md <<'J'
# ADR-0002: Month keys
Status: accepted (2026-05-10)

Rollups are keyed by ISO month strings, e.g. "2026-09".
J
  fi
  commit_all "scaffold" "2026-09-14T09:00:00"
  git checkout -q -b feat/monthly-rollup
  put ledgerkit/parse.py <<'J'
from datetime import date


def parse_line(line):
    """'2026-09-03,-12.50' -> (date(2026, 9, 3), -12.5)"""
    d, amt = line.strip().split(",")
    y, m, day = map(int, d.split("-"))
    return date(y, m, day), float(amt)
J
  put tests/test_parse.py <<'J'
import unittest
from datetime import date
from ledgerkit.parse import parse_line


class ParseTest(unittest.TestCase):
    def test_parses_a_line(self):
        self.assertEqual(parse_line("2026-09-03,-12.50"), (date(2026, 9, 3), -12.5))
J
  sed -i.bak 's/^- \[ \] T001/- [x] T001/' tasks.md && rm tasks.md.bak
  commit_all "T001: parse ledger lines" "2026-09-15T10:00:00"
  put ledgerkit/totals.py <<'J'
def total(entries):
    return round(sum(a for _, a in entries), 2)
J
  put tests/test_totals.py <<'J'
import unittest
from datetime import date
from ledgerkit.totals import total


class TotalsTest(unittest.TestCase):
    def test_sums_amounts(self):
        self.assertEqual(total([(date(2026, 9, 1), 1.5), (date(2026, 9, 2), 2.25)]), 3.75)
J
  sed -i.bak 's/^- \[ \] T002/- [x] T002/' tasks.md && rm tasks.md.bak
  commit_all "T002: compute totals" "2026-09-16T10:00:00"
  if [ -n "${LEDGER_ADRS:-}" ]; then   # the superseding ADR lands AFTER the plan text was last written
    put docs/adr/0005-month-keys-as-tuples.md <<'J'
# ADR-0005: Month keys as tuples
Status: accepted (2026-09-17)
Supersedes: ADR-0002

Rollups are keyed by (year, month) tuples so callers can sort and compare them without parsing strings.
J
    commit_all "docs: ADR-0005 month keys as tuples (supersedes ADR-0002)" "2026-09-17T08:00:00"
  fi
  put ledgerkit/report.py <<'J'
def rollup_by_month(entries):
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
J
  commit_all "T003 (part 1): group entries by month" "2026-09-17T09:30:00"
  sync_mtimes
  # ---- uncommitted work: the second half of T003 ----
  put ledgerkit/report.py <<'J'
def rollup_by_month(entries):
    """Sum amounts per month. Empty input returns an empty rollup."""
    if not entries:
        return {}
    out = {}
    for d, amt in entries:
        key = d.strftime("%Y-%m")
        out[key] = round(out.get(key, 0) + amt, 2)
    return out
J
  stamp 202609171500 ledgerkit/report.py
}
