def refund_amount(original_cents: int, percent_off: int) -> int:
    """Used by the admin refund tool -- recomputes what was actually
    charged (after discount) so refunds match the original charge, not
    the pre-discount price. Deliberately separate from
    checkout/pricing.py: refunds run against historical orders that may
    have used an older discount formula.
    """
    return original_cents - (original_cents * percent_off // 100)
