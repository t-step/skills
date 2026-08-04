# Verification evidence

```
$ pytest search/test_views.py -v
search/test_views.py::test_search_returns_matching_articles PASSED
search/test_views.py::test_search_caps_at_20_results PASSED

2 passed in 0.41s
```

Both tests run against a small fixture dataset (30 articles). No test was
run against the production-sized article table (~140,000 rows).
