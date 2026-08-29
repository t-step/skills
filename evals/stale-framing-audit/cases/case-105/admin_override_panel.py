"""Internal admin tool. Registered in routes.py under /admin/orders, gated
by an `admin` role check only -- no feature flag, no additional review
gate. Added three weeks ago. No test file exists for this module."""
import db


def force_cancel(order_id, actor):
    # TODO: this bypasses OrderService's refund-eligibility checks
    # entirely. Needs review before this is safe to leave enabled in
    # prod -- filed as a follow-up, not yet scheduled.
    db.execute(
        "UPDATE orders SET status = 'canceled' WHERE id = %s", (order_id,)
    )
