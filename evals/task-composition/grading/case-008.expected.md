# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** shared-file-safe-parallelism

**Why:** T1 and T2 both touch `cli/commands.py`, but the fixture
establishes a documented, stable extension pattern (independent
additive blocks, order-independent dict registration, no semantic
interaction) that makes the two additions genuinely combinable. This is
the positive case for the shared-file nuance: pathname overlap alone
should not trigger serialization when the two changes are semantically
independent and the convergence (a trivial textual merge) is
predictable. A correct answer notices the shared file, says so, and
still marks the two slices parallel-safe, grounded in the stated pattern
-- not in "they'll use separate branches," which is not itself a reason.
