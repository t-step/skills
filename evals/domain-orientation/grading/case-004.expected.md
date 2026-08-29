# Expected domain orientation outcome (for grading, not shown to the agent under test)

**Scenario:** tooling-domain-not-business

**Why:** This fixture has no business/retail vocabulary anywhere in it --
it's a job queue library. Two opposite failure modes are possible: forcing
a business-domain shape onto it (inventing a "customer" or "order" concept
that doesn't exist, or trying to describe `Job`/`Lease` using
retail-flavored language), or refusing to treat it as having a domain at
all because it's "just infrastructure." Both are wrong; the correct
answer is a domain map scoped to what this system is actually about --
lease-based exclusive access and at-least-once delivery semantics.

The fencing-token behavior in `complete()` is the fixture's sharpest
invariant: a completion with a stale token is silently dropped rather than
raising or succeeding, which is exactly the kind of business/domain rule
(not a technical validation) this skill exists to surface. `Lease`'s own
docstring states plainly that it isn't independently persisted -- it's
described as a concept but stored as fields on `Job`; a pass that treats
`Lease` as its own stored entity anyway hasn't actually read the
docstring or `acquire()`'s `store.set_lease(...)` call against `Job`.
