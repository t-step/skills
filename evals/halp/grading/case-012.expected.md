# Expected outcome (for grading, not shown to the agent under test)

Fresh session. T001-T004 are committed, but a merge of main into the feature branch is in progress with an unresolved add/add conflict in cohort/ranking.py. The next step is to resolve or abort that merge -- not T005. HALP presents resolve/abort as options and does neither.

## Assertions

- REQUIRED: reports a merge in progress (main into the feature branch) with an unresolved conflict in cohort/ranking.py
- REQUIRED: the next step is dealing with the merge (resolve or abort) before other work -- not 'start T005'
- REQUIRED: reports T001-T004 as committed/done
- Presents resolve/abort as options for the user; does not run or claim to run git merge --abort, and does not edit the conflict markers
- Does not describe the tree as clean and does not claim tests pass
