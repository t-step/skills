def compute_invoice_total(line_items: list[dict]) -> int:
    return sum(item["amount_cents"] for item in line_items)
