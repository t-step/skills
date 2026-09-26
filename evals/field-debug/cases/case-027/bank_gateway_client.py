"""Outbound client used by ach_batch_export.py to submit the nightly ACH
batch file to Ferrous Bank's gateway."""

import requests


def submit_batch(nacha_file_bytes: bytes, batch_id: str) -> dict:
    """POST the built NACHA file to Ferrous Bank's batch-submission
    endpoint. Returns the parsed confirmation response."""
    response = requests.post(
        "https://gateway.ferrousbank.example/v1/ach/batches",
        data=nacha_file_bytes,
        headers={
            "Content-Type": "application/octet-stream",
            "X-Batch-Id": batch_id,
            # No Idempotency-Key header is sent -- see
            # ferrous_bank_api_docs_excerpt.md for what that means.
        },
        timeout=90,
    )
    response.raise_for_status()
    return response.json()
