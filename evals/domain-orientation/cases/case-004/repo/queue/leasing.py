"""Lease acquisition and completion. This is where the queue's core
correctness invariant lives: at most one worker may believe it holds a
valid lease on a given job at any moment, and a worker that lost its lease
(expired before it finished) must not be able to mark the job done."""

import time

from .models import DeadLetterEntry, Job

VISIBILITY_TIMEOUT_SECONDS = 30


class LeaseConflict(Exception):
    pass


def acquire(job: Job, worker_id: str, store) -> int:
    """Returns a fencing token. Raises LeaseConflict if another worker
    currently holds an unexpired lease on this job."""
    now = time.time()
    current = store.get_lease(job.id)
    if current is not None and current["expires_at"] > now:
        raise LeaseConflict(f"job {job.id} already leased by {current['worker_id']}")
    fencing_token = store.next_fencing_token(job.id)
    store.set_lease(job.id, worker_id=worker_id, expires_at=now + VISIBILITY_TIMEOUT_SECONDS,
                     fencing_token=fencing_token)
    job.status = "leased"
    return fencing_token


def complete(job: Job, worker_id: str, fencing_token: int, store) -> None:
    """A completion is only honored if fencing_token matches the store's
    current token for this job -- this is what prevents a worker whose
    lease already expired (and was re-acquired by someone else) from
    completing a job out from under the new lease holder."""
    current_token = store.current_fencing_token(job.id)
    if fencing_token != current_token:
        # Stale completion: silently dropped, not an error the caller sees
        # differently from success -- the job's fate is already decided by
        # whoever holds the current token.
        return
    job.status = "done"
    store.clear_lease(job.id)


def fail(job: Job, worker_id: str, error: str, store) -> None:
    job.attempts += 1
    store.clear_lease(job.id)
    if job.attempts >= job.max_attempts:
        job.status = "dead"
        store.write_dead_letter(DeadLetterEntry(
            job_id=job.id, payload=job.payload, final_error=error, died_at=time.time(),
        ))
    else:
        job.status = "queued"
