# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** independent-vertical-paths

**Why:** CSV export (T1-T3) and notification opt-out (T4-T6) share no
file, table, or endpoint. Each is a small, coherent, end-to-end unit
with its own direct test. There is no shared prerequisite work here (T4,
the migration, only serves the opt-out feature -- nothing else needs
it), so a correct answer proposes exactly two vertical slices, not a
horizontal enabler, not six single-task slices, and not one combined
slice. The two slices should be marked safe to run in parallel, with the
reason grounded in "no shared file" rather than asserted on faith.
