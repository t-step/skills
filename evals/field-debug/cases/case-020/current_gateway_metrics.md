# orders-svc -> partner-erp-gateway metrics (pulled just now, 10:50 UTC)

**Window**: 10:35-10:50 UTC (last 15 minutes).

**Overall failure rate**: 34% of outbound calls to partner-erp-gateway
are failing with 502/504, up sharply from the ~9% blended rate observed
during the 40%-canary window. Since 100% of pods are now on v3.15, there
is no per-version split to compute anymore -- every pod is running the
same code Jordan already found in `outbound_gateway_client.py`.

**partner-erp-gateway's public status page** (checked just now): no
active incidents reported. Their most recent posted incident was 3 weeks
ago and unrelated (a scheduled maintenance window for an unrelated
region).

**orders-svc's own outbound connection-pool metrics**: still normal, no
exhaustion or queueing signal -- unchanged from what Jordan already
observed.
