"""Order cancellation, per order_spec.md. The long-standing, spec-
conforming cancellation path -- CI references test_order_service.py
against this module (not included in this fixture)."""
import db


def cancel_order(order_id, actor):
    order = db.get_order(order_id)
    if not is_refund_eligible(order):
        raise RefundNotEligible(order_id)
    db.execute(
        "UPDATE orders SET status = 'canceled' WHERE id = %s", (order_id,)
    )
    issue_refund(order)


def is_refund_eligible(order):
    return (
        order.age_days <= 30
        and order.payment_captured
        and not order.has_active_dispute
    )


def issue_refund(order):
    ...


class RefundNotEligible(Exception):
    pass
