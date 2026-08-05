#!/usr/bin/env python3
"""Focused verification for scripts/skill-usage-report.py.

Stdlib-only, no test framework, run directly: `python3 scripts/test-skill-usage-report.py`.
Follows the same runpy.run_path(..., run_name="test") pattern this script's own
implementation history used for its own dev-time verification — calls functions
directly without needing the hyphenated filename to be importable.

Each fixture is built in a temp directory and torn down automatically.
"""

import json
import pathlib
import runpy
import subprocess
import sys
import tempfile

REPO = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "skill-usage-report.py"

failures = []


def check(name, condition):
    if condition:
        print(f"OK: {name}")
    else:
        print(f"FAIL: {name}")
        failures.append(name)


def load_module():
    return runpy.run_path(str(SCRIPT), run_name="test")


def assistant_line(skill, session_id="sess-1", ts="2026-08-01T10:00:00.000Z", uuid="u1"):
    return json.dumps(
        {
            "type": "assistant",
            "sessionId": session_id,
            "timestamp": ts,
            "uuid": uuid,
            "message": {"content": [{"type": "tool_use", "name": "Skill", "input": {"skill": skill}}]},
        }
    )


def test_discover_tracked_skills():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        root = pathlib.Path(tmp)
        for name in ("alpha", "beta"):
            skill_dir = root / "skills" / name
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("---\nname: " + name + "\n---\n")
        (root / "skills" / "no-skill-md").mkdir(parents=True)
        result = mod["discover_tracked_skills"](root)
        check("discover_tracked_skills finds skills/*/SKILL.md dirs", result == {"alpha", "beta"})


def test_parse_matching_invocation():
    mod = load_module()
    text = assistant_line("tracked-skill") + "\n"
    rows = list(mod["parse_skill_invocations"](text, {"tracked-skill"}))
    check(
        "parse_skill_invocations extracts skill_name/session_id/ts",
        rows == [("tracked-skill", "sess-1", "2026-08-01T10:00:00.000Z")],
    )


def test_ignores_untracked_skill():
    mod = load_module()
    text = assistant_line("untracked-skill") + "\n"
    rows = list(mod["parse_skill_invocations"](text, {"tracked-skill"}))
    check("parse_skill_invocations ignores untracked skill names", rows == [])


def test_malformed_json_tolerance():
    mod = load_module()
    text = (
        assistant_line("tracked-skill", session_id="sess-a", uuid="u1")
        + "\n"
        + '{"type":"assistant", not valid json\n'
        + assistant_line("tracked-skill", session_id="sess-b", uuid="u2")
        + "\n"
    )
    rows = list(mod["parse_skill_invocations"](text, {"tracked-skill"}))
    check(
        "parse_skill_invocations skips malformed lines without crashing, keeps good ones",
        len(rows) == 2 and {r[1] for r in rows} == {"sess-a", "sess-b"},
    )


def test_duplicate_invocations_in_separate_records_count_separately():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        projects_root = pathlib.Path(tmp) / "projects" / "proj-a"
        projects_root.mkdir(parents=True)
        transcript = projects_root / "session1.jsonl"
        transcript.write_text(
            assistant_line("tracked-skill", session_id="sess-1", ts="2026-08-01T10:00:00.000Z", uuid="u1")
            + "\n"
            + assistant_line("tracked-skill", session_id="sess-1", ts="2026-08-01T10:05:00.000Z", uuid="u2")
            + "\n"
        )
        stats = mod["scan_transcripts"](pathlib.Path(tmp) / "projects", {"tracked-skill"})
        check(
            "two separate assistant records invoking the same skill both count",
            stats["tracked-skill"].total == 2,
        )


def test_unused_skill_shows_zero():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        projects_root = pathlib.Path(tmp) / "projects"
        stats = mod["scan_transcripts"](projects_root, {"used-skill", "unused-skill"})
        check(
            "unused tracked skill appears with zero count and no last_used",
            stats["unused-skill"].total == 0 and stats["unused-skill"].last_used is None,
        )


def test_most_recent_timestamp_selection():
    mod = load_module()
    with tempfile.TemporaryDirectory() as tmp:
        projects_root = pathlib.Path(tmp) / "projects" / "proj-a"
        projects_root.mkdir(parents=True)
        transcript = projects_root / "session1.jsonl"
        transcript.write_text(
            assistant_line("tracked-skill", ts="2026-07-01T10:00:00.000Z", uuid="u1")
            + "\n"
            + assistant_line("tracked-skill", ts="2026-08-01T10:00:00.000Z", uuid="u2")
            + "\n"
            + assistant_line("tracked-skill", ts="2026-06-01T10:00:00.000Z", uuid="u3")
            + "\n"
        )
        stats = mod["scan_transcripts"](pathlib.Path(tmp) / "projects", {"tracked-skill"})
        check(
            "most recent timestamp is selected out of three, not first/last-in-file",
            stats["tracked-skill"].last_used == "2026-08-01T10:00:00.000Z",
        )


def test_missing_transcript_root():
    mod = load_module()
    missing = pathlib.Path(tempfile.gettempdir()) / "skill-usage-report-does-not-exist-xyz"
    stats = mod["scan_transcripts"](missing, {"tracked-skill"})
    check(
        "missing projects root returns zeroed stats instead of raising",
        stats["tracked-skill"].total == 0,
    )


def test_full_cli_output_against_fixture():
    with tempfile.TemporaryDirectory() as tmp:
        projects_root = pathlib.Path(tmp) / "projects" / "proj-a"
        projects_root.mkdir(parents=True)
        transcript = projects_root / "session1.jsonl"
        transcript.write_text(assistant_line("slice-review", ts="2026-08-01T10:00:00.000Z", uuid="u1") + "\n")

        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--projects-root", str(pathlib.Path(tmp) / "projects")],
            capture_output=True,
            text=True,
            cwd=REPO,
        )
        out = result.stdout
        check("CLI exits 0 against a small fixture", result.returncode == 0)
        check("CLI output lists the invoked tracked skill with its count", "slice-review" in out and "1" in out)
        check("CLI output shows 'never' for a tracked skill with no invocations", "never" in out)


def main():
    test_discover_tracked_skills()
    test_parse_matching_invocation()
    test_ignores_untracked_skill()
    test_malformed_json_tolerance()
    test_duplicate_invocations_in_separate_records_count_separately()
    test_unused_skill_shows_zero()
    test_most_recent_timestamp_selection()
    test_missing_transcript_root()
    test_full_cli_output_against_fixture()

    if failures:
        print(f"\ntest-skill-usage-report: FAIL ({len(failures)} problem(s))")
        for name in failures:
            print(f"  - {name}")
        return 1
    print("\ntest-skill-usage-report: OK (all checks passed)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
