from app.discounts.coupon import apply_coupon


def test_flat_discount():
    assert apply_coupon(1000, {"type": "flat", "value": 300}) == 700


def test_flat_discount_cannot_go_negative():
    assert apply_coupon(200, {"type": "flat", "value": 300}) == 0


def test_percent_discount():
    assert apply_coupon(1000, {"type": "percent", "value": 20}) == 800


def test_unknown_type_raises():
    try:
        apply_coupon(1000, {"type": "bogus", "value": 10})
        assert False
    except ValueError:
        pass
