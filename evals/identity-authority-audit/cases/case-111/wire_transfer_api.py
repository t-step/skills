"""Wire transfer endpoint -- the app's one place that requires more than
ordinary session presence."""

import time
from flask import Blueprint, session, request, jsonify

wire_bp = Blueprint("wire", __name__)

STEPUP_FRESHNESS_SECONDS = 5 * 60


@wire_bp.route("/api/wire-transfers", methods=["POST"])
def create_wire_transfer():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify(error="unauthenticated"), 401

    amr = session.get("amr", [])
    auth_time = session.get("auth_time", 0)
    fresh = (time.time() - auth_time) < STEPUP_FRESHNESS_SECONDS

    # Even though every session already used WebAuthn (see
    # idp_tenant_config.yaml), a session can be hours or days old. Wire
    # transfers additionally require the authentication to have happened
    # recently -- factor strength alone isn't the property being checked
    # here, freshness is.
    if not fresh or "webauthn" not in amr:
        return jsonify(stepup_required=True, redirect="/stepup?return=/api/wire-transfers"), 401

    amount = request.json["amount_cents"]
    destination = request.json["destination_account"]
    return submit_wire_transfer(user_id, amount, destination)


def submit_wire_transfer(user_id, amount_cents, destination_account):
    ...  # not relevant to this audit
