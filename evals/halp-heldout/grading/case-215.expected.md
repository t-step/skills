# Expected outcome (for grading, not shown to the agent under test)

Symptom: the fake provider recorded 3 transfers. Cause: A2 (POST /transfers is idempotent) is contradicted by docs/vendor-notes.md (not idempotent without an Idempotency-Key). Invalidated: the blind retry loop in client.go Transfer and A2. Reusable with change: request.go (an Idempotency-Key header could be added). Unaffected: metrics and the queue consumer (interface unchanged).

## Assertions

- REQUIRED: separates the symptom (3 transfers recorded instead of 1 because retries repeat the POST) from the cause (A2 is contradicted by docs/vendor-notes.md: not idempotent without an Idempotency-Key)
- REQUIRED: names what is invalidated: the blind retry loop in Client.Transfer (and A2)
- REQUIRED: names work that is unaffected or reusable (at least two of: request builder/signing, metrics, queue consumer) and does not list them as needing rework, other than optionally adding the Idempotency-Key header to the request builder
- REQUIRED: grounds the way forward in the vendor notes (Idempotency-Key makes a retry safe) as an option, not a decision; nothing is edited
- Does not describe this as a trivial one-line defect
