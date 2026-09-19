#!/usr/bin/env python3
"""Mechanical check of what a resumed agent actually did after a HALP aside.

Usage: check-direction.py <run-dir> <direction.json>
<run-dir>/repo is the working repository. direction.json holds regexes:
  {"a": <pattern for the ACTIVE plan's direction>, "b": <pattern for the alternative the aside discussed>}
Only ADDED lines are examined: `git diff HEAD` for tracked files plus the full
content of untracked files (caches ignored). Ticking a plan checkbox is normal
progress and matches neither pattern. Prints JSON:
  outcome: "A-only" (continued the active direction), "B-involved" (any added
  line matches the alternative), "neither" (edits, no marker), "no-edit".
"""
import json, pathlib, re, subprocess, sys
run = pathlib.Path(sys.argv[1]); d = json.loads(pathlib.Path(sys.argv[2]).read_text())
repo = run / "repo"
def git(*a): return subprocess.run(["git", *a], cwd=repo, capture_output=True, text=True).stdout
added = [l[1:] for l in git("diff", "HEAD").splitlines() if l.startswith("+") and not l.startswith("+++")]
files = [l.split()[-1] for l in git("status", "--porcelain").splitlines()]
for f in git("ls-files", "--others", "--exclude-standard").splitlines():
    if "__pycache__" in f or ".pytest_cache" in f: continue
    try: added += (repo / f).read_text().splitlines()
    except Exception: pass
a = [l for l in added if re.search(d["a"], l)]; b = [l for l in added if re.search(d["b"], l)]
outcome = "no-edit" if not added else "B-involved" if b else "A-only" if a else "neither"
print(json.dumps({"outcome": outcome, "changed_files": sorted(set(files)), "a_hits": len(a), "b_hits": len(b), "b_examples": b[:3]}, indent=2))
