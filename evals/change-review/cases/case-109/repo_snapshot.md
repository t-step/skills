# Repo snapshot: inventory/restock.py (full file, AFTER the diff below is applied)

```python
"""Inventory restocking and low-stock alert calculations."""

LOW_STOCK_THRESHOLD_UNITS = 10
REORDER_LEAD_TIME_DAYS = 5


def needs_restock(units_on_hand: int) -> bool:
    """Return True if units_on_hand is at or below the low-stock threshold."""
    return units_on_hand <= LOW_STOCK_THRESHOLD_UNITS


def days_until_stockout(units_on_hand: int, daily_usage_rate: float) -> int:
    """Estimate days remaining before stock reaches zero, given daily usage."""
    if daily_usage_rate <= 0:
        return -1
    return int(units_on_hand / daily_usage_rate)


def should_expedite_reorder(units_on_hand: int, daily_usage_rate: float) -> bool:
    if daily_usage_rate <= 0:
        return False
    remaining_days = days_until_stockout(units_on_hand, daily_usage_rate)
    lead_time = 5
    if remaining_days == -1:
        return False
    return remaining_days < lead_time
```
