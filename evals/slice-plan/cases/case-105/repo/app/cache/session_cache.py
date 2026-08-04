"""In-memory session cache. All access MUST go through get()/set()/
invalidate() -- never touch _store directly -- because those functions
also update _last_touched, which the cleanup job relies on to expire
stale sessions.
"""

_store: dict[str, dict] = {}
_last_touched: dict[str, float] = {}


def get(session_id: str) -> dict | None:
    return _store.get(session_id)


def set(session_id: str, data: dict, now: float) -> None:
    _store[session_id] = data
    _last_touched[session_id] = now


def invalidate(session_id: str, now: float) -> None:
    _store.pop(session_id, None)
    _last_touched.pop(session_id, None)
