"""Field validators shared across signup and profile-update flows."""

import re

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def validate_email(email: str) -> None:
    """Raise ValueError if `email` is not a syntactically valid address."""
    if not EMAIL_RE.match(email):
        raise ValueError(f"invalid email format: {email!r}")
