# Review: Add ViewSerializer for persisting filter state

**Verdict:** Ready to merge

## Blocking
None.

## Non-blocking
None.

## Out of scope
None.

## Verification evidence
Ran the serializer test suite (16 tests, all passing) and confirmed the
"recently viewed items" sidebar (its only current caller) round-trips
filter state correctly across 10 manual test sessions.

## Reasoning
Serialization and deserialization are correct and lossless for every
filter shape currently in use.
