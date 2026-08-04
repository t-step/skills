# Plan

Add per-IP rate limiting to `middleware.py`: reject requests beyond 100 per
60-second window per IP, returning HTTP 429. The plan was to use the
`redis-py` token-bucket recipe from Redis's docs so the limiter state is
shared correctly across all app instances in production (we run 4
instances behind a load balancer).
