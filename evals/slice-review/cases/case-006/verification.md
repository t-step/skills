# Verification evidence

```
$ pytest auth/test_session.py -v
auth/test_session.py::test_valid_before_expiry PASSED
auth/test_session.py::test_expired_after_expiry PASSED
auth/test_session.py::test_expired_exactly_at_expiry PASSED

3 passed in 0.01s
```
