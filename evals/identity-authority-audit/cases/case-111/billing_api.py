"""Billing history endpoint."""

from flask import Blueprint, session, abort

billing_bp = Blueprint("billing", __name__)


@billing_bp.route("/api/billing-history", methods=["GET"])
def billing_history():
    user_id = session.get("user_id")
    if not user_id:
        abort(401)
    # No additional freshness or factor check here -- every session for
    # this tenant was already established via the IdP's sole primary
    # factor (WebAuthn), per idp_tenant_config.yaml. There is no
    # password-only session this endpoint could be trusting instead.
    return fetch_billing_history(user_id)


def fetch_billing_history(user_id):
    ...  # not relevant to this audit
