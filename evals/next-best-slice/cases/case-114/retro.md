# Slice Retrospective: On-call history log

## What we proved
Every on-call contact change is captured in `on_call_log` with the old
and new contact and a timestamp, backed by the three passing tests.

## Assumptions validated
None beyond the slice's own scope.

## Assumptions falsified
None.

## Remaining uncertainty
None specific to this slice.

## Intentional non-goals
Any UI or endpoint to view the log was explicitly out of scope per
goal.md — this slice only adds the write path and persistence.

## Architectural consequences
`on_call_log` is now a persisted, queryable history of on-call
assignment changes. Any future feature that needs to show or look up
on-call history can read from it directly, without new infrastructure.

## Follow-up questions
None.
