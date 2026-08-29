# Repo snapshot: notifications/dedup.py (full file, AFTER the diff below is applied)

```python
"""Notification dedup helpers."""

DEDUP_WINDOW_SECONDS = 3600


def record_event(user_id: str, event_key: str, ts: int, event_log: dict) -> None:
    """Record that `event_key` occurred for `user_id` at `ts`, for audit history."""
    event_log[(user_id, event_key)] = ts


def should_send_notification(usr_id: str, event_key: str, sent_log: dict, now_ts: int) -> bool:
    """Return True if a notification for this event should be sent now.

    Per the dedup contract: the same event must not be re-sent to the same
    user within the dedup window, but different users must always receive
    their own notifications independently of each other.
    """
    window = DEDUP_WINDOW_SECONDS
    last_ts = sent_log.get(event_key)
    if last_ts is None:
        return True
    elapsed = now_ts - last_ts
    return elapsed >= window


def mark_sent(usr_id: str, event_key: str, sent_log: dict, now_ts: int) -> None:
    """Record that a notification for this event was just sent."""
    sent_log[event_key] = now_ts
```
