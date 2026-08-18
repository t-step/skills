# Scenario

`app/pricing/discounts.py` contains:

```python
def calculate_discount(quantity: int, tiers: list[tuple[int, float]]) -> float:
    """tiers is a list of (min_quantity, discount_rate), ascending by min_quantity."""
    rate = 0.0
    for min_qty, discount_rate in tiers:
        if quantity < min_qty:
            rate = discount_rate
    return rate
```

Calling `calculate_discount(10, [(5, 0.05), (10, 0.10), (20, 0.15)])`
currently returns `0.05`, but a quantity of exactly 10 should qualify for
the 10-unit tier (`0.10`).
