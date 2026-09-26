"""shipping-label-consumer's contract for the order.created event.

This is the consumer's own source of truth for what it accepts -- not
the producer's. The producer team maintains its own copy of this
contract in `order-events-producer`'s repo (not included here); this
file is what actually runs at validation time in this service.
"""

REQUIRED_FIELDS = {
    "order_id": str,
    "customer_id": str,
    "shipping_method": str,
    "destination_zip": str,
}

SHIPPING_METHOD_VALUES = {"STANDARD", "EXPRESS", "OVERNIGHT"}


class OrderCreatedValidationError(Exception):
    pass


def validate_order_created(payload: dict) -> None:
    for field_name, field_type in REQUIRED_FIELDS.items():
        if field_name not in payload:
            raise OrderCreatedValidationError(
                f"1 validation error for OrderCreatedEvent\n"
                f"{field_name}\n"
                f"  field required (type=value_error.missing)"
            )
        if not isinstance(payload[field_name], field_type):
            raise OrderCreatedValidationError(
                f"1 validation error for OrderCreatedEvent\n"
                f"{field_name}\n"
                f"  str type expected (type=type_error.str)"
            )

    if payload["shipping_method"] not in SHIPPING_METHOD_VALUES:
        raise OrderCreatedValidationError(
            f"1 validation error for OrderCreatedEvent\n"
            f"shipping_method\n"
            f"  value is not a valid enumeration member; permitted: "
            f"{sorted(SHIPPING_METHOD_VALUES)} (type=type_error.enum)"
        )
