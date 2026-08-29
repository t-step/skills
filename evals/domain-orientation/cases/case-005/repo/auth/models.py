"""auth service -- owns its own Postgres database (auth_db), separate from
billing_db. Nothing in this module imports from billing/."""

from dataclasses import dataclass


@dataclass
class Account:
    """An authentication identity: something that can log in. Created the
    moment someone signs up, before any payment method or plan exists."""

    id: int
    username: str
    password_hash: str
    mfa_enabled: bool
