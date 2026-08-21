"""Consumes IdentityProfileUpdated events published by the Identity
service and upserts them into the local profile replica. This is the
only code path that writes to the profile cache.
"""

from dataclasses import dataclass
from typing import Optional

from app.profiles.models import ProfileCacheRow

_PROFILE_CACHE: dict[str, ProfileCacheRow] = {}


@dataclass(frozen=True)
class IdentityProfileUpdated:
    """Identity's published event contract for profile changes."""

    user_id: str
    display_name: str
    email: str
    phone_number: Optional[str]
    plan_tier: str
    updated_at: str


def handle_identity_profile_updated(event: IdentityProfileUpdated) -> None:
    _PROFILE_CACHE[event.user_id] = ProfileCacheRow(
        user_id=event.user_id,
        display_name=event.display_name,
        email=event.email,
        phone_number=event.phone_number,
        plan_tier=event.plan_tier,
        updated_at=event.updated_at,
    )


def get_cached_profile(user_id: str) -> Optional[ProfileCacheRow]:
    return _PROFILE_CACHE.get(user_id)
