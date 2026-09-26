# Deploy diff: platform-svc v2.3.0 -> v2.3.1, 2026-09-24 ~16:00 UTC

```diff
--- a/platform-svc/requirements.txt
+++ b/platform-svc/requirements.txt
@@ -12,7 +12,7 @@
-structlog==23.1.0
+structlog==24.4.0

--- a/platform-svc/health.py
+++ b/platform-svc/health.py
@@ -1,5 +1,5 @@
 HEALTH_CHECK_TIMEOUT_S = 5
-READINESS_TIMEOUT_S = 2
+READINESS_TIMEOUT_S = 3
```

Changelog entry: "Bump structlog for a CVE fix; slightly relax readiness
probe timeout after a couple of flaky-probe pages last week. No behavior
changes to any request-serving or job code."

This diff touches only logging-library version and a k8s readiness-probe
timeout constant. It does not touch, import, or share any module with
either the search-indexing path or the analytics-export job below.
