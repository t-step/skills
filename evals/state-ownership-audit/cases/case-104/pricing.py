"""Pricing service. Computes and caches final_price for a product, which
factors in whatever discount Promotions currently reports as active."""

import cache
import promotions_client


def compute_final_price(product_id: str, base_price_cents: int) -> int:
    discount = promotions_client.get_active_discount(product_id)
    final_price = base_price_cents - discount["amount_cents"]
    cache.set(f"final_price:{product_id}", final_price)
    return final_price


def get_cached_final_price(product_id: str) -> int:
    """Read accessor other services (including Promotions, for
    price-matched promos) call to see this service's current view of
    final_price. Returns whatever was last cached by compute_final_price;
    does not recompute."""
    return cache.get(f"final_price:{product_id}")
