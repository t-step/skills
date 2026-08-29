CREATE TABLE products (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    price_cents INTEGER NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- No other table, view, or materialized view references price_cents.
-- The only cached representation of price lives in Redis, keyed
-- "product:{id}:price", populated exclusively by pricing_service.py's
-- get_price() on a cache miss.
