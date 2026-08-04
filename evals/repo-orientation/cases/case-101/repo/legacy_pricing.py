from orders import Order


def calculate_member_price(order: Order) -> int:
    # duplicated from pricing.apply_member_discount, slightly different
    # rounding — still called by orders.checkout()
    return int(order.total_cents * 0.9)
