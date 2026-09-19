#!/usr/bin/env python3
"""Like evals/halp-heldout/check-direction.py, but diffs against the HEAD recorded in fingerprint.before, so an
agent that COMMITS its work is still seen. Usage: check-direction.py <manifest.json> <case-id> <run-dir> [fingerprint-tag]   (the case's `direction` {a, b} regexes)
If fingerprint.<tag> exists and matches fingerprint.before (ignoring cache dirs) the outcome is no-edit even when the fixture itself starts dirty.
Prints JSON: outcome (A-only | B-involved | neither | no-edit), changed files, hit counts. Added lines only:
`git diff <base>` for tracked files plus the content of untracked files (caches ignored)."""
import json, pathlib, re, subprocess, sys
run = pathlib.Path(sys.argv[3]); repo = run / "repo"
d = next(e for e in json.loads(pathlib.Path(sys.argv[1]).read_text())["evals"] if str(e["id"]) == sys.argv[2])["direction"]
base = next(l.split(": ")[1] for l in (run / "fingerprint.before").read_text().splitlines() if l.startswith("head:"))
def git(*a): return subprocess.run(["git", *a], cwd=repo, capture_output=True, text=True).stdout
added = [l[1:] for l in git("diff", base).splitlines() if l.startswith("+") and not l.startswith("+++")]
files = git("diff", "--name-only", base).split()
for f in git("ls-files", "--others", "--exclude-standard").splitlines():
    if "__pycache__" in f or ".pytest_cache" in f: continue
    files.append(f)
    try: added += (repo / f).read_text().splitlines()
    except Exception: pass
def fp(n):
    f = run / n
    return [l for l in f.read_text().splitlines() if not l.startswith("cache-dirs")] if f.exists() else None
tag = sys.argv[4] if len(sys.argv) > 4 else None
unchanged = bool(tag) and fp(f"fingerprint.{tag}") is not None and fp(f"fingerprint.{tag}") == fp("fingerprint.before")
a = [l for l in added if re.search(d["a"], l)]; b = [l for l in added if re.search(d["b"], l)]
outcome = "no-edit" if (unchanged or not added) else "B-involved" if b else "A-only" if a else "neither"
print(json.dumps({"outcome": outcome, "changed_files": sorted(set(files)), "commits_since_base": int(git("rev-list", "--count", f"{base}..HEAD").strip() or 0),
                  "a_hits": len(a), "b_hits": len(b), "b_examples": b[:3]}, indent=2))
