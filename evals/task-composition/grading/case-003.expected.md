# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** convergent-dispatch

**Why:** This fixture mirrors the repository's own motivating example
for this skill almost directly: two independent branches (config,
T1-T3; coding-agent, T4-T5) that don't share any files, followed by a
dispatch task (T6) that explicitly requires both to be finished, and an
end-to-end test (T7) that only makes sense once dispatch exists. A
correct answer proposes config and coding-agent as two parallel-safe
vertical slices, and dispatch+e2e as a convergence/integration slice
depending on both -- not folded into one giant slice, and not missing
the dependency on one of the two branches. T8 (lint + changelog) is
purely mechanical and should be folded into the dispatch slice rather
than given its own slice, per the skill's "don't add ceremony" guidance.
