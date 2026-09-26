# DNS resolution check for ledger-svc.internal (checked 11:50 UTC)

Resolved from three separate `billing-api` pods, back to back: each
resolves `ledger-svc.internal` to the same current address in under 2ms,
consistent across all three lookups. No `SERVFAIL`, no stale/expired
cache entry, no mismatch between pods.

For comparison: the March incident Priya's note refers to (internal
ticket PAY-0940, closed) was a stale resolver cache on a small number of
`billing-api` pods after a DNS record change, cleared by a resolver
restart -- a different mechanism than anything observed here, and there
has been no DNS record change for `ledger-svc.internal` recently (last
change: 2026-01-14, per its zone history).
