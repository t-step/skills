"""checkout-drops: reserves one unit of a limited-quantity drop SKU and
confirms the order. Backed by sqlite for this working copy; production
runs against the same schema on Postgres.
"""

import sqlite3


class SoldOutError(Exception):
    pass


SCHEMA = """
CREATE TABLE IF NOT EXISTS inventory (
    sku TEXT PRIMARY KEY,
    available INTEGER NOT NULL,
    last_updated_by TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    sku TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.commit()


def reserve_and_confirm(
    conn: sqlite3.Connection,
    sku: str,
    order_id: str,
    app_instance: str,
    created_at: str,
    after_read=None,
) -> str:
    """Reserve one unit of `sku` and confirm `order_id` against it.

    `after_read` is an optional zero-arg callback; production never
    passes one -- it exists only so a test can pause one call at a fixed
    point to make a two-worker interleaving deterministic instead of
    timing-dependent.
    """
    row = conn.execute(
        "SELECT available FROM inventory WHERE sku = ?", (sku,)
    ).fetchone()
    if row is None:
        raise ValueError(f"unknown sku {sku}")

    current_available = row[0]
    if current_available <= 0:
        raise SoldOutError(f"{sku} is sold out")

    new_available = current_available - 1

    if after_read is not None:
        after_read()

    conn.execute(
        "UPDATE inventory SET available = ?, last_updated_by = ? WHERE sku = ?",
        (new_available, app_instance, sku),
    )
    conn.execute(
        "INSERT INTO orders (order_id, sku, status, created_at) VALUES (?, ?, 'confirmed', ?)",
        (order_id, sku, created_at),
    )
    conn.commit()
    return "confirmed"
