# payments-svc inbound security group (current, attached by NetOps)

```
# payments-svc-inbound-sg
allow tcp/443 from 10.4.2.0/24   # checkout-bff gateway pool (added 2025-11-03, ticket INFRA-2201)
allow tcp/443 from 10.4.9.0/24   # internal admin tooling
deny all
```

Last modified: 2025-11-03. No changes since.
