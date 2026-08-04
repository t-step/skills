# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** deferred-not-yet-justified

**Why:** The Redis-backed limiter was deferred for a specific, named
infrastructure reason (Redis not provisioned) — that's a genuine
Intentional non-goal per retro.md, not a mistake or an oversight. Nothing
in this case's evidence shows that reason has changed: no new infra
ticket, no measurement showing the per-instance gap is actually being
exploited. Recommending it now would be treating "it's on the backlog" as
justification on its own, which is exactly the trap this case targets. The
rejection-metric slice is the right next step because it's the smallest
thing that would tell us whether the deferred work is actually needed —
directly answering retro.md's own follow-up question about real-world
circumvention — rather than committing real effort to infrastructure work
nothing yet justifies. The allowlist and admin-dashboard candidates are
distractors: both are plausible small features, but neither touches the
open question this case is testing.
