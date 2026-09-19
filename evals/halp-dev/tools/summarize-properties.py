#!/usr/bin/env python3
"""One line per property result for a run: id RESULT. Usage: summarize-properties.py <manifest> <id> <run>"""
import json, subprocess, sys, pathlib
here = pathlib.Path(__file__).parent
res = json.loads(subprocess.run([sys.executable, str(here / "check-properties.py"), *sys.argv[1:4]], capture_output=True, text=True, check=True).stdout)
print(sys.argv[2], " ".join(f"{r['id']}={r['result']}" + (f"<{r['match']}>" if r.get('match') else "") for r in res))
