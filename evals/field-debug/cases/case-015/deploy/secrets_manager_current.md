# Secrets manager -- current state for checkout-svc

```
$ secrets-cli show checkout-svc/PAYMENT_API_KEY
name:            checkout-svc/PAYMENT_API_KEY
current_version: v14
rotated_at:       2026-09-19T09:00:03Z
previous_version: v13 (revoked at rotation time, per SEC-2291's rotation policy -- PaymentCo invalidates the prior key the moment the new one is issued, it does not run both in parallel)
```

`PAYMENT_API_KEY` is injected into each pod's environment at container
start from whichever secret version was current *at that pod's start
time* -- a pod does not re-fetch the secret after starting. A pod
started before `09:00:03Z` on 2026-09-19 has `v13` (now revoked) baked
into its environment; a pod started at or after that time has `v14`.
