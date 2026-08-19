import contextlib


class RateLimiter:
    """Caps how often any single caller can proceed per minute.

    Used to keep a bad event storm from hammering an outbound provider
    (email/SMS/whatever) and getting the account throttled or banned.
    """

    def __init__(self, max_per_minute):
        self.max_per_minute = max_per_minute
        self._counts = {}

    @contextlib.contextmanager
    def guard(self, key):
        # (rate accounting omitted for this fixture)
        yield
