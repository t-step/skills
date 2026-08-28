"""ingestion/import_job.py -- owned by the Data Platform team."""

import enum
from datetime import datetime

from db import session
from models import ImportJob, ImportJobStatus
from catalog_client import create_draft_dataset_version


class ImportJobStatus(str, enum.Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


def start(job_id: int) -> None:
    job = session.get(ImportJob, job_id)
    assert job.status == ImportJobStatus.QUEUED.value
    job.status = ImportJobStatus.RUNNING.value
    job.started_at = datetime.utcnow()
    session.commit()


def finish(job_id: int, row_count: int) -> None:
    job = session.get(ImportJob, job_id)
    assert job.status == ImportJobStatus.RUNNING.value
    job.status = ImportJobStatus.COMPLETED.value
    job.completed_at = datetime.utcnow()
    job.row_count = row_count
    session.commit()

    # Fire-and-forget call into the Catalog service (owned by a different
    # team). This is the only place ImportJob code ever calls into
    # Catalog. Catalog's own API returns the new version's id; ImportJob
    # does not store it or look it up again afterward.
    create_draft_dataset_version(source_job_id=job.id, row_count=row_count)


def fail(job_id: int, error: str) -> None:
    job = session.get(ImportJob, job_id)
    job.status = ImportJobStatus.FAILED.value
    job.error_message = error
    job.completed_at = datetime.utcnow()
    session.commit()
    # No call into Catalog on failure -- no dataset version is created.
