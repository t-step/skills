# case-003 — mixed-repo-discrimination

**In-contract expectation:** this fixture combines both signals in one
pass. `LocalCache` is a generic LRU-with-TTL cache — a textbook commodity
pattern — used for an ordinary, non-domain-specific purpose (caching
product lookups by ID), with no comment, no ADR, no rationale beyond a
bare commit message. It should be flagged. `apply_tier_pricing()`
resembles "pricing engine" vocabulary but is tightly coupled to this
project's own `Contract.tiers` data model, with an inline comment
explaining why no general library fits. It should NOT be flagged. The
real test is whether both calls are made correctly in a single audit
pass, not just one or the other in isolation.

**Pass requires:**
1. Flags `app/cache/local_cache.py`'s `LocalCache` as a finding (missing
   decision evidence, resembles a general LRU/TTL cache pattern used for
   a generic purpose).
2. Does NOT flag `app/pricing/tier_calculator.py`'s `apply_tier_pricing()`
   — lists it under "considered, not flagged," citing its coupling to
   `Contract.tiers` and/or its inline rationale comment.
3. The `LocalCache` finding's recommendation is to re-run build-vs-adopt,
   not a prescribed replacement.
4. Both determinations are correct in the same response — a response that
   gets only one of the two right does not fully pass this case.
