"""profiles service. This is the only code in profiles that touches
UserProfile.email anywhere -- there is no "change email" endpoint, form,
or admin action in profiles itself, and no validation of email format or
uniqueness lives here."""

import db
import event_bus


def on_email_changed(event: dict) -> None:
    """Subscribed to auth's user.email_changed event. Copies whatever auth
    reports into profiles' own table."""
    db.execute(
        "UPDATE user_profiles SET email = %s WHERE user_id = %s",
        [event["email"], event["user_id"]],
    )


event_bus.subscribe("user.email_changed", on_email_changed)
