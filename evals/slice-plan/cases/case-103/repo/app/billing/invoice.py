def format_cents(amount_cents: int) -> str:
    """Formats a cents integer as a dollar string, e.g. 150 -> "$1.50"."""
    dollars = amount_cents // 100
    cents = amount_cents % 100
    return f"${dollars}.{cents:02d}"


def render_invoice_total(amount_cents: int) -> str:
    return f"Total: {format_cents(amount_cents)}"
