"""catalog/dataset_version.py -- owned by the Catalog team."""

import enum
from datetime import datetime

from db import session
from models import DatasetVersion


class DatasetVersionStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


def create_draft(source_job_id: int, row_count: int) -> int:
    """Called by the ingestion pipeline (see ingestion/import_job.py's
    `finish()`) after a successful import. This is the only way a
    DatasetVersion is ever created -- there is no manual creation path.
    """
    version = DatasetVersion(
        status=DatasetVersionStatus.DRAFT.value,
        source_job_id=source_job_id,
        row_count=row_count,
        created_at=datetime.utcnow(),
    )
    session.add(version)
    session.commit()
    return version.id


def publish(version_id: int, curator_id: int) -> None:
    """Manually triggered by a curator from the Catalog UI, any time
    after a version is created. Nothing about `source_job_id` or the
    ingestion pipeline is consulted here -- publish only checks the
    version's own current status and the curator's permissions.
    """
    version = session.get(DatasetVersion, version_id)
    assert version.status == DatasetVersionStatus.DRAFT.value
    version.status = DatasetVersionStatus.PUBLISHED.value
    version.published_by = curator_id
    version.published_at = datetime.utcnow()
    session.commit()


def archive(version_id: int) -> None:
    version = session.get(DatasetVersion, version_id)
    assert version.status == DatasetVersionStatus.PUBLISHED.value
    version.status = DatasetVersionStatus.ARCHIVED.value
    session.commit()
