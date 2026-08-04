#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Report how often this repo's skills (skills/*/SKILL.md) get invoked
across Claude Code sessions on this machine, to guide where to focus
development effort: usage volume per skill, skills that have gone quiet
long enough to be archive candidates, and a digest of recent sessions
for manually spotting cases where a skill should have fired but didn't.

Run with `uv run scripts/skill-usage-report.py`. State persists in a
local SQLite database (default ~/.claude/skill-usage/store.db); no full
prompt text is ever stored long-term — see
docs/superpowers/specs/2026-08-04-skill-usage-report-design.md.
"""

import argparse
import json
import pathlib
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

REPO = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_PROJECTS_ROOT = pathlib.Path.home() / ".claude" / "projects"
DEFAULT_DB_PATH = pathlib.Path.home() / ".claude" / "skill-usage" / "store.db"
DEFAULT_ARCHIVE_WINDOW_DAYS = 60
DEFAULT_DIGEST_DAYS = 7
RECENT_WINDOW_DAYS = 30


@dataclass(frozen=True)
class InvocationRow:
    skill_name: str
    session_id: str
    cwd: str | None
    project_slug: str
    ts: str
    source_uuid: str


@dataclass(frozen=True)
class VolumeStats:
    skill_name: str
    total: int
    recent_count: int
    last_used: datetime | None


@dataclass(frozen=True)
class SessionDigestEntry:
    session_id: str
    project_slug: str
    cwd: str | None
    prompts: list[str]
    skills_fired: list[str]


def discover_tracked_skills(repo_root: pathlib.Path) -> set[str]:
    """Skill names = directory names under skills/ containing a SKILL.md.

    check-skill-frontmatter.py already enforces name == directory name,
    so the directory name is a reliable, YAML-parse-free source of truth.
    """
    return {p.parent.name for p in repo_root.glob("skills/*/SKILL.md")}


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Report on how often this repo's skills get invoked.")
    parser.add_argument("--projects-root", type=pathlib.Path, default=DEFAULT_PROJECTS_ROOT)
    parser.add_argument("--db-path", type=pathlib.Path, default=DEFAULT_DB_PATH)
    parser.add_argument("--archive-window", type=int, default=DEFAULT_ARCHIVE_WINDOW_DAYS)
    parser.add_argument("--digest-days", type=int, default=DEFAULT_DIGEST_DAYS)
    parser.add_argument("--skill", type=str, default=None)
    parser.add_argument("--json", action="store_true")
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    tracked_skills = discover_tracked_skills(REPO)
    if not tracked_skills:
        print("skill-usage-report: no skills/*/SKILL.md found in this repo", file=sys.stderr)
        return 1
    print("tracked skills:")
    for name in sorted(tracked_skills):
        print(f"  - {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
