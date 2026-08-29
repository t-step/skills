"""OrderEvents: the append-only event log. This is the only place an order's
facts (items, totals, status) are ever originated. Nothing else in this
system writes order data directly -- every other representation of an
order is built by replaying or consuming this log."""

import db
import queue_client


def place_order(order_id: str, items: list, total_cents: int) -> None:
    db.execute(
        "INSERT INTO order_events (order_id, event_type, payload, occurred_at) "
        "VALUES (%s, 'OrderPlaced', %s, now())",
        [order_id, {"items": items, "total_cents": total_cents}],
    )
    # Publish to the projection queue. Delivery is at-least-once; the
    # projector (see summary_projector.py) is idempotent per event_id.
    queue_client.publish("order-events", {"order_id": order_id, "event_type": "OrderPlaced"})
