#!/usr/bin/env bash
# Usage: obs-all3.sh <manifest> <exp> <label> <ws> <arm.k>...   -- checkpoint several v3 runs of one experiment after one turn; one line each.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"; m="$1"; e="$2"; l="$3"; ws="$4"; shift 4
for a in "$@"; do
  python3 "$here/observe3.py" "$m" "$e" "$ws/$e/$a" "$l" >/dev/null
  python3 - "$ws/$e/$a" "$l" "$e/$a" <<'PY'
import json, sys
d = json.load(open(f"{sys.argv[1]}/snapshots/{sys.argv[2]}.json"))
print(f"{sys.argv[3]:10} {sys.argv[2]:7} worked={d['worked']!s:5} areas={','.join(d['areas']) or '-':20} commits={d['commits']} verify(turn)={d['verify_calls_in_turn']} verified@={d['verified_after_last_edit']} path={d['probe'].get('path')} plan={d['plan_edited']} probe_side_effect={d['probe_side_effect']}")
PY
done
