# AGENTS

Working instructions for the skills repository, shared by all coding agents. Codex reads this file natively; Claude Code loads it through the `@AGENTS.md` import in CLAUDE.md. Keep shared policy here; put harness-specific notes in the harness's own file.

## What this repo is

A collection of portable Agent Skills — self-contained skill definitions (SKILL.md plus supporting `examples/`, `references/`, `templates/`, `scripts/`) usable across harnesses. Currently a skeleton: three skill directories exist (`skills/create-session-handoff/`, `skills/investigate-tradeoff/`, `skills/retrieve-prior-work/`) with no SKILL.md files authored yet, plus empty `evals/` and `scripts/` directories and a `.github/workflows/` stub.

## Project memory (projectmem) — MANDATORY

This repository uses projectmem for persistent memory and workflow rules.

- At session start, load the project instructions and summary before answering questions about the project — via the projectmem MCP tools (`get_instructions()`, `get_summary()`, and `get_project_map()` when structure matters) where the server is connected, otherwise via the CLI: `pjm instructions`, `pjm show`, `pjm map`.
- Before modifying any file, check its failure history: `precheck_file(path)` or `pjm precheck <path>`.
- Log while working:
  - bug or unexpected behavior → `log_issue` / `pjm log`
  - each fix attempt → `record_attempt` / `pjm attempt`
  - confirmed fix → `record_fix` / `pjm fix`
  - design choice → `add_decision` / `pjm decision`
  - gotcha or setup detail → `add_note` / `pjm note`
- Never edit `.projectmem/summary.md` or `events.jsonl` directly — the summary regenerates from the event log, and direct edits break audit replay. `PROJECT_MAP.md` and `plan.md` may be edited directly.
- Prefer these tools over re-scanning source files when they answer the same question.

Harness note: the projectmem MCP server is registered for Claude Code (`.mcp.json`) and globally for Codex (no `--root`; the server parent-walks from the session directory to find `.projectmem/`). Prefer the MCP tools when connected; the `pjm` CLI is the fallback.

## Verification — local-first

This repository is private, so GitHub CI runs rarely and must never be the first place checks execute. Run whatever checks exist locally (skill evals under `evals/`, scripts under `scripts/`) and confirm they pass before opening a PR. Do not claim work is complete or PR-ready on the expectation that CI will catch problems.
