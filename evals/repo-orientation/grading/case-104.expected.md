# Expected orientation outcome (for grading, not shown to the agent under test)

**Failure mode:** stale README claims.

**In-contract.** SKILL.md's "deterministic artifact over prose" rule
applies directly: `app.py` defines only Flask REST routes, there is no
GraphQL library in `requirements.txt`, and `AGENTS.md` states the routes
are "plain REST." The README's "exposes a GraphQL API" claim is simply
wrong (stale, or aspirational and never built) and must be named as
contradicted by the code, not repeated as the actual API shape.
