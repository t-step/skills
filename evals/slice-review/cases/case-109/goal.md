# Goal

Add `should_expedite_reorder(units_on_hand, daily_usage_rate)` to
`inventory/restock.py`: return True when the estimated days until
stockout (via the existing `days_until_stockout` helper) is less than
the standard reorder lead time, so the team knows to expedite an order
instead of waiting for the normal restock cycle. Return False when the
usage rate is zero or negative (no estimate available).
