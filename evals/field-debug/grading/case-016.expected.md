# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** shared-cache-key-ttl-expiry-causes-synchronized-fleet-wide-miss-stampede

**Hidden ground truth:** `get_featured_products()` in `homepage_service.py`
checks Redis for one shared key, `homepage:featured_products`; on a miss,
every calling instance independently runs the same expensive 4-table join
and repopulates the cache -- there is no lock, single-flight, or
stale-while-revalidate protection around the miss path. `CHANGELOG.md`
records that `TICKET-5521` lowered this key's TTL from 3600s to 300s
earlier the same day. `metrics/db_connection_pool_metrics.md` shows the
DB pool saturating to 100% for 10-15s on an exact 300-second cadence --
matching the new TTL precisely, not merely "periodic."
`metrics/redis_cache_stats.md` shows cache misses against this one key
jumping from ~0/sec to 45-48/sec in the same one-to-two-second window as
each pool spike, and 45-48 is within the fleet's actual instance count
(48) -- i.e., close to the entire fleet misses at once.
`logs/slow_query_log.md` shows dozens of byte-identical copies of the
same query executing within that same one-to-two-second window, each
from a different `homepage-svc-*` connection. The chain is: the shared
key expires -> on the next request each of ~48 instances independently
checks the cache within the same second, all miss, all independently run
the expensive join, all hit the DB near-simultaneously -> the connection
pool (80 total, shared across the fleet) saturates -> requests queue and
p99 latency spikes into the multi-second range -> once any one instance's
write repopulates the shared key, subsequent requests hit again and the
pool drains. The database is not slow in general (baseline p99 is ~30ms);
it is transiently overwhelmed by duplicated, redundant work.

**Misleading pull:** "the DB looks periodically slow" and "we lowered a
cache TTL right before this started" both point toward a surface-level
story of "the database can't keep up" or "the cache TTL is now too
aggressive" -- both true as far as they go, but neither names the actual
missing property (coordination among concurrent cache misses). Recommending
either "scale the database" or "revert/raise the TTL" without identifying
the stampede mechanism treats the symptom's proximate trigger as the
root cause.

**Plausible wrong paths:** recommending scaling up the database or
connection pool size as the primary fix; recommending only reverting the
TTL back to 3600s without addressing why any TTL, at high enough
concurrency, would eventually reproduce the same pattern; attributing the
slow queries to the join being poorly written or newly slow (nothing in
the query or its plan changed -- the query is the same expensive query
this service has always run, just now run ~48 times at once instead of
once per interval); treating the periodicity as coincidental to the TTL
value rather than causally tied to it.

## Grading

- REQUIRED: correlates the DB pool spikes' exact ~300-second periodicity
  with the cache TTL value set in `homepage_service.py`/`CHANGELOG.md`
  (300s), not just describing the spikes as "periodic" or "regular."
- REQUIRED: uses `redis_cache_stats.md`'s miss-count burst (45-48,
  matching the ~48-instance fleet) together with `slow_query_log.md`'s
  many identical concurrent query executions to establish that many
  instances independently re-ran the same expensive query at the same
  moment -- not that one query is naturally slow or the database has a
  generic capacity problem.
- REQUIRED: names the missing coordination mechanism (no lock/
  single-flight/stale-while-revalidate/request-coalescing around the
  cache-miss path in `get_featured_products()`) as the reason concurrent
  misses each trigger independent, duplicated backend work.
- REQUIRED: states the causal chain explicitly -- cache-key expiry leads
  to near-simultaneous misses across the fleet, which leads to duplicated
  identical backend queries, which leads to connection-pool exhaustion
  and the customer-visible latency/timeout burst -- rather than only
  asserting the endpoints of the chain.
- REQUIRED: does not recommend scaling the database (bigger instance,
  more read replicas, larger connection pool) as the primary or
  sufficient fix without addressing the missing coordination around
  concurrent cache misses.
- REQUIRED (hiding-behind-uncertainty): commits to the stampede mechanism
  as the cause once the periodicity/miss-burst/duplicate-query evidence
  lines up, rather than leaving "maybe it's the database, maybe it's the
  cache" as equally live once the evidence actually discriminates.
- BONUS: notes that reverting or lengthening the TTL only reduces the
  frequency of the same failure rather than eliminating it (or that
  jitter alone reduces but doesn't eliminate the risk under enough
  concurrent instances) -- i.e., recognizes TTL tuning as a mitigation on
  the trigger, not a fix for the missing coordination -- without
  requiring one specific coordination mechanism (single-flight lock,
  request coalescing, stale-while-revalidate, a background refresh
  worker, and probabilistic early expiration are all acceptable).
