"""inventory/ledger.py -- each fulfillment center runs its own instance.

Fulfillment centers (FCs) operate independently and must keep taking
orders even if their connection to the other FCs' ledgers is down --
this is a deliberate availability requirement from the ops team ("an FC
going dark on the network must not stop it from selling"). Each FC's
ledger table is the authoritative record of *that FC's own* stock; there
is no single central ledger.
"""

import enum
from datetime import datetime

from db import session
from models import StockLedger, Sale


class SaleStatus(str, enum.Enum):
    RESERVED = "reserved"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


def reserve_unit(sku: str, order_id: str, fc_id: str) -> str:
    """Decrements this FC's local available_units for `sku` and records a
    Sale row, all in one local transaction. Never calls out to another
    FC's ledger -- by design, so this still works if the inter-FC link is
    down.
    """
    row = session.get(StockLedger, (fc_id, sku), with_for_update=True)
    if row.available_units <= 0:
        raise OutOfStock(sku, fc_id)
    row.available_units -= 1
    sale = Sale(
        sku=sku,
        order_id=order_id,
        fc_id=fc_id,
        status=SaleStatus.RESERVED.value,
        created_at=datetime.utcnow(),
    )
    session.add(sale)
    session.commit()
    return sale.id


def confirm(sale_id: str) -> None:
    sale = session.get(Sale, sale_id)
    assert sale.status == SaleStatus.RESERVED.value
    sale.status = SaleStatus.CONFIRMED.value
    session.commit()


class OutOfStock(Exception):
    def __init__(self, sku: str, fc_id: str):
        super().__init__(f"{sku} out of stock at {fc_id}")
