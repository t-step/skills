# case-107 (p7) — expected: timezone-aware aggregation, decline vague refactor — deliberate boundary case

**In-contract expectation:** the response recommends backlog item 1 (make
the monthly aggregation report use each team's real timezone), grounded
explicitly in the concrete, immediate product outcome (finance teams
currently see month-end totals that don't match their own books), and
declines item 2 (query-layer consistency refactor) for having no such
concrete connection.

**Grounded in SKILL.md:** "Pure technical or architectural cleanup is not
eligible here unless there's a concrete, near-term, evidence-traceable
connection to what a user can accomplish." Item 1 is technical/data-model
work (a timezone-aware aggregation change) whose product connection is
immediate and named -- this is the direct positive case for "Product value
isn't a layer." Item 2 is technical work described only as probably
helping future development speed -- the canonical example of what this
skill declines.

This case is deliberately built at the boundary between "technical work
that creates product value" and a correctness fix, since the aggregation
mismatch is itself a kind of defect -- it exists specifically to test
whether the skill can recognize the exception ("the fix itself is what
unlocks the user-visible outcome") rather than to serve as a clean
positive case. See `pressure-tests/README.md`. A response that declines
item 1 as "just a bug, not product work" misses the exception SKILL.md
states explicitly.
