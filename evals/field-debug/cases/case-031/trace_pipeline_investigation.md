# Internal investigation notes

**Clock skew between checkout-svc and payment-capture-svc:** ruled out.
NTP sync check on both services shows drift under 5ms, far below Beacon's
documented span-linking tolerance window (2s).

**Recent SDK/config change:** ruled out as the trigger. `git log` on
`beacon-sdk` pinning in checkout-svc's dependency file shows no change in
the last 45 days; the affected requests only started appearing 6 days ago,
so a stale SDK version can't be the cause on its own.

**Pattern isolated:** every `payment_capture_span_missing` request sampled
so far is routed through `async_worker route` -- the code path where
payment capture is dispatched to a background worker rather than called
inline (`sync_route`). Beacon's SDK docs (available separately) describe
trace-context propagation as automatic for synchronous calls, and note
that async/background dispatch requires the caller to manually re-inject
the trace context into the worker's job payload -- code review confirms
`async_worker route`'s job-enqueue call does pass a `trace_context` field,
so propagation is *attempted*, but there is no way from Northwind's side
to see whether Beacon's collector actually receives and links both spans
correctly for a request shaped this way, or silently drops the
child-span link under some condition on its ingestion side.

This is as far as internal evidence can take it: the pattern (async
dispatch path) is real and reproducible, but confirming *why* Beacon's
collector fails to link these specific spans requires visibility into
Beacon's own ingestion pipeline, which Northwind cannot see.
