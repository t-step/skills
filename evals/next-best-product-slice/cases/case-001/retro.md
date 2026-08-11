# Slice Retrospective: Generalize document-request field validation into a FieldValidator registry

## What we proved
`FieldValidator` lets a new field type register its own `validate(value) ->
Result` without touching the shared request-submission handler. Replaying
two weeks of real submissions through both the old and new validation path
produced identical accept/reject results.

## Assumptions validated
Field validation was assumed separable from the submission handler; the
replay confirms it.

## Assumptions falsified
None.

## Remaining uncertainty
None material to this slice.

## Intentional non-goals
This slice did not change what a recipient sees when their submission is
rejected. That was explicitly out of scope — the registry only changes how
a field's validation rule is defined, not what happens after a rule fails.

## Architectural consequences
Adding a new field type is now a small, additive registration instead of a
change to the shared handler. Concretely, the backlog's "date range" field
type (item 1) becomes a direct registration against `FieldValidator`.

## Follow-up questions
Should the "date range" field type be built next, now that it's a direct
registration against the validator?
