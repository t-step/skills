# Slice Retrospective: Add retry-with-backoff to `fetch_inventory_count()`

## What we proved
`fetch_inventory_count()` now retries on transient failure with correct
backoff timing (tests), and in the week since deploying to staging, 2 real
transient failures were automatically recovered without paging on-call —
previously every such failure raised and paged (staging logs).

## Assumptions validated
Transient network failures on this specific call are common enough to be
worth handling — 2 in one week, versus zero tolerance before.

## Assumptions falsified
None.

## Remaining uncertainty
Whether other HTTP call sites in the codebase have the same
transient-failure pattern hasn't been checked — this slice only touched
`fetch_inventory_count()`.

## Intentional non-goals
Unifying the codebase's several HTTP client libraries (a mix of `requests`,
`httpx`, and one legacy `urllib3` caller) into a single wrapper was
explicitly out of scope — goal.md scoped this slice to "fix the specific
call site that's paging on-call."

## Architectural consequences
A reusable `with_retry(fn, max_attempts, backoff)` helper now exists and
can wrap any call regardless of which HTTP library it uses underneath.

## Follow-up questions
Which other call sites page on-call for the same kind of transient
failure?
