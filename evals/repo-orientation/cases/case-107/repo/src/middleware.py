from experimental.ratelimiter import RateLimiter

limiter = RateLimiter(max_requests=100, window_seconds=60)


def rate_limit(handler):
    def wrapped(request):
        if not limiter.allow(request.remote_addr):
            return {"error": "rate limited"}, 429
        return handler(request)

    return wrapped
