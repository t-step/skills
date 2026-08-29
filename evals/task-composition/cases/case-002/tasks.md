# Tasks: Audit Trail for Billing Actions

This is the complete plan and task list for this piece of work. There is
no other backlog, roadmap, or context beyond what's written here.

## Foundation

- T1: Add an `audit_log` table via `migrations/0012_add_audit_log.py`
  (columns: `actor_id`, `action`, `target_type`, `target_id`,
  `created_at`).
- T2: Add `write_audit_entry(actor_id, action, target_type, target_id)`
  in `services/audit.py`, backed by T1's table.

## Refund flow

- T3: Add `POST /billing/refund` endpoint in `api/billing_refund.py`.
- T4: Call `write_audit_entry(...)` from T3 whenever a refund is issued.
- T5: Add test `tests/test_refund_audit.py` asserting a refund creates
  an `audit_log` row.

## Plan-cancellation flow

- T6: Add `POST /billing/cancel` endpoint in `api/billing_cancel.py`.
- T7: Call `write_audit_entry(...)` from T6 whenever a plan is
  cancelled.
- T8: Add test `tests/test_cancel_audit.py` asserting a cancellation
  creates an `audit_log` row.

Both the refund flow and the plan-cancellation flow need T1 and T2 to
exist before either can call `write_audit_entry`. The refund and
cancellation flows don't touch any of the same files as each other. No
priority is stated between them.
