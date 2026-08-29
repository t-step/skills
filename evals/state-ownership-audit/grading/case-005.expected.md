# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** genuine-second-writer-hazard

**Why:** Unlike case-002, there is no shared authoritative source here --
`billing_webhook.py` treats Stripe's event payload as ground truth and
applies it unconditionally, while `admin_console.py` treats a support
rep's direct input as ground truth, with zero coordination, ordering
check, or version/timestamp comparison between them. The incident (a
stale, delayed webhook silently clobbering a manual override) is the
concrete failure this skill's hazard hunt exists to catch: two legitimate-
looking write paths, no fencing, no reconciliation. This is the
"must-catch" case in the suite -- a report that describes both paths
neutrally as "representations" or "synchronization mechanisms" without
naming this a hazard has missed the actual point of the audit. The skill
explicitly refuses to design the fix (a version check, a lock, a
one-directional-only override policy); it should name the hazard and stop
there.
