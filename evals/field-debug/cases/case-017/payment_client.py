"""payments-svc's client for capturing a previously-authorized payment
against PaymentGate.
"""

import logging

import requests

logger = logging.getLogger("payments_svc.payment_client")

GATEWAY_URL = "https://api.paymentgate.example/v1/captures"
CLIENT_TIMEOUT_SECONDS = 5.0


def capture_payment(order_id: str, amount_cents: int, attempt: int = 1) -> dict:
    logger.info("capture_payment(%s, %s) started (attempt %d)", order_id, amount_cents, attempt)
    try:
        response = requests.post(
            GATEWAY_URL,
            json={"order_id": order_id, "amount_cents": amount_cents},
            timeout=CLIENT_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        result = response.json()
        logger.info(
            "capture_payment(%s) succeeded, gateway_txn_id=%s",
            order_id,
            result["gateway_txn_id"],
        )
        return result
    except requests.exceptions.Timeout:
        logger.warning(
            "capture_payment(%s) request timed out after %.1fs -- retrying",
            order_id,
            CLIENT_TIMEOUT_SECONDS,
        )
        if attempt >= 2:
            raise
        return capture_payment(order_id, amount_cents, attempt=attempt + 1)
