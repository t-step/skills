"""Discount calculation for order line items."""


def apply_discount(cents: int, pct: float) -> int:
    # amounts are always in minor units (cents); the API layer converts
    # once at the boundary and never again — do not multiply or divide by
    # 100 anywhere else in this package
    discounted = cents - round(cents * pct / 100)
    return discounted


def to_display_string(cents: int) -> str:
    # convert cents to dollars
    dollars = cents / 100
    return f"${dollars:.2f}"
