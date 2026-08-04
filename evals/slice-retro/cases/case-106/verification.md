# Verification evidence

```
$ pytest worker/test_loop.py -v
worker/test_loop.py::test_completed_job_ids_stay_bounded PASSED

1 passed in 0.22s
```

Also ran a local repro: process RSS memory sampled every 500 jobs over
10,000 synthetic jobs. Before the change, RSS grew roughly linearly from
80MB to 340MB over the run. After the change, RSS stays flat at ~85MB for
the whole run.

No data was collected on the scheduler pods' OOM-kill history or on
whether this worker's memory pattern is related to those incidents.
