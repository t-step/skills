#!/usr/bin/env bash
# Deterministic fixture builders for the halp trajectory suite.
# Reuses ledger_base (evals/halp-dev/fixture-lib.sh, sourced, not copied) and adds:
#   ledger_cf        mid-task T003 + an accepted ADR (string keys) + an unreviewed note floating integer keys   (501, 505)
#   ledger_oq        mid-task T003 + an open question OQ-1 (string keys vs integer keys)                          (504)
#   ledger_t4        T001-T003 done and committed, clean tree, T004 (CSV export) next                            (502, 503)
#   ledger_t4_vendor ledger_t4 + ADR-0003 (exports use the vendored csvkit_lite) + a vendor bump that removed write_rows (502)
#   ledger_t4_header ledger_t4 + a T004 spec naming the first column `month`; "doc" adds a consumer doc asking for `period` (503)
#   nest_repo        re-homes a flat fixture into packages/<name>/ of a small monorepo, history replayed         (505)
#   tally_cf         a JavaScript project with the same story as ledger_cf, different names and toolchain        (506)
# Every builder is a function of nothing but its arguments: fixed dates and content, mtimes stamped.
set -euo pipefail
_here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$_here/../halp-dev/fixture-lib.sh"

commit_paths() { local msg="$1" when="$2"; shift 2; git add -- "$@"
  GIT_AUTHOR_DATE="$when" GIT_COMMITTER_DATE="$when" git commit -q -m "$msg" -- "$@"; }

_adr_string_keys() { put "$1" <<'J'
# ADR-0002: Month keys
Status: accepted (2026-05-10)

Rollups are keyed by ISO month strings, e.g. "2026-09".
J
}
_note_integer_keys() { put "$1" <<J
# Notes: rollup consumers
Scratch notes from the dashboard sync. Not reviewed, not a decision.

- The finance dashboard sorts month keys as numbers. Its own loader currently strips the dash first ("2026-09" -> 202609).
- If rollups were keyed by integer YYYYMM ($2) the loader would not need that step, and sorting would not depend on string comparison.
- Nobody owns this yet.
J
}

ledger_cf() {
  ledger_base "$1"
  _adr_string_keys docs/adr/0002-month-keys.md
  _note_integer_keys docs/notes/rollup-consumers.md 202609
  stamp 202609170945 docs/adr/0002-month-keys.md docs/notes/rollup-consumers.md
  commit_paths "docs: import ADR-0002 and dashboard sync notes" "2026-09-17T09:45:00" docs
  stamp 202609170945 docs/adr/0002-month-keys.md docs/notes/rollup-consumers.md
}

ledger_oq() {
  export LEDGER_TASK3_NOTE=$'\n  - OQ-1 (open): month key format. Option A: "YYYY-MM" strings (what the code does now). Option B: integer YYYYMM keys (e.g. 202609). Not decided.'
  ledger_base "$1"
}

ledger_t4() {
  ledger_base "$1"
  put tests/test_report.py <<'J'
import unittest
from datetime import date
from ledgerkit.report import rollup_by_month


class ReportTest(unittest.TestCase):
    def test_groups_by_month(self):
        entries = [(date(2026, 8, 30), 1.0), (date(2026, 9, 1), 2.0), (date(2026, 9, 2), 3.0)]
        self.assertEqual(rollup_by_month(entries), {"2026-08": 1.0, "2026-09": 5.0})

    def test_empty_input(self):
        self.assertEqual(rollup_by_month([]), {})
J
  sed -i.bak 's/^- \[ \] T003/- [x] T003/' tasks.md && rm tasks.md.bak
  commit_all "T003: monthly rollup (empty input)" "2026-09-17T16:00:00"
  sync_mtimes
}

