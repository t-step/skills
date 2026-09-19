#!/usr/bin/env bash
# Builds repo/ deterministically. Usage: ./setup.sh [absolute-output-dir]
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
source "$here/../../fixture-lib.sh"
out="${1:-$here/repo}"
# long branch, many changed files, longer task list
new_repo "$out"; through_t003 oq
{ echo "# Tasks: cohort ranking"; echo; } > $SPEC/tasks.md
for i in $(seq 1 20); do
  n=$(printf 'T%03d' "$i")
  mark=" "; [ "$i" -le 15 ] && mark="x"
  echo "- [$mark] $n Step $i in \`cohort/step_$i.py\`" >> $SPEC/tasks.md
done
cat >> $SPEC/spec.md <<'SP'
- OQ-2: Should cohorts over 200 learners be paged? Undecided.
- OQ-3: Is the weekly cutoff Sunday or Monday? Undecided.
SP
for i in $(seq 4 15); do
  printf '"""Step %s."""\n\n\ndef run():\n    return %s\n' "$i" "$i" > "cohort/step_$i.py"
  commit_all "$(printf 'T%03d' "$i"): step $i" "2026-09-15T$(printf '%02d' $((i+8))):00:00"
done
for i in $(seq 4 15); do echo "# revised" >> "cohort/step_$i.py"; done
for i in 16 17 18 19 20; do printf '"""Step %s (draft)."""\n' "$i" > "cohort/step_$i.py"; done
