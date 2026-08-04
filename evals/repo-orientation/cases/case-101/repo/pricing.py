from orders import Order


def apply_discount(order: Order, pct: float) -> int:
    return int(order.total_cents * (1 - pct))


def apply_member_discount(order: Order) -> int:
    # duplicated from legacy_pricing.calculate_member_price, slightly
    # different rounding
    return round(order.total_cents * 0.9)
