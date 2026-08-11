#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Run a skill's small divergence fixture set in two fresh, independent
conditions -- baseline (no target skill) and skill (target SKILL.md
appended to the system prompt) -- and report whether their outputs
diverged, plus any declared deterministic verification result.

This is not a grader. It never decides that "different" means "better" --
it captures both conditions' outputs, runs any declared verify command
against the resulting fixture state, and prints a concise table so a human
can judge. See evals/eval-runner-demo/ for a self-contained fixture that
exercises this end to end.

Baseline condition, stated precisely because it must not be misrepresented:
the same headless `claude -p` invocation as the skill condition, with
`--disable-slash-commands` (so no repo/plugin/personal skill can trigger)
and no `--append-system-prompt`. The skill condition is identical except
the target skill's SKILL.md text is appended to the system prompt via
`--append-system-prompt` -- this proves divergence under direct instruction
injection, not normal Agent Skill description-based triggering/discovery.

Run with `uv run scripts/eval-divergence.py <skill> --compare baseline`.
"""

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CLAUDE_TIMEOUT_SECONDS = 300
TOOLS = "Read,Edit,Write,Glob"


def load_manifest(path: Path) -> dict:
    if not path.is_file():
        sys.exit(f"eval-divergence: manifest not found: {path}")
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as e:
        sys.exit(f"eval-divergence: invalid JSON in {path}: {e}")


def select_cases(manifest: dict, wanted: list[str] | None) -> list[dict]:
    cases = manifest.get("evals", [])
    if not wanted:
        return cases
    wanted_set = set(wanted)
    selected = [c for c in cases if str(c.get("id")) in wanted_set or c.get("name") in wanted_set]
    missing = wanted_set - {str(c.get("id")) for c in selected} - {c.get("name") for c in selected}
    if missing:
        sys.exit(f"eval-divergence: unknown case(s) in manifest: {', '.join(sorted(missing))}")
    return selected


def run_claude(prompt: str, cwd: Path, skill_text: str | None, model: str | None) -> dict:
    cmd = [
        "claude", "-p", prompt,
        "--output-format", "json",
        "--disable-slash-commands",
        "--permission-mode", "acceptEdits",
        "--tools", TOOLS,
    ]
    if model:
        cmd += ["--model", model]
    if skill_text is not None:
        cmd += ["--append-system-prompt", skill_text]

    try:
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=CLAUDE_TIMEOUT_SECONDS
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"timed out after {CLAUDE_TIMEOUT_SECONDS}s", "raw_stdout": "", "raw_stderr": ""}

    if proc.returncode != 0:
        return {
            "ok": False,
            "error": f"claude exited {proc.returncode}",
            "raw_stdout": proc.stdout,
            "raw_stderr": proc.stderr,
        }

    try:
        parsed = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"ok": False, "error": "non-JSON output", "raw_stdout": proc.stdout, "raw_stderr": proc.stderr}

    return {
        "ok": not parsed.get("is_error", False),
        "error": None if not parsed.get("is_error") else "agent reported is_error",
        "result_text": parsed.get("result", ""),
        "cost_usd": parsed.get("total_cost_usd"),
        "session_id": parsed.get("session_id"),
        "raw_stdout": proc.stdout,
        "raw_stderr": proc.stderr,
    }


def run_verify(verify_specs: list[dict], cwd: Path) -> list[dict]:
    results = []
    for spec in verify_specs:
        try:
            proc = subprocess.run(
                spec["cmd"], shell=True, cwd=cwd, capture_output=True, text=True, timeout=60
            )
            results.append({
                "cmd": spec["cmd"],
                "description": spec.get("description", ""),
                "passed": proc.returncode == 0,
                "output": (proc.stdout + proc.stderr).strip(),
            })
        except subprocess.TimeoutExpired:
            results.append({
                "cmd": spec["cmd"], "description": spec.get("description", ""),
                "passed": False, "output": "timed out",
            })
    return results


def diff_trees(a: Path, b: Path) -> tuple[bool, str]:
    proc = subprocess.run(["diff", "-ru", str(a), str(b)], capture_output=True, text=True)
    diverged = proc.returncode != 0
    return diverged, proc.stdout


def run_condition(case: dict, condition: str, src_repo: Path, skill_text: str | None,
                   model: str | None, case_run_dir: Path) -> dict:
    scratch = Path(tempfile.mkdtemp(prefix=f"eval-divergence-{case['id']}-{condition}-"))
    shutil.copytree(src_repo, scratch, dirs_exist_ok=True)

    outcome = run_claude(case["prompt"], scratch, skill_text, model)
    verify_results = run_verify(case.get("verify", []), scratch)

    dest = case_run_dir / condition
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copytree(scratch, dest / "repo", dirs_exist_ok=True)
    (dest / "transcript.json").write_text(json.dumps(outcome, indent=2))
    if outcome.get("raw_stderr"):
        (dest / "stderr.txt").write_text(outcome["raw_stderr"])

    shutil.rmtree(scratch, ignore_errors=True)
    return {"outcome": outcome, "verify": verify_results, "repo_dir": dest / "repo"}


def run_case(case: dict, skill_text: str, model: str | None, run_dir: Path) -> dict:
    src_repo = REPO / case["files"][0]
    if not src_repo.is_dir():
        sys.exit(f"eval-divergence: case {case['id']} 'files' entry not found: {src_repo}")

    case_run_dir = run_dir / f"case-{case['id']:03d}"
    baseline = run_condition(case, "baseline", src_repo, None, model, case_run_dir)
    skill = run_condition(case, "skill", src_repo, skill_text, model, case_run_dir)

    diverged, diff_text = diff_trees(baseline["repo_dir"], skill["repo_dir"])
    (case_run_dir / "diff.txt").write_text(diff_text)

    return {"case": case, "baseline": baseline, "skill": skill, "diverged": diverged, "run_dir": case_run_dir}


def format_verify(verify_results: list[dict]) -> str:
    if not verify_results:
        return "(none declared)"
    return ", ".join(f"{'PASS' if v['passed'] else 'FAIL'}" for v in verify_results)


def print_summary(results: list[dict], baseline_desc: str, skill_desc: str) -> None:
    print()
    print(f"Baseline condition: {baseline_desc}")
    print(f"Skill condition:    {skill_desc}")
    print()
    col_name, col_verify, col_diverged = 45, 24, 9
    header = f"{'Fixture':<{col_name}} {'Baseline verify':<{col_verify}} {'Skill verify':<{col_verify}} {'Diverged':<{col_diverged}} Output"
    print(header)
    print("-" * len(header))
    for r in results:
        name = f"{r['case']['id']}-{r['case']['name']}"
        b_ok = "ok" if r["baseline"]["outcome"]["ok"] else "ERROR"
        s_ok = "ok" if r["skill"]["outcome"]["ok"] else "ERROR"
        b_cell = f"{format_verify(r['baseline']['verify'])} ({b_ok})"
        s_cell = f"{format_verify(r['skill']['verify'])} ({s_ok})"
        diverged = "yes" if r["diverged"] else "no"
        rel = r["run_dir"].relative_to(REPO)
        print(f"{name:<{col_name}} {b_cell:<{col_verify}} {s_cell:<{col_verify}} {diverged:<{col_diverged}} {rel}")
    print()


def write_summary_md(run_dir: Path, results: list[dict], skill_name: str,
                      baseline_desc: str, skill_desc: str) -> None:
    lines = [
        f"# eval-divergence run: {skill_name}",
        "",
        f"Run directory: `{run_dir.relative_to(REPO)}`",
        "",
        f"**Baseline condition:** {baseline_desc}",
        "",
        f"**Skill condition:** {skill_desc}",
        "",
        "| Fixture | Baseline verify | Skill verify | Diverged | Output |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        name = f"{r['case']['id']}-{r['case']['name']}"
        b_verify = format_verify(r["baseline"]["verify"])
        s_verify = format_verify(r["skill"]["verify"])
        diverged = "yes" if r["diverged"] else "no"
        rel = r["run_dir"].relative_to(REPO)
        lines.append(f"| {name} | {b_verify} | {s_verify} | {diverged} | `{rel}` |")
    lines.append("")
    lines.append("The runner does not judge whether divergence is an improvement. "
                  "Inspect `diff.txt` and each condition's `transcript.json` under the "
                  "fixture's output directory to judge.")
    (run_dir / "summary.md").write_text("\n".join(lines) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("skill", help="skill name (matches skills/<skill>/SKILL.md by default)")
    parser.add_argument("--compare", required=True, choices=["baseline"],
                         help="what to compare the skill condition against")
    parser.add_argument("--manifest", type=Path, default=None,
                         help="default: evals/<skill>/divergence.json")
    parser.add_argument("--skill-file", type=Path, default=None,
                         help="default: skills/<skill>/SKILL.md")
    parser.add_argument("--cases", default=None,
                         help="comma-separated case ids or names; default: all cases in the manifest")
    parser.add_argument("--model", default=None, help="pin a model for both conditions")
    args = parser.parse_args()

    def resolve_repo_path(p: Path | None, default: Path) -> Path:
        if p is None:
            return default
        return p if p.is_absolute() else REPO / p

    manifest_path = resolve_repo_path(args.manifest, REPO / "evals" / args.skill / "divergence.json")
    skill_file = resolve_repo_path(args.skill_file, REPO / "skills" / args.skill / "SKILL.md")
    if not skill_file.is_file():
        sys.exit(f"eval-divergence: skill file not found: {skill_file}")
    skill_text = skill_file.read_text()

    manifest = load_manifest(manifest_path)
    wanted = [c.strip() for c in args.cases.split(",")] if args.cases else None
    cases = select_cases(manifest, wanted)
    if not cases:
        sys.exit("eval-divergence: no cases selected")

    run_dir = REPO / "evals" / args.skill / "runs" / datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    run_dir.mkdir(parents=True, exist_ok=True)

    baseline_desc = "claude -p, --disable-slash-commands, no --append-system-prompt"
    skill_desc = (f"claude -p, --disable-slash-commands, --append-system-prompt="
                  f"contents of {skill_file.relative_to(REPO)} "
                  "(this proves behavior change under direct system-prompt injection, "
                  "not normal Agent Skill description-based triggering)")
    if args.model:
        baseline_desc += f", --model {args.model}"
        skill_desc += f", --model {args.model}"

    results = [run_case(case, skill_text, args.model, run_dir) for case in cases]

    print_summary(results, baseline_desc, skill_desc)
    write_summary_md(run_dir, results, args.skill, baseline_desc, skill_desc)

    if any(not r["baseline"]["outcome"]["ok"] or not r["skill"]["outcome"]["ok"] for r in results):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
