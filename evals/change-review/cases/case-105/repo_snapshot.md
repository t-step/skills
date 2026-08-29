# Repo snapshot (files relevant to this change, as they stand AFTER the diff below is applied)

## rate_limiter/legacy.py (unchanged by this diff — still present)
```python
class LegacyRateLimiter:
    @staticmethod
    def check(request):
        # old live-traffic rate-limiting path — no longer called from
        # api/middleware.py as of this diff
        ...

    @staticmethod
    def parse_legacy_config(raw_config: str) -> dict:
        """Parses the pre-2024 INI-style rate-limit config format.

        Kept because admin/legacy_config.py still needs to read old config
        files uploaded by customers who haven't migrated to the new YAML
        format yet — this is a config-file parser, unrelated to live
        request rate limiting. See ADR-042 for why this stays until the
        legacy-config migration project (tracked separately) finishes.
        """
        ...
```

## rate_limiter/token_bucket.py (new, added by this diff)
```python
import time


class TokenBucketRateLimiter:
    CAPACITY = 10
    REFILL_PER_SEC = 1.0

    _buckets = {}

    @staticmethod
    def check(request):
        key = getattr(request, "client_id", "global")
        now = time.monotonic()
        tokens, last = TokenBucketRateLimiter._buckets.get(
            key, (TokenBucketRateLimiter.CAPACITY, now)
        )
        tokens = min(
            TokenBucketRateLimiter.CAPACITY,
            tokens + (now - last) * TokenBucketRateLimiter.REFILL_PER_SEC,
        )
        allowed = tokens >= 1
        TokenBucketRateLimiter._buckets[key] = (tokens - 1 if allowed else tokens, now)
        return allowed
```

## api/middleware.py (changed by this diff)
```python
from rate_limiter.token_bucket import TokenBucketRateLimiter

def handle_request(request):
    if not TokenBucketRateLimiter.check(request):
        return Response("Too Many Requests", status=429)
    return next_handler(request)
```

## admin/legacy_config.py (NOT touched by this diff — exists elsewhere in the repo)
```python
from rate_limiter.legacy import LegacyRateLimiter

def import_customer_config(raw_upload: str) -> dict:
    """Admin tool: import an old-format rate-limit config file a customer
    uploaded, for accounts that haven't migrated to the new format yet."""
    return LegacyRateLimiter.parse_legacy_config(raw_upload)
```
