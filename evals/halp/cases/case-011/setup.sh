#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# plain directory, not a git repository
new_dir "$out"
printf '# scratch\n\nMisc scripts.\n' > README.md
printf 'print("hello")\n' > main.py
