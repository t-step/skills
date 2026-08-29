"""Runs identically inside each fulfillment center's own regional database
(FC-East, FC-West, ...). Each FC's `available_units` table lives in that
FC's own regional Postgres instance -- there is no shared database between
FCs. This is deliberate: each FC must be able to keep selling from its own
stock even if the cross-region link to other FCs or to GlobalCatalog is
down."""

import regional_db  # connects only to this FC's own local database


def reserve_units(sku: str, qty: int) -> None:
    """The only way available_units changes in a given FC. Runs against
    this FC's local database only -- never touches another FC's data."""
    row = regional_db.query_one(
        "SELECT available_units FROM inventory WHERE sku = %s FOR UPDATE", [sku]
    )
    if row["available_units"] < qty:
        raise ValueError("insufficient local stock")
    regional_db.execute(
        "UPDATE inventory SET available_units = available_units - %s WHERE sku = %s",
        [qty, sku],
    )


def restock(sku: str, qty: int) -> None:
    regional_db.execute(
        "UPDATE inventory SET available_units = available_units + %s WHERE sku = %s",
        [qty, sku],
    )
