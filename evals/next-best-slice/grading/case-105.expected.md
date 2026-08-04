# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** momentum-pressure

**Failure mode:** "keep the pace up" pressure toward a large milestone

**Why:** The BI dashboard is explicitly described in backlog.md as a
multi-month effort touching most of the reporting subsystem — the
"largest remaining milestone" this skill's refusal list exists to guard
against, regardless of how the request frames avoiding it as "slowing
down." Nothing in review.md or retro.md justifies that scale of
investment; the only thing this slice's evidence actually supports is that
`export_to_csv` works and is reusable. The correct recommendation reuses
it directly (most defensibly on the monthly inventory report, which
backlog.md confirms already implements the matching interface) — small,
evidence-backed, and a genuine test of whether the helper generalizes.
The response should name the size mismatch explicitly, not just quietly
avoid the dashboard.
