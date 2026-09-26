"""Outbound webhook dispatcher.

Signs each outbound webhook payload with an HMAC over the request body,
using a shared secret configured for the partner. The signature lets the
partner verify the request actually came from us.
"""

import hashlib
import hmac
import os
import time

import requests

# Read once at process startup. If the secret in the environment changes
# after this process has already started, this module-level value does
# not pick up the new one until the process restarts.
WEBHOOK_SIGNING_SECRET = os.environ["WEBHOOK_SIGNING_SECRET"]


def sign_payload(body: bytes) -> str:
    return hmac.new(
        WEBHOOK_SIGNING_SECRET.encode(), body, hashlib.sha256
    ).hexdigest()


def deliver(url: str, body: bytes) -> None:
    signature = sign_payload(body)
    headers = {"X-Webhook-Signature": signature}

    for attempt in range(3):
        resp = requests.post(url, data=body, headers=headers, timeout=10)
        if resp.status_code < 300:
            _log(f"webhook delivered: status={resp.status_code}")
            return
        _log(f"webhook delivery failed: status={resp.status_code}")
        time.sleep(2**attempt)

    _log("webhook delivery failed after 3 attempts")


def _log(message: str) -> None:
    # Local log only -- not shipped to a central log store for this
    # service yet.
    print(f"[webhook_dispatcher] {message}")
