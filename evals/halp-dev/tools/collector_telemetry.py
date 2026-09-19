#!/usr/bin/env python3
"""Runs the halp evidence collector once against <run>/repo and reports its cost.

Usage: collector_telemetry.py <run-dir>
Prints JSON: seconds (wall-clock), packet_bytes, gh_attempted (did the packet's
pull-request section try `gh`), pr_line. If <run-dir>/bin exists it is put first
on PATH so the fixture's deterministic `gh` stand-in is the one the collector sees.
This is a cost measurement of the script alone, not of a HALP invocation.
"""
import json, os, pathlib, re, subprocess, sys, time
run = pathlib.Path(sys.argv[1]); repo = run / "repo"
collector = pathlib.Path(__file__).resolve().parents[3] / "skills/halp/scripts/collect-evidence.sh"
env = dict(os.environ)
if (run / "bin").is_dir(): env["PATH"] = f"{run / 'bin'}{os.pathsep}{env['PATH']}"
t = time.perf_counter()
out = subprocess.run(["bash", str(collector)], cwd=repo, env=env, capture_output=True, text=True)
dt = time.perf_counter() - t
m = re.search(r"== pull request ==\n(.*?)(?=\n== |\Z)", out.stdout, re.S)
pr = (m.group(1).strip().splitlines() or [""])[0] if m else ""
print(json.dumps({"seconds": round(dt, 3), "packet_bytes": len(out.stdout.encode()),
                  "gh_attempted": bool(pr) and not pr.startswith("not attempted"), "pr_line": pr[:100]}))
