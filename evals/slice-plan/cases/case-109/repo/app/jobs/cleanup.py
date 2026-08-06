"""Scheduled maintenance jobs."""

from app.audit.logger import record_event


def purge_stale_sessions() -> int:
    purged_count = 7  # stand-in for real purge logic
    record_event("sessions_purged", {"count": purged_count})
    return purged_count
