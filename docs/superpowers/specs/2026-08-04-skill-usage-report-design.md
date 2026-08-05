# Skill usage report — design (first slice)

**Date:** 2026-08-05 (rewritten; original design 2026-08-04)
**Status:** Implemented

## Problem

This repo's skills (`skills/*/SKILL.md`) are meant to be used from Claude Code sessions in other project directories, distributed via a personal `~/.claude/skills/` symlink. Once that's true, there's no visibility into whether it's working at all: which skills actually get invoked, how often, and how recently.

## What this slice proves

Running one local command answers exactly one question: **which of this repo's skills have actually been invoked in local Claude Code sessions, how often, and how recently?** That's a cheap, quantitative signal for deciding where to spend the more valuable qualitative effort — reading actual transcripts to judge whether a skill's output was any good.

## What this slice does not prove

- Whether a skill's output was correct or useful when it did fire.
- Whether a skill *should have* fired but didn't (a missed-trigger problem) — answering that would require extracting and semantically analyzing prompt text. This slice reads transcript files only to locate `Skill` tool invocations; it never extracts, retains, or analyzes prompt content.
- Usage across other machines — this is single-machine, single-user only.
- Whether a low-usage skill should be archived. Usage frequency is one maintenance signal among several; a rarely invoked skill may still be highly valuable. This tool reports counts and recency, nothing more — it never labels a skill an "archive candidate" or takes any action on skill files.

## Scope

- Tracks only skills defined in this repo (`skills/*/SKILL.md`), matched by name at run time — no hardcoded skill list.
- Single machine, single user, no aggregation.
- Quantitative counts and timestamps only. Transcript files are read locally, in memory, solely to locate `Skill` tool invocations — prompt text within them is never extracted, retained, displayed, persisted, analyzed, or transmitted. The tool performs no semantic analysis of prompts, and no prompt-derived information is written anywhere.
- The script never moves, deletes, or modifies skill files, and never takes any action based on the counts — it only prints them.

## Architecture

One script: `scripts/skill-usage-report.py`, a `uv run --script` single-file script (same convention as `scripts/check-skill-frontmatter.py`: PEP 723 inline dependency block, stdlib-only, no third-party dependencies).

```
discover skills (skills/*/SKILL.md)
    ↓
scan JSONL transcripts (~/.claude/projects/**/*.jsonl)
    ↓
aggregate in memory (per skill: total, sessions, projects, last invoked)
    ↓
print report
```

Every run does a **full, stateless scan** — no database, no byte-offset bookkeeping, no incremental ingest. Every `.jsonl` file under `~/.claude/projects/` is re-read and re-parsed on every invocation, including nested subagent transcripts (`rglob`, not a top-level-only `glob`).

Discovery: `discover_tracked_skills(repo_root)` returns the set of directory names under `skills/` that contain a `SKILL.md` — `check-skill-frontmatter.py` already enforces `name == directory name`, so the directory name is a reliable, YAML-parse-free source of truth.

Parsing: `parse_skill_invocations(text, tracked_skills)` inspects `assistant`-type transcript lines for `message.content` blocks where `type == "tool_use"` and `name == "Skill"`, yielding `(skill_name, session_id, timestamp)` for each block whose `input.skill` matches a tracked name. Malformed JSON lines and unexpected record shapes are skipped, never fatal.

Aggregation: `scan_transcripts(projects_root, tracked_skills)` walks every transcript, calls the parser on each, and accumulates per-skill totals, distinct session IDs, distinct project slugs (the first path component under `projects_root`), and the lexicographically-greatest timestamp seen (transcript timestamps are consistently formatted ISO 8601 with a fixed-width millisecond `Z` suffix, so string comparison correctly selects the most recent one without a parsing step).

## Why stateless is sufficient (measured, not assumed)

Measured on this machine (2026-08-05) against real transcript history:

- **483 files**, **167.5 MB** total, under `~/.claude/projects/**/*.jsonl`
- **~2.1–2.7 seconds** wall-clock for a full scan (via the standalone measurement script and via the actual CLI)
- **12** matching tracked-skill invocations found

A ~2-second full scan run on demand is well within "fast enough for one local command." There is no observed performance problem to justify persistent state, incremental byte-offset scanning, or a database. If usage or transcript volume grows enough that this stops being true, that's a concrete, measurable trigger to revisit — not something to build in advance of evidence.

## Error handling

- Malformed/partial JSON line → skipped silently, never fatal to the rest of the file.
- Unexpected record shapes (missing `message`, non-list `content`, non-dict blocks, etc.) → skipped.
- `~/.claude/projects/` missing → `scan_transcripts` returns zeroed stats for every tracked skill; the report prints an explicit "no transcript directory found" note instead of crashing or printing nothing.
- A tracked skill with zero invocations prints `never invoked`, not a blank or missing row.

## Terminology

Report output uses neutral language only: `total`, `last invoked` / `never invoked`, `sessions`, `projects`. Nothing in this tool is labeled an "archive candidate" — usage volume is one input to a maintenance decision, not a verdict.

## Verification

`scripts/test-skill-usage-report.py` — a stdlib-only, fixture-based script (no third-party test framework, consistent with the rest of `scripts/`) covering: tracked-skill discovery, matching invocation parsing, ignoring untracked skill names, malformed-JSON tolerance, duplicate invocations across separate transcript records counting separately, unused skills reporting zero, most-recent-timestamp selection among several, a missing transcript root, and full CLI output against a temporary fixture. Run with `python3 scripts/test-skill-usage-report.py`; wired into `scripts/check.sh` since it only touches synthetic fixtures (no dependency on real machine state), so it's cheap and safe to run on every check.

Additionally verified directly against this machine's real transcript history (see "Why stateless is sufficient" above) and confirmed idempotent — rerunning produces an identical report, since there is no state to drift.

## Out of scope / deferred

Deferred, not designed against, and not present as disabled scaffolding in the implementation — revisit only if real usage of this tool demonstrates a need:

- **Persistence** (SQLite, any store) and **incremental scanning** (byte offsets, mtime-based skip) — no observed performance problem to justify either; see measurement above.
- **Missed-trigger analysis**, automated or manual-digest — requires extracting and analyzing prompt text. This slice reads transcript files only to locate `Skill` tool invocations and never extracts, retains, or analyzes prompt content.
- **`--json` output, `--skill` filter** — no current consumer; add if/when something needs to script against this.
- **Archive-candidate classification or any archival action** — usage counts inform a human decision; this tool doesn't make one.
- **Multi-machine aggregation, OpenTelemetry/collectors** — single-machine local tool only.
