"""Exercises the real sync_batch() against the real sandbox. Run this
(or run_sync.py) after any change to confirm what actually happens --
don't infer the result from reading the code alone."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fulfillco_client import sync_batch

ORDERS = [
    {
        "order_id": f"ORD-{7000 + i}",
        "warehouse_id": "WH-4",
        "items": [{"sku": "SKU-1", "qty": 1, "unit": "ea"}],
    }
    for i in range(25)
]


def test_full_batch_syncs_successfully():
    results = sync_batch(ORDERS)
    failing = {order_id: resp for order_id, resp in results.items() if resp.status != 200}
    assert not failing, f"{len(failing)}/{len(ORDERS)} orders failed; example: {next(iter(failing.values()))}"
