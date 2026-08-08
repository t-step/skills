#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Report which of this repo's skills (skills/*/SKILL.md) have actually
been invoked in local Claude Code sessions, how often, and how recently.

Scans ~/.claude/projects/**/*.jsonl transcripts fresh on every run — no
persistent state, no database. See
docs/superpowers/specs/2026-08-04-skill-usage-report-design.md for what
this proves and what it deliberately does not.

Run with `uv run scripts/skill-usage-report.py`.
"""

import argparse
import json
import pathlib
import re
import sys
from dataclasses import dataclass, field

REPO = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_PROJECTS_ROOT = pathlib.Path.home() / ".claude" / "projects"

# A user-typed `/skill-name` slash command is expanded by the harness into a
# `type: "user"` record whose message content is plain text containing this
# tag — no Skill tool_use block is ever produced for that invocation path, so
# it needs its own detection alongside the assistant tool_use path below.
COMMAND_NAME_RE = re.compile(r"<command-name>/([a-zA-Z0-9_-]+)</command-name>")


@dataclass
class SkillStats:
    total: int = 0
    last_used: str | None = None
    sessions: set = field(default_factory=set)
    projects: set = field(default_factory=set)


def discover_tracked_skills(repo_root: pathlib.Path) -> set[str]:
    """Skill names = directory names under skills/ containing a SKILL.md.

    check-skill-frontmatter.py already enforces name == directory name,
    so the directory name is a reliable, YAML-parse-free source of truth.
    """
    return {p.parent.name for p in repo_root.glob("skills/*/SKILL.md")}


def parse_skill_invocations(text: str, tracked_skills: set[str]):
    """Yield (skill_name, session_id, timestamp) for each tracked skill
    invocation found in this already-decoded transcript text, via either
    invocation path: the model calling the Skill tool, or the user typing a
    `/skill-name` slash command directly (which never produces a Skill
    tool_use block).

    Malformed lines and unexpected record shapes are skipped, not fatal.
    """
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(entry, dict):
            continue
        entry_type = entry.get("type")
        if entry_type not in ("assistant", "user"):
            continue
        message = entry.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        session_id = entry.get("sessionId") or entry.get("session_id") or ""
        ts = entry.get("timestamp") or ""

        if entry_type == "assistant":
            if not isinstance(content, list):
                continue
            for block in content:
                if not isinstance(block, dict):
                    continue
                if block.get("type") != "tool_use" or block.get("name") != "Skill":
                    continue
                inp = block.get("input")
                skill_name = inp.get("skill") if isinstance(inp, dict) else None
                if skill_name in tracked_skills:
                    yield skill_name, session_id, ts
            continue

        # entry_type == "user": look for a `/skill-name` slash-command tag.
        texts = []
        if isinstance(content, str):
            texts.append(content)
        elif isinstance(content, list):
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    texts.append(block.get("text") or "")
        for t in texts:
            for m in COMMAND_NAME_RE.finditer(t):
                skill_name = m.group(1)
                if skill_name in tracked_skills:
                    yield skill_name, session_id, ts


def scan_transcripts(projects_root: pathlib.Path, tracked_skills: set[str]) -> dict[str, SkillStats]:
    """Full stateless scan of every transcript under projects_root.

    A missing projects_root produces zeroed stats for every tracked skill
    rather than raising, so the report has a clean empty state.
    """
    stats = {name: SkillStats() for name in tracked_skills}
    if not projects_root.exists():
        return stats
    for transcript in sorted(projects_root.rglob("*.jsonl")):
        try:
            project_slug = transcript.relative_to(projects_root).parts[0]
        except ValueError:
            project_slug = transcript.parent.name
        try:
            text = transcript.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for skill_name, session_id, ts in parse_skill_invocations(text, tracked_skills):
            s = stats[skill_name]
            s.total += 1
            if session_id:
                s.sessions.add(session_id)
            s.projects.add(project_slug)
            if ts and (s.last_used is None or ts > s.last_used):
                s.last_used = ts
    return stats


def format_report(stats: dict[str, SkillStats], projects_root: pathlib.Path) -> str:
    lines = []
    if not projects_root.exists():
        lines.append(f"no transcript directory found at {projects_root} — nothing scanned\n")

    lines.append(f"{'skill':<28} {'total':>6} {'sessions':>9} {'projects':>9}  last invoked")
    for name in sorted(stats):
        s = stats[name]
        last = s.last_used if s.last_used else "never invoked"
        lines.append(f"{name:<28} {s.total:>6} {len(s.sessions):>9} {len(s.projects):>9}  {last}")
    return "\n".join(lines)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Report how often this repo's skills have been invoked in local Claude Code sessions."
    )
    parser.add_argument("--projects-root", type=pathlib.Path, default=DEFAULT_PROJECTS_ROOT)
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    tracked_skills = discover_tracked_skills(REPO)
    if not tracked_skills:
        print("skill-usage-report: no skills/*/SKILL.md found in this repo", file=sys.stderr)
        return 1

    stats = scan_transcripts(args.projects_root, tracked_skills)
    print(format_report(stats, args.projects_root))
    return 0


if __name__ == "__main__":
    sys.exit(main())
