# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** actual-dependency-cycle

**Why (revised after iteration 2 run evidence):** T1's implementation
calls into T2, and T2's implementation reads T1's result -- a genuine
mutual dependency between two tasks, not a numeric-order illusion
(case-004) or a missing-information gap (case-007). Iteration 2 evidence
(both baseline and with-skill runs, independently) also noticed this
fixture is arguably a literal infinite-recursion bug at the runtime
level, not just a build-order cycle -- that's a genuine, useful
observation but not itself what this case grades.

What's actually required, defensible, or wrong:

- **Required:** the report explicitly names the cycle/mutual dependency
  -- not silence, not a vague "these are related."
- **Required:** no confident cross-slice T1-then-T2 or T2-then-T1
  execution order is presented as if it resolves the dependency.
- **Required:** the cycle is named under Topology issues (or
  equivalent), not buried only in one slice's Risk/uncertainty field.
- **Defensible, not graded pass/fail on its own:** resolving the cycle
  by keeping T1 and T2 in one slice together, since they're small enough
  that co-location needs no cross-slice ordering at all. Refusing to
  produce any plan whatsoever would be over-conservative for a cycle
  this size -- the skill's job is to decide the right slice boundary,
  and "put them in the same slice" is a legitimate boundary decision
  here, not a dodge, provided the cycle is still named rather than
  silently absorbed.
- **Wrong:** silently treating T1/T2 as independent; inventing an
  unstated design fix (e.g. a new intermediate field/module) to break
  the cycle without naming it as a change to the plan -- this skill
  groups already-decomposed tasks, it does not redesign them, so
  proposing a fix is out of scope even when the fix is a good idea.
