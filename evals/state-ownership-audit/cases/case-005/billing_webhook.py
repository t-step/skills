"""Consumes Stripe webhook events and updates local subscription state to
match what Stripe reports."""

import db


def handle_stripe_event(event: dict) -> None:
    if event["type"] not in ("customer.subscription.updated", "customer.subscription.created"):
        return

    stripe_sub = event["data"]["object"]
    customer_id = stripe_sub["customer"]
    plan_tier = _tier_from_stripe_price(stripe_sub["items"]["data"][0]["price"]["id"])

    # No check against the current value or its last-modified time before
    # overwriting -- this handler always applies whatever Stripe's event
    # payload says, including for webhooks that arrive late or out of order
    # relative to when Stripe's event actually occurred.
    db.execute(
        "UPDATE subscriptions SET plan_tier = %s, updated_at = now() WHERE customer_id = %s",
        [plan_tier, customer_id],
    )


def _tier_from_stripe_price(price_id: str) -> str:
    return {"price_free": "free", "price_pro": "pro", "price_ent": "enterprise"}[price_id]
