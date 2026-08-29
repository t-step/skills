#!/usr/bin/env bash
# Cheap, deterministic local invariants for the canonical skills/ and evals/
# trees. Run before any commit or PR touching those trees.
set -euo pipefail
cd "$(dirname "$0")/.."

uv run scripts/check-skill-frontmatter.py
python3 scripts/check-eval-isolation.py
python3 scripts/check-skill-deps.py