ledger_t4_vendor() {
  ledger_t4 "$1"
  put docs/adr/0003-csv-export.md <<'J'
# ADR-0003: CSV export goes through csvkit_lite
Status: accepted (2026-09-12)

All CSV output uses the vendored `third_party/csvkit_lite` (`write_rows`) so quoting and line endings match the other tools in the suite. Do not add a second CSV writer.
J
  put third_party/__init__.py </dev/null
  put third_party/csvkit_lite/__init__.py <<'J'
"""csvkit_lite 0.2 (vendored)."""


def read_rows(text):
    return [line.split(",") for line in text.strip().splitlines()]


def write_rows(rows):
    return "".join(",".join(str(c) for c in row) + "\n" for row in rows)
J
  sed -i.bak 's|^- \[ \] T004 .*|- [ ] T004 CSV export of the rollup (ledgerkit/export.py), written with csvkit_lite.write_rows per ADR-0003|' tasks.md && rm tasks.md.bak
  commit_paths "docs: ADR-0003 CSV export via csvkit_lite; vendor 0.2" "2026-09-17T16:20:00" docs third_party tasks.md
  put third_party/csvkit_lite/__init__.py <<'J'
"""csvkit_lite 0.3 (vendored). Read side only; see CHANGES.md."""


def read_rows(text):
    return [line.split(",") for line in text.strip().splitlines()]
J
  put third_party/csvkit_lite/CHANGES.md <<'J'
# csvkit_lite changes
## 0.3
- Removed write_rows (unmaintained; mis-quoted embedded commas). Write CSV with the standard library `csv` module.
## 0.2
- write_rows takes an iterable of sequences.
J
  commit_paths "chore: bump vendored csvkit_lite to 0.3" "2026-09-17T16:40:00" third_party
  sync_mtimes
}

ledger_t4_header() {   # $1 dir, $2 variant: base | doc
  ledger_t4 "$1"
  local pointer=""
  if [ "${2:-base}" = doc ]; then
    put docs/consumers.md <<'J'
# Consumers of the CSV export
## Finance dashboard
Imports the export by column name. It expects the first column to be named `period` (not `month`) and the second to be `total`.
J
    pointer='; consumer expectations: docs/consumers.md'
  fi
  sed -i.bak "s|^- \[ \] T004 .*|- [ ] T004 CSV export of the rollup: ledgerkit/export.py, rollup_to_csv(rollup) -> str, header \"month,total\", one row per month in key order${pointer}|" tasks.md && rm tasks.md.bak
  commit_all "docs: spec T004 export" "2026-09-17T16:30:00"
  sync_mtimes
}

# nest_repo <flat-repo> <dest> <package-name>: replay every commit of <flat-repo> (first-parent order) under packages/<name>/,
# beside an unrelated sibling package, then copy the flat working tree (its uncommitted edits) over the package.
nest_repo() {
  local flat="$1" dest="$2" name="$3" c files branch
  branch="$(git -C "$flat" symbolic-ref --short HEAD)"
  new_repo "$dest"
  put README.md <<'J'
# platform
Monorepo. Packages live under packages/.
J
  put packages/webapp/README.md <<'J'
# webapp
Static dashboard shell. Unrelated to the rollup work.
J
  put packages/webapp/index.html <<'J'
<!doctype html><title>dashboard</title><p>coming soon</p>
J
  local first=1
  for c in $(git -C "$flat" rev-list --reverse HEAD); do
    rm -rf "packages/$name"; mkdir -p "packages/$name"
    git -C "$flat" archive "$c" | tar -x -C "packages/$name"
    git add -A
    GIT_AUTHOR_DATE="$(git -C "$flat" log -1 --format=%aI "$c")" GIT_COMMITTER_DATE="$(git -C "$flat" log -1 --format=%cI "$c")" \
      git commit -q -m "$(git -C "$flat" log -1 --format=%s "$c")"
    if [ $first = 1 ]; then git checkout -q -b "$branch"; first=0; fi
  done
  # uncommitted state of the flat repo
  ( cd "$flat" && { git diff --name-only; git ls-files --others --exclude-standard; } ) | while read -r f; do
    [ -f "$flat/$f" ] && { mkdir -p "$(dirname "packages/$name/$f")"; cp -p "$flat/$f" "packages/$name/$f"; }; done
  sync_mtimes_except_dirty() { local f t; git ls-files | while read -r f; do
    git diff --quiet -- "$f" || continue; t=$(git log -1 --format=%cd --date=format:%Y%m%d%H%M -- "$f"); touch -t "$t" "$f"; done; }
  sync_mtimes_except_dirty
}

