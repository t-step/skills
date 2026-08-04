# Verification evidence

```
$ pytest auth/test_login.py -v
auth/test_login.py::test_failed_login_increments_attempts PASSED
auth/test_login.py::test_successful_login_resets_attempts PASSED

2 passed in 0.01s
```

No test was run or shown for `auth/session.py` / `SESSION_TTL`.
