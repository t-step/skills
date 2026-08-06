"""HTTP handlers for order creation."""

from app.audit.logger import record_event


def create_order(user_id: str, items: list) -> dict:
    order = {"user_id": user_id, "items": items}
    record_event("order_created", order)
    return order
