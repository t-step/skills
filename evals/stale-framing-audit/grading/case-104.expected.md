# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** cumulative-individually-plausible-statements

**Why:** cache_docs.md's "Caching" section, about get_summary(), is
actually accurate -- it really does consult the cache. An agent that reads
the Overview, spot-checks the one function the Overview's framing points
at (an aggregate-sounding get_summary()), confirms it matches, and stops
has done a plausible-looking but incomplete audit: store.py shows get()
and get_by_id_range() route through the exact same _read_through()
cache-first helper as get_summary(), directly contradicting the API
reference's "Bypasses the cache for consistency" claim for both, and
contradicting the Overview's "by default, reads go straight to the primary
datastore" framing as a general description of the read path. This case
specifically tests whether the audit checks every claim a doc makes
against the code, not just the one claim that happens to be true and
easiest to verify. A correct report identifies that all three read
functions are cache-first, names both the API-reference bullets and the
Overview framing as contradicted (not just one), and states plainly that
no function here currently provides an uncached read -- directly relevant
to the engineer's stated need for a strongly consistent read.
