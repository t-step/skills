"""Username validation used at signup."""

MIN_LENGTH = 3


def validate_username(username: str) -> list[str]:
    """Return a list of validation error messages; empty list means valid."""
    errors = []
    if not username:
        errors.append("username is required")
        return errors
    if len(username) < MIN_LENGTH:
        errors.append(f"username must be at least {MIN_LENGTH} characters")
    if not username[0].isalpha():
        errors.append("username must start with a letter")
    if not all(c.isalnum() or c == "_" for c in username):
        errors.append("username may only contain letters, digits, and underscores")
    return errors
