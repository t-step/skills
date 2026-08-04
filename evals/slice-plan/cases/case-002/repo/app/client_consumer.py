"""Stand-in for the mobile client's response parser. Reads the exact
keys serialize_user() promises; an extra or renamed key here doesn't
break parsing (it ignores unknown keys), but a removed or renamed
existing key does.
"""

REQUIRED_KEYS = {"id", "email", "display_name", "created_at"}


def parse_user_response(payload: dict) -> None:
    missing = REQUIRED_KEYS - payload.keys()
    if missing:
        raise ValueError(f"user response missing required keys: {missing}")
