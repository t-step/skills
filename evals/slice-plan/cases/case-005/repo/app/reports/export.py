def discounted_line_total(subtotal_cents: int, percent_off: int) -> int:
    """Used by the nightly CSV export for finance. Recomputes the
    discounted total for reporting purposes only -- not shown to
    customers or used in any live charge.
    """
    return subtotal_cents - (subtotal_cents * percent_off // 100)
