def reserve_stock(available: int, requested: int) -> int:
    """Reserves stock for an order, returns the new available count.
    Raises if not enough stock is available.
    """
    if requested > available:
        raise ValueError("not enough stock")
    return available - requested


def restock(current: int, incoming: int) -> int:
    """Adds incoming stock to current stock."""
    return current + incoming


def is_low_stock(current: int, threshold: int) -> bool:
    return current < threshold
