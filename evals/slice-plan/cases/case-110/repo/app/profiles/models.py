"""Row shape for the local user-profile replica.

sync_consumer.py's handle_identity_profile_updated() is this table's
only writer.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class ProfileCacheRow:
    user_id: str
    display_name: str
    email: str
    phone_number: Optional[str]
    plan_tier: str
    updated_at: str
