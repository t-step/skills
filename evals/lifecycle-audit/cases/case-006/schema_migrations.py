"""platform/schema_migrations.py -- owned by the Platform/Infra team.

Tracks database schema migrations. Rows are inserted by the migration
tool itself when a migration file is first discovered in the repo; this
module only updates status as the migration runner executes them.
"""

import enum
from datetime import datetime

from db import session
from models import SchemaMigration


class MigrationStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    FAILED = "failed"


def run_migration(migration_id: str) -> None:
    m = session.get(SchemaMigration, migration_id)
    assert m.status == MigrationStatus.PENDING.value
    m.status = MigrationStatus.RUNNING.value
    m.started_at = datetime.utcnow()
    session.commit()
    try:
        _execute_sql(m.sql_path)
    except Exception as exc:
        m.status = MigrationStatus.FAILED.value
        m.error = str(exc)
        session.commit()
        raise
    m.status = MigrationStatus.COMPLETE.value
    m.completed_at = datetime.utcnow()
    session.commit()


def _execute_sql(path: str) -> None:
    ...
