"""Converts internal User models into the public API representation.

Consumers outside app/ (e.g. the mobile client's response parser)
depend on this exact key set -- adding or removing a key here is a
public API change, not an internal refactor.
"""

from app.models import User


def serialize_user(user: User) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "display_name": user.display_name,
        "created_at": user.created_at.isoformat(),
    }
