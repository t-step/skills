"""user-service's own copy of notification preferences -- predates the
extraction of notification-service into its own repo."""

import db


def get_preferences(user_id: str) -> dict:
    return db.query_one(
        "SELECT channels, quiet_hours FROM user_notification_prefs WHERE user_id = %s",
        [user_id],
    )


def update_preferences(user_id: str, channels: list, quiet_hours: dict) -> None:
    db.execute(
        "UPDATE user_notification_prefs SET channels = %s, quiet_hours = %s WHERE user_id = %s",
        [channels, quiet_hours, user_id],
    )
