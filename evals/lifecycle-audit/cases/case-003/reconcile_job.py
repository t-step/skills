"""inventory/reconcile_job.py -- nightly, owned by the Inventory Platform
team.

FC-A's ledger and FC-B's ledger are each independently authoritative for
their own available_units -- neither is a copy of the other, and there
is no single global ledger table. But the two are not free to disagree
indefinitely about stock that's mid-transfer: the business invariant is
that units are conserved (nothing sold twice, nothing silently
vanishes) across a dispatch/receive pair. This job is the only thing in
the codebase that checks that.
"""

from datetime import datetime, timedelta

from db import session
from models import Transfer
from transfer import TransferStatus


STALE_TRANSFER_THRESHOLD = timedelta(hours=48)


def run() -> None:
    now = datetime.utcnow()
    stale = (
        session.query(Transfer)
        .filter(Transfer.status == TransferStatus.DISPATCHED.value)
        .filter(Transfer.dispatched_at < now - STALE_TRANSFER_THRESHOLD)
        .all()
    )
    for t in stale:
        # Units have been out of both ledgers' available_units for more
        # than 48h with no scan-in. Today this only creates a ticket for
        # a human in the ops queue -- it does not automatically credit
        # either FC's ledger, refund the units, or mark the transfer
        # RECONCILED. What the correct resolution should be (assume lost
        # and write off as shrinkage vs. assume the scan simply failed
        # and credit the destination vs. require a physical recount) is
        # not decided anywhere in this codebase or its docs.
        open_ops_ticket(
            f"Transfer {t.id} ({t.units}x {t.sku}, {t.from_fc} -> {t.to_fc}) "
            f"dispatched {t.dispatched_at.isoformat()}, never scanned in."
        )


def open_ops_ticket(message: str) -> None:
    ...
