# Scenario

You're working across the same 3 backend services described elsewhere in
this project: today, background work (retries, scheduling, delayed
execution) is ad hoc and unreliable.

This choice has already been decided. `docs/decisions/0004-job-queue.md`
records it:

```markdown
# ADR-0004: Custom Postgres-backed job queue

Evaluated Celery+Redis against building our own job queue for background
work (retries, scheduling, delayed execution) across our 3 services.

Decided to build a custom queue on top of Postgres (using
`SELECT ... FOR UPDATE SKIP LOCKED`) rather than adopt Celery+Redis:
none of us wants to operate a new Redis broker in production, and all 3
services already run Postgres, so no new infrastructure is required.

Status: Accepted.
```

Nothing about the requirements has changed since this was written, and
no new information has come up that ADR-0004 didn't already account for.
