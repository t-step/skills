"""risk/user_trust.py -- owned by the Risk team."""

import enum
from datetime import datetime

from db import session
from models import User, TrustLevelHistory


class TrustLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def recompute_trust_level(user_id: int) -> None:
    """Runs nightly for every user (see nightly_batch.py), and also
    on-demand right after checkout completes for that one user.
    `trust_level` gates the spending-limit check in checkout/limits.py.
    """
    user = session.get(User, user_id)
    order_count = count_completed_orders(user_id)
    chargeback_count = count_chargebacks(user_id)
    account_age_days = (datetime.utcnow() - user.created_at).days

    old_value = user.trust_level
    new_value = _score(order_count, chargeback_count, account_age_days)

    if new_value != old_value:
        user.trust_level = new_value
        session.add(TrustLevelHistory(
            user_id=user_id,
            old_value=old_value,
            new_value=new_value,
            computed_at=datetime.utcnow(),
        ))
    session.commit()


def _score(order_count: int, chargeback_count: int, account_age_days: int) -> str:
    """Pure function of current signals. No memory of the previous
    value, no notion of a 'transition' -- every call recomputes from
    scratch and can move the result in either direction (e.g. a fresh
    chargeback can drop a user from HIGH straight to LOW on the very
    next nightly run)."""
    if chargeback_count > 0:
        return TrustLevel.LOW.value
    if order_count >= 20 and account_age_days >= 180:
        return TrustLevel.HIGH.value
    if order_count >= 3:
        return TrustLevel.MEDIUM.value
    return TrustLevel.LOW.value


def count_completed_orders(user_id: int) -> int:
    ...


def count_chargebacks(user_id: int) -> int:
    ...
