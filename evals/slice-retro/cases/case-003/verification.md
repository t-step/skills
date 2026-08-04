# Verification evidence

Unit test:

```
$ pytest notify/test_digest.py -v
notify/test_digest.py::test_batch_continues_after_individual_failure PASSED

1 passed in 0.02s
```

Staging dry-run against a snapshot of 500 real (fake/test) subscribed users,
with the staging SMTP relay intentionally rate-limited to reproduce some
real-world timeouts:

```
$ python -m notify.digest --dry-run-staging
sent: 480
failed: 20  (all logged as: smtp timeout)
batch completed without raising, total runtime 41s
```

No run was performed with the SMTP relay fully unavailable (0/500
succeeding). Email body rendering was checked once, visually, for a single
sample user's output in the staging run; the other 479 rendered bodies were
not individually inspected.
