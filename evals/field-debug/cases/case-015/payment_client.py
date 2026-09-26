"""checkout-svc's client for the PaymentCo gateway.

API_KEY is read once, at process start, from the environment. There is
no code path anywhere in this module (or the rest of checkout-svc) that
re-reads PAYMENT_API_KEY after start-up -- picking up a rotated key
requires the process to restart.
"""

import os

import requests

API_KEY = os.environ["PAYMENT_API_KEY"]

GATEWAY_URL = "https://api.paymentco.example/v1/charges"


def charge(order_id: str, amount_cents: int) -> dict:
    response = requests.post(
        GATEWAY_URL,
        json={"order_id": order_id, "amount_cents": amount_cents},
        headers={"Authorization": f"Bearer {API_KEY}"},
        timeout=8,
    )
    response.raise_for_status()
    return response.json()
