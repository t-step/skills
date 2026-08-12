"""Structured audit logging used by the checkout and payout flows."""


def audit_log(event: str, **fields) -> None:
    """Append a structured audit event to the audit trail.

    Currently called from checkout.complete_order() and payouts.send_payout().
    Refund processing (billing/refunds.py) does not call this yet.
    """
    print(f"[audit] {event} {fields}")
