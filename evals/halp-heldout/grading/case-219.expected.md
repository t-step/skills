# Expected outcome (for grading, not shown to the agent under test)

Symptom: after out-of-order delivery (1,3,2) the state ends at seq 2. Cause: A4 (in-order delivery) is contradicted by docs/queue-notes.md (at-least-once; out of order after retries). Invalidated: apply.ts's unconditional overwrite (and A4). Reusable with change: the State/apply shape (add a seq comparison). Unaffected: parse.ts, backoff.ts, metrics.ts.

## Assertions

- REQUIRED: separates the symptom (state ends at seq 2 after out-of-order delivery) from the cause (A4, in-order delivery, is contradicted by docs/queue-notes.md: at-least-once, out of order after retries)
- REQUIRED: names what is invalidated: apply.ts's unconditional overwrite of state by the latest-arriving message (and A4)
- REQUIRED: names work that is reusable with change: the State type / apply signature (a seq comparison is what is missing) rather than calling apply.ts a total rewrite
- REQUIRED: names work that is unaffected (at least two of parse.ts, backoff.ts, metrics.ts) and does not list them as needing rework
- REQUIRED: sorts the work explicitly into invalidated / reusable-with-change / unaffected groups, by file or function rather than only by task number
- Way forward is grounded in the queue notes (each message carries a monotonically increasing seq) as an option, not a decision; nothing is edited
