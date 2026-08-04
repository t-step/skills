# Verification evidence

The author ran the new test file and pasted this output:

```
$ pytest email/test_send_queue.py -v
email/test_send_queue.py::test_email_service_enqueues PASSED

1 passed in 0.01s
```

No test was run against `password_reset.py`, and it is not mentioned in the
diff or the PR description.
