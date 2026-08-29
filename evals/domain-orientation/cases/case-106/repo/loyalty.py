"""Loyalty program. A Guest is created only through explicit program
enrollment (sign-up form or front-desk enrollment flow, not shown here)."""

from dataclasses import dataclass


@dataclass
class Guest:
    id: int
    email: str
    tier: str  # "member" | "silver" | "gold"
    points_balance: int
    enrolled_at: str
