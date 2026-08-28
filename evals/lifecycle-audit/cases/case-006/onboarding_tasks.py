"""growth/onboarding_tasks.py -- owned by the Growth team.

Tracks each new user's personal onboarding checklist ("verify email",
"invite a teammate", "connect an integration"). One row per
(user_id, task_key). Rows are created when a user signs up, seeded from
a fixed template list.
"""

import enum
from datetime import datetime

from db import session
from models import OnboardingTask


class OnboardingTaskStatus(str, enum.Enum):
    PENDING = "pending"
    COMPLETE = "complete"


def mark_complete(user_id: int, task_key: str) -> None:
    """Called by the relevant product surface when the user actually
    does the thing (e.g. the integrations page calls this when an OAuth
    connection succeeds). No 'running' or 'failed' state exists here --
    a task is either not yet done or done."""
    task = session.get(OnboardingTask, (user_id, task_key))
    if task.status == OnboardingTaskStatus.COMPLETE.value:
        return  # idempotent; already done
    task.status = OnboardingTaskStatus.COMPLETE.value
    task.completed_at = datetime.utcnow()
    session.commit()
    maybe_send_progress_email(user_id)
