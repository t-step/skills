#!/usr/bin/env bash
# Grades + checkpoints a small batch (checkpoint = run.json + outputs/, see checkpoint.py). Usage: batch-grade.sh <manifest> <suite-dir> <workspace> <date-tag> <id>...
# Prints one compact line per run: words/budget, repo-unchanged, pattern hits, action phrases, collector cost.
set -euo pipefail
tools="$(cd "$(dirname "$0")" && pwd)"; manifest="$1"; suite="$2"; ws="$3"; tag="$4"; shift 4
for id in "$@"; do
  bash "$tools/grade.sh" "$manifest" "$id" "$ws/$id" >/dev/null
  python3 - "$ws/$id" "$id" <<'P'
import json, sys, pathlib
r = pathlib.Path(sys.argv[1]); c = json.loads((r/"check.json").read_text()); k = json.loads((r/"collector.json").read_text())
print(sys.argv[2], f"words={c['words']}/{c['max_words']}", "OK-budget" if c["within_budget"] else "OVER", "unchanged" if c["repo_unchanged"] else f"MUTATED{c['changed_fields']}",
      "forbid=" + str(c["forbidden_pattern_hits"]) if c["forbidden_pattern_hits"] else "", "dump?" if c["raw_dump_suspected"] else "",
      "action=" + str(c["permission_or_action_phrases"]) if c["permission_or_action_phrases"] else "", f"| collector {k['seconds']}s {k['packet_bytes']}B gh={k['gh_attempted']}")
P
done
python3 "$tools/checkpoint.py" "$ws" "$suite" "$tag" "$@"
