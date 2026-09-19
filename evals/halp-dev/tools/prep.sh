#!/usr/bin/env bash
# Builds one run workspace for a halp eval case, outside the agent-visible tree.
# Usage: prep.sh <suite-dir> <case-id> <workspace> [instruction-template, default agent-prompt.md]
#   <suite-dir>  e.g. evals/halp-heldout (contains cases/case-<id>/{setup.sh,prompt.md})
# Creates <workspace>/<id>/{repo,bin?,prompt.md,outputs/,fingerprint.before,collector.json}.
set -euo pipefail
tools="$(cd "$(dirname "$0")" && pwd)"; root="$(cd "$tools/../../.." && pwd)"
suite="$(cd "$1" && pwd)"; id="$2"; ws="$3"; run="$ws/$id"
rm -rf "$run"; mkdir -p "$run/outputs"
bash "$suite/cases/case-$id/setup.sh" "$run/repo"
cp "$suite/cases/case-$id/prompt.md" "$run/prompt.md"
# A fixture with a GitHub-looking origin but no gh stand-in would make the collector call the real
# gh over the network (result depends on the operator's auth). Give it an offline default instead.
if [ ! -x "$run/bin/gh" ]; then
  mkdir -p "$run/bin"
  printf '#!/bin/sh\necho "error connecting to api.github.com" >&2; exit 1\n' > "$run/bin/gh"; chmod +x "$run/bin/gh"
fi
bash "$root/evals/halp/fingerprint.sh" "$run/repo" > "$run/fingerprint.before"
python3 "$tools/collector_telemetry.py" "$run" > "$run/collector.json"
# Per-run instructions for the agent under test (short launch prompt: "follow <run>/instructions.md")
sed "s|{RUN}|$run|g" "$tools/${4:-agent-prompt.md}" > "$run/instructions.md"
