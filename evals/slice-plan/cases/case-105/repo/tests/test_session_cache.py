from app.cache import session_cache
from app.cache.cleanup_job import expire_stale_sessions


def test_set_and_get():
    session_cache.set("s1", {"user_id": 1}, now=1000.0)
    assert session_cache.get("s1") == {"user_id": 1}


def test_expire_stale_session():
    session_cache.set("s2", {"user_id": 2}, now=0.0)
    expired = expire_stale_sessions(now=1000.0, max_age_seconds=100.0)
    assert "s2" in expired
    assert session_cache.get("s2") is None
