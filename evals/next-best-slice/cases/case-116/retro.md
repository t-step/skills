# Slice Retrospective: Add on-call contact to service registration

## What we proved
`on_call_contact` is required at registration time and renders correctly
on `/catalog`, backed by the two passing tests.

## Assumptions validated
None beyond the slice's own scope.

## Assumptions falsified
None.

## Remaining uncertainty
None specific to this slice.

## Intentional non-goals
Backfilling `on_call_contact` for services registered before this slice
was explicitly out of scope per goal.md.

## Architectural consequences
None beyond the new field — no new seam, no reusable capability.

## Follow-up questions
None.
