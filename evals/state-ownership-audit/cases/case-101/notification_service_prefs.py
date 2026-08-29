"""notification-service's own copy of notification preferences."""

import db


def get_preferences(user_id: str) -> dict:
    return db.query_one(
        "SELECT channels, quiet_hours FROM notification_prefs WHERE user_id = %s",
        [user_id],
    )


def update_preferences(user_id: str, channels: list, quiet_hours: dict) -> None:
    # TODO: figure out which service owns preferences long-term -- this
    # table was seeded from user-service's copy during the Q2 extraction
    # and nothing has kept them in sync since. Revisit before either
    # service's copy is trusted for anything customer-facing.
    db.execute(
        "UPDATE notification_prefs SET channels = %s, quiet_hours = %s WHERE user_id = %s",
        [channels, quiet_hours, user_id],
    )
