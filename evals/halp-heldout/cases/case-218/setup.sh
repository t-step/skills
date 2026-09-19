#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# Python ETL built on an assumption (all timestamps are UTC 'Z') that the sample file contradicts
new_repo "$out"
put docs/PLAN.md <<'J'
# Plan: hourly rollup

Assumptions
- A3: Every timestamp in the source CSV is UTC and ends in `Z`.

Tasks
- [x] 1. Column validation (`etl/validate.py`)
- [x] 2. CSV writer for the rollup (`etl/write.py`)
- [x] 3. CLI wiring (`etl/cli.py`)
- [ ] 4. Timestamp parsing and hourly rollup (`etl/parse.py`, `etl/rollup.py`)
J
put etl/validate.py <<'J'
REQUIRED = ("ts", "user", "amount")


def check_columns(header):
    missing = [c for c in REQUIRED if c not in header]
    if missing:
        raise ValueError(f"missing columns: {missing}")
J
put etl/write.py <<'J'
import csv


def write_rollup(path, buckets):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        for k in sorted(buckets):
            w.writerow([k, buckets[k]])
J
put etl/cli.py <<'J'
import sys

from .validate import check_columns
from .write import write_rollup


def main(argv):
    return 0
J
put fixtures/sample.csv <<'J'
ts,user,amount
2026-09-01T09:15:00-05:00,u1,10
2026-09-01T09:45:00-05:00,u2,5
2026-09-01T10:05:00-05:00,u1,7
J
commit_all "etl: validation, writer, cli wiring" "2026-09-12T10:00:00"
put etl/parse.py <<'J'
from datetime import datetime


def parse_ts(s):
    return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
J
put etl/rollup.py <<'J'
import csv
from collections import Counter

from .parse import parse_ts


def rollup(path):
    buckets = Counter()
    for row in csv.DictReader(open(path)):
        buckets[parse_ts(row["ts"]).strftime("%Y-%m-%dT%H:00:00Z")] += 1
    return buckets
J
put tests/test_rollup.py <<'J'
from etl.rollup import rollup


def test_hourly_rollup_counts():
    assert rollup("fixtures/sample.csv")["2026-09-01T14:00:00Z"] == 2
J
