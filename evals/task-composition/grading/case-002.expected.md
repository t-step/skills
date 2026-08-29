# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** shared-migration-enabler

**Why:** T1 and T2 (the audit_log table and its write helper) are a
genuine shared prerequisite: both the refund flow and the cancellation
flow call `write_audit_entry`, and the fixture states this explicitly.
Duplicating T1-T2 inside each vertical slice would either double the
migration or force one flow to depend on internal details of the other.
The correct answer isolates T1-T2 as a narrowly bounded horizontal
enabler, names both downstream flows it unblocks, and proposes the
refund (T3-T5) and cancellation (T6-T8) flows as separate, parallel-safe
vertical slices depending on it. This is close to the config/coding-agent
convergence pattern but distinct: here the shared piece comes *before*
the branches (an enabler), not *after* them (convergence) -- a correct
answer shouldn't confuse this with case-003's convergence shape.
