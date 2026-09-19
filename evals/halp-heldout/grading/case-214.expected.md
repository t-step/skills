# Expected outcome (for grading, not shown to the agent under test)

Symptom: the loader never terminates (nextCursor is undefined, not null, so 'while (cursor !== null)' spins). Cause: assumption A1 (cursor pagination) is contradicted by fixtures/messages.sample.json, which is offset/limit/total. Invalidated: the cursor loop and Page.nextCursor (and A1). Unaffected: formatDate, MessageList, the Message type. Reusable with adaptation: the fetch client and hook skeleton. A guard would hide the mismatch (it would load one page and stop).

## Assertions

- REQUIRED: separates the symptom (test timeout / loop that never ends) from the cause (A1, cursor pagination, is contradicted by the recorded API sample using offset/limit/total)
- REQUIRED: names what the failed assumption invalidates (the cursor/nextCursor logic in the client and loader, the Page type, A1 in the plan)
- REQUIRED: names work that is unaffected or still valid (at least two of: MessageList, the Message type, formatDate) and does not list those as needing rework
- REQUIRED: does not recommend just guarding the undefined cursor as the fix; if mentioned, notes it would hide the mismatch (e.g. load only the first page)
- Next options are grounded and advisory (e.g. confirm the API's pagination contract and update A1 before reworking); nothing is edited
