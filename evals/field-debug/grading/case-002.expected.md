# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** checkout-latency-tax-vendor-blocking-call (full-telemetry
tier; paired with `case-003`, same underlying incident, logs unavailable
there -- see that grading file for the observability-degradation
comparison)

**Hidden ground truth:** the root cause is `pricing-svc`'s new
`get_tax_rate()` client (`pricing_svc_tax_client.py`, shipped 14:15 UTC)
calling the external tax-rate vendor with `requests.get()` and no
`timeout=` kwarg. The vendor's own endpoint started responding slowly
starting ~14:32 UTC (visible in `metrics_pricing_outbound.md`'s p50/p99
spike, and directly in the trace and log evidence for a representative
slow request) -- with no client-side timeout, pricing-svc simply waits as
long as the vendor takes, and that wait sits entirely on the checkout hot
path before `inventory.reserve` is ever called. `inventory-svc`'s pool
change (40 -> 25 connections) at 14:30 is a real, genuine change but a red
herring for this incident: its own wait-queue-depth metric stays at 0 the
entire window (never queuing for a connection) and its own p99 latency
metric is flat (~37-44ms) throughout -- the pool resize had no observable
effect on anything. The two changes are temporally close (14:15 and
14:30) but not causally related to each other or to the incident the same
way.

**Misleading clue:** the ticket's own framing ("maybe unrelated, maybe a
delayed effect") invites treating the pool change as at least a candidate
worth defending or attacking on priors, when the metrics settle it
directly and immediately (flat p99, zero queue depth) without needing any
inference at all.

**High-information probes, ranked:** (1) `metrics_inventory_pool.md`'s
wait-queue-depth and p99 latency series -- flat/zero rules out the pool
hypothesis outright, no inference required; (2) `trace_breakdown.md`'s
span breakdown -- shows essentially 100% of the added latency sits inside
`pricing_svc.get_tax_rate`, before `inventory.reserve` even starts; (3)
`metrics_pricing_outbound.md`'s p50/p99 spike, time-aligned to 14:32; (4)
`pricing_svc_tax_client.py`'s missing timeout as the mechanism that lets a
slow vendor response translate into unbounded checkout latency; (5)
`pricing_svc_logs.md`'s matching-trace-id log lines, which directly show
the 3.83s gap between the outbound call and its (successful, 200) response
with no retry or error anywhere.

**Plausible wrong paths:** naming the inventory-svc pool change as the
cause, or as a contributing cause, without checking its own metrics first;
treating "two changes landed close together" as license to blame both or
split the difference; assuming a slow-but-successful vendor call must
involve an error somewhere in pricing-svc's own logs (it doesn't -- the
call simply took 3.83s and returned 200).

## Grading

- REQUIRED: rules out the inventory-svc pool-size change as the cause,
  explicitly citing `metrics_inventory_pool.md`'s flat p99 and zero
  wait-queue-depth as the evidence -- not "it's probably fine" without a
  citation.
- REQUIRED: identifies `pricing_svc.get_tax_rate` (via the trace breakdown
  and/or the outbound-call metric) as where essentially all the added
  latency lives.
- REQUIRED: names the missing `timeout=` on the `requests.get()` call in
  `pricing_svc_tax_client.py` as the mechanism that lets a slow vendor
  response become unbounded checkout latency.
- REQUIRED: attributes the trigger to the tax-rate vendor's own slowdown
  starting ~14:32 (via the outbound-latency metric's timing), not to the
  14:15 deploy itself -- the deploy added the *exposure*, the vendor's
  slowdown at 14:32 is what *triggered* the incident; a report that
  conflates "the deploy caused it" with "the deploy created the
  vulnerable path that a later vendor slowdown then hit" should
  distinguish the two, but crediting either framing is acceptable as long
  as both facts (deploy time and vendor-slowdown time) are cited
  correctly.
- REQUIRED: does not present both the pool change and the tax-rate call as
  co-equal, undifferentiated candidates in the final answer -- the report
  discriminates, it doesn't hedge across both.
- BONUS: proposes a fix scoped to the actual mechanism (add a client-side
  timeout, and/or move the call off the synchronous hot path) rather than
  a generic "improve resilience" gesture.
