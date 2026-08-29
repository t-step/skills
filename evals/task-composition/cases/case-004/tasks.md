# Tasks: Per-Endpoint Rate Limiting

This is the complete plan and task list for this piece of work, in the
order it was written down. There is no other backlog, roadmap, or
context beyond what's written here.

- T1: Add a `RateLimiter` class in `middleware/rate_limit.py` with a
  `check(key, limit) -> bool` method.
- T2: Wire `RateLimiter` into `api/search.py`'s search endpoint, calling
  `check(user_id, limit=cfg.search_rate_limit)` before running the
  search.
- T3: Add a `search_rate_limit` field (default `30`) to the config
  schema in `config/schema.py`. T2's code reads `cfg.search_rate_limit`
  from this field.
- T4: Add test `tests/test_search_rate_limit.py` covering T2: requests
  over `cfg.search_rate_limit` are rejected, requests under it are not.

No priority is stated for this list beyond the order the tasks are
numbered in.
