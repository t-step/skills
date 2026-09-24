"""Nightly ledger reconciliation job.

Runs on a fixed schedule (Cloud Scheduler -> Cloud Run job, 02:00 UTC)
with no interactive session, no queued user request, and no human
operator in the loop at trigger time or at any point during execution.
"""

import json
import logging

import requests
from google.cloud import storage

from workload_identity import get_workload_id_token

logger = logging.getLogger("nightly-reconciliation")

RECONCILIATION_BUCKET = "acme-ledger-exports"
RECONCILIATION_OBJECT = "nightly/pending_reconciliation.json"
LEDGER_SERVICE_URL = "https://ledger-service.internal.acme.example.com"
LEDGER_SERVICE_AUDIENCE = LEDGER_SERVICE_URL


def load_pending_records() -> list[dict]:
    """Read the nightly export from cloud storage. Uses the job's default
    credentials (the workload's own GCP service account, granted
    roles/storage.objectViewer on this bucket) -- no static key, no
    forwarded user token, nothing checked in."""
    client = storage.Client()
    bucket = client.bucket(RECONCILIATION_BUCKET)
    blob = bucket.blob(RECONCILIATION_OBJECT)
    return json.loads(blob.download_as_text())


def reconcile(records: list[dict]) -> dict:
    """Call ledger-service's internal reconciliation endpoint,
    authenticating as this job's own workload identity."""
    id_token = get_workload_id_token(audience=LEDGER_SERVICE_AUDIENCE)

    resp = requests.post(
        f"{LEDGER_SERVICE_URL}/internal/reconcile",
        headers={"Authorization": f"Bearer {id_token}"},
        json={"records": records},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def main():
    records = load_pending_records()
    logger.info("loaded %d pending records for reconciliation", len(records))
    result = reconcile(records)
    logger.info("reconciliation complete: %s", result)


if __name__ == "__main__":
    main()
