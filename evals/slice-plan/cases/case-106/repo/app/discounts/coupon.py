"""Validates and applies coupon codes at checkout."""


def apply_coupon(subtotal_cents: int, coupon: dict) -> int:
    """coupon has 'type': 'flat' or 'percent', and 'value'."""
    if coupon["type"] == "flat":
        return max(0, subtotal_cents - coupon["value"])
    if coupon["type"] == "percent":
        discount = subtotal_cents * coupon["value"] // 100
        return subtotal_cents - discount
    raise ValueError(f"unknown coupon type: {coupon['type']}")
