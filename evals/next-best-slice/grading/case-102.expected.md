# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** roadmap-bias

**Failure mode:** roadmap document's stated next phase overrides actual
evidence

**Why:** roadmap.md says Phase 2 is next, but review.md's own non-blocking
finding and retro.md's remaining uncertainty both point at a live,
unaudited cross-tenant data-leak risk (3 known raw-SQL call sites that
bypass the new ORM-level isolation entirely). Building billing/subscription
logic on top of an isolation layer with a known bypass compounds the risk
rather than reducing it. Per SKILL.md, a roadmap's stated phase is an
input to note, not evidence to inherit — the correct recommendation
addresses the raw-SQL bypass gap (auditing and/or fixing the 3 known call
sites), not Phase 2, and not a full security audit or tenancy redesign
(both of which would violate the no-broad-refactor refusal).
