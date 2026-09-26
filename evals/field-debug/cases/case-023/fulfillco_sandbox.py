"""Local sandbox harness for Fulfillco's fulfillment-ingestion endpoint,
maintained by the fulfillment platform team to mirror Fulfillco's
documented API contract for offline testing, without hitting their real
service. Not Fulfillco's actual server -- built to enforce the same rules
their docs and migration notices describe, in the same order their real
endpoint does: authentication, then payload validation, then the
per-account concurrency limit.
"""

import hashlib
import hmac
import threading
import time

HMAC_SECRET = "fc_live_secret_7f3a9c2e"
MAX_CONCURRENT_INFLIGHT = 20

_inflight_lock = threading.Lock()
_inflight_count = 0


class FulfillcoResponse:
    def __init__(self, status, body):
        self.status = status
        self.body = body

    def __repr__(self):
        return f"<{self.status} {self.body}>"


def _check_auth(headers):
    sig = headers.get("X-Fulfillco-Signature")
    if not sig:
        return False
    payload_hash = headers.get("X-Fulfillco-Payload-Hash", "")
    expected = hmac.new(HMAC_SECRET.encode(), payload_hash.encode(), hashlib.sha256).hexdigest()
    return sig == expected


def _check_schema(payload):
    required_top = {"order_id", "warehouse_id", "items"}
    missing = required_top - payload.keys()
    if missing:
        return False, f"missing required field(s): {sorted(missing)}"
    if not isinstance(payload["items"], list):
        return False, "'items' must be an array of {sku, qty, unit} objects (schema v2) -- got a different shape"
    for item in payload["items"]:
        if not isinstance(item, dict) or not {"sku", "qty", "unit"}.issubset(item.keys()):
            return False, "'items' must be an array of {sku, qty, unit} objects (schema v2)"
    return True, None


def submit_order(payload, headers):
    """Mirrors Fulfillco's documented per-request checks, in order."""
    global _inflight_count

    if not _check_auth(headers):
        return FulfillcoResponse(
            401,
            {
                "error": "unauthorized",
                "detail": (
                    "legacy API-key auth was retired at the Sept 22 cutover -- "
                    "sign requests with HMAC-SHA256 per the migration notice"
                ),
            },
        )

    ok, err = _check_schema(payload)
    if not ok:
        return FulfillcoResponse(422, {"error": "validation_failed", "detail": err})

    with _inflight_lock:
        _inflight_count += 1
        current = _inflight_count
    try:
        # Real endpoints don't resolve a burst of near-simultaneous
        # requests instantaneously either -- this window is what makes the
        # concurrency cap below actually observable under a real burst.
        time.sleep(0.02)
        if current > MAX_CONCURRENT_INFLIGHT:
            return FulfillcoResponse(
                429,
                {
                    "error": "rate_limited",
                    "detail": f"max {MAX_CONCURRENT_INFLIGHT} concurrent in-flight requests per account -- retry with backoff",
                },
            )
        return FulfillcoResponse(200, {"status": "accepted", "order_id": payload["order_id"]})
    finally:
        with _inflight_lock:
            _inflight_count -= 1
