"""Notification channel registry and shared send-path guard."""

from core.rate_limit import RateLimiter

_CHANNELS = {}
_limiter = RateLimiter(max_per_minute=30)


def register_channel(name):
    def decorator(cls):
        _CHANNELS[name] = cls
        return cls

    return decorator


class NotificationChannel:
    """Base class for anything that can deliver a notification.

    Subclasses implement _deliver(message). send() is the only entry
    point callers should use -- it wraps _deliver with the shared rate
    limiter so no single channel can flood a downstream provider.
    """

    def send(self, message):
        with _limiter.guard(self.__class__.__name__):
            self._deliver(message)

    def _deliver(self, message):
        raise NotImplementedError


def get_channel(name):
    return _CHANNELS[name]()
