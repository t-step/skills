from app.cache import session_cache


def expire_stale_sessions(now: float, max_age_seconds: float) -> list[str]:
    """Runs periodically; relies on _last_touched being accurate for
    every session in _store to decide what to expire.
    """
    expired = []
    for session_id, touched_at in list(session_cache._last_touched.items()):
        if now - touched_at > max_age_seconds:
            session_cache.invalidate(session_id, now)
            expired.append(session_id)
    return expired
