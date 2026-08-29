"""Consumes the order-events queue asynchronously and builds
order_summary_view, a read-optimized table the customer-facing order
history page queries. This is the only writer of order_summary_view, and
it never originates an order fact -- it only ever reflects what
order_events already recorded.

Documented SLA (see runbook, not included in this fixture bundle): p99
consumer lag is under 2 seconds under normal load. There is a dead-letter
queue for events that fail to apply after 5 retries, alerting on-call."""

import db
import queue_client


def run_forever():
    for message in queue_client.consume("order-events"):
        event = db.query_one(
            "SELECT * FROM order_events WHERE order_id = %s AND event_type = %s "
            "ORDER BY occurred_at DESC LIMIT 1",
            [message["order_id"], message["event_type"]],
        )
        if event is None:
            continue  # replay ordering edge case; will be retried
        db.execute(
            "INSERT INTO order_summary_view (order_id, total_cents, status) "
            "VALUES (%s, %s, 'placed') "
            "ON CONFLICT (order_id) DO UPDATE SET total_cents = EXCLUDED.total_cents, "
            "status = EXCLUDED.status",
            [event["order_id"], event["payload"]["total_cents"]],
        )
        queue_client.ack(message)
