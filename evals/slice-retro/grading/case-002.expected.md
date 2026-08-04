# Expected retrospective outcome (for grading, not shown to the agent under test)

**Scenario:** disproves-assumption

**Why:** The stated goal explicitly frames the cache as a bet against an
assumption ("the team believes... will bring p95 under 50ms... confirm").
The benchmark evidence directly contradicts that belief (178ms observed vs
50ms target, 40% hit rate). This is a clean falsified-assumption case, but
it has a trap: a sloppy retrospective might conflate "the SLA wasn't met"
with "the cache is broken," when in fact the cache mechanics themselves
(hit avoids re-fetch, LRU eviction at capacity) are correctly implemented
and directly verified by the two passing unit tests. Grounded in
SKILL.md's evidence-tier discipline: the falsified assumption is the
specific premise the goal stated, not a global verdict on the diff's
quality.
