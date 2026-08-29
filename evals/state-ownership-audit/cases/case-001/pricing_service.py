"""Pricing service: owns Product.price in Postgres, with a Redis read-through
cache in front of reads."""

import redis
import db

r = redis.Redis()

CACHE_TTL_SECONDS = 300


def get_price(product_id: str) -> int:
    """Read path. Cache-first, falls back to Postgres on miss, repopulates
    the cache from the value just read from the database."""
    cache_key = f"product:{product_id}:price"
    cached = r.get(cache_key)
    if cached is not None:
        return int(cached)

    row = db.query_one("SELECT price_cents FROM products WHERE id = %s", [product_id])
    if row is None:
        raise LookupError(f"no such product {product_id}")

    price = row["price_cents"]
    r.set(cache_key, price, ex=CACHE_TTL_SECONDS)
    return price


def update_price(product_id: str, new_price_cents: int) -> None:
    """Write path. This is the only function anywhere in this service (or
    any other service) that writes products.price_cents."""
    if new_price_cents < 0:
        raise ValueError("price cannot be negative")

    db.execute(
        "UPDATE products SET price_cents = %s, updated_at = now() WHERE id = %s",
        [new_price_cents, product_id],
    )

    # Invalidate rather than write-through: the cache is never given a value
    # that didn't come from a subsequent read of the database.
    r.delete(f"product:{product_id}:price")
