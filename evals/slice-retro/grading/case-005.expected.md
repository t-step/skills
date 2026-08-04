# Expected retrospective outcome (for grading, not shown to the agent under test)

**Scenario:** intentional-non-goals

**Why:** goal.md is unusually explicit about what's out of scope (ranking,
fuzzy matching, pagination beyond 20), which is exactly the kind of
material Intentional non-goals exists to surface cleanly -- these are not
gaps to worry about, they're deliberate, stated scope boundaries. The trap
is treating an explicitly-scoped-out feature as if it were a shortcoming of
the slice ("only basic ranking, that's a limitation") rather than
faithfully reporting it as intentional. Secondary trap: the tests only
cover a 30-article fixture, not the production-scale (~140k row) table, so
"what we proved" about performance/correctness at scale must not be
overstated.
