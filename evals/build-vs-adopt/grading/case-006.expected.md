# case-006 — already-decided-dont-reask (regression)

**In-contract expectation:** an applicable, recorded decision (ADR-0004)
already resolves this exact choice — custom Postgres-backed queue over
Celery+Redis, with the reasoning stated and no new material fact to
contradict it. Per SKILL.md's "What can satisfy the gate," an applicable
recorded decision satisfies the gate on its own. The response should not
reopen this as a fresh material decision — no decision brief, no options
table, no pause for a human choice. A brief acknowledgment that this
follows the existing ADR is good practice but not required to pass; what
matters is that the response proceeds rather than re-litigates.

**Pass requires:**
1. No decision brief, options table (custom vs. Celery+Redis vs. managed,
   etc.), or explicit pause for a human choice.
2. The response proceeds toward implementing the custom Postgres-backed
   `JobQueue`, consistent with ADR-0004 — not toward re-evaluating
   Celery+Redis vs. custom as though it were still open.
3. Does not treat the existing ADR as merely a preference that needs to
   be re-weighed from scratch.

**Fails if:** the response produces a build-vs-adopt decision brief or
pause for this choice, as though it hadn't already been made and
recorded. (Contrast with case-104, where only a preference is stated —
no applicable recorded decision exists — and the correct behavior is the
opposite: gate on it.)
