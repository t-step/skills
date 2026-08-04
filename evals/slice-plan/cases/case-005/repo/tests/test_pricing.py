from app.checkout.pricing import apply_discount


def test_whole_cent_discount_unaffected():
    assert apply_discount(1000, 10) == 900


def test_fractional_discount_currently_truncates():
    # 999 * 10 / 100 = 99.9 -- currently truncates to 99, so total is 900.
    assert apply_discount(999, 10) == 900