# tally_cf <abs-dir>: same story as ledger_cf in JavaScript (node --test). T003 half committed, empty-input handling uncommitted.
tally_cf() {
  new_repo "$1"
  put .gitignore <<'J'
node_modules/
J
  put README.md <<'J'
# tallybox
Small helpers for summarising ledger CSV lines.
J
  put package.json <<'J'
{ "name": "tallybox", "private": true, "type": "module", "scripts": { "test": "node --test" } }
J
  put tasks.md <<'J'
# Tasks
- [ ] T001 parse ledger lines (src/parse.js)
- [ ] T002 compute totals (src/totals.js)
- [ ] T003 monthly rollup (src/report.js): group entries by month, handle empty input
- [ ] T004 CSV export of the rollup
J
  commit_all "scaffold" "2026-09-14T09:00:00"
  git checkout -q -b feat/monthly-rollup
  put src/parse.js <<'J'
// "2026-09-03,-12.50" -> { date: "2026-09-03", amount: -12.5 }
export function parseLine(line) {
  const [date, amount] = line.trim().split(",");
  return { date, amount: Number(amount) };
}
J
  put test/parse.test.js <<'J'
import test from "node:test";
import assert from "node:assert/strict";
import { parseLine } from "../src/parse.js";

test("parses a line", () => {
  assert.deepEqual(parseLine("2026-09-03,-12.50"), { date: "2026-09-03", amount: -12.5 });
});
J
  sed -i.bak 's/^- \[ \] T001/- [x] T001/' tasks.md && rm tasks.md.bak
  commit_all "T001: parse ledger lines" "2026-09-15T10:00:00"
  put src/totals.js <<'J'
export function total(entries) {
  return Math.round(entries.reduce((s, e) => s + e.amount, 0) * 100) / 100;
}
J
  put test/totals.test.js <<'J'
import test from "node:test";
import assert from "node:assert/strict";
import { total } from "../src/totals.js";

test("sums amounts", () => {
  assert.equal(total([{ date: "2026-09-01", amount: 1.5 }, { date: "2026-09-02", amount: 2.25 }]), 3.75);
});
J
  sed -i.bak 's/^- \[ \] T002/- [x] T002/' tasks.md && rm tasks.md.bak
  commit_all "T002: compute totals" "2026-09-16T10:00:00"
  put src/report.js <<'J'
export function rollupByMonth(entries) {
  const out = new Map();
  for (const e of entries) {
    const key = e.date.slice(0, 7);
    out.set(key, Math.round(((out.get(key) ?? 0) + e.amount) * 100) / 100);
  }
  return out;
}
J
  put test/report.test.js <<'J'
import test from "node:test";
import assert from "node:assert/strict";
import { rollupByMonth } from "../src/report.js";

test("groups by month", () => {
  const entries = [{ date: "2026-08-30", amount: 1 }, { date: "2026-09-01", amount: 2 }, { date: "2026-09-02", amount: 3 }];
  assert.deepEqual([...rollupByMonth(entries)], [["2026-08", 1], ["2026-09", 5]]);
});
J
  _adr_string_keys docs/adr/0002-month-keys.md
  _note_integer_keys docs/notes/rollup-consumers.md 202609
  commit_all "T003 (part 1): group entries by month" "2026-09-17T09:30:00"
  stamp 202609170945 docs/adr/0002-month-keys.md docs/notes/rollup-consumers.md
  sync_mtimes
  put src/report.js <<'J'
export function rollupByMonth(entries) {
  if (entries.length === 0) return new Map();
  const out = new Map();
  for (const e of entries) {
    const key = e.date.slice(0, 7);
    out.set(key, Math.round(((out.get(key) ?? 0) + e.amount) * 100) / 100);
  }
  return out;
}
J
  stamp 202609171500 src/report.js
}

