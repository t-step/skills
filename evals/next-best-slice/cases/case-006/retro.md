# Slice Retrospective: Add in-process LRU cache in front of `/api/recommendations`

## What we proved
The LRU cache correctly serves a cached response on hit and evicts the
oldest entry once 128-entry capacity is reached — backed by the three
passing unit tests. In a 10-minute staging load test against
production-like traffic, it achieved a 40% hit rate and p95 latency of
178ms.

## Assumptions validated
The cache mechanics themselves — hit, miss, and eviction — work exactly as
implemented.

## Assumptions falsified
The core premise this slice was built on — that a simple in-process LRU
cache alone would bring this endpoint's p95 under the 50ms target — is
falsified by the measured 178ms result.

## Remaining uncertainty
Why hit rate is only 40% hasn't been root-caused. Three live hypotheses:
the 128-entry capacity is too small for the working set, the key space is
larger than expected, or this endpoint's traffic genuinely isn't repetitive
enough for any single-process cache to help much.

## Intentional non-goals
Any shared or distributed cache was out of scope for this slice per
goal.md, which specifically scoped it to "try the simplest thing first
before reaching for shared infrastructure."

## Architectural consequences
An injectable `Cache` interface now sits in front of this endpoint. A
future implementation (different capacity, different eviction policy, a
shared backend) can be swapped in without touching the endpoint's own code.

## Follow-up questions
Is the low hit rate a sizing problem, a key-space problem, or evidence that
this traffic pattern isn't cacheable at all with a single-process approach?
