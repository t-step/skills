"""Nightly inventory sync job.

Pulls SKU price/quantity updates from upstream vendor feeds and applies
them to the inventory database. Anything that can't be applied is written
to a dead-letter file for later inspection rather than raising, per repo
convention (see README.md).
"""

import json
import logging
from datetime import date, datetime
from pathlib import Path

logger = logging.getLogger("sync_job")

DEAD_LETTER_DIR = Path("var/dead_letters")


def parse_price(raw_price: str) -> float:
    # Vendor feeds are expected to send plain decimal strings, e.g. "12.99".
    return float(raw_price)


def write_dead_letter(record: dict, error: str) -> None:
    DEAD_LETTER_DIR.mkdir(parents=True, exist_ok=True)
    path = DEAD_LETTER_DIR / f"sync-{date.today().isoformat()}.jsonl"
    entry = {
        "sku": record.get("sku"),
        "source_feed": record.get("source_feed"),
        "raw_record": record,
        "error": error,
        "at": datetime.utcnow().isoformat(),
    }
    with path.open("a") as f:
        f.write(json.dumps(entry) + "\n")


def apply_update(record: dict) -> bool:
    """Apply one SKU update. Returns True if applied, False if skipped."""
    try:
        price = parse_price(record["price"])
        quantity = int(record["quantity"])
    except (ValueError, KeyError, TypeError) as exc:
        write_dead_letter(record, str(exc))
        return False

    _apply_to_inventory_db(record["sku"], price, quantity)
    return True


def _apply_to_inventory_db(sku: str, price: float, quantity: int) -> None:
    # Placeholder for the actual DB write -- not relevant to this
    # investigation; every call here succeeds in this evidence set.
    pass


def run(records: list[dict]) -> None:
    applied = 0
    skipped = 0
    for record in records:
        for attempt in range(3):
            if apply_update(record):
                applied += 1
                break
        else:
            skipped += 1

    logger.info("sync complete: applied=%d skipped=%d", applied, skipped)
