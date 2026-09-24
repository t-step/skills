#!/usr/bin/env python3
"""Builds one v3 (real-repository) trajectory run workspace outside the repository and records its t0 checkpoint.

Usage: prep3.py <experiments-v3.json> <exp-id> <arm[.k]> <workspace>
Creates <workspace>/<exp-id>/<arm[.k]>/ with
  subject/{repo,bin,prompt.md,instructions.md,outputs/}   the ONLY directory the subject agent is told about
  turns.json fingerprint.before verify.log snapshots/t0.json tree.t0   grader-side files (never inside subject/)
`cases/case-<id>/setup.sh <dest>` builds the fixture (a real upstream checkout at a pinned commit plus the frozen work-in-progress;
dependencies and caches live in ignored paths). The manifest's `shims` (with {REPO} substituted) put logging wrappers for the test
runners first on the subject's PATH.
"""
import hashlib, json, pathlib, shutil, subprocess, sys
here = pathlib.Path(__file__).resolve().parent; suite = here.parent
manifest, expid, armid, ws = sys.argv[1], sys.argv[2], sys.argv[3], pathlib.Path(sys.argv[4]).resolve()
exp = next(e for e in json.loads(pathlib.Path(manifest).read_text())["evals"] if str(e["id"]) == expid)
armname = armid.split(".")[0]
a = next(x for x in exp["arms"] if x["arm"] == armname)
run = ws / expid / armid
# the subject only ever sees an opaque path (no experiment id, arm name or replicate); the grader-side name is a symlink to it
opaque = ws / "_s" / hashlib.sha1(f"{expid}/{armid}".encode()).hexdigest()[:10]
subj = opaque / "subject"
shutil.rmtree(run, ignore_errors=True); shutil.rmtree(opaque, ignore_errors=True); (subj / "outputs").mkdir(parents=True); run.mkdir(parents=True, exist_ok=True)
(run / "subject").symlink_to(subj); (run / "verify.log").symlink_to(opaque / "verify.log")
case = suite / "cases" / f"case-{expid}"
subprocess.run(["bash", str(case / "setup.sh"), str(subj / "repo")], check=True, stdout=subprocess.DEVNULL)
# every fixture presents the same session shape: a named work branch (not a detached HEAD) and a local identity for any commit the user asks for
g = lambda *a: subprocess.run(["git", *a], cwd=subj / "repo", capture_output=True, text=True)
if g("symbolic-ref", "-q", "HEAD").returncode != 0 or g("symbolic-ref", "--short", "HEAD").stdout.strip() in ("main", "master", "base"): g("checkout", "-q", "-B", "fix-issue")
g("config", "user.name", "fixture-user"); g("config", "user.email", "fixture@example.invalid")
turns = [{"n": i + 1, **t} for i, t in enumerate(a.get("head", []) + a.get("tail", exp["tail"]))]
extra = "\n".join(exp.get("narrative", []) + a.get("narrative_extra", []))
prompt = (case / "prompt.md").read_text().replace("{{EXTRA}}\n", extra + "\n" if extra else "").replace("{{FIRST_MESSAGE}}", turns[0]["message"])
(subj / "prompt.md").write_text(prompt)
(run / "turns.json").write_text(json.dumps({"turns": turns}, indent=1, ensure_ascii=False) + "\n")
shims = [s.replace("{REPO}", str(subj / "repo")) for s in exp.get("shims", [])]
subprocess.run(["bash", str(here / "mkshims.sh"), str(subj / "bin"), str(opaque / "verify.log"), *shims], check=True)
(run / "fingerprint.before").write_text(subprocess.run(["bash", str(here / "fingerprint3.sh"), str(subj / "repo")], capture_output=True, text=True).stdout)
(subj / "instructions.md").write_text((here / "agent-prompt.md").read_text().replace("{RUN}", str(subj)))
subprocess.run([sys.executable, str(here / "observe3.py"), manifest, expid, str(run), "t0"], check=True, stdout=subprocess.DEVNULL)
print(subj)
