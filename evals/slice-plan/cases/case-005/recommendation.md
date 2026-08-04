# Accepted Slice: Round discounts in the checkout flow in the customer's favor

## Goal
apply_discount() in app/checkout/pricing.py currently truncates the
discount calculation, which rounds in the store's favor by up to one
cent. Change it to round in the customer's favor (i.e. round the
discount amount up, so the charged total is never higher than a fair
calculation would produce).

## Why now
A customer complaint plus a support audit confirmed the off-by-one-cent
rounding is real and affects a small percentage of checkout totals;
legal flagged it as worth fixing proactively before it's customer-visible
at scale.

## What this slice proves
That apply_discount() now rounds the discount amount up (in the
customer's favor) rather than truncating, for the checkout flow.

## Explicit non-goals
Does not change refund_amount() in app/admin/refunds.py or
discounted_line_total() in app/reports/export.py -- both compute
against historical/reporting data with their own reasons to stay as-is,
and neither was flagged by the audit.

## Acceptance evidence
A test showing apply_discount() with a subtotal/percent combination
that previously truncated (e.g. a case where the exact discount amount
isn't a whole number of cents) now rounds up instead of down.
