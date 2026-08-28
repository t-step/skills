"""bidding/bid.py -- owned by the Bidding team.

Bid rows live in the Bidding service's own database, separate from the
Auctions service's database. Bidding calls Auctions' read API to check
auction state when it needs to (see `accept` below); Auctions calls
Bidding's `reject_all_open_bids` RPC when an auction closes (see
auction.py). Neither service reads the other's database directly.
"""

import enum
from datetime import datetime

from db import session
from models import Bid
from auctions_client import get_auction_status


class BidStatus(str, enum.Enum):
    SUBMITTED = "submitted"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


def submit(auction_id: int, bidder_id: int, amount_cents: int) -> int:
    bid = Bid(
        auction_id=auction_id,
        bidder_id=bidder_id,
        amount_cents=amount_cents,
        status=BidStatus.SUBMITTED.value,
        created_at=datetime.utcnow(),
    )
    session.add(bid)
    session.commit()
    return bid.id


def accept(bid_id: int, seller_id: int) -> None:
    """Called when a seller accepts a specific bid. Checks the auction's
    current status via Auctions' API before accepting -- this is the
    only place Bidding enforces the shared invariant from its own side.
    """
    bid = session.get(Bid, bid_id)
    assert bid.status == BidStatus.SUBMITTED.value
    if get_auction_status(bid.auction_id) != "open":
        raise ValueError("cannot accept a bid on an auction that is not open")
    bid.status = BidStatus.ACCEPTED.value
    bid.accepted_at = datetime.utcnow()
    session.commit()


def withdraw(bid_id: int, bidder_id: int) -> None:
    """Bidder-initiated. No auction-state check at all -- a bidder can
    withdraw their own submitted bid regardless of whether the auction
    is open or closed."""
    bid = session.get(Bid, bid_id)
    assert bid.status == BidStatus.SUBMITTED.value
    bid.status = BidStatus.WITHDRAWN.value
    session.commit()


def reject_all_open(auction_id: int) -> None:
    """The RPC handler Auctions calls from close_auction(). Rejects
    every `submitted` bid for this auction. Idempotent -- calling it
    twice for the same auction is safe, since it only touches rows still
    in `submitted`."""
    bids = (
        session.query(Bid)
        .filter(Bid.auction_id == auction_id)
        .filter(Bid.status == BidStatus.SUBMITTED.value)
        .all()
    )
    for b in bids:
        b.status = BidStatus.REJECTED.value
    session.commit()
