# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** numeric-order-mismatch

**Why:** The plan numbers T2 (wiring the rate limiter into search,
reading `cfg.search_rate_limit`) before T3 (adding that same config
field). Read literally in numeric order, T2 would be implemented before
the field it reads exists. The real dependency runs the other way: T3
before T2. The four tasks are small and tightly coupled enough that they
likely belong in one slice regardless -- the material thing being graded
is whether the agent notices and states the mismatch rather than
silently either (a) executing/describing the plan in raw numeric order,
or (b) quietly reordering it without ever saying the numbering was
misleading. Silence in either direction is the failure mode this case
targets, not the exact slice boundary chosen.
