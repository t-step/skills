# Verification evidence

First pass — the targeted regression test for issue #482 (concurrent
`increment()` only, no concurrent `flush()`):

```
$ pytest metrics/test_counters.py::test_concurrent_increments_no_lost_updates -v
metrics/test_counters.py::test_concurrent_increments_no_lost_updates PASSED

1 passed in 0.18s
```

Second pass — a more thorough test added afterward that also exercises
`flush()` running concurrently with `increment()` (5 trials):

```
$ pytest metrics/test_counters.py::test_concurrent_increment_and_flush -v
metrics/test_counters.py::test_concurrent_increment_and_flush FAILED

trial 2: got 49987, expected 50000

AssertionError: trial 2: got 49987, expected 50000
1 failed in 0.61s
```

Re-run 4 more times: 3 of those 4 reruns passed all 5 trials; 1 rerun failed
on trial 4 with `got 49991, expected 50000`. The discrepancy reproduces
intermittently, only in the concurrent-flush scenario, not in the
increment-only scenario.
