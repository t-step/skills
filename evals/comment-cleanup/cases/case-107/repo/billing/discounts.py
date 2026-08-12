"""Discount validity checks used by checkout and the admin dashboard."""

from datetime import date


def is_discount_valid(expiry: date, today: date) -> bool:
    """Return True if the discount is still valid.

    A discount is valid up to and including its expiry date — this
    compares with <=, not <, so a discount expiring today is still usable
    for the rest of that day. Both checkout and the admin dashboard rely
    on this exact boundary; do not change it to strict '<' without
    checking both call sites.
    """
    return today <= expiry
