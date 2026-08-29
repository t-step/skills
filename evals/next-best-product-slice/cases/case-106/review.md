# Review: Add live sales aggregation query to the organizer API

**Verdict:** Ready to merge

## Blocking
None.

## Non-blocking
None.

## Out of scope
None.

## Verification evidence
Ran the aggregation test suite (12 tests, all passing) and compared the
new query's output against a hand-counted total for 5 real events;
matched exactly.

## Reasoning
The query returns a correct real-time count; no other organizer-facing
behavior changed.
