"""orders-svc's outbound client for partner-erp-gateway. Current version
(v3.15) -- added automatic retry-on-5xx this release."""

import time

import requests

GATEWAY_URL = "https://gateway.partner-erp.example/v1/orders/sync"
RETRY_COUNT = 3
RETRY_INTERVAL_SECONDS = 0.2  # fixed interval, no backoff, no jitter


def _call_gateway(order_payload):
    last_response = None
    for attempt in range(RETRY_COUNT + 1):
        last_response = requests.post(GATEWAY_URL, json=order_payload, timeout=5)
        if last_response.status_code < 500:
            return last_response
        if attempt < RETRY_COUNT:
            time.sleep(RETRY_INTERVAL_SECONDS)
    return last_response


def sync_order(order_payload):
    response = _call_gateway(order_payload)
    if response.status_code >= 500:
        raise GatewaySyncError(
            f"partner-erp-gateway returned {response.status_code} after {RETRY_COUNT} retries"
        )
    return response.json()


class GatewaySyncError(Exception):
    pass
