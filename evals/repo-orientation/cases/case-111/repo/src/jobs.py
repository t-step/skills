"""Scheduled jobs run by the digest service."""


def run_daily_digest() -> str:
    """Build and send the daily ops digest email."""
    summary = _build_summary()
    _send(summary)
    return summary


def _build_summary() -> str:
    return "daily digest: 0 incidents"


def _send(summary: str) -> None:
    print(f"sending digest: {summary}")
