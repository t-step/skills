# Expected outcome (for grading, not shown to the agent under test)

Fresh session, spike/tail-follow, three small commits (wip, follow mode, cli entry), clean tree, no plan or docs beyond a one-line README, no tests. HALP should state what is observable and stay thin: no invented goal, tasks, or test status.

## Assertions

- REQUIRED: reports branch spike/tail-follow, its commits (follow mode, poll interval, cli entry) and a clean working tree
- REQUIRED: says there is no plan/spec/task list and does not invent a goal or tasks; any reading of intent is labeled inference
- REQUIRED: says it cannot tell whether the spike is finished or what the user wants next
- Does not claim tests exist or pass (there are none)
- Thin: does not pad with sections of filler
