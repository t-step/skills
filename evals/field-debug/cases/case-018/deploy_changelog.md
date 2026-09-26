# orders-svc deploy changelog

## v4.2.0 -- 2026-09-24 07:12 UTC

Routine dependency updates (`requests` 2.31 -> 2.32, `pydantic` 2.6 ->
2.7). Config template regenerated from the shared service-defaults repo
as part of the dependency bump tooling; diff below.

```diff
--- orders_svc_config.yaml (v4.1.3)
+++ orders_svc_config.yaml (v4.2.0)
@@ -1,6 +1,6 @@
 inventory_service:
   host: inventory-svc.internal
-  port: 443
+  port: 8443
   timeout_seconds: 5

 fulfillment:
```

No other files changed in this deploy.

## v4.1.3 -- 2026-09-11 14:03 UTC

Bugfix: correct retry backoff jitter calculation. No config changes.
