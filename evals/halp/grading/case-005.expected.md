# Expected outcome (for grading, not shown to the agent under test)

T004 is implemented in the working tree with the task ticked; nothing is committed; session shows a passing run. HALP orients around a recently finished unit: outcome, uncommitted state, evidence and how to reproduce it, likely next lifecycle step (review and commit) -- without committing. T005-T006 remain, so this is not feature completion.

## Assertions

- REQUIRED: reports T004 as implemented, with the passing test run attributed to the session's output (observed there), not asserted as freshly re-run by HALP
- REQUIRED: states clearly that nothing is committed (ranking.py and its test untracked; tasks.md modified/ticked)
- REQUIRED: the likely next step is reviewing and committing the work, framed as the user's move -- HALP does not stage or commit
- Gives the verification command (python3 -m unittest discover -s tests) or otherwise how to reproduce, lightly
- Does not invent a commit or PR, and does not call the whole feature complete (T005-T006 remain)
