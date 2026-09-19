#!/usr/bin/env bash
# Copies a run's non-repo artifacts (responses, fingerprints, check JSON, collector telemetry, agent usage
# notes) from the scratch workspace into the ignored raw-run directory of its suite.
# Usage: checkpoint.sh <workspace> <suite-dir> <date-tag> <case-id>...
set -euo pipefail
ws="$1"; suite="$(cd "$2" && pwd)"; tag="$3"; shift 3
for id in "$@"; do
  dest="$suite/runs/$tag/$id"; mkdir -p "$dest"
  (cd "$ws/$id" && find . \( -path ./repo -o -path ./repo.origin \) -prune -o -type f -print | grep -v '^./bin/' | while read -r f; do mkdir -p "$dest/$(dirname "$f")"; cp "$f" "$dest/$f"; done)
done
