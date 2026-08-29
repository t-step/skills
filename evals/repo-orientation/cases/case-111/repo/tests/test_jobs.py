from src.jobs import run_daily_digest


def test_run_daily_digest_returns_summary():
    assert "digest" in run_daily_digest()
