from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    email: str
    display_name: str
    password_hash: str
    created_at: datetime
    last_login_at: datetime | None = None
