"""Password reset request handling."""

RESET_LIMIT_PER_HOUR = 5
_HOUR_SECONDS = 3600

_RESET_ATTEMPTS: dict[str, list[float]] = {}

_GENERIC_MESSAGE = "If that email is registered, a reset link has been sent."


def _prune_old_attempts(email: str, now: float) -> None:
    attempts = _RESET_ATTEMPTS.get(email, [])
    _RESET_ATTEMPTS[email] = [t for t in attempts if now - t < _HOUR_SECONDS]


def request_password_reset(email: str, now: float) -> dict:
    """Handle a password reset request for `email`.

    Rejects the 6th+ request for the same email within a rolling hour
    with a 429. Returns the same generic message on both the success
    and rate-limited paths so the response itself can't be used to
    enumerate registered emails.
    """
    _prune_old_attempts(email, now)
    attempts = _RESET_ATTEMPTS[email]
    if len(attempts) >= RESET_LIMIT_PER_HOUR:
        return {"status": 429, "message": _GENERIC_MESSAGE}
    attempts.append(now)
    send_reset_email(email)
    return {"status": 200, "message": _GENERIC_MESSAGE}


def send_reset_email(email: str) -> None:
    """Stub -- actual email delivery is out of scope for this module."""
    pass
