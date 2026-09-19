#!/usr/bin/env python3
"""Persists one small record per run from a scratch workspace into the suite's ignored raw-run directory.

Usage: checkpoint.py <workspace> <suite-dir> <date-tag> <case-id>...
Writes <suite-dir>/runs/<date-tag>/<id>/run.json plus outputs/*.md (the agent's replies). run.json gathers what
the graders left in the workspace: fingerprints (before/after/turnN), the response check, collector telemetry,
the direction result and any turn notes. The fixture repo, the per-run prompt/instructions (derivable from the
case) and the stub gh are not copied.
"""
import json, pathlib, shutil, sys

ws, suite, tag, ids = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]).resolve(), sys.argv[3], sys.argv[4:]
def load(p): return json.loads(p.read_text()) if p.exists() else None
for cid in ids:
    src, dest = ws / cid, suite / "runs" / tag / cid
    (dest / "outputs").mkdir(parents=True, exist_ok=True)
    rec = {"case": cid,
           "fingerprints": {f.name.split(".", 1)[1]: f.read_text().splitlines() for f in sorted(src.glob("fingerprint.*"))},
           "check": load(src / "check.json"), "collector": load(src / "collector.json"), "direction": load(src / "direction.json"),
           "notes": {f.name: f.read_text().strip() for f in sorted(src.glob("*-note.txt"))}}
    (dest / "run.json").write_text(json.dumps(rec, indent=1) + "\n")
    for f in sorted((src / "outputs").glob("*")):
        shutil.copy(f, dest / "outputs" / f.name)
