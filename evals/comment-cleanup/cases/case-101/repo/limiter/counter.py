"""Simple counters used by the request-rate limiter."""


def increment(x: int) -> int:
    # add 1 to x
    return x + 1


def decrement_floor(x: int, floor: int = 0) -> int:
    # never let the counter go below floor — callers (see rate_limiter.py)
    # treat a negative count as "unlimited remaining", so clamping here
    # prevents an underflow from silently disabling the rate limit
    return max(floor, x - 1)
