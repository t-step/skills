"""Routes a payment request to the right processor based on method."""

from app.payments import stripe_processor, paypal_processor


def process_payment(method: str, amount_cents: int) -> str:
    if method == "credit_card":
        return stripe_processor.charge(amount_cents)
    elif method == "paypal":
        return paypal_processor.charge(amount_cents)
    else:
        raise ValueError(f"unsupported payment method: {method}")
