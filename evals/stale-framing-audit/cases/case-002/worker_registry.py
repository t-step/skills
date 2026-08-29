"""Authoritative worker state.

This is the only module that writes to the `workers` table. Every check-in,
check-out, and health-status change is written here.
"""
import db


def check_in(worker_id, capacity):
    db.execute(
        """
        INSERT INTO workers (id, capacity, status, last_seen)
        VALUES (%s, %s, 'online', now())
        ON CONFLICT (id) DO UPDATE
        SET capacity = EXCLUDED.capacity, status = 'online', last_seen = now()
        """,
        (worker_id, capacity),
    )
    publish_event("worker.checked_in", worker_id=worker_id, capacity=capacity)


def check_out(worker_id):
    db.execute("UPDATE workers SET status = 'offline' WHERE id = %s", (worker_id,))
    publish_event("worker.checked_out", worker_id=worker_id)


def publish_event(name, **fields):
    ...  # pushes onto the internal event bus Coordinator subscribes to
