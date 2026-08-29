# Slice Retrospective: Add idempotency guard to retry_charge()

## What we proved
`retry_charge()` is now idempotent per (invoice_id, attempt_number),
backed by the three passing tests including one exercising concurrent
retries.

## Assumptions validated
The `charge_attempts` table can dedupe retries without an external
idempotency-key service from the payment processor.

## Assumptions falsified
None.

## Remaining uncertainty
`billing/jobs.py`'s `reconcile_pending_charges()` — the nightly
reconciliation job — also retries failed charges, through its own retry
path that does not use `charge_attempts`. If that job is still actively
running, it could still double-charge customers the exact way
`retry_charge()` did before this fix. This slice did not touch it.

## Intentional non-goals
Migrating to the payment processor's own idempotency-key header was out
of scope per goal.md — this slice uses a local table instead.

## Architectural consequences
`charge_attempts` is now the canonical idempotency-guard pattern for any
charge-retry code path in this codebase.

## Follow-up questions
Is `reconcile_pending_charges()` still actively scheduled? If so, its
retry path needs the same `charge_attempts` guard this slice just added
to `retry_charge()`.
