#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# T001-T003 committed; uncommitted edit to selectors.py; T004 not started
new_repo "$out"; through_t003 oq
cat > cohort/selectors.py <<'PY'
"""Selector normalization (FR-4)."""


def normalize_selector(raw):
    if not raw or not raw.strip():
        raise ValueError("empty selector")
    return raw.strip().lower().replace(" ", "-")
PY
