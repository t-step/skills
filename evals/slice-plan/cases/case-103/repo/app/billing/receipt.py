def format_cents(amount_cents: int) -> str:
    """Formats a cents integer as a dollar string. Duplicated from
    invoice.py -- written independently before the two modules' authors
    realized they needed the same thing.
    """
    dollars = amount_cents // 100
    cents = amount_cents % 100
    return f"${dollars}.{cents:02d}"


def render_receipt_line(item_name: str, amount_cents: int) -> str:
    return f"{item_name}: {format_cents(amount_cents)}"
