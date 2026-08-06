"""Writes audit trail entries. The attribution report (finance/
compliance) is built from these entries and needs to know who or what
triggered each one -- an entry missing that shows up as a gap in that
report."""

_EVENTS = []


def record_event(event_type: str, payload: dict) -> None:
    _EVENTS.append({"event_type": event_type, "payload": payload})


def all_events() -> list:
    return list(_EVENTS)
