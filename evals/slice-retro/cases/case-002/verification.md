# Verification evidence

Unit tests:

```
$ pytest profiles/test_service.py -v
profiles/test_service.py::test_second_call_hits_cache PASSED
profiles/test_service.py::test_cache_evicts_oldest_over_capacity PASSED

2 passed in 0.04s
```

Latency benchmark (`bench/profile_latency.py`, replays 20,000 real
production `get_user_profile` calls from yesterday's access log against a
staging instance with the cache warm):

```
$ python bench/profile_latency.py --replay logs/2026-08-01-profile-calls.jsonl
requests: 20000
distinct user_ids: 14,812
cache hits: 8,014 (40.1% hit rate)
cache misses: 11,986

p50: 42ms
p95: 178ms
p99: 205ms

target: p95 < 50ms — NOT MET
```
