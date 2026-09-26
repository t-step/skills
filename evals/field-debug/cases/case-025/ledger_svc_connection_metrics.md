# ledger-svc inbound connection metrics (from ledger-svc's own dashboard)

**Window**: 08:30-11:45 UTC.

Inbound connection *attempts* from `billing-api`'s pool
(`10.2.4.0/24`) are flat across the whole window -- no drop in attempts,
no spike in resets, no spike in refused connections. `ledger-svc` itself
reports normal request volume and normal latency for the connections it
does receive; its own error rate is unchanged from baseline.

From `ledger-svc`'s side, this whole incident is invisible -- it is
receiving and successfully handling every connection `billing-api`
actually sends it. (Consistent with `billing_api_app_errors.md`: the
failing 40% never leave `billing-api`'s process, so `ledger-svc` never
sees an attempt for them at all.)
