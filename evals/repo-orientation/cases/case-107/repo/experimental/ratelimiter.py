import time


class RateLimiter:
    """Token-bucket rate limiter.

    Named `experimental/` from when this started as a spike.
    """

    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits: dict[str, list[float]] = {}

    def allow(self, key: str) -> bool:
        now = time.time()
        hits = [t for t in self._hits.get(key, []) if now - t < self.window_seconds]
        hits.append(now)
        self._hits[key] = hits
        return len(hits) <= self.max_requests
