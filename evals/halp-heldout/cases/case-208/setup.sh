#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# feature branch mid-rebase onto main; stopped on a conflict in the second of three commits
new_repo "$out"
put tinyq/queue.py <<'J'
class Queue:
    def __init__(self):
        self.items = []

    def push(self, x):
        self.items.append(x)

    def pop(self):
        return self.items.pop(0)
J
commit_all "Initial tinyq" "2026-09-05T09:00:00"
git checkout -q -b feat/priority-queue
cat >> tinyq/queue.py <<'J'

    def peek(self):
        return self.items[0]
J
commit_all "queue: add peek" "2026-09-12T09:00:00"
python3 - <<'PY'
p="tinyq/queue.py"; s=open(p).read()
open(p,"w").write(s.replace("        self.items.append(x)","        self.items.append(x)\n        self.items.sort()"))
PY
commit_all "queue: keep items sorted on push" "2026-09-12T11:00:00"
put tests/test_queue.py <<'J'
from tinyq.queue import Queue


def test_sorted_push():
    q = Queue(); q.push(3); q.push(1)
    assert q.peek() == 1
J
commit_all "tests: sorted push" "2026-09-12T12:00:00"
git checkout -q main
python3 - <<'PY'
p="tinyq/queue.py"; s=open(p).read()
open(p,"w").write(s.replace("    def push(self, x):\n        self.items.append(x)","    def push(self, x):\n        self.items.append(x)\n        return len(self.items) - 1"))
PY
commit_all "queue: push returns the new index" "2026-09-13T10:00:00"
git checkout -q feat/priority-queue
GIT_COMMITTER_DATE="2026-09-14T09:00:00" GIT_EDITOR=true git rebase main >/dev/null 2>&1 || true
