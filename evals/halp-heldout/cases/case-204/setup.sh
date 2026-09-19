#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# small Python package; no spec, plan, task list, or docs beyond a one-line README
new_repo "$out"
put README.md <<'J'
# logtail
J
put logtail/__init__.py <<'J'
J
put logtail/tail.py <<'J'
def tail(path, n=10):
    with open(path) as f:
        return f.readlines()[-n:]
J
commit_all "initial" "2026-09-13T09:00:00"
git checkout -q -b spike/tail-follow
put logtail/tail.py <<'J'
import time


def tail(path, n=10):
    with open(path) as f:
        return f.readlines()[-n:]


def follow(path):
    with open(path) as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.2)
                continue
            yield line
J
commit_all "wip" "2026-09-14T09:10:00"
put logtail/tail.py <<'J'
import time


def tail(path, n=10):
    with open(path) as f:
        return f.readlines()[-n:]


def follow(path, poll=0.2):
    with open(path) as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(poll)
                continue
            yield line
J
commit_all "wip: follow mode, poll interval" "2026-09-14T11:40:00"
put logtail/cli.py <<'J'
import sys
from .tail import follow

if __name__ == "__main__":
    for line in follow(sys.argv[1]):
        sys.stdout.write(line)
J
commit_all "add cli entry" "2026-09-15T08:30:00"