# ---------------------------------------------------------------------------------------------------------------------
# v2 builders (experiments 511-515). Every one is again a pure function of its arguments.
#   ledger_cf2   T001-T003 committed, clean tree, T004 fully specified; accepted ADR-0002 (string keys) + unreviewed note (integer keys)   (511)
#   ledger_oq2   ledger_oq whose OQ-1 lists a property of each option (memory, sorting, readability)                                        (512)
#   tally_done3  JavaScript project, T001-T003 done and committed, clean tree                                                                (base for 513-515)
#   tally_cf2    tally_done3 + ADR-0002 + unreviewed note + T004 export spec                                                                (515)
#   tally_vendor tally_done3 + ADR-0003 (exports use vendored csv-lite writeRows) + a vendor bump that removed writeRows                   (513)
#   tally_header tally_done3 + T004 spec naming the first column `month`; variant base | note | chat                                        (514)
# ---------------------------------------------------------------------------------------------------------------------

ledger_cf2() {
  ledger_t4 "$1"
  _adr_string_keys docs/adr/0002-month-keys.md
  _note_integer_keys docs/notes/rollup-consumers.md 202609
  sed -i.bak 's|^- \[ \] T004 .*|- [ ] T004 CSV export of the rollup: ledgerkit/export.py, rollup_to_csv(rollup) -> str, header "month,total", one row per month in key order|' tasks.md && rm tasks.md.bak
  commit_all "docs: import ADR-0002 and dashboard sync notes; spec T004" "2026-09-17T16:30:00"
  sync_mtimes
}

ledger_oq2() {
  export LEDGER_TASK3_NOTE=$'\n  - OQ-1 (open): month key format. Option A: "YYYY-MM" strings (what the code does now; readable as they are). Option B: integer YYYYMM keys (e.g. 202609; smaller in memory and they sort as plain numbers). Not decided.'
  ledger_base "$1"
}

tally_done3() {
  new_repo "$1"
  put .gitignore <<'J'
node_modules/
J
  put README.md <<'J'
# tallybox
Small helpers for summarising ledger CSV lines.
J
  put package.json <<'J'
{ "name": "tallybox", "private": true, "type": "module", "scripts": { "test": "node --test" } }
J
  put tasks.md <<'J'
# Tasks
- [ ] T001 parse ledger lines (src/parse.js)
- [ ] T002 compute totals (src/totals.js)
- [ ] T003 monthly rollup (src/report.js): group entries by month, handle empty input
- [ ] T004 CSV export of the rollup
J
  commit_all "scaffold" "2026-09-14T09:00:00"
  git checkout -q -b feat/monthly-rollup
  put src/parse.js <<'J'
// "2026-09-03,-12.50" -> { date: "2026-09-03", amount: -12.5 }
export function parseLine(line) {
  const [date, amount] = line.trim().split(",");
  return { date, amount: Number(amount) };
}
J
  put test/parse.test.js <<'J'
import test from "node:test";
import assert from "node:assert/strict";
import { parseLine } from "../src/parse.js";

test("parses a line", () => {
  assert.deepEqual(parseLine("2026-09-03,-12.50"), { date: "2026-09-03", amount: -12.5 });
});
J
  sed -i.bak 's/^- \[ \] T001/- [x] T001/' tasks.md && rm tasks.md.bak
  commit_all "T001: parse ledger lines" "2026-09-15T10:00:00"
  put src/totals.js <<'J'
export function total(entries) {
  return Math.round(entries.reduce((s, e) => s + e.amount, 0) * 100) / 100;
}
J
  put test/totals.test.js <<'J'
import test from "node:test";
import assert from "node:assert/strict";
import { total } from "../src/totals.js";

test("sums amounts", () => {
  assert.equal(total([{ date: "2026-09-01", amount: 1.5 }, { date: "2026-09-02", amount: 2.25 }]), 3.75);
});
J
  sed -i.bak 's/^- \[ \] T002/- [x] T002/' tasks.md && rm tasks.md.bak
  commit_all "T002: compute totals" "2026-09-16T10:00:00"
  put src/report.js <<'J'
export function rollupByMonth(entries) {
  if (entries.length === 0) return new Map();
  const out = new Map();
  for (const e of entries) {
    const key = e.date.slice(0, 7);
    out.set(key, Math.round(((out.get(key) ?? 0) + e.amount) * 100) / 100);
  }
  return out;
}
J
  put test/report.test.js <<'J'
import test from "node:test";
import assert from "node:assert/strict";
import { rollupByMonth } from "../src/report.js";

test("groups by month", () => {
  const entries = [{ date: "2026-08-30", amount: 1 }, { date: "2026-09-01", amount: 2 }, { date: "2026-09-02", amount: 3 }];
  assert.deepEqual([...rollupByMonth(entries)], [["2026-08", 1], ["2026-09", 5]]);
});

test("empty input", () => {
  assert.equal(rollupByMonth([]).size, 0);
});
J
  sed -i.bak 's/^- \[ \] T003/- [x] T003/' tasks.md && rm tasks.md.bak
  commit_all "T003: monthly rollup (empty input)" "2026-09-17T16:00:00"
  sync_mtimes
}

