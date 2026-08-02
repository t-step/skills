# Project Map - skills

Status: populated by AI session (2026-08-02); repo is a pre-content skeleton — refine as skills are authored.

## Project purpose
A collection of portable Agent Skills: self-contained skill definitions (SKILL.md plus supporting examples, references, templates, and scripts) usable across coding-agent harnesses (Claude Code, Codex, and others). No skill content is authored yet — only the directory scaffold exists.

## Stack
- Tags: github-actions
- Detected from: .github/workflows

## Structure
- `AGENTS.md` — authoritative shared agent instructions; `CLAUDE.md` is an `@AGENTS.md` import bridge
- `skills/` — one directory per skill, each intended to hold a `SKILL.md` plus supporting material
  - `skills/create-session-handoff/` — scaffold (`examples/`, `templates/`); no SKILL.md yet
  - `skills/investigate-tradeoff/` — scaffold (`examples/`, `references/`); no SKILL.md yet
  - `skills/retrieve-prior-work/` — scaffold (`examples/`, `references/`, `scripts/`); no SKILL.md yet
- `evals/` — empty; intended for skill evaluations
- `scripts/` — empty; intended for repo utilities
- `.github/workflows/` — empty stub; note verification is local-first (private repo, CI runs rarely)

## Relationships
- Nothing wired yet — no skill references another, and no eval or script exists. Update this section as SKILL.md files land.
