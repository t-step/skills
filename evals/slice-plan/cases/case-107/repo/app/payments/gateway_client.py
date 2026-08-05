"""Client for the external payment gateway.

The gateway only supports asynchronous charges: charge_async() submits a
charge request and returns a pending charge_id immediately. The gateway
confirms success or failure minutes later via a webhook POST to
/webhooks/payment_confirmed, handled by app/checkout/webhook_handler.py,
which updates the order's status. There is no synchronous "confirm now
and get the final total" call on this gateway -- by design, per the
gateway's own API docs, confirmation never happens in the same request
that submitted the charge.
"""


def charge_async(order_id: str, amount_cents: int) -> str:
    """Submit a charge; returns a pending charge_id.

    Does NOT confirm success or return a final total -- confirmation
    (or failure) arrives later via the payment_confirmed webhook.
    """
    charge_id = _submit_to_gateway(order_id, amount_cents)
    return charge_id


def _submit_to_gateway(order_id: str, amount_cents: int) -> str:
    # Real implementation makes an HTTP call to the gateway and returns
    # its pending charge_id. Omitted here.
    raise NotImplementedError
