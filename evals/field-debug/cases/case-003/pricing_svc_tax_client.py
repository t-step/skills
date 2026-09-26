"""Tax-rate lookup client, added to pricing-svc's checkout path 2026-09-24
14:15 UTC (deploy pricing-svc v4.12.0)."""

import requests

TAX_VENDOR_URL = "https://api.taxratevendor.example.com/v1/rate"


def get_tax_rate(zip_code: str, subtotal_cents: int) -> float:
    """Look up the effective tax rate for this order.

    Called synchronously on the checkout hot path, once per checkout
    request. No caching yet -- tracked as a follow-up, not in scope for
    this incident.
    """
    resp = requests.get(
        TAX_VENDOR_URL,
        params={"zip": zip_code, "subtotal_cents": subtotal_cents},
    )
    resp.raise_for_status()
    return resp.json()["rate"]
