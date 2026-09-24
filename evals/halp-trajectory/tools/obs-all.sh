#!/usr/bin/env bash
# Usage: obs-all.sh <manifest> <exp> <label> <ws> <arm.k>...   -- checkpoint several runs of one experiment after one turn (fingerprint + snapshot), one line each.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"; m="$1"; e="$2"; l="$3"; ws="$4"; shift 4
for a in "$@"; do
  python3 "$here/observe.py" "$m" "$e" "$ws/$e/$a" "$l" >/dev/null
  python3 - "$ws/$e/$a" "$l" "$e/$a" <<'PY'
import json, sys
d = json.load(open(f"{sys.argv[1]}/snapshots/{sys.argv[2]}.json")); ex = d["probe"].get("export", {})
print(f"{sys.argv[3]:12} {sys.argv[2]:6} worked={d['worked']!s:5} areas={','.join(d['areas']) or '-':22} ticked={','.join(t for t in d['ticked'] if t > 'T003') or '-':5} key={d['probe'].get('key_class')} export={ex.get('header_first', '-')}/{ex.get('writer', '-')} tests={d['tests_pass']} oq1={str(d.get('oq1'))[:8]} plan={d['plan_edited']} claims={d['decision_claims']}")
PY
done
