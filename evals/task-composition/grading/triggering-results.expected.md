# Expected outcomes (for grading, not shown to the agent under test)

| Case | Prompt | Expected selection |
|---|---|---|
| 201 | How should these tasks be grouped into agent assignments? | task-composition |
| 202 | Given this task list, which of these tasks can run in parallel? | task-composition |
| 203 | Turn this task plan into agent-sized work packages/sessions. | task-composition |
| 204 | Which task should I do next? | next-best-slice |
| 205 | Plan the implementation of T024. | slice-plan |
| 206 | Break this spec into tasks. | none of the four candidates |

**Why 204/205/206 are the contrast cases:** 204 and 205 both sound
superficially like "which piece of work" questions, but 204 asks for a
*priority pick among many candidates* (next-best-slice's job) and 205
asks for an *implementation plan for one already-chosen unit*
(slice-plan's job) -- neither is a request to partition or group
already-decomposed work, which is task-composition's specific job. 206
is a decomposition request (turning a spec into tasks in the first
place), which task-composition explicitly assumes is already done and
refuses to perform.
