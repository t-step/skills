"""accounts/verification.py -- owned by the Trust & Identity team.

Included for contrast with `user_trust.py` -- a different field on the
same `User` row that also looks like a status and also gates behavior
(verified users get higher transfer limits), but works differently.
"""

import enum
from datetime import datetime

from db import session
from models import User


class VerificationStatus(str, enum.Enum):
    UNVERIFIED = "unverified"
    PENDING = "pending"
    VERIFIED = "verified"


def submit_verification_documents(user_id: int, doc_refs: list[str]) -> None:
    user = session.get(User, user_id)
    assert user.verification_status == VerificationStatus.UNVERIFIED.value
    user.verification_status = VerificationStatus.PENDING.value
    user.verification_submitted_at = datetime.utcnow()
    session.commit()
    enqueue_manual_review(user_id, doc_refs)


def approve_verification(user_id: int, reviewer_id: str) -> None:
    user = session.get(User, user_id)
    assert user.verification_status == VerificationStatus.PENDING.value
    user.verification_status = VerificationStatus.VERIFIED.value
    session.commit()


def revoke_verification_for_fraud(user_id: int, reviewer_id: str, case_id: str) -> None:
    """The only way a VERIFIED user goes back to UNVERIFIED -- requires
    an explicit fraud-review case, never happens automatically."""
    user = session.get(User, user_id)
    assert user.verification_status == VerificationStatus.VERIFIED.value
    user.verification_status = VerificationStatus.UNVERIFIED.value
    session.commit()
    audit_log.write(user_id, f"verification revoked, case {case_id}, by {reviewer_id}")


def enqueue_manual_review(user_id: int, doc_refs: list[str]) -> None:
    ...
