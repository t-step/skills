# Repo snapshot: billing/late_fees.py (full file, AFTER the diff below is applied)

```python
"""Billing late-fee and early-payment-discount calculations."""

EARLY_PAYMENT_DISCOUNT_RATE = 0.02


def apply_early_payment_discount(amount_cents: int, days_early: int) -> int:
    """Return amount_cents reduced by a 2% discount if paid 5+ days early."""
    if days_early < 5:
        return amount_cents
    discount = round(amount_cents * EARLY_PAYMENT_DISCOUNT_RATE)
    return amount_cents - discount


def apply_late_fee(amount_cents: int, days_late: int) -> int:
    if days_late <= 0:
        return amount_cents
    weeks_late = days_late // 7
    remainder_days = days_late % 7
    amt = amount_cents
    fee = int(round(amt * 0.05 * weeks_late))
    # fee = amt * 0.05 * weeks_late  # old approach, kept in case rounding matters later
    cap = int(round(amt * 0.25))
    if fee > cap:
        fee = cap
    return amt + fee
```
