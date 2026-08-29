"""Worker entry point. Reads exclusively from the `tasks` table in
Postgres via db.py. Imports no Redis client anywhere in this file or
anything it imports."""
import db


def run():
    while True:
        row = db.execute(
            """
            UPDATE tasks SET status = 'in_flight'
            WHERE id = (
                SELECT id FROM tasks WHERE status = 'pending'
                ORDER BY priority DESC LIMIT 1 FOR UPDATE SKIP LOCKED
            )
            RETURNING id
            """
        )
        if row:
            handle(row[0])


def handle(task_id):
    ...


if __name__ == "__main__":
    run()
