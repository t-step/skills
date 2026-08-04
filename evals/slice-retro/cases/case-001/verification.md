# Verification evidence

```
$ pytest net/test_client.py -v
net/test_client.py::test_succeeds_after_two_failures PASSED
net/test_client.py::test_raises_after_exhausting_attempts PASSED

2 passed in 0.03s
```

The first test also asserts the recorded `sleep` calls were `0.1` then `0.2`
seconds (mocked, not actually slept), matching the backoff formula.
