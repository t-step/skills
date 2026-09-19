# Expected outcome (for grading, not shown to the agent under test)

Fresh session, clean tree, T001-T003 ticked and committed, T004-T006 open, T005 waiting on OQ-1. Likely continuation is T004. HALP has no memory and must say it can't tell whether the user means to continue or switch.

## Assertions

- REQUIRED: states the last durable work as T003 complete and committed (T001-T003 done) and the remaining tasks as T004-T006
- REQUIRED: names T004 as the likely next continuation and marks that as inference (probably/likely), not as fact
- REQUIRED: says it cannot establish whether the user intends to continue this work or switch to something else
- Reports the tree as clean / nothing in progress; does not invent uncommitted work, earlier session events, or a remembered intent
- If T005 is mentioned, it is correctly described as waiting on the undecided OQ-1
