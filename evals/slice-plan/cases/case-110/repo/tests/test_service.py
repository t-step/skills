import app.identity.client as identity_client
from app.profiles.models import ProfileCacheRow
from app.profiles.service import get_user_summary
from app.profiles.sync_consumer import _PROFILE_CACHE


def _seed(user_id="u1", phone_number=None):
    _PROFILE_CACHE[user_id] = ProfileCacheRow(
        user_id=user_id,
        display_name="Ada Lovelace",
        email="ada@example.com",
        phone_number=phone_number,
        plan_tier="pro",
        updated_at="2026-08-01T00:00:00Z",
    )


def test_get_user_summary_reads_only_from_cache(monkeypatch):
    _seed()

    def _blocked(*args, **kwargs):
        raise AssertionError("get_user_summary must not perform network calls")

    monkeypatch.setattr(identity_client.requests, "get", _blocked)

    summary = get_user_summary("u1")

    assert summary.display_name == "Ada Lovelace"
    assert summary.plan_tier == "pro"


def test_get_user_summary_missing_user_raises():
    try:
        get_user_summary("does-not-exist")
        assert False, "expected KeyError"
    except KeyError:
        pass
