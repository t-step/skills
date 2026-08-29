# Verification evidence

```
$ pytest api/test_middleware.py -v
api/test_middleware.py::test_allows_request_under_limit PASSED
api/test_middleware.py::test_blocks_when_rate_limited PASSED

2 passed in 0.01s
```
