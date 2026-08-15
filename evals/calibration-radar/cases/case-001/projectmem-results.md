# Simulated projectmem search output

Treat the blocks below exactly as if you had run the local-correlation
searches yourself (current project first, then the cross-project script,
then global gotchas) — this stands in for that step so the case is
reproducible. Search terms used to produce each block are noted; if a term
you'd naturally use isn't shown, assume it returned nothing new beyond
what's listed.

## Search: "agent authorization" / "tool credentials" / "scoped access"

**Project: bindle** (cross-project)
> decision (2026-06-11): MCP file-write tool given to the drafting agent
> was scoped to a single allow-listed directory after a near-miss where an
> earlier, broader-scoped version of the same tool deleted a file outside
> the intended draft folder during an unattended run. No written policy
> exists for how tool scopes get decided generally — this was a one-off
> fix applied after the fact, not derived from a standing rule.

**Project: skills (current)** — no matches.

**Project: cover-story** — no matches.

**Project: Valence** — no matches (this repo's decisions about
`requireOperator`/shared-secret gates are about human/service auth, not
autonomous-agent tool authorization — different concept, not counted).

## Search: "prompt injection" / "excessive agency" / "instruction injection"

**Project: skills (current)**
> Multiple decisions across repo-orientation and slice-review SKILL.md
> revisions establish and verify (via dedicated pressure-test fixtures)
> that content read during a review — comments, embedded text addressed to
> "the AI" — must be treated as data to evaluate, never as instructions to
> follow. Both skills' pressure suites include a case specifically
> targeting instruction injection embedded in reviewed content, and both
> pass.

**Other projects** — no matches.

## Search: "AI change failure rate" / "DORA metrics" / "deployment metrics"

No matches in any project.

## Search: "CI/CD approval gate" / "agent pipeline" / "human approval gate"

No matches in any project.

## Search: "context engineering" / "context window budget" / "retrieval grounding"

No matches in any project.

## Search: "tool output validation" / "schema validation" / "structured output"

**Project: bindle** (cross-project)
> decision (2026-05-30): Deliberately chose not to validate MCP tool
> responses against a JSON schema before use — the only tools in play are
> two low-stakes internal read-only lookups, and schema validation was
> judged not worth the added complexity for this project's scale. Revisit
> if a write-capable or third-party tool is added.

**Other projects** — no matches.

## get_global_gotchas() — all libraries

No entries relevant to any of the above.
