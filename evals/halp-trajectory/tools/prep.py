#!/usr/bin/env python3
"""Builds one trajectory run workspace, outside the repository, and records its t0 snapshot.

Usage: prep.py <experiments.json> <exp-id> <arm[.k]> <workspace>
`arm.k` (v2) is replicate k of the manifest's arm/cell `arm`; plain `arm` (v1) is unchanged.
Creates <workspace>/<exp-id>/<arm[.k]>/ with
  subject/{repo,bin,prompt.md,instructions.md,outputs/}   the ONLY directory the subject agent is told about (v2; v1 had these beside the grader files)
  initial/ turns.json fingerprint.before snapshots/t0.json  grader-side files (v2: not inside the subject's directory)
`initial/` is a copy of the fixture as the session begins (the reference for 'what did the agent change'). turns.json lists the whole
scripted conversation (label, mode, message) for the operator; only turn 1 is in prompt.md, the rest are sent later.
"""
import json, pathlib, shutil, subprocess, sys
here = pathlib.Path(__file__).resolve().parent; suite = here.parent; root = suite.parent.parent
manifest, expid, armid, ws = sys.argv[1], sys.argv[2], sys.argv[3], pathlib.Path(sys.argv[4]).resolve()
exp = next(e for e in json.loads(pathlib.Path(manifest).read_text())["evals"] if str(e["id"]) == expid)
armname = armid.split(".")[0]
a = next(x for x in exp["arms"] if x["arm"] == armname)
run = ws / expid / armid; subj = run / "subject"
shutil.rmtree(run, ignore_errors=True); (subj / "outputs").mkdir(parents=True)
case = suite / "cases" / f"case-{expid}"
subprocess.run(["bash", str(case / "setup.sh"), str(subj / "repo")] + ([a["variant"]] if a.get("variant") else []), check=True)
turns = [{"n": i + 1, **t} for i, t in enumerate(a.get("head", []) + a.get("tail", exp["tail"]))]
extra = "\n".join(exp.get("narrative", []) + a.get("narrative_extra", []))
prompt = (case / "prompt.md").read_text().replace("{{EXTRA}}\n", extra + "\n" if extra else "").replace("{{FIRST_MESSAGE}}", turns[0]["message"])
(subj / "prompt.md").write_text(prompt)
(run / "turns.json").write_text(json.dumps({"turns": turns}, indent=1, ensure_ascii=False) + "\n")
shutil.copytree(subj / "repo", run / "initial", ignore=shutil.ignore_patterns(".git"), symlinks=True)
(subj / "bin").mkdir(); (subj / "bin/gh").write_text('#!/bin/sh\necho "error connecting to api.github.com" >&2; exit 1\n'); (subj / "bin/gh").chmod(0o755)
(run / "fingerprint.before").write_text(subprocess.run(["bash", str(root / "evals/halp/fingerprint.sh"), str(subj / "repo")], capture_output=True, text=True).stdout)
(subj / "instructions.md").write_text((here / "agent-prompt.md").read_text().replace("{RUN}", str(subj)))
subprocess.run([sys.executable, str(here / "observe.py"), manifest, expid, str(run), "t0"], check=True, stdout=subprocess.DEVNULL)
print(subj)
