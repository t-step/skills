# SEC-2291: PaymentCo API key rotation -- rollout controller log

`checkout-svc` runs as 8 replicas (`checkout-pod-01` through
`checkout-pod-08`) behind a load balancer. `PAYMENT_API_KEY` is delivered
as an environment variable from the secrets manager; picking up a new
value requires the pod to restart (there is no in-process reload path --
see `payment_client.py`). Key rotations are applied by triggering a
rolling restart of all 8 replicas, one at a time (`maxUnavailable: 1,
maxSurge: 0`), waiting for each new pod to pass its readiness probe
before moving to the next.

```
2026-09-19T09:00:03Z  secrets-manager: PAYMENT_API_KEY rotated (SEC-2291), new version=v14
2026-09-19T09:00:05Z  rollout-controller: starting rolling restart of checkout-svc (8 replicas)
2026-09-19T09:02:11Z  rollout-controller: checkout-pod-01 terminated, replacement scheduled
2026-09-19T09:03:47Z  rollout-controller: checkout-pod-01 (new) passed readiness probe
2026-09-19T09:03:50Z  rollout-controller: checkout-pod-02 terminated, replacement scheduled
2026-09-19T09:05:22Z  rollout-controller: checkout-pod-02 (new) passed readiness probe
2026-09-19T09:05:25Z  rollout-controller: checkout-pod-08 terminated, replacement scheduled
2026-09-19T09:07:01Z  rollout-controller: checkout-pod-08 (new) passed readiness probe
2026-09-19T09:07:04Z  rollout-controller: checkout-pod-04 terminated, replacement scheduled
2026-09-19T09:11:04Z  rollout-controller: checkout-pod-04 (new) FAILED readiness probe (4/4 attempts, warm-cache dependency timeout -- unrelated to PAYMENT_API_KEY)
2026-09-19T09:11:04Z  rollout-controller: rollout PAUSED -- 3/8 replicas updated (checkout-pod-01, checkout-pod-02, checkout-pod-08), 5/8 replicas not yet restarted (checkout-pod-03, checkout-pod-04, checkout-pod-05, checkout-pod-06, checkout-pod-07)
2026-09-19T09:11:04Z  rollout-controller: awaiting manual resume (paused rollouts do not auto-retry)
```

No entry after `09:11:04Z` exists in this log -- the rollout has not been
manually resumed since it paused.
