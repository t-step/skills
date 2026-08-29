# Goal

Add `apply_late_fee(amount_cents, days_late)` to `billing/late_fees.py`: a
5% fee per full week late, rounded to the nearest cent, capped at 25% of
the amount, applied only when `days_late > 0` (zero or negative
`days_late` returns the amount unchanged).
