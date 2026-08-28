"""accounts/trust_and_safety.py -- the only writer of User.status."""

from datetime import datetime

from db import session
from user_model import User, UserAccountStatus


def suspend(user_id: int, admin_id: str, reason: str) -> None:
    user = session.get(User, user_id)
    if user.status == UserAccountStatus.DELETED.value:
        raise ValueError("cannot suspend a deleted account")
    user.status = UserAccountStatus.SUSPENDED.value
    user.status_changed_at = datetime.utcnow()
    user.status_changed_by = admin_id
    session.commit()
    audit_log.write(user_id, f"suspended by {admin_id}: {reason}")
    # No call to the search service here. The write to `users` is the
    # entire operation as far as this function is concerned.


def reinstate(user_id: int, admin_id: str) -> None:
    user = session.get(User, user_id)
    if user.status != UserAccountStatus.SUSPENDED.value:
        raise ValueError(f"cannot reinstate from {user.status}")
    user.status = UserAccountStatus.ACTIVE.value
    user.status_changed_at = datetime.utcnow()
    user.status_changed_by = admin_id
    session.commit()
    audit_log.write(user_id, f"reinstated by {admin_id}")
