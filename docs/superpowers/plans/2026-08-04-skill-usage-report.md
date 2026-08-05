# Skill Usage Report — implementation note (first slice)

**Status:** Implemented. This replaces the earlier 7-task, SQLite-backed plan (2026-08-04) with a note matching what actually got built after descoping to a first slice — see `docs/superpowers/specs/2026-08-04-skill-usage-report-design.md` for the full design and the measured evidence behind the scope decision.

## What was built

`scripts/skill-usage-report.py` — one stateless, stdlib-only script. Each run:

1. Discovers tracked skills from `skills/*/SKILL.md` directory names.
2. Scans every `~/.claude/projects/**/*.jsonl` transcript from scratch (`rglob`, including nested subagent transcripts).
3. Parses `assistant`-type lines for `Skill` tool invocations naming a tracked skill.
4. Aggregates per skill: total count, distinct sessions, distinct projects, most recent invocation timestamp.
5. Prints a table; a tracked skill with zero invocations shows `never invoked`.

No SQLite, no byte-offset tracking, no incremental scan state, no `--json`/`--skill` flags, no archive-candidate labeling, no prompt extraction, no missed-trigger digest. A real full-scan measurement (483 files, 167.5 MB, ~2.1–2.7s) showed no performance problem to justify any of that — see the design doc's "Why stateless is sufficient" section.

## Verification

`scripts/test-skill-usage-report.py`, run via `python3 scripts/test-skill-usage-report.py` and wired into `scripts/check.sh`. Covers discovery, parsing (matching/ignored/malformed), duplicate-record counting, zero-count display, most-recent-timestamp selection, a missing transcript root, and full CLI output against a fixture.

## Deferred

Persistence, incremental scanning, missed-trigger analysis, `--json`/`--skill` filters, and any archive-candidate concept — all deliberately deferred until real usage of this tool shows a concrete need. See the design doc's "Out of scope / deferred" section for the full list and rationale.
