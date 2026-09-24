"""Acquires a short-lived, audience-scoped identity token for this
workload's own GCP service account, via the metadata server -- the
mechanism GKE Workload Identity (and Cloud Run's built-in service
identity) exposes automatically to every pod/instance running under it.

No static key is issued, stored, or checked in anywhere for this job: the
token is minted on demand by the metadata server, is valid for one
audience only, and expires in under an hour.
"""

import requests

METADATA_SERVER_BASE = "http://metadata.google.internal/computeMetadata/v1"
METADATA_HEADERS = {"Metadata-Flavor": "Google"}


def get_workload_id_token(audience: str) -> str:
    """Return an OIDC identity token scoped to `audience`, signed by
    Google, asserting this workload's own service account identity
    (currently `nightly-reconciliation@acme-prod.iam.gserviceaccount.com`,
    bound via Workload Identity to this job's Kubernetes service account --
    no key file, no long-lived secret involved)."""
    resp = requests.get(
        f"{METADATA_SERVER_BASE}/instance/service-accounts/default/identity",
        params={"audience": audience, "format": "full"},
        headers=METADATA_HEADERS,
        timeout=5,
    )
    resp.raise_for_status()
    return resp.text
