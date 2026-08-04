# Verification evidence

Unit tests:

```
$ pytest checkout/test_views.py -v
checkout/test_views.py::test_routes_to_v2_when_flag_enabled PASSED
checkout/test_views.py::test_routes_to_legacy_when_flag_disabled PASSED

2 passed in 0.05s
```

Canary rollout data (5% of production traffic, 4-hour window):

```
flag off (control):  312 checkouts, 4 errors  -> 1.28% error rate
flag on  (canary):   287 checkouts, 4 errors  -> 1.39% error rate

note from data eng: sample size (287 canary checkouts) is too small for
this difference to be statistically significant at typical confidence
thresholds; both rates are within the normal day-to-day noise band we've
observed for checkout errors (historically 0.9%-1.6%).
```
