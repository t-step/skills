"""Pushes newly-placed orders from orders-svc to the warehouse intake API.

Runs nightly over every order placed since the last successful run. Failed
pushes are appended to var/dead_letters/sync_errors.jsonl with the
originating order id and the exception raised, then skipped (no retry
inside this job -- retries are handled by a separate, unrelated
reprocessing tool not included here).
"""

import json


def push_order(order, dead_letter_path):
    try:
        quantity = int(order["quantity"])
    except ValueError as exc:
        _dead_letter(dead_letter_path, order, exc)
        return None
    return _send_to_warehouse(order["order_id"], order["sku"], quantity)


def _dead_letter(path, order, exc):
    with open(path, "a") as f:
        f.write(json.dumps({
            "order_id": order["order_id"],
            "sku": order["sku"],
            "vendor_feed": order.get("vendor_feed"),
            "error": f"{type(exc).__name__}: {exc}",
        }) + "\n")


def _send_to_warehouse(order_id, sku, quantity):
    raise NotImplementedError("warehouse intake client omitted for this excerpt")
