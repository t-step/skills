"""The actual domain logic: turning a stream of generated_events.py
objects into Sessions and, when warranted, Anomalies."""

from datetime import datetime, timedelta
from dataclasses import dataclass, field

SESSION_GAP_MINUTES = 30
FAILED_LOGIN_ANOMALY_THRESHOLD = 5


@dataclass
class Session:
    """A run of events from the same user_id with no gap longer than
    SESSION_GAP_MINUTES between consecutive events. Not persisted directly
    -- recomputed by group_into_sessions() each time it's needed from the
    raw event stream."""

    user_id: str
    events: list = field(default_factory=list)


@dataclass
class Anomaly:
    """Persisted the moment it's detected -- the only row in this module
    written anywhere outside a pure function. Once created, nothing in
    this codebase ever deletes or updates one; a human dismisses it
    through a separate ops tool not included in this excerpt."""

    id: str
    session: Session
    reason: str
    detected_at: str


def group_into_sessions(events: list, gap_minutes: int = SESSION_GAP_MINUTES) -> list[Session]:
    sessions: list[Session] = []
    by_user: dict[str, list] = {}
    for event in sorted(events, key=lambda e: e.occurred_at):
        by_user.setdefault(event.raw["user_id"], []).append(event)
    gap = timedelta(minutes=gap_minutes)
    for user_id, user_events in by_user.items():
        current = None
        last_seen = None
        for event in user_events:
            occurred_at = datetime.fromisoformat(event.occurred_at)
            if current is None or occurred_at - last_seen > gap:
                current = Session(user_id=user_id)
                sessions.append(current)
            current.events.append(event)
            last_seen = occurred_at
    return sessions


def detect_anomalies(session: Session, store) -> list[Anomaly]:
    failure_type = "LoginFailureEvent"
    failures = [e for e in session.events if type(e).__name__ == failure_type]
    if len(failures) >= FAILED_LOGIN_ANOMALY_THRESHOLD:
        anomaly = Anomaly(id=store.next_id(), session=session,
                           reason=f"{len(failures)} failed logins in one session",
                           detected_at="now")
        store.save(anomaly)
        return [anomaly]
    return []
