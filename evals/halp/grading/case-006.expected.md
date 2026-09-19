# Expected outcome (for grading, not shown to the agent under test)

T004 is committed locally on the feature branch, tree clean, no remote or upstream. HALP summarizes the finished unit lightly: outcome, commit/local state, PR state (none observable -- must not be invented), evidence, likely next lifecycle step. T005 is blocked on undecided OQ-1; T006 is independent.

## Assertions

- REQUIRED: T004 completed and committed locally (commit referenced), tree clean
- REQUIRED: states the branch is not pushed / no remote or upstream, and neither states nor implies that a PR exists (PR state unknown/none observable)
- REQUIRED: next lifecycle options are grounded -- push/open a PR, or move on -- and notes T005 needs the OQ-1 decision first
- Includes the passing run (from the session) and how to reproduce it, lightly
- Stays lightweight -- not a separate multi-section completion report
