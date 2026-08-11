# Review: Add per-team timezone field to team settings

**Verdict:** Ready to merge

## Blocking
None.

## Non-blocking
None.

## Out of scope
None.

## Verification evidence
Ran the settings test suite (9 tests, all passing) and confirmed the new
`timezone` field is correctly stored and retrievable for all 40 existing
teams (defaulted to UTC on backfill).

## Reasoning
The field is stored and retrieved correctly; no aggregation logic changed
in this slice.
