"""ledger-service: internal reconciliation endpoint.

Only ever called by scheduled reconciliation workloads, never by an
end-user session or a BFF acting on a user's behalf -- reconciliation
operates over the whole ledger, not one account's records, so there is no
per-user resource to scope against here.
"""

from flask import Flask, abort, jsonify, request
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token

app = Flask(__name__)

EXPECTED_AUDIENCE = "https://ledger-service.internal.acme.example.com"

# Workload identities allowed to invoke reconciliation. Hardcoded here
# rather than sourced from the org's central policy engine -- every caller
# still goes through the signature/issuer/audience verification below;
# this list only decides which already-authenticated workload identity is
# then permitted to proceed.
ALLOWED_RECONCILIATION_WORKLOADS = {
    "nightly-reconciliation@acme-prod.iam.gserviceaccount.com",
}


def authenticate_workload():
    """Validate the bearer token's signature, issuer, and audience against
    Google's public keys, and return the caller's service-account identity
    claims."""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        abort(401, "missing bearer token")
    token = auth_header[len("Bearer "):]

    try:
        claims = google_id_token.verify_oauth2_token(
            token, google_requests.Request(), audience=EXPECTED_AUDIENCE
        )
    except ValueError as exc:
        abort(401, f"invalid workload identity token: {exc}")

    return claims


def authorize_reconciliation_workload(claims: dict):
    """Workload-scoped authorization check: is this specific calling
    service identity on the allow-list for the reconciliation operation."""
    caller_identity = claims.get("email")
    if not claims.get("email_verified") or caller_identity not in ALLOWED_RECONCILIATION_WORKLOADS:
        abort(403, f"workload identity {caller_identity!r} not permitted to run reconciliation")


@app.route("/internal/reconcile", methods=["POST"])
def reconcile():
    claims = authenticate_workload()
    authorize_reconciliation_workload(claims)

    records = request.get_json()["records"]
    processed = _apply_reconciliation(records)

    return jsonify({"status": "ok", "processed": processed, "workload": claims["email"]})


def _apply_reconciliation(records: list[dict]) -> int:
    # Ledger-matching logic, elided for this review.
    return len(records)
