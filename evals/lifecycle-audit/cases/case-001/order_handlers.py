"""orders/handlers.py -- the only place order.status is ever written."""

from datetime import datetime

from models import Order, OrderStatus
from db import session


def mark_paid(order_id: int) -> None:
    order = session.get(Order, order_id)
    if order.status != OrderStatus.PENDING.value:
        raise InvalidTransition(f"cannot mark paid from {order.status}")
    order.status = OrderStatus.PAID.value
    order.updated_at = datetime.utcnow()
    session.commit()


def mark_shipped(order_id: int) -> None:
    order = session.get(Order, order_id)
    if order.status != OrderStatus.PAID.value:
        raise InvalidTransition(f"cannot ship from {order.status}")
    order.status = OrderStatus.SHIPPED.value
    order.updated_at = datetime.utcnow()
    session.commit()


def mark_delivered(order_id: int) -> None:
    order = session.get(Order, order_id)
    if order.status != OrderStatus.SHIPPED.value:
        raise InvalidTransition(f"cannot deliver from {order.status}")
    order.status = OrderStatus.DELIVERED.value
    order.updated_at = datetime.utcnow()
    session.commit()


def cancel(order_id: int) -> None:
    order = session.get(Order, order_id)
    if order.status in (OrderStatus.SHIPPED.value, OrderStatus.DELIVERED.value):
        raise InvalidTransition(f"cannot cancel from {order.status}")
    order.status = OrderStatus.CANCELLED.value
    order.updated_at = datetime.utcnow()
    session.commit()


def flag_for_review(order_id: int, reason: str) -> None:
    """Ops-only action. Does not touch order.status."""
    order = session.get(Order, order_id)
    order.is_flagged_for_review = True
    session.commit()
    audit_log.write(order_id, f"flagged: {reason}")


class InvalidTransition(Exception):
    pass
