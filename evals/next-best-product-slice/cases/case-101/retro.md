# Slice Retrospective: Generalize macro execution into a reusable MacroRunner

## What we proved
`MacroRunner` executes a macro's steps without touching the ticket-update
handler directly. A week of replayed real macro executions matched the old
and new paths exactly.

## Assumptions validated
Macro execution was assumed separable from the ticket-update handler; the
replay confirms it.

## Assumptions falsified
None.

## Remaining uncertainty
None material to this slice.

## Intentional non-goals
This slice did not touch what happens when a customer replies to a ticket
after it's been closed — explicitly out of scope.

## Architectural consequences
Adding a new macro trigger type is now a small, additive registration
against `MacroRunner` instead of a change to the ticket-update handler.

## Follow-up questions
Should the "auto-tag on reopen" macro trigger (backlog item 1) be built
next, now that it's a direct registration?
