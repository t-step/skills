"""auctions/auction.py -- owned by the Auctions team."""

import enum
from datetime import datetime

from db import session
from models import Auction, Bid
from bidding_client import reject_all_open_bids


class AuctionStatus(str, enum.Enum):
    DRAFT = "draft"
    OPEN = "open"
    CLOSED = "closed"
    SETTLED = "settled"


def open_auction(auction_id: int) -> None:
    a = session.get(Auction, auction_id)
    assert a.status == AuctionStatus.DRAFT.value
    a.status = AuctionStatus.OPEN.value
    a.opened_at = datetime.utcnow()
    session.commit()


def close_auction(auction_id: int) -> None:
    """Closing time reached (or a seller manually closes early). Per the
    documented invariant, no bid may be `accepted` while its auction is
    not `open` -- so every outstanding `submitted` bid on this auction
    must stop being acceptable the moment this runs.
    """
    a = session.get(Auction, auction_id)
    assert a.status == AuctionStatus.OPEN.value
    a.status = AuctionStatus.CLOSED.value
    a.closed_at = datetime.utcnow()
    session.commit()

    # Cross-service call into Bidding (owned by a different team -- see
    # bidding/bid.py). If this call fails after the commit above, the
    # auction is already CLOSED but Bidding's `submitted` bids for it are
    # never rejected -- nothing here retries or rolls back the status
    # change.
    reject_all_open_bids(auction_id)


def settle(auction_id: int) -> None:
    a = session.get(Auction, auction_id)
    assert a.status == AuctionStatus.CLOSED.value
    a.status = AuctionStatus.SETTLED.value
    session.commit()
