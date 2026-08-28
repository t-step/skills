"""billing/dunning_job.py -- daily cron, owned by the Billing team.

Product decision (see the dunning policy doc linked in the team wiki,
not included here): a subscription that goes past_due keeps full feature
access for a 3-day grace period, to absorb ordinary card-expiry/retry
noise without punishing customers who fix payment quickly. Only after 3
days of remaining past_due does this job cancel the subscription.
"""

from datetime import datetime, timedelta

from db import session
from models import Subscription
from subscription import SubscriptionStatus, cancel_for_nonpayment


GRACE_PERIOD = timedelta(days=3)


def run() -> None:
    now = datetime.utcnow()
    overdue = (
        session.query(Subscription)
        .filter(Subscription.status == SubscriptionStatus.PAST_DUE.value)
        .filter(Subscription.past_due_since < now - GRACE_PERIOD)
        .all()
    )
    for sub in overdue:
        cancel_for_nonpayment(sub.id)
