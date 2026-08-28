"""billing/subscription.py -- owned by the Billing team."""

import enum
from datetime import datetime

from db import session
from models import Subscription


class SubscriptionStatus(str, enum.Enum):
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"


def mark_payment_failed(sub_id: int) -> None:
    """Called by the payment-processor webhook handler when a renewal
    charge fails."""
    sub = session.get(Subscription, sub_id)
    assert sub.status == SubscriptionStatus.ACTIVE.value
    sub.status = SubscriptionStatus.PAST_DUE.value
    sub.past_due_since = datetime.utcnow()
    session.commit()


def mark_payment_recovered(sub_id: int) -> None:
    sub = session.get(Subscription, sub_id)
    assert sub.status == SubscriptionStatus.PAST_DUE.value
    sub.status = SubscriptionStatus.ACTIVE.value
    sub.past_due_since = None
    session.commit()


def cancel_for_nonpayment(sub_id: int) -> None:
    """Called by the dunning cron job -- see dunning_job.py."""
    sub = session.get(Subscription, sub_id)
    assert sub.status == SubscriptionStatus.PAST_DUE.value
    sub.status = SubscriptionStatus.CANCELED.value
    session.commit()
