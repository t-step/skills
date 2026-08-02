# CLAUDE.md

@AGENTS.md

The import above loads AGENTS.md, the authoritative instruction set shared with Codex and other agents (Claude Code does not read AGENTS.md natively; the `@` import is the documented bridge). This file only adds what AGENTS.md cannot express portably. In Claude Code the projectmem MCP server (registered in `.mcp.json`) injects its own detailed tool instructions at session start — use the MCP tools, not the `pjm` CLI fallback, when the server is connected.
