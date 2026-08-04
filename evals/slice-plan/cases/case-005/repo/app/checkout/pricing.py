def apply_discount(subtotal_cents: int, percent_off: int) -> int:
    """Used by the checkout flow to compute the discounted total."""
    return subtotal_cents - (subtotal_cents * percent_off // 100)
