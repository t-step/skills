# ledger-svc inbound security group (current)

```
# ledger-svc-inbound-sg
allow tcp/8443 from 10.2.4.0/24   # billing-api pool (added 2025-06-11, ticket PAY-1187)
allow tcp/8443 from 10.2.9.0/24   # internal admin tooling
deny all
```

**Last modified**: 2025-06-11. No changes since -- more than three
months before this morning's deploy or this incident.

`billing-api`'s current pod IP pool is `10.2.4.0/24` -- unchanged since
well before this incident (no gateway/pod-IP-reassigning redeploy has
happened for `billing-api` recently, unlike its own last redeploy this
morning which was a routine in-place rolling update with no IP-pool
change).
