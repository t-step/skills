scenario_id: checkout-latency-2026-09-24

# Context

PagerDuty incident, checkout flow, opened 14:41 UTC:

> p99 latency on `POST /checkout` jumped from ~200ms to ~4s starting
> around 14:32 UTC. Nothing is erroring -- requests are just slow.
> Checkout goes browser -> `web-bff` -> `pricing-svc` -> `inventory-svc`.
> Two things landed around the same window: `inventory-svc` shipped a
> connection-pool config change at 14:30, and `pricing-svc` shipped a new
> tax-rate lookup at 14:15 (already running in prod for ~15 minutes
> before things got slow, so maybe unrelated, maybe a delayed effect).
> Which one is it, and can you show your work?

Files in this directory are the complete evidence available for this
incident. **Log aggregation for both services was down from 14:20 to
15:00 UTC during this incident (an unrelated, already-known outage in the
logging pipeline)** -- no application request logs exist for this window.
Traces, metrics, and source code are available; logs are not.
