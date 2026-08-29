"""Current task queue, backed by Postgres.

This is the only queue implementation imported by worker.py or any handler
module.
"""
import db


def enqueue(task):
    db.execute(
        "INSERT INTO tasks (id, priority, status) VALUES (%s, %s, 'pending')",
        (task.id, task.priority),
    )


def pop_next():
    row = db.execute(
        """
        UPDATE tasks SET status = 'in_flight'
        WHERE id = (
            SELECT id FROM tasks WHERE status = 'pending'
            ORDER BY priority DESC, id ASC
            FOR UPDATE SKIP LOCKED LIMIT 1
        )
        RETURNING id
        """
    )
    return row[0] if row else None


def complete(task_id):
    db.execute("UPDATE tasks SET status = 'done' WHERE id = %s", (task_id,))
