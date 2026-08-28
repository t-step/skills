"""entitlements/feature_access.py -- owned by the Mobile Platform team.

The mobile app cannot afford a live DB round-trip to Billing on every
screen render, so entitlement checks read from `feature_access_cache`
(one row per user, refreshed by `refresh_cache_job` below) instead of
computing access live. Nothing in this file writes to `subscriptions` or
reads it directly outside of the refresh job.
"""

from datetime import datetime, timedelta

from db import session
from models import Subscription, FeatureAccessCache
from subscription import SubscriptionStatus


GRACE_PERIOD = timedelta(days=3)
REFRESH_INTERVAL = timedelta(minutes=15)


def compute_access(sub: Subscription, now: datetime) -> bool:
    """The actual entitlement rule. Not just `status == active` --
    incorporates the billing team's grace-period policy directly."""
    if sub.status == SubscriptionStatus.ACTIVE.value:
        return True
    if sub.status == SubscriptionStatus.PAST_DUE.value:
        return (now - sub.past_due_since) < GRACE_PERIOD
    return False  # canceled


def refresh_cache_job() -> None:
    """Runs every 15 minutes. For every subscription, recomputes access
    and upserts into feature_access_cache. This is the only writer of
    that table."""
    now = datetime.utcnow()
    for sub in session.query(Subscription).yield_per(500):
        access = compute_access(sub, now)
        row = session.get(FeatureAccessCache, sub.user_id) or FeatureAccessCache(user_id=sub.user_id)
        row.has_access = access
        row.computed_at = now
        session.merge(row)
    session.commit()


def check_access(user_id: int) -> bool:
    """What the mobile API actually calls. Reads the cache only -- never
    calls compute_access() directly, never touches `subscriptions`."""
    row = session.get(FeatureAccessCache, user_id)
    return row.has_access if row else False
