# projectmem - skills

_Last updated: 2026-08-02_

## Project purpose
A collection of portable Agent Skills: self-contained skill definitions (SKILL.md plus supporting examples, references, templates, and scripts) usable across coding-agent harnesses (Claude Code, Codex, and others). No skill content is authored yet — only the directory scaffold exists.

## Recent issues
- No issues logged yet.

## Decisions
- Agent-file wiring (2026-08-02, at repo creation): AGENTS.md is the shared authoritative instruction set (Codex-native) carrying the projectmem mandate and the local-first verification rule; CLAUDE.md is an @AGENTS.md import bridge (Claude Code does not read AGENTS.md natively as of v2.1.220). projectmem MCP registered for Claude via .mcp.json; Codex reaches it through the global root-less registration in ~/.codex/config.toml. Same pattern as bindle, cover-story, Valence. [AGENTS.md]

## Notes
- Repo is private: GitHub CI runs rarely — all checks (future evals/, scripts/) must pass locally before any PR; CI is a backstop only.

## Key files
- `AGENTS.md`
- `CLAUDE.md`
- `v2.1.220`
- `.mcp.json`
- `/.codex/config.toml`

## Open questions
- None logged yet.
