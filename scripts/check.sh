#!/usr/bin/env bash
# Canonical repository checks (AGENTS.md, "Verification — local-first").
# Run before any commit or PR; the machine-local pre-commit hook and the
# CI backstop (.github/workflows/checks.yml) both invoke this same script,
# so passing here means passing everywhere. Add new checks here — this is
# the single entry point.
set -euo pipefail
cd "$(dirname "$0")/.."

uv run scripts/check-skill-frontmatter.py
uv run scripts/generate-skill-inventory.py --check
python3 scripts/check-eval-isolation.py
python3 scripts/check-skill-deps.py
python3 scripts/test-skill-usage-report.py
python3 scripts/test-eval-divergence.py
