from experimental.ratelimiter import RateLimiter


def test_allows_up_to_max_requests():
    limiter = RateLimiter(max_requests=2, window_seconds=60)
    assert limiter.allow("a")
    assert limiter.allow("a")
    assert not limiter.allow("a")
