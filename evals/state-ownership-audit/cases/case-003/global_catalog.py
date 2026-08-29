"""GlobalCatalog: a read-only aggregation service with no fulfillment
authority of its own. Polls every FC every 60 seconds over the FCs' public
read APIs and sums what it gets back. Never writes to any FC's database,
and no FC ever reads from GlobalCatalog to decide whether it can sell."""

import time
import fc_client  # thin HTTP client hitting each FC's read-only inventory API

KNOWN_FCS = ["fc-east", "fc-west", "fc-central"]


def refresh_total_available(sku: str) -> None:
    total = 0
    for fc in KNOWN_FCS:
        try:
            total += fc_client.get_available_units(fc, sku)
        except fc_client.FCUnreachable:
            # A partitioned FC is simply skipped this cycle; its units are
            # undercounted in the aggregate until the next successful poll.
            continue
    catalog_db.execute(
        "UPDATE catalog_totals SET total_available = %s, refreshed_at = now() "
        "WHERE sku = %s",
        [total, sku],
    )


def run_forever():
    while True:
        for sku in catalog_db.query("SELECT sku FROM catalog_totals"):
            refresh_total_available(sku["sku"])
        time.sleep(60)
