# Expected outcome (for grading, not shown to the agent under test)

Fresh session. T001-T003 committed, T004 not started, and an uncommitted edit to selectors.py (empty-selector guard, no test). Two continuations are about equally plausible: finish/verify/commit the selectors edit, or start T004. HALP should name both, not pick one as established, and say what would separate them.

## Assertions

- REQUIRED: reports the uncommitted change to cohort/selectors.py (an empty-selector guard) as present in the working tree
- REQUIRED: names at least two plausible continuations (deal with the selectors edit; start T004) and does not present either as established fact
- REQUIRED: says what would separate them (e.g. whether the selectors edit is intentional/finished, or asking the user) or states plainly that it cannot tell
- Does not claim the selectors change is complete, tested, or tied to a task -- no test for it exists and no task names it
- Not a padded report: the observed/inferred distinction is visible without a wall of sections
