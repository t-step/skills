"""Internal support tool. Lets a support rep override a customer's plan
tier directly, for cases like goodwill upgrades or manual corrections."""

import db


def set_plan_tier(customer_id: str, plan_tier: str, rep_id: str) -> None:
    """Writes subscriptions.plan_tier directly. Does not call Stripe, does
    not create a corresponding Stripe subscription/price change, and does
    not check whether a Stripe webhook for this customer is in flight."""
    if plan_tier not in ("free", "pro", "enterprise"):
        raise ValueError("unknown plan tier")

    db.execute(
        "UPDATE subscriptions SET plan_tier = %s, updated_at = now(), "
        "last_admin_override_by = %s WHERE customer_id = %s",
        [plan_tier, rep_id, customer_id],
    )
