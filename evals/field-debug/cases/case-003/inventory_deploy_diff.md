# Deploy diff: inventory-svc, 14:30 UTC

```diff
--- a/inventory-svc/config/db.yaml
+++ b/inventory-svc/config/db.yaml
@@ -3,7 +3,7 @@ db:
   host: inventory-db.internal
   port: 5432
   pool:
-    max_size: 40
+    max_size: 25
     min_size: 5
     idle_timeout_s: 60
```

Changelog entry: "Right-sizing inventory-svc's DB pool -- 40 connections
was leftover from a load test and is larger than steady-state traffic
needs; dropping to 25 to free up headroom on the shared DB instance.
No behavior change expected."
