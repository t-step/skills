"""shipping-label-consumer: consumes order.created events and generates
a shipping label for each valid one.
"""

import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from schema.order_created_schema import OrderCreatedValidationError, validate_order_created

logger = logging.getLogger("shipping_label_consumer")


def handle_order_created(message_id: str, payload: dict) -> bool:
    try:
        validate_order_created(payload)
    except OrderCreatedValidationError as exc:
        logger.error("rejected message %s: %s", message_id, exc)
        return False

    generate_shipping_label(payload)
    return True


def generate_shipping_label(payload: dict) -> None:
    # Label generation itself is out of scope for this working copy --
    # every code path that reaches here is already known-valid.
    pass
