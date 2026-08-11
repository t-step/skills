# Review: Generalize document-request field validation into a FieldValidator registry

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
None.

## Out of scope
None.

## Verification evidence
Ran the validator test suite (28 tests, all passing) and replayed two weeks
of real submitted document requests through both the old inline validation
and the new registry; results matched for every request in the window.

## Reasoning
The registry reproduces existing validation behavior exactly and no
existing field type's behavior changed.
