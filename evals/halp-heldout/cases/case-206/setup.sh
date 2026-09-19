#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# GitHub-looking origin; two local commits not pushed; stubbed `gh` finds no PR; no verification artifacts
new_repo "$out"
put billing_worker/retry.py <<'J'
import random


def backoff(attempt, base=0.5):
    return base * (2 ** attempt)
J
put README.md <<'J'
# billing-worker
J
commit_all "Initial billing worker" "2026-09-09T09:00:00"
git checkout -q -b fix/retry-jitter
make_origin "git@github.com:acme/billing-worker.git" main fix/retry-jitter
git branch -q -u origin/fix/retry-jitter
put billing_worker/retry.py <<'J'
import random


def backoff(attempt, base=0.5, jitter=0.1):
    return base * (2 ** attempt) * (1 + random.uniform(-jitter, jitter))
J
commit_all "retry: add jitter to backoff" "2026-09-16T10:00:00"
put billing_worker/retry.py <<'J'
import random


def backoff(attempt, base=0.5, jitter=0.1, cap=30.0):
    return min(cap, base * (2 ** attempt) * (1 + random.uniform(-jitter, jitter)))
J
commit_all "retry: cap backoff at 30s" "2026-09-16T11:30:00"
gh_shim "$out" none
