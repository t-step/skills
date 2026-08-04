from app.payments.router import process_payment


def test_credit_card():
    assert process_payment("credit_card", 500) == "stripe_charge_500"


def test_paypal():
    assert process_payment("paypal", 500) == "paypal_charge_500"


def test_unsupported():
    try:
        process_payment("bitcoin", 500)
        assert False
    except ValueError:
        pass
