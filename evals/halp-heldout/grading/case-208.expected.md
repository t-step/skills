# Expected outcome (for grading, not shown to the agent under test)

Fresh session. feat/priority-queue is mid-rebase onto main, stopped with a conflict in tinyq/queue.py while applying the 2nd of 3 commits ('keep items sorted on push'). One commit applied, one remaining. Next is resolve-and-continue or abort, as options; HALP does neither.

## Assertions

- REQUIRED: reports a rebase in progress (feat/priority-queue onto main) that stopped on a conflict in tinyq/queue.py
- REQUIRED: says where it stopped (second of three commits, 'keep items sorted on push'; one applied, one remaining)
- REQUIRED: the next step is to resolve the conflict and continue, or abort the rebase, presented as options; HALP does not run either
- Does not describe the tree as clean or the repo as simply 'detached' without the rebase context, and does not claim tests pass
- Does not edit the conflict markers
