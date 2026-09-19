#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# default branch is `trunk`; no remote, no origin/HEAD; feature branch three commits ahead
new_repo "$out" trunk
put sched/core.py <<'J'
def next_run(now, every):
    return now + every
J
put README.md <<'J'
# sched
J
commit_all "Initial sched" "2026-09-04T09:00:00"
git checkout -q -b feat/cron-syntax
put sched/cron.py <<'J'
def parse(expr):
    return expr.split()
J
commit_all "cron: parse fields" "2026-09-14T09:00:00"
put sched/cron.py <<'J'
def parse(expr):
    parts = expr.split()
    if len(parts) != 5:
        raise ValueError("expected 5 fields")
    return parts
J
commit_all "cron: validate field count" "2026-09-14T15:00:00"
put sched/core.py <<'J'
from .cron import parse


def next_run(now, every):
    return now + every
J
commit_all "core: import cron parser" "2026-09-15T10:00:00"
