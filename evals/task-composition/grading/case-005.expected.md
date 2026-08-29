# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** paired-implementation-test

**Why:** This is the simplest possible test of "task IDs are not session
boundaries": two tasks, one endpoint and its own direct test, nothing
else in the plan. The specific failure mode this targets is producing
two slices (one per task ID) out of habit or literal-mindedness, instead
of recognizing there's no useful checkpoint between writing the endpoint
and proving it works. A correct answer is exactly one slice covering
both tasks, with a stated (not just implied-by-omission) reason.
