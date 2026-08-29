def charge_card(card_number: str, amount_cents: int) -> str:
    last4 = card_number[-4:]
    # ... calls out to the payment processor ...
    return f"charged ****{last4} for {amount_cents} cents"
