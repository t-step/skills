"""auth service. Owns the customer-facing "change my email" flow."""

import db
import event_bus


def request_email_change(user_id: str, new_email: str) -> None:
    """The only place an email change originates. Validates format and
    uniqueness, requires a confirmation step (not shown), and on
    confirmation is the only code path anywhere in this system that writes
    users.email."""
    if "@" not in new_email:
        raise ValueError("invalid email format")

    existing = db.query_one("SELECT id FROM users WHERE email = %s", [new_email])
    if existing is not None:
        raise ValueError("email already in use")

    db.execute("UPDATE users SET email = %s WHERE id = %s", [new_email, user_id])

    # Tells the rest of the system this happened. profiles is one of the
    # consumers of this event.
    event_bus.publish("user.email_changed", {"user_id": user_id, "email": new_email})