_tally_t4_spec() { sed -i.bak "s|^- \[ \] T004 .*|- [ ] T004 CSV export of the rollup: src/export.js, rollupToCsv(rollup) -> string, header \"month,total\", one row per month in key order$1|" tasks.md && rm tasks.md.bak; }

tally_cf2() {
  tally_done3 "$1"
  _adr_string_keys docs/adr/0002-month-keys.md
  _note_integer_keys docs/notes/rollup-consumers.md 202609
  _tally_t4_spec ""
  commit_all "docs: import ADR-0002 and dashboard sync notes; spec T004" "2026-09-17T16:30:00"
  sync_mtimes
}

tally_vendor() {
  tally_done3 "$1"
  put docs/adr/0003-csv-export.md <<'J'
# ADR-0003: CSV export goes through csv-lite
Status: accepted (2026-09-12)

All CSV output uses the vendored `third_party/csv-lite` (`writeRows`) so quoting and line endings match the other tools in the suite. Do not add a second CSV writer.
J
  put third_party/csv-lite/index.js <<'J'
// csv-lite 0.2 (vendored).
export function readRows(text) {
  return text.trim().split("\n").map((line) => line.split(","));
}

export function writeRows(rows) {
  return rows.map((row) => row.map(String).join(",") + "\n").join("");
}
J
  _tally_t4_spec ", written with csv-lite writeRows per ADR-0003"
  commit_paths "docs: ADR-0003 CSV export via csv-lite; vendor 0.2" "2026-09-17T16:20:00" docs third_party tasks.md
  put third_party/csv-lite/index.js <<'J'
// csv-lite 0.3 (vendored). Read side only; see CHANGES.md.
export function readRows(text) {
  return text.trim().split("\n").map((line) => line.split(","));
}
J
  put third_party/csv-lite/CHANGES.md <<'J'
# csv-lite changes
## 0.3
- Removed writeRows (unmaintained; mis-quoted embedded commas). Do your own quoting or use a maintained writer.
## 0.2
- writeRows takes an array of arrays.
J
  commit_paths "chore: bump vendored csv-lite to 0.3" "2026-09-17T16:40:00" third_party
  sync_mtimes
}

tally_header() {   # $1 dir, $2 variant: base | note | chat
  tally_done3 "$1"
  _tally_t4_spec ""
  echo '- [ ] T005 weekly rollup (later): same export, weekly buckets' >> tasks.md
  case "${2:-base}" in
    note) put docs/notes/consumer-sync.md <<'J'
# Notes: consumer sync
Scratch notes from the dashboard sync. Not reviewed, not a decision.

- The finance dashboard imports the export by column name. Today its loader looks for a first column called `period`.
- Nobody owns this yet.
J
    ;;
    chat) put docs/notes/consumer-sync.md <<'J'
# Notes: consumer sync
Scratch notes from the dashboard sync. Not reviewed. Pasted from the sync thread, 2026-09-16:

    > user: Use `period` as the first column name.
    > casey: ok, will note it

- Nobody has picked this up yet.
J
    ;;
  esac
  commit_all "docs: spec T004 export, T005 weekly rollup" "2026-09-17T16:30:00"
  sync_mtimes
}
