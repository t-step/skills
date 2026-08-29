# Verification evidence

```
$ pytest db/test_client.py -v --staging-db
db/test_client.py::test_ten_concurrent_queries_reuse_pool PASSED

1 passed in 0.31s
```

Staging connection log for the test run confirms exactly 10 physical
connections were opened (matching pool size) and reused across the 10
concurrent query threads, with no new connections opened mid-test. No test
was run above 10 concurrent callers (i.e. what happens when demand exceeds
the pool size was not exercised).
