"""Refund processing helpers."""

MAX_REFUND_CENTS = 1_000_000


def process_refund(order_id: str, amount_cents: int, reason: str) -> dict:
    # TODO: cap refunds at MAX_REFUND_CENTS
    if amount_cents > MAX_REFUND_CENTS:
        raise ValueError(f"refund exceeds cap of {MAX_REFUND_CENTS} cents")

    # TODO: log refund reason to the audit trail
    return {
        "order_id": order_id,
        "amount_cents": amount_cents,
        "reason": reason,
        "status": "refunded",
    }
