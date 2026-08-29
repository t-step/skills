"""Public API response shapes for the v2 API surface, maintained by the
Platform API team."""

from billing.models import Customer


def account_response(customer: Customer) -> dict:
    return {
        "account_id": customer.id,
        "account_email": customer.email,
        "billing_address": customer.billing_address,
    }


def get_account(account_id: int) -> dict:
    """GET /v2/accounts/{account_id}"""
    from billing.db import get_customer  # local import, db wiring omitted

    customer = get_customer(account_id)
    return account_response(customer)
