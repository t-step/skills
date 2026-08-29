"""Promotions service. Computes the active discount for a product. Most
promo types are self-contained (percent off, flat amount off), but
'price-matched' promos are defined relative to a competing bundle's
current final price, which it gets by calling back into Pricing."""

import pricing_client


def get_active_discount(product_id: str) -> dict:
    promo = _load_promo_for(product_id)

    if promo["type"] == "price-matched":
        # For this promo type, the discount amount is defined as "however
        # much is needed to match the competing bundle's current final
        # price" -- which means reading Pricing's own cached final_price
        # for that bundle.
        competitor_final_price = pricing_client.get_cached_final_price(
            promo["competitor_product_id"]
        )
        this_base_price = _base_price_for(product_id)
        amount_cents = max(0, this_base_price - competitor_final_price)
        return {"type": "price-matched", "amount_cents": amount_cents}

    return {"type": promo["type"], "amount_cents": promo["amount_cents"]}


def _load_promo_for(product_id: str) -> dict:
    ...  # loads from the promotions table; not relevant to this audit


def _base_price_for(product_id: str) -> int:
    ...  # loads from the catalog; not relevant to this audit
