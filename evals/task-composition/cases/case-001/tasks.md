# Tasks: Order Exports & Notification Preferences

This is the complete plan and task list for this piece of work. There is
no other backlog, roadmap, or context beyond what's written here.

## CSV export

- T1: Add `GET /orders/export.csv` endpoint in `api/orders.py` that
  streams all orders as CSV.
- T2: Add `format_orders_csv(orders)` in `services/csv_export.py`, used
  by T1.
- T3: Add test `tests/test_csv_export.py` covering T1 and T2.

## Notification opt-out

- T4: Add an `unsubscribed` boolean column to the `notifications` table
  via `migrations/0007_add_unsubscribed.py`.
- T5: Add `POST /notifications/opt-out` endpoint in
  `api/notifications.py` that sets `unsubscribed=True`, using T4's
  column.
- T6: Add test `tests/test_notification_optout.py` covering T4 and T5.

Nothing in either group references a file, table, or endpoint from the
other group. No priority is stated between them.
