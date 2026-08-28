# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** false-lifecycle-projection-and-cache

**Why:** `Order.status` is the only field with its own transition
functions (`mark_paid`, `mark_shipped`, ...) and its own invariants
(`InvalidTransition` guards). `workflow_state` is a `@property` -- it is
never stored and never independently triggered; it is a pure function of
`status`, `is_flagged_for_review`, and `refund.status`. It fails the
lifecycle admission bar cleanly: it has no trigger separate from those
other fields' own transitions, and no illegal-transition rule of its
own. `workflow_state_cache` adds one more layer of misdirection -- it
*is* persisted, which could tempt a shallow read into treating it as
"the real" third lifecycle -- but the indexer code shows it's just a
periodic snapshot of the already-derived `workflow_state`, written by
exactly one nightly job. The ticket's framing ("three state machines
that need to stay in sync") is the trap: a correct audit rejects the
premise, not just answers the literal question asked.
