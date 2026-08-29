"""billing service -- owns its own Postgres database (billing_db), separate
from auth_db. Nothing in this module imports from auth/."""

from dataclasses import dataclass


@dataclass
class Account:
    """A billing subscription: a plan and a payment method. Created only
    when someone starts a paid plan -- a signed-up user with no plan has
    no row here at all."""

    id: int
    plan: str  # "free" | "pro" | "enterprise"
    payment_method_id: str | None
