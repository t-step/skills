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


def init_db(db_path: pathlib.Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS invocations (
            id INTEGER PRIMARY KEY,
            skill_name TEXT NOT NULL,
            session_id TEXT NOT NULL,
            cwd TEXT,
            project_slug TEXT NOT NULL,
            ts TEXT NOT NULL,
            source_uuid TEXT NOT NULL UNIQUE
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS scanned_files (
            path TEXT PRIMARY KEY,
            mtime REAL NOT NULL,
            byte_offset INTEGER NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def get_scan_state(conn: sqlite3.Connection, path: str) -> tuple[float, int]:
    row = conn.execute("SELECT mtime, byte_offset FROM scanned_files WHERE path = ?", (path,)).fetchone()
    return (row[0], row[1]) if row else (0.0, 0)


def set_scan_state(conn: sqlite3.Connection, path: str, mtime: float, byte_offset: int) -> None:
    conn.execute(
        """
        INSERT INTO scanned_files (path, mtime, byte_offset) VALUES (?, ?, ?)
        ON CONFLICT(path) DO UPDATE SET mtime = excluded.mtime, byte_offset = excluded.byte_offset
        """,
        (path, mtime, byte_offset),
    )
    conn.commit()


def parse_new_invocations(
    text: str, tracked_skills: set[str], project_slug: str
) -> tuple[list[InvocationRow], int]:
    parts = text.split("\n")
    leftover = parts[-1]
    complete_lines = parts[:-1]
    consumed_text = text[: len(text) - len(leftover)]
    consumed_bytes = len(consumed_text.encode("utf-8"))

    rows: list[InvocationRow] = []
    for line in complete_lines:
        if not line.strip():
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError as exc:
            print(f"skill-usage-report: skipping malformed line: {exc}", file=sys.stderr)
            continue
        if entry.get("type") != "assistant":
            continue
        content = entry.get("message", {}).get("content")
        if not isinstance(content, list):
            continue
        session_id = entry.get("sessionId") or entry.get("session_id") or ""
        cwd = entry.get("cwd")
        ts = entry.get("timestamp") or ""
        line_uuid = entry.get("uuid")
        for index, block in enumerate(content):
            if not isinstance(block, dict):
                continue
            if block.get("type") != "tool_use" or block.get("name") != "Skill":
                continue
            skill_name = block.get("input", {}).get("skill")
            if skill_name not in tracked_skills:
                continue
            rows.append(
                InvocationRow(
                    skill_name=skill_name,
                    session_id=session_id,
                    cwd=cwd,
                    project_slug=project_slug,
                    ts=ts,
                    source_uuid=f"{line_uuid}:{index}",
                )
            )
    return rows, consumed_bytes


def scan_transcript_file(
    path: pathlib.Path, tracked_skills: set[str], project_slug: str, start_offset: int
) -> tuple[list[InvocationRow], int]:
    with path.open("rb") as f:
        f.seek(start_offset)
        raw = f.read()
    text = raw.decode("utf-8", errors="replace")
    rows, consumed = parse_new_invocations(text, tracked_skills, project_slug)
    return rows, start_offset + consumed


def ingest(conn: sqlite3.Connection, projects_root: pathlib.Path, tracked_skills: set[str]) -> tuple[int, int]:
    """Scan every transcript under projects_root; insert new invocation rows.

    Returns (files_scanned, rows_inserted).
    """
    if not projects_root.exists():
        return (0, 0)
    before = conn.execute("SELECT COUNT(*) FROM invocations").fetchone()[0]
    files_scanned = 0
    for project_dir in sorted(p for p in projects_root.iterdir() if p.is_dir()):
        project_slug = project_dir.name
        for transcript in sorted(project_dir.glob("*.jsonl")):
            path_str = str(transcript)
            stat = transcript.stat()
            stored_mtime, stored_offset = get_scan_state(conn, path_str)
            abnormal = stat.st_size < stored_offset or stat.st_mtime < stored_mtime
            start_offset = 0 if abnormal else stored_offset
            rows, new_offset = scan_transcript_file(transcript, tracked_skills, project_slug, start_offset)
            for row in rows:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO invocations
                        (skill_name, session_id, cwd, project_slug, ts, source_uuid)
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (row.skill_name, row.session_id, row.cwd, row.project_slug, row.ts, row.source_uuid),
                )
            set_scan_state(conn, path_str, stat.st_mtime, new_offset)
            files_scanned += 1
    conn.commit()
    after = conn.execute("SELECT COUNT(*) FROM invocations").fetchone()[0]
    return files_scanned, after - before


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
    conn = init_db(args.db_path)
    files_scanned, rows_inserted = ingest(conn, args.projects_root, tracked_skills)
    print(f"scanned {files_scanned} transcript file(s), {rows_inserted} new invocation(s)")
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
