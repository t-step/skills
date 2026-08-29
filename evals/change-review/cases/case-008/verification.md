# Verification evidence

```
$ pytest jobs/test_worker.py -v
jobs/test_worker.py::test_run_job_succeeds_first_try PASSED
jobs/test_worker.py::test_run_job_raises_after_max_retries PASSED
jobs/test_worker.py::test_run_job_succeeds_after_transient_failure PASSED

3 passed in 3.02s
```

(The 3.02s runtime is consistent with the new backoff sleeps: the two tests
that hit retries each incur ~1.5s of real `time.sleep` from the diff's
`0.5 * (attempt + 1)` backoff.)
