# Skill Usage Report Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build `scripts/skill-usage-report.py`, a local, SQLite-backed CLI that reports how often this repo's skills get invoked across Claude Code sessions on this machine, to guide where to focus development effort.

**Architecture:** One `uv run --script` single-file Python script (stdlib only). Each run does two phases: incrementally scan `~/.claude/projects/*/*.jsonl` for `Skill` tool invocations naming this repo's skills and persist them to a local SQLite DB, then print a report (per-skill volume, archive candidates, and a manual-review digest of recent sessions).

**Tech Stack:** Python 3.11+, stdlib only (`sqlite3`, `json`, `argparse`, `pathlib`, `dataclasses`, `datetime`).

## Global Constraints

- Design source of truth: `docs/superpowers/specs/2026-08-04-skill-usage-report-design.md`. Every requirement below traces to it.
- Local-only: no OpenTelemetry, no collector, no network calls, no multi-machine aggregation.
- Persistent store (`~/.claude/skill-usage/store.db`) holds only skill names + metadata (session id, cwd, project slug, timestamp) — **never** full prompt/conversation text.
- The report only ever flags archive candidates; it never moves, deletes, or modifies skill files.
- Tracked skill names come from `skills/*/SKILL.md` directory names in this repo, read fresh at run time — no hardcoded list. (`check-skill-frontmatter.py` already enforces `name` == directory name, so the directory name is a reliable source of truth without parsing YAML.)
- Not added to `scripts/check.sh` — this is an on-demand report, not a correctness gate.
- Follow existing `scripts/check-*.py` conventions: `#!/usr/bin/env -S uv run --script` + PEP 723 header, `REPO = pathlib.Path(__file__).resolve().parent.parent`, plain `print`-based output.
- No pytest / dedicated test suite (matches the spec's verification approach and the existing `scripts/check-*.py` scripts, which have none). Each task instead verifies against ephemeral fixtures created in `/tmp` at verification time, using `runpy.run_path(..., run_name="test")` to call functions directly without needing the hyphenated filename to be importable.

---

## File Structure

Single file, built incrementally: `scripts/skill-usage-report.py`. No other files are created or modified.

## Task 1: Scaffold, CLI args, tracked-skill discovery

**Files:**
- Create: `scripts/skill-usage-report.py`

**Interfaces:**
- Produces: `discover_tracked_skills(repo_root: pathlib.Path) -> set[str]`; `build_arg_parser() -> argparse.ArgumentParser` with flags `--projects-root` (Path, default `~/.claude/projects`), `--db-path` (Path, default `~/.claude/skill-usage/store.db`), `--archive-window` (int, default 60), `--digest-days` (int, default 7), `--skill` (str, default `None`), `--json` (flag); dataclasses `InvocationRow`, `VolumeStats`, `SessionDigestEntry` (fields fixed now so later tasks don't redefine them — see below).

- [ ] **Step 1: Write the script**

```python
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
```

- [ ] **Step 2: Make it executable and run it**

```bash
chmod +x scripts/skill-usage-report.py
uv run scripts/skill-usage-report.py
```

Expected stdout (exact — matches the 8 skill directories currently under `skills/`):

```
tracked skills:
  - create-session-handoff
  - investigate-tradeoff
  - next-best-slice
  - repo-orientation
  - retrieve-prior-work
  - slice-plan
  - slice-retro
  - slice-review
```

If the skill list in the repo has changed since this plan was written, the output should match whatever `skills/*/SKILL.md` currently contains — the point of this check is that the printed set matches `ls skills/`, not the literal list above.

- [ ] **Step 3: Commit**

```bash
git add scripts/skill-usage-report.py
git commit -m "feat(scripts): scaffold skill-usage-report with tracked-skill discovery"
```

## Task 2: SQLite schema + scan-state helpers

**Files:**
- Modify: `scripts/skill-usage-report.py`

**Interfaces:**
- Consumes: `REPO`, `DEFAULT_DB_PATH` from Task 1.
- Produces: `init_db(db_path: pathlib.Path) -> sqlite3.Connection`; `get_scan_state(conn: sqlite3.Connection, path: str) -> tuple[float, int]` (returns `(0.0, 0)` if unseen); `set_scan_state(conn: sqlite3.Connection, path: str, mtime: float, byte_offset: int) -> None`.

- [ ] **Step 1: Write a verification script targeting functions that don't exist yet**

```bash
cat > /tmp/skill-usage-t2.py <<'PYEOF'
import runpy, pathlib, tempfile

mod = runpy.run_path("scripts/skill-usage-report.py", run_name="test")

with tempfile.TemporaryDirectory() as tmp:
    db_path = pathlib.Path(tmp) / "store.db"
    conn = mod["init_db"](db_path)
    assert mod["get_scan_state"](conn, "foo.jsonl") == (0.0, 0)
    mod["set_scan_state"](conn, "foo.jsonl", 123.5, 456)
    assert mod["get_scan_state"](conn, "foo.jsonl") == (123.5, 456)
    mod["set_scan_state"](conn, "foo.jsonl", 789.0, 999)
    assert mod["get_scan_state"](conn, "foo.jsonl") == (789.0, 999), "upsert should overwrite, not duplicate"

    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    assert tables == {"invocations", "scanned_files"}, tables

    # re-init against the same path must not raise (CREATE TABLE IF NOT EXISTS)
    mod["init_db"](db_path)

print("OK: init_db + scan_state round-trip")
PYEOF
python3 /tmp/skill-usage-t2.py
```

Expected: `KeyError: 'init_db'` (the function doesn't exist yet).

- [ ] **Step 2: Add the schema and scan-state functions**

Insert after `discover_tracked_skills` in `scripts/skill-usage-report.py`:

```python
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
```

Also update `main()` to initialize the DB (insert before `return 0`):

```python
    conn = init_db(args.db_path)
    print(f"database ready at {args.db_path}")
    conn.close()
```

- [ ] **Step 3: Re-run verification**

```bash
python3 /tmp/skill-usage-t2.py
```

Expected: `OK: init_db + scan_state round-trip`

Also confirm the CLI wiring:

```bash
uv run scripts/skill-usage-report.py --db-path /tmp/skill-usage-t2.db
sqlite3 /tmp/skill-usage-t2.db ".tables"
```

Expected: the CLI prints `database ready at /tmp/skill-usage-t2.db`, and `.tables` lists `invocations` and `scanned_files`.

- [ ] **Step 4: Commit**

```bash
rm -f /tmp/skill-usage-t2.py /tmp/skill-usage-t2.db
git add scripts/skill-usage-report.py
git commit -m "feat(scripts): add SQLite schema and scan-state helpers"
```

## Task 3: Transcript line parser (pure function)

**Files:**
- Modify: `scripts/skill-usage-report.py`

**Interfaces:**
- Consumes: `InvocationRow` from Task 1.
- Produces: `parse_new_invocations(text: str, tracked_skills: set[str], project_slug: str) -> tuple[list[InvocationRow], int]`. `text` is already-decoded transcript content (may end mid-line); returns the matched rows plus the number of UTF-8 bytes consumed through the last complete (newline-terminated) line — a trailing partial line is left unconsumed.

- [ ] **Step 1: Write a verification script targeting the function**

```bash
cat > /tmp/skill-usage-t3.py <<'PYEOF'
import runpy

mod = runpy.run_path("scripts/skill-usage-report.py", run_name="test")

line1 = '{"type":"assistant","sessionId":"sess-1","cwd":"/tmp/proj","timestamp":"2026-08-01T10:00:00.000Z","uuid":"uuid-1","message":{"content":[{"type":"tool_use","name":"Skill","input":{"skill":"slice-review","args":"go"}}]}}\n'
line2 = '{"type":"assistant","sessionId":"sess-1","cwd":"/tmp/proj","timestamp":"2026-08-01T10:05:00.000Z","uuid":"uuid-2","message":{"content":[{"type":"tool_use","name":"Skill","input":{"skill":"update-config"}}]}}\n'
line3 = '{"type":"user","sessionId":"sess-1","cwd":"/tmp/proj","timestamp":"2026-08-01T10:06:00.000Z","uuid":"uuid-3","message":{"content":"please review this"}}\n'
line4 = '{"type":"assistant", not valid json\n'
line5_partial = '{"type":"assistant","sessionId":"sess-1"'  # no trailing newline: incomplete

complete_text = line1 + line2 + line3 + line4
text = complete_text + line5_partial

rows, consumed = mod["parse_new_invocations"](text, {"slice-review"}, "test-project")

assert consumed == len(complete_text.encode("utf-8")), (consumed, len(complete_text.encode("utf-8")))
assert len(rows) == 1, rows
row = rows[0]
assert row.skill_name == "slice-review", row
assert row.session_id == "sess-1", row
assert row.cwd == "/tmp/proj", row
assert row.project_slug == "test-project", row
assert row.ts == "2026-08-01T10:00:00.000Z", row
assert row.source_uuid == "uuid-1:0", row

print("OK: parse_new_invocations")
PYEOF
python3 /tmp/skill-usage-t3.py
```

Expected: `KeyError: 'parse_new_invocations'` (doesn't exist yet).

This fixture exercises: a tracked-skill match (row produced), an untracked-skill match (`update-config`, filtered out), a `user`-type line (ignored), a malformed line (skipped with a warning, not fatal), and a trailing partial line (excluded from both output and the consumed-byte count).

- [ ] **Step 2: Add the parser**

Insert after `set_scan_state`:

```python
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
```

- [ ] **Step 3: Re-run verification**

```bash
python3 /tmp/skill-usage-t3.py
```

Expected: a `skill-usage-report: skipping malformed line: ...` warning on stderr (from `line4`), then `OK: parse_new_invocations` on stdout.

- [ ] **Step 4: Commit**

```bash
rm -f /tmp/skill-usage-t3.py
git add scripts/skill-usage-report.py
git commit -m "feat(scripts): add transcript line parser for Skill invocations"
```

## Task 4: Incremental file scanning + ingest

**Files:**
- Modify: `scripts/skill-usage-report.py`

**Interfaces:**
- Consumes: `parse_new_invocations` (Task 3), `get_scan_state`/`set_scan_state`/`init_db` (Task 2).
- Produces: `scan_transcript_file(path: pathlib.Path, tracked_skills: set[str], project_slug: str, start_offset: int) -> tuple[list[InvocationRow], int]` (returns rows plus the new absolute byte offset); `ingest(conn: sqlite3.Connection, projects_root: pathlib.Path, tracked_skills: set[str]) -> tuple[int, int]` (returns `(files_scanned, rows_inserted)`).

- [ ] **Step 1: Build a fixture and verify `ingest` doesn't exist yet**

```bash
mkdir -p /tmp/skill-usage-t4/projects/proj-a
cat > /tmp/skill-usage-t4/projects/proj-a/session1.jsonl <<'EOF'
{"type":"assistant","sessionId":"session1","cwd":"/tmp/proj-a","timestamp":"2026-08-01T10:00:00.000Z","uuid":"uuid-a1","message":{"content":[{"type":"tool_use","name":"Skill","input":{"skill":"slice-review","args":"go"}}]}}
{"type":"user","sessionId":"session1","cwd":"/tmp/proj-a","timestamp":"2026-08-01T09:59:00.000Z","uuid":"uuid-a0","message":{"content":"please review"}}
EOF

uv run scripts/skill-usage-report.py --projects-root /tmp/skill-usage-t4/projects --db-path /tmp/skill-usage-t4/store.db
```

Expected: the current script (Tasks 1-3) only prints `tracked skills:` and `database ready at ...` — it doesn't scan transcripts yet, so there's no ingest summary line. This confirms the behavior doesn't exist yet.

- [ ] **Step 2: Add `scan_transcript_file` and `ingest`**

Insert after `parse_new_invocations`:

```python
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
            unchanged = stat.st_mtime == stored_mtime and stat.st_size >= stored_offset
            start_offset = stored_offset if unchanged else 0
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
```

`stat.st_size >= stored_offset` catches a file that shrank or was replaced out from under us (per the spec's error-handling note) — such a file is rescanned from byte 0 rather than seeking past its own end. Duplicate rows are prevented by the `source_uuid` unique constraint regardless.

Update `main()` — replace the `conn = init_db(...)` block with:

```python
    conn = init_db(args.db_path)
    files_scanned, rows_inserted = ingest(conn, args.projects_root, tracked_skills)
    print(f"scanned {files_scanned} transcript file(s), {rows_inserted} new invocation(s)")
    conn.close()
```

- [ ] **Step 3: Re-run against the fixture, twice**

```bash
uv run scripts/skill-usage-report.py --projects-root /tmp/skill-usage-t4/projects --db-path /tmp/skill-usage-t4/store.db
```

Expected: includes `scanned 1 transcript file(s), 1 new invocation(s)`.

```bash
uv run scripts/skill-usage-report.py --projects-root /tmp/skill-usage-t4/projects --db-path /tmp/skill-usage-t4/store.db
```

Expected (idempotency — same command, run again): `scanned 1 transcript file(s), 0 new invocation(s)`.

```bash
sqlite3 /tmp/skill-usage-t4/store.db "SELECT skill_name, session_id, project_slug, ts FROM invocations;"
```

Expected: exactly one row: `slice-review|session1|proj-a|2026-08-01T10:00:00.000Z`

- [ ] **Step 4: Commit**

```bash
git add scripts/skill-usage-report.py
git commit -m "feat(scripts): add incremental transcript scanning and ingest"
```

(Leave `/tmp/skill-usage-t4/` in place — Tasks 5-7 reuse this fixture.)

## Task 5: Volume table + archive candidates

**Files:**
- Modify: `scripts/skill-usage-report.py`

**Interfaces:**
- Consumes: `VolumeStats` (Task 1), the `invocations` table (Task 2/4).
- Produces: `compute_volume_table(conn: sqlite3.Connection, tracked_skills: set[str], now: datetime, recent_window_days: int = RECENT_WINDOW_DAYS) -> dict[str, VolumeStats]`; `archive_candidates(volume: dict[str, VolumeStats], now: datetime, archive_window_days: int) -> list[str]`.

- [ ] **Step 1: Write a verification script with a fixed `now` and hand-inserted rows**

```bash
cat > /tmp/skill-usage-t5.py <<'PYEOF'
import runpy, pathlib, tempfile
from datetime import datetime, timezone

mod = runpy.run_path("scripts/skill-usage-report.py", run_name="test")

with tempfile.TemporaryDirectory() as tmp:
    db_path = pathlib.Path(tmp) / "store.db"
    conn = mod["init_db"](db_path)
    tracked = {"slice-review", "slice-plan"}
    rows = [
        ("slice-review", "s1", "/p", "proj", "2026-07-30T10:00:00.000Z", "u1"),  # 5 days before "now"
        ("slice-review", "s2", "/p", "proj", "2026-05-06T10:00:00.000Z", "u2"),  # 90 days before "now"
        ("slice-plan", "s3", "/p", "proj", "2026-05-06T10:00:00.000Z", "u3"),    # 90 days before "now"
    ]
    for r in rows:
        conn.execute(
            "INSERT INTO invocations (skill_name, session_id, cwd, project_slug, ts, source_uuid) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            r,
        )
    conn.commit()

    now = datetime(2026, 8, 4, tzinfo=timezone.utc)
    volume = mod["compute_volume_table"](conn, tracked, now)

    assert volume["slice-review"].total == 2, volume["slice-review"]
    assert volume["slice-review"].recent_count == 1, volume["slice-review"]
    assert volume["slice-review"].last_used == datetime(2026, 7, 30, 10, 0, tzinfo=timezone.utc)

    assert volume["slice-plan"].total == 1, volume["slice-plan"]
    assert volume["slice-plan"].recent_count == 0, volume["slice-plan"]

    candidates = mod["archive_candidates"](volume, now, 60)
    assert candidates == ["slice-plan"], candidates

print("OK: compute_volume_table + archive_candidates")
PYEOF
python3 /tmp/skill-usage-t5.py
```

Expected: `KeyError: 'compute_volume_table'` (doesn't exist yet).

- [ ] **Step 2: Add the report functions**

Insert after `ingest`:

```python
def compute_volume_table(
    conn: sqlite3.Connection,
    tracked_skills: set[str],
    now: datetime,
    recent_window_days: int = RECENT_WINDOW_DAYS,
) -> dict[str, VolumeStats]:
    cutoff = now - timedelta(days=recent_window_days)
    totals = {name: 0 for name in tracked_skills}
    recents = {name: 0 for name in tracked_skills}
    last_used: dict[str, datetime | None] = {name: None for name in tracked_skills}
    for skill_name, ts in conn.execute("SELECT skill_name, ts FROM invocations"):
        if skill_name not in tracked_skills:
            continue
        try:
            when = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        except ValueError:
            continue
        totals[skill_name] += 1
        if when >= cutoff:
            recents[skill_name] += 1
        if last_used[skill_name] is None or when > last_used[skill_name]:
            last_used[skill_name] = when
    return {
        name: VolumeStats(
            skill_name=name, total=totals[name], recent_count=recents[name], last_used=last_used[name]
        )
        for name in sorted(tracked_skills)
    }


def archive_candidates(volume: dict[str, VolumeStats], now: datetime, archive_window_days: int) -> list[str]:
    cutoff = now - timedelta(days=archive_window_days)
    return sorted(
        name for name, stats in volume.items() if stats.last_used is None or stats.last_used < cutoff
    )
```

Update `main()` — replace `conn.close()` (from Task 4) with:

```python
    now = datetime.now(timezone.utc)
    volume = compute_volume_table(conn, tracked_skills, now)
    candidates = archive_candidates(volume, now, args.archive_window)
    conn.close()

    print(f"\n{'skill':<28} {'total':>6} {'30d':>6}  last used")
    for stats in volume.values():
        last = stats.last_used.date().isoformat() if stats.last_used else "never"
        print(f"{stats.skill_name:<28} {stats.total:>6} {stats.recent_count:>6}  {last}")

    print(f"\narchive candidates (no use in {args.archive_window}d):")
    if candidates:
        for name in candidates:
            print(f"  - {name}")
    else:
        print("  (none)")
```

- [ ] **Step 3: Re-run verification**

```bash
python3 /tmp/skill-usage-t5.py
```

Expected: `OK: compute_volume_table + archive_candidates`

Smoke-test the CLI against the Task 4 fixture (exact counts aren't asserted here since they depend on wall-clock "now"; just confirm the new sections render):

```bash
uv run scripts/skill-usage-report.py --projects-root /tmp/skill-usage-t4/projects --db-path /tmp/skill-usage-t4/store.db --archive-window 60 | grep -E "skill|archive candidates"
```

Expected: both a table header line and an `archive candidates (no use in 60d):` line appear.

- [ ] **Step 4: Commit**

```bash
rm -f /tmp/skill-usage-t5.py
git add scripts/skill-usage-report.py
git commit -m "feat(scripts): add volume table and archive-candidate report"
```

## Task 6: Recent-session digest

**Files:**
- Modify: `scripts/skill-usage-report.py`

**Interfaces:**
- Consumes: `SessionDigestEntry` (Task 1).
- Produces: `build_digest(projects_root: pathlib.Path, now: datetime, digest_days: int = DEFAULT_DIGEST_DAYS, prompt_truncate: int = 200) -> list[SessionDigestEntry]`, sorted oldest-to-newest by file mtime. Does not touch the DB — reads transcripts directly, deliberately (see spec: no long-term prompt storage).

- [ ] **Step 1: Write a verification script with a recent and an artificially old file**

```bash
cat > /tmp/skill-usage-t6.py <<'PYEOF'
import runpy, pathlib, tempfile, os, time
from datetime import datetime, timezone

mod = runpy.run_path("scripts/skill-usage-report.py", run_name="test")

with tempfile.TemporaryDirectory() as tmp:
    root = pathlib.Path(tmp) / "projects" / "proj-a"
    root.mkdir(parents=True)

    recent = root / "recent.jsonl"
    recent.write_text(
        '{"type":"user","cwd":"/p","message":{"content":"do the thing"}}\n'
        '{"type":"assistant","message":{"content":[{"type":"tool_use","name":"Skill","input":{"skill":"slice-review"}}]}}\n'
    )

    old = root / "old.jsonl"
    old.write_text('{"type":"user","cwd":"/p","message":{"content":"old prompt"}}\n')
    old_time = time.time() - 30 * 86400
    os.utime(old, (old_time, old_time))

    now = datetime.now(timezone.utc)
    digest = mod["build_digest"](pathlib.Path(tmp) / "projects", now, digest_days=7)

    assert len(digest) == 1, digest
    entry = digest[0]
    assert entry.session_id == "recent", entry
    assert entry.prompts == ["do the thing"], entry
    assert entry.skills_fired == ["slice-review"], entry

print("OK: build_digest filters by mtime and extracts prompts/skills")
PYEOF
python3 /tmp/skill-usage-t6.py
```

Expected: `KeyError: 'build_digest'` (doesn't exist yet).

- [ ] **Step 2: Add `build_digest`**

Insert after `archive_candidates`:

```python
def build_digest(
    projects_root: pathlib.Path,
    now: datetime,
    digest_days: int = DEFAULT_DIGEST_DAYS,
    prompt_truncate: int = 200,
) -> list[SessionDigestEntry]:
    if not projects_root.exists():
        return []
    cutoff = now - timedelta(days=digest_days)
    scored: list[tuple[datetime, SessionDigestEntry]] = []
    for project_dir in sorted(p for p in projects_root.iterdir() if p.is_dir()):
        project_slug = project_dir.name
        for transcript in sorted(project_dir.glob("*.jsonl")):
            stat = transcript.stat()
            mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
            if mtime < cutoff:
                continue
            prompts: list[str] = []
            skills_fired: list[str] = []
            cwd: str | None = None
            for line in transcript.read_text(encoding="utf-8", errors="replace").splitlines():
                if not line.strip():
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                cwd = entry.get("cwd") or cwd
                entry_type = entry.get("type")
                content = entry.get("message", {}).get("content")
                if entry_type == "user":
                    if isinstance(content, str):
                        prompts.append(content[:prompt_truncate])
                    elif isinstance(content, list):
                        for block in content:
                            if isinstance(block, dict) and block.get("type") == "text":
                                prompts.append(block.get("text", "")[:prompt_truncate])
                elif entry_type == "assistant" and isinstance(content, list):
                    for block in content:
                        if (
                            isinstance(block, dict)
                            and block.get("type") == "tool_use"
                            and block.get("name") == "Skill"
                        ):
                            skill_name = block.get("input", {}).get("skill")
                            if skill_name:
                                skills_fired.append(skill_name)
            if prompts:
                scored.append(
                    (
                        mtime,
                        SessionDigestEntry(
                            session_id=transcript.stem,
                            project_slug=project_slug,
                            cwd=cwd,
                            prompts=prompts,
                            skills_fired=skills_fired,
                        ),
                    )
                )
    scored.sort(key=lambda pair: pair[0])
    return [entry for _, entry in scored]
```

Update `main()` — after the archive-candidates block, add:

```python
    digest = build_digest(args.projects_root, now, args.digest_days)
    print(f"\nrecent sessions (last {args.digest_days}d):")
    if not digest:
        print("  (none)")
    for entry in digest:
        fired = ", ".join(entry.skills_fired) if entry.skills_fired else "none"
        print(f"\n  session {entry.session_id}  [{entry.project_slug}]  cwd={entry.cwd}")
        print(f"    skills fired: {fired}")
        for prompt in entry.prompts:
            print(f"    > {prompt}")
```

- [ ] **Step 3: Re-run verification**

```bash
python3 /tmp/skill-usage-t6.py
```

Expected: `OK: build_digest filters by mtime and extracts prompts/skills`

```bash
uv run scripts/skill-usage-report.py --projects-root /tmp/skill-usage-t4/projects --db-path /tmp/skill-usage-t4/store.db --digest-days 7
```

Expected: a `recent sessions (last 7d):` section listing `session session1` with `skills fired: slice-review` and the prompt `> please review`.

- [ ] **Step 4: Commit**

```bash
rm -f /tmp/skill-usage-t6.py
git add scripts/skill-usage-report.py
git commit -m "feat(scripts): add recent-session digest for manual missed-trigger review"
```

## Task 7: --skill filter, --json output, end-to-end verification

**Files:**
- Modify: `scripts/skill-usage-report.py`

**Interfaces:**
- Consumes: everything from Tasks 1-6.
- Produces: no new functions — wires `args.skill` and `args.json` into `main()`'s existing output.

- [ ] **Step 1: Confirm current behavior ignores `--skill` and `--json`**

```bash
uv run scripts/skill-usage-report.py --projects-root /tmp/skill-usage-t4/projects --db-path /tmp/skill-usage-t4/store.db --skill slice-review --json
```

Expected: prints the full human-readable report for all skills (the flags exist on the parser from Task 1 but `main()` doesn't act on them yet) — confirms the gap this task closes.

- [ ] **Step 2: Wire the flags into `main()`**

Replace the full body of `main()` with:

```python
def main() -> int:
    args = build_arg_parser().parse_args()
    tracked_skills = discover_tracked_skills(REPO)
    if not tracked_skills:
        print("skill-usage-report: no skills/*/SKILL.md found in this repo", file=sys.stderr)
        return 1

    conn = init_db(args.db_path)
    files_scanned, rows_inserted = ingest(conn, args.projects_root, tracked_skills)

    now = datetime.now(timezone.utc)
    volume = compute_volume_table(conn, tracked_skills, now)
    candidates = archive_candidates(volume, now, args.archive_window)
    conn.close()

    digest = build_digest(args.projects_root, now, args.digest_days)

    if args.skill:
        volume = {args.skill: volume[args.skill]} if args.skill in volume else {}
        digest = [e for e in digest if args.skill in e.skills_fired]

    if args.json:
        payload = {
            "volume": [
                {
                    "skill_name": s.skill_name,
                    "total": s.total,
                    "recent_30d": s.recent_count,
                    "last_used": s.last_used.isoformat() if s.last_used else None,
                }
                for s in volume.values()
            ],
            "archive_candidates": candidates,
        }
        print(json.dumps(payload, indent=2))
        return 0

    print(f"skill-usage-report: scanned {files_scanned} transcript file(s), {rows_inserted} new invocation(s)")

    print(f"\n{'skill':<28} {'total':>6} {'30d':>6}  last used")
    if not volume:
        print("  (no matching tracked skills)")
    for stats in volume.values():
        last = stats.last_used.date().isoformat() if stats.last_used else "never"
        print(f"{stats.skill_name:<28} {stats.total:>6} {stats.recent_count:>6}  {last}")

    print(f"\narchive candidates (no use in {args.archive_window}d):")
    if candidates:
        for name in candidates:
            print(f"  - {name}")
    else:
        print("  (none)")

    print(f"\nrecent sessions (last {args.digest_days}d):")
    if not digest:
        print("  (none)")
    for entry in digest:
        fired = ", ".join(entry.skills_fired) if entry.skills_fired else "none"
        print(f"\n  session {entry.session_id}  [{entry.project_slug}]  cwd={entry.cwd}")
        print(f"    skills fired: {fired}")
        for prompt in entry.prompts:
            print(f"    > {prompt}")

    return 0
```

- [ ] **Step 3: Verify `--skill` and `--json`**

```bash
uv run scripts/skill-usage-report.py --projects-root /tmp/skill-usage-t4/projects --db-path /tmp/skill-usage-t4/store.db --skill slice-review --json
```

Expected: valid JSON with exactly one entry under `"volume"` (`"skill_name": "slice-review"`). Confirm it parses:

```bash
uv run scripts/skill-usage-report.py --projects-root /tmp/skill-usage-t4/projects --db-path /tmp/skill-usage-t4/store.db --json | python3 -c "import json,sys; d=json.load(sys.stdin); assert 'volume' in d and 'archive_candidates' in d; print('OK: valid JSON output')"
```

```bash
uv run scripts/skill-usage-report.py --projects-root /tmp/skill-usage-t4/projects --db-path /tmp/skill-usage-t4/store.db --skill slice-plan
```

Expected: the volume table shows `(no matching tracked skills)` (fixture only ever invoked `slice-review`), and the digest section shows `(none)`.

- [ ] **Step 4: Verify the clean-state path**

```bash
uv run scripts/skill-usage-report.py --projects-root /tmp/skill-usage-empty --db-path /tmp/skill-usage-empty-db/store.db
```

Expected: exit code 0; `scanned 0 transcript file(s), 0 new invocation(s)`; every tracked skill shows `never`; `archive candidates` lists every tracked skill (never used); `recent sessions` shows `(none)`.

- [ ] **Step 5: Run once against real data as a final smoke test**

```bash
uv run scripts/skill-usage-report.py
```

Expected: exit code 0, and a real report against this machine's actual `~/.claude/projects` history (exact counts aren't asserted — this just confirms the tool runs cleanly against real, non-fixture data of unknown shape).

- [ ] **Step 6: Clean up fixtures and commit**

```bash
rm -rf /tmp/skill-usage-t4 /tmp/skill-usage-empty /tmp/skill-usage-empty-db
git add scripts/skill-usage-report.py
git commit -m "feat(scripts): wire --skill filter and --json output into skill-usage-report"
```

---

## Post-plan note

Not part of any task, but worth doing once this is in regular use: after a few weeks of real data, revisit whether the manual-review digest is enough or whether an automated missed-trigger pass (LLM-judge or heuristic) earns its cost — the spec deferred that deliberately, pending real volume data.
