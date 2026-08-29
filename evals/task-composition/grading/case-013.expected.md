# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** legitimate-horizontal-enabler-behavior

**Why:** T1 (`verify_signed_request`) is a genuine horizontal enabler,
not a technical-layer grouping wearing that label: the fixture states
explicitly that all three admin endpoints call it, and that
implementing the HMAC check separately in each of the three files would
triplicate the logic and require three edits for any future signing-scheme
change. It passes all three of the skill's enabler tests (why it should
exist independently: avoids duplicated auth logic and drift risk across
three files; what it unlocks: purge-cache, reindex, and rotate-keys,
named individually; parallelism gained: unblocks three vertical slices
to run concurrently instead of one) and it fails the absorbable-enabler
question -- it cannot be folded into just one of the three endpoint
slices without either duplicating it in the other two or making them
depend on that one endpoint's module. The correct composition isolates
T1 as its own horizontal-enabler slice with that justification stated,
and proposes purge-cache (T2+T5), reindex (T3+T6), and rotate-keys
(T4+T7) as three separate vertical slices, each depending on the
enabler and parallel-safe with each other (no shared files). T1's own
"Delivers" is a meaningful, independently verifiable property in its
own right -- requests can be verified against the shared signing scheme
-- not just "adds a verifier module."
