"""inventory/transfer.py -- moving stock between fulfillment centers.

A transfer decrements the source FC's ledger immediately when the truck
leaves, but the destination FC's ledger is only incremented when a
warehouse worker physically scans the shipment in on arrival. Between
those two events, the units are "in transit": no longer in FC-A's
available_units, not yet in FC-B's.
"""

import enum
from datetime import datetime

from db import session
from models import Transfer, StockLedger


class TransferStatus(str, enum.Enum):
    DISPATCHED = "dispatched"     # source decremented, truck left
    RECEIVED = "received"         # destination incremented, scan completed
    RECONCILED = "reconciled"     # closed out by the nightly job (see below)


def dispatch(transfer_id: str, sku: str, units: int, from_fc: str, to_fc: str) -> None:
    row = session.get(StockLedger, (from_fc, sku), with_for_update=True)
    assert row.available_units >= units
    row.available_units -= units
    t = Transfer(
        id=transfer_id,
        sku=sku,
        units=units,
        from_fc=from_fc,
        to_fc=to_fc,
        status=TransferStatus.DISPATCHED.value,
        dispatched_at=datetime.utcnow(),
    )
    session.add(t)
    session.commit()


def receive(transfer_id: str) -> None:
    """Called by the handheld scanner app when a worker scans the
    shipment in at the destination FC. If the scan never happens --
    handheld battery dies, shipment misrouted, worker forgets -- this is
    simply never called, and the transfer sits in `dispatched` forever
    with no automatic timeout or alert from this code path.
    """
    t = session.get(Transfer, transfer_id)
    assert t.status == TransferStatus.DISPATCHED.value
    dest_row = session.get(StockLedger, (t.to_fc, t.sku), with_for_update=True)
    dest_row.available_units += t.units
    t.status = TransferStatus.RECEIVED.value
    t.received_at = datetime.utcnow()
    session.commit()
