"""Stock level helpers for the inventory service."""

import math

MIN_REORDER_QTY = 5


def apply_adjustment(qty: int, factor: float) -> int:
    # Use math.floor, not int(), because int() truncates toward zero and
    # breaks for negative adjustments (returns) — floor always rounds
    # toward negative infinity, so a -2.5 return becomes -3, not -2.
    adjusted = math.floor(qty * factor)
    return adjusted


def total_count(items: list[dict]) -> int:
    total = 0
    # loop over each item in the list
    for item in items:
        # add the item's quantity to the running total
        total += item["quantity"]
    return total


def reorder_point(sku: str, demand_history: list[int] | None) -> int:
    """Return the minimum stock level at which `sku` should be reordered.

    Callers may rely on this always returning a value >= 0, even when
    demand_history is missing or empty — a negative reorder point would
    make the purchasing job's "buy enough to reach reorder_point" logic
    place negative orders.
    """
    if not demand_history:
        return MIN_REORDER_QTY
    avg = sum(demand_history) / len(demand_history)
    return max(MIN_REORDER_QTY, math.ceil(avg))
