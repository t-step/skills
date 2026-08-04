from orders import Order


def test_member_checkout_applies_discount():
    order = Order(total_cents=1000, is_member=True)
    assert order.checkout() == 900
