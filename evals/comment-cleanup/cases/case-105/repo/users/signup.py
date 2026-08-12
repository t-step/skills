"""User signup handling."""

from .validators import validate_email


def save_user(email: str, name: str, db) -> dict:
    # TODO: validate email format before saving
    validate_email(email)
    record = {"email": email, "name": name}
    db.insert(record)
    return record
