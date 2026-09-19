#!/usr/bin/env bash
# Deterministic post-run checks for one halp run.
# Usage: grade.sh <manifest.json> <case-id> <run-dir> [tag]
# tag (default "after"): writes fingerprint.<tag> from <run-dir>/repo (use "after"
# for the first turn, "turn2" etc. later), then runs check-response.py against
# fingerprint.before/fingerprint.after. Prints its JSON.
set -euo pipefail
tools="$(cd "$(dirname "$0")" && pwd)"; root="$(cd "$tools/../../.." && pwd)"
manifest="$1"; id="$2"; run="$3"; tag="${4:-after}"
[ -e "$run/fingerprint.$tag" ] && { echo "grade.sh: fingerprint.$tag already exists; refusing to overwrite (the repo may have moved on)" >&2; [ "$tag" = after ] && cat "$run/check.json"; exit 0; }
bash "$root/evals/halp/fingerprint.sh" "$run/repo" > "$run/fingerprint.$tag"
[ "$tag" = after ] && python3 "$root/evals/halp/check-response.py" "$manifest" "$id" "$run" | tee "$run/check.json"
