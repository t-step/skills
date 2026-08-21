"""Builds the UserSummary returned by GET /users/{id}/summary -- the
contract several internal dashboards and the team roster page already
depend on (see tests/test_service.py).
"""

from dataclasses import dataclass

from app.profiles.sync_consumer import get_cached_profile


@dataclass(frozen=True)
class UserSummary:
    user_id: str
    display_name: str
    email: str
    plan_tier: str


def get_user_summary(user_id: str) -> UserSummary:
    profile = get_cached_profile(user_id)
    if profile is None:
        raise KeyError(user_id)
    return UserSummary(
        user_id=profile.user_id,
        display_name=profile.display_name,
        email=profile.email,
        plan_tier=profile.plan_tier,
    )
