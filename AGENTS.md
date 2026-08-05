# AGENTS

Working instructions for the skills repository, shared by all coding agents. Codex reads this file natively; Claude Code loads it through the `@AGENTS.md` import in CLAUDE.md. Keep shared policy here; put harness-specific notes in the harness's own file.

## What this repo is

A collection of portable Agent Skills — self-contained skill definitions (SKILL.md plus supporting `examples/`, `references/`, `templates/`, `scripts/`) usable across harnesses. First content skill: `skills/slice-review/`, with its eval suites under `evals/slice-review/` (agent-visible inputs in `cases/`, answer keys isolated in `grading/`, committed benchmark evidence in `RESULTS.md` and `runs/`). Repository-wide guard scripts live under `scripts/`.

## Project memory (projectmem) — MANDATORY

This repository uses projectmem for persistent memory and workflow rules.

- At session start, load the project instructions and summary before answering questions about the project — via the projectmem MCP tools (`get_instructions()`, `get_summary()`, and `get_project_map()` when structure matters) where the server is connected, otherwise via the CLI: `pjm instructions`, `pjm show`, `pjm map`.
- Before modifying any file, check its failure history: `precheck_file(path)` or `pjm precheck <path>`.
- Log while working:
  - bug or unexpected behavior → `log_issue` / `pjm log`
  - each fix attempt → `record_attempt` / `pjm attempt`
  - confirmed fix → `record_fix(summary, issue_id=...)` / `pjm fix` — always pass the explicit issue id; never let the tool infer the target from "most recent open issue" (that default once attached a fix to the wrong issue, #0003)
  - design choice → `add_decision` / `pjm decision`
  - gotcha or setup detail → `add_note` / `pjm note`
- After a meaningful investigation or fix, briefly consider whether a failed approach produced reusable negative knowledge; if so, record it with `record_attempt` — failed approaches are the one thing git history cannot preserve.
- Do not copy commit messages or ordinary code changes into projectmem; git is canonical for those. An event earns its place only by preserving rationale, an assumption change, an unresolved risk, or reusable negative knowledge. `add_note` is a fallback for durable context, not a second git log.
- Never edit `.projectmem/summary.md` or `events.jsonl` directly — the summary regenerates from the event log, and direct edits break audit replay. `PROJECT_MAP.md` and `plan.md` may be edited directly.
- Prefer these tools over re-scanning source files when they answer the same question.

Harness note: the projectmem MCP server is registered for Claude Code (`.mcp.json`) and globally for Codex (no `--root`; the server parent-walks from the session directory to find `.projectmem/`). Prefer the MCP tools when connected; the `pjm` CLI is the fallback.

## Verification — local-first

This repository is private, so GitHub CI runs rarely and must never be the first place checks execute. Run whatever checks exist locally (skill evals under `evals/`, scripts under `scripts/`) and confirm they pass before opening a PR. Do not claim work is complete or PR-ready on the expectation that CI will catch problems.

The canonical check command is `bash scripts/check.sh`. It runs the strict-YAML skill-frontmatter lint (`scripts/check-skill-frontmatter.py`, a uv script), the eval answer-leakage guard (`scripts/check-eval-isolation.py`), the cross-skill dependency check (`scripts/check-skill-deps.py`), and the skill-usage-report test suite (`scripts/test-skill-usage-report.py`), and it must pass before any commit or PR. It is enforced at three layers: run it directly while working; the machine-local pre-commit hook invokes it (appended below projectmem's fenced block in `.git/hooks/pre-commit` — hooks are untracked, so re-append on a fresh clone); and `.github/workflows/checks.yml` re-runs the identical script in CI as a backstop, never as the first execution. Add future checks to `check.sh` itself, not to the hook or the workflow.

## Skill usage measurement

`scripts/skill-usage-report.py` reports how often each `skills/*/SKILL.md` has actually been invoked in local Claude Code sessions (total count, distinct sessions/projects, last-used timestamp), by scanning `~/.claude/projects/**/*.jsonl` transcripts fresh on every run. Run it manually with `uv run scripts/skill-usage-report.py` when deciding whether a skill is getting used or is an archive candidate — it is deliberately stateless and not wired into any automated schedule or hook; see `docs/superpowers/specs/2026-08-04-skill-usage-report-design.md` for the scope decision and what's deferred until real usage shows a need.
