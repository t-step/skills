"""Runs a representative nightly batch through fulfillco_client against
the sandbox, and reports the outcome. Re-run this after any change to
confirm the actual result -- don't assume a fix worked."""

from fulfillco_client import sync_batch

ORDERS = [
    {
        "order_id": f"ORD-{7000 + i}",
        "warehouse_id": "WH-4",
        "items": [{"sku": "SKU-1", "qty": 1, "unit": "ea"}],
    }
    for i in range(25)
]


def main():
    results = sync_batch(ORDERS)
    by_status = {}
    for order_id, resp in results.items():
        by_status.setdefault(resp.status, []).append(order_id)

    print(f"batch size: {len(ORDERS)}")
    for status in sorted(by_status):
        print(f"  {status}: {len(by_status[status])} orders")

    failing = [r for r in results.values() if r.status != 200]
    if failing:
        print(f"sample failing response: {failing[0]}")
    else:
        print("all orders accepted")


if __name__ == "__main__":
    main()
