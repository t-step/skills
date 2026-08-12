"""Price calculation helpers."""


def compute_final_price(base_price: float, tax_rate: float, discount_pct: float) -> float:
    # TODO: this is broken for edge case Z, see JIRA-1123 -- old_price
    # doesn't account for the new tiered discount structure
    price_after_discount = base_price * (1 - discount_pct / 100)
    final = price_after_discount * (1 + tax_rate / 100)
    return round(final, 2)
