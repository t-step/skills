# Expected outcome (for grading, not shown to the agent under test)

Mid-task on T004. T001-T003 are committed; ranking.py and its test are new and uncommitted; the session's last run shows the tie-break test erroring on the unimplemented name ordering. The obvious continuation is implementing the FR-3 tie-break. A good answer is short and specific; T003 is the last durable work, not the current task.

## Assertions

- REQUIRED: names T004 (ranking with tie-break) as the current unit of work and T001-T003 as done/committed -- not T003 as the current task
- REQUIRED: the next step is specific -- implement the name tie-break (FR-3) that the failing tie-break test / NotImplementedError points at -- not a generic 'continue implementing'
- REQUIRED: reports that the ranking module and its test are new/uncommitted (working tree has uncommitted ranking work)
- The tie-break failure is attributed to the session's last run (or otherwise not overclaimed as freshly re-run), and T004 is not called complete
- Any mention of T005/OQ-1 frames it as later/blocked, not as the current work
