from dataclasses import dataclass


@dataclass
class Job:
    id: str
    payload: bytes
    status: str  # "queued" | "leased" | "done" | "dead"
    attempts: int
    max_attempts: int = 5


@dataclass
class Lease:
    """A worker's temporary, exclusive right to work one Job. This
    dataclass documents the concept's shape; it is never constructed by
    leasing.py, which reads and writes the actual lease record through
    the store's own accessors (store.get_lease/set_lease/clear_lease)
    instead. See leasing.py's acquire() for the real storage path."""

    job_id: str
    worker_id: str
    expires_at: float
    fencing_token: int


@dataclass
class DeadLetterEntry:
    job_id: str
    payload: bytes
    final_error: str
    died_at: float
