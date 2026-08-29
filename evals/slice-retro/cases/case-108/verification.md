# Verification evidence

```
$ pytest db/test_connection.py -v
db/test_connection.py::test_succeeds_after_one_retry PASSED
db/test_connection.py::test_raises_after_three_failed_attempts PASSED

2 passed in 0.03s
```
