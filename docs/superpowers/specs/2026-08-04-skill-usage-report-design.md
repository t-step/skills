# Skill usage report — design

**Date:** 2026-08-04
**Status:** Approved (design), pre-implementation

## Problem

This repo's skills (`skills/*/SKILL.md`) are meant to be used from Claude Code sessions in other project directories, distributed via a personal `~/.claude/skills/` symlink. Once that's true, there's no visibility into whether it's working: which skills actually get invoked, how often, and — the case that matters most for maintenance — skills that quietly never fire, either because they're unneeded (archive candidates) or because their trigger description isn't matching real prompts (needs a description fix).

The goal is a quantitative usage signal that's cheap enough to check regularly, used to *triage* where to spend the more valuable qualitative effort (reading actual transcripts to judge whether a skill's output was good), not to replace it.

## Scope

- Tracks only skills defined in this repo (`skills/*/SKILL.md`), matched by name at run time — no hardcoded skill list.
- Single machine, single user. No OTel, no collector, no multi-machine aggregation. This was an explicit simplification: "local store... I am the only customer."
- Quantitative only. Missed-trigger detection is a manual-review digest (prompts + what fired), not an automated judge — chosen over an LLM-judge pass or keyword-overlap heuristic to avoid false-positive/negative noise and token cost at this stage. Can be revisited once volume data shows where attention is needed.
- Archiving is a flag in the report, never an automated action. The script never moves, deletes, or modifies skill files.

## Architecture

One script: `scripts/skill-usage-report.py`, a `uv run --script` single-file script (same convention as `scripts/check-skill-frontmatter.py`: PEP 723 inline dependency block, stdlib-only otherwise — `sqlite3` is stdlib so no new dependency).

Running it with no arguments does two phases in sequence:

### 1. Ingest

- Discover tracked skill names by reading `skills/*/SKILL.md` frontmatter (`name:` field) in this repo at run time. Adding a new skill directory makes it tracked automatically; no script changes needed.
- Glob `~/.claude/projects/*/*.jsonl` (every session transcript across every project on this machine).
- For each transcript file, look up its last-scanned position in the `scanned_files` table (keyed by path, storing `mtime` and `byte_offset`). If the file's `mtime` and size are unchanged since last scan, skip it entirely. Otherwise read only the bytes after `byte_offset`.
- Parse each new line as JSON. Skip lines that fail to parse (partial trailing line from a session still being written) — log a one-line warning to stderr, continue.
- For `assistant`-type entries, inspect `message.content` for blocks where `type == "tool_use"` and `name == "Skill"`. If `input.skill` matches a tracked skill name, insert a row into `invocations`. Uniqueness is enforced on the transcript line's `uuid`, so re-ingesting an already-seen file (or overlapping byte ranges) is a no-op rather than a duplicate.
- After processing a file, update its `scanned_files` row to the new `mtime`/`byte_offset`.

### 2. Report

- Query `invocations` grouped by `skill_name` for: total count, count within the last 30 days (a fixed constant for at-a-glance recency, independent of `--archive-window`), and most recent `ts` (or "never" if zero rows) — all from the DB, no transcript re-reading needed.
- Archive candidates: tracked skills with zero rows in `invocations` within `--archive-window` days (default 60).
- Recent-session digest: **not** sourced from the DB. Re-glob `~/.claude/projects/*/*.jsonl`, filter to files modified within `--digest-days` (default 7), parse `user`-type entries for prompt text and `assistant` Skill tool_use entries for what fired, and print them grouped by session (project `cwd`, timestamp, truncated prompts, skills fired or "none"). This is deliberately computed fresh each run rather than persisted (see Data model below for why).

## Data model

SQLite database at `~/.claude/skill-usage/store.db`, created on first run if the directory/file don't exist.

```sql
CREATE TABLE invocations (
  id           INTEGER PRIMARY KEY,
  skill_name   TEXT NOT NULL,
  session_id   TEXT NOT NULL,
  cwd          TEXT,               -- from the transcript line's "cwd"
  project_slug TEXT,               -- the ~/.claude/projects/<slug>/ directory name the transcript file lives under
  ts           TEXT NOT NULL,       -- ISO 8601, from the transcript line's "timestamp"
  source_uuid  TEXT NOT NULL UNIQUE -- the transcript line's "uuid"; dedup key
);

CREATE TABLE scanned_files (
  path        TEXT PRIMARY KEY,
  mtime       REAL NOT NULL,
  byte_offset INTEGER NOT NULL
);
```

**Deliberately no prompt text is persisted.** Only skill names and metadata (session id, cwd, timestamp) go into the long-term store. The recent-session digest, which needs actual prompt text, reads it live from transcripts that are still on disk — those are inherently recent (still within the digest window), so there's no need to duplicate that content into a second store. This keeps `store.db` small and free of cross-project conversation content, which matters since it aggregates data from every project on the machine, not just this repo.

## CLI

```
uv run scripts/skill-usage-report.py [--archive-window N] [--digest-days N] [--skill NAME] [--json]
```

- `--archive-window` (default 60): rolling-window size in days for the archive-candidate check.
- `--digest-days` (default 7): how far back the recent-session digest looks.
- `--skill NAME`: filter the volume table and digest to a single skill.
- `--json`: emit only the volume table and archive candidates as JSON instead of a formatted table (for future scripting). The digest is omitted entirely in JSON mode — not printed to stdout or stderr — since it's a manual-review aid meant for human reading, not machine consumption.

No subcommands. Ingest always runs before report — it's incremental and cheap, so there's nothing to remember to run separately.

## Error handling

- Malformed/partial JSON line → skip with a stderr warning, continue processing the rest of the file. Never fatal.
- `~/.claude/projects/` missing or no matching transcripts → report prints an explicit "no data" state for each section, not a crash or empty output.
- `~/.claude/skill-usage/` directory and `store.db` are created on first run if absent.
- A transcript file that shrinks or whose `mtime` predates the stored `scanned_files` row (e.g. a file replaced out from under us) is treated as changed and rescanned from byte 0; duplicate rows are prevented by the `source_uuid` unique constraint regardless.

## Out of scope / explicitly deferred

- OpenTelemetry export, collectors, or any multi-machine aggregation.
- Automated missed-trigger detection (LLM-judge or heuristic scoring) — the digest is manual-review only for now.
- Automatic archiving action (moving/deleting skill directories) — the report only flags candidates.
- Adding this script to `scripts/check.sh` — it's an on-demand report, not a correctness gate, so it stays outside the mandatory pre-commit/CI path described in `AGENTS.md`.

## Verification approach

No dedicated unit-test suite, consistent with the existing `scripts/check-*.py` scripts in this repo, which verify themselves against real repo/transcript state rather than fixtures. Verification before considering this done:

1. Run against real transcript history on this machine; manually cross-check a couple of the reported per-skill counts against `grep -c '"name":"Skill"' <file>` plus a `skill` field match, to confirm the parsing logic agrees with ground truth.
2. Run twice in a row; confirm the second run's report is identical to the first (ingest is idempotent, no double-counting).
3. Confirm behavior on a machine/directory state with zero prior transcripts (clean `~/.claude/skill-usage/`) produces the "no data" path cleanly rather than erroring.
