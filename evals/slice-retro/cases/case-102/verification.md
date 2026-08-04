# Verification evidence

```
$ pytest validation/test_email.py -v
validation/test_email.py::test_rejects_missing_at_sign PASSED
validation/test_email.py::test_rejects_double_at_sign PASSED
validation/test_email.py::test_rejects_empty_string PASSED
validation/test_email.py::test_rejects_missing_domain PASSED
validation/test_email.py::test_accepts_ordinary_address PASSED

5 passed in 0.02s
```

None of the 5 tests use a string with consecutive dots in the local or
domain part (e.g. `"a..b@example.com"`), which the regex `[^@\s]+` does not
reject.
