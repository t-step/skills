"""warehouse-svc's integration client for Fulfillco's order-ingestion
endpoint. Sends the nightly batch of pending fulfillment orders."""

import threading
import warnings

from fulfillco_sandbox import submit_order

# Current auth config -- unchanged since before Fulfillco's Sept 22 cutover.
API_KEY = "legacy-key-88214-DEPRECATED"


def build_headers(payload):
    return {"Authorization": f"Bearer {API_KEY}"}


def build_payload(order):
    return {
        "order_id": order["order_id"],
        "warehouse_id": order["warehouse_id"],
        "line_items": order["items"],
    }


def sync_one(order, results):
    warnings.warn(
        "fulfillco_sdk_compat: falling back to legacy TLS cipher list for this host",
        DeprecationWarning,
        stacklevel=2,
    )
    payload = build_payload(order)
    headers = build_headers(payload)
    resp = submit_order(payload, headers)
    results[order["order_id"]] = resp


def sync_batch(orders):
    """Fires the whole batch at once -- historically fine at our old,
    much smaller nightly order volume."""
    results = {}
    threads = [threading.Thread(target=sync_one, args=(o, results)) for o in orders]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return results
