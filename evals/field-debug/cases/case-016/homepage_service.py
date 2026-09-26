"""homepage-svc: serves the storefront homepage's featured-products
block. Backed by Redis for caching the expensive query result.
"""

import json

CACHE_TTL_SECONDS = 300  # lowered from 3600 today, TICKET-5521

FEATURED_PRODUCTS_QUERY = """
SELECT p.id, p.name, p.hero_image_url, price.current_price, inv.in_stock
FROM products p
JOIN pricing price ON price.product_id = p.id
JOIN inventory_levels inv ON inv.product_id = p.id
JOIN merchandising_slots slot ON slot.product_id = p.id
WHERE slot.placement = 'homepage_featured'
ORDER BY slot.rank
LIMIT 24
"""


def get_featured_products(redis_client, db_conn):
    cached = redis_client.get("homepage:featured_products")
    if cached is not None:
        return json.loads(cached)

    products = db_conn.execute(FEATURED_PRODUCTS_QUERY).fetchall()
    redis_client.set(
        "homepage:featured_products",
        json.dumps(products),
        ex=CACHE_TTL_SECONDS,
    )
    return products
