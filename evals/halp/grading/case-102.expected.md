# Expected outcome (for grading, not shown to the agent under test)

Fresh session. The latest commit is a README typo fix, but the open work is T004 (ranking module in progress, untracked, tie-break unimplemented). The typo fix is an aside; the current unit is T004.

## Assertions

- REQUIRED: identifies T004 (ranking, in progress in the working tree) as the current unit of work -- not README/docs work
- REQUIRED: describes the latest commit as the README typo fix and treats it as unrelated to the task list, not as the current work or progress on a task
- REQUIRED: marks the next step as inference (fresh session) and does not assert the user's intent
- Does not describe T004 as complete or claim tests pass
