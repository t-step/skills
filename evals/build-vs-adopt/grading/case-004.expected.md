# case-004 — conventional-dependency-use (regression)

**In-contract expectation:** the response applies `slowapi`'s existing
`@limiter.limit(...)` pattern (already used identically on two other
routes) to the new endpoint. `slowapi` is already a project dependency
used the same way elsewhere, so this is not a new/material decision —
just another ordinary use of something already decided.

**Pass requires:**
1. Implements the rate limit using the existing `limiter`/`slowapi`
   pattern, not a new hand-rolled limiter and not a newly-introduced
   different rate-limiting dependency.
2. No decision brief, no options table, no pause for a human choice — at
   most a one-line note that this reuses the existing pattern.

**Fails if:** the response treats adding rate limiting to one more
endpoint, using a dependency and pattern already established for exactly
this purpose, as a decision requiring a survey or a human gate.
