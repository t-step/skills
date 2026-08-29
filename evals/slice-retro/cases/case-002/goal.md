# Goal

`get_user_profile(user_id)` in `profiles/service.py` is too slow — p95
latency is 210ms, dominated by an upstream network fetch. The team believes
an in-process LRU cache (size 128) in front of it will bring p95 under the
50ms SLA target. Implement the cache and run the existing latency benchmark
script (`bench/profile_latency.py`) against it to confirm.
