import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from schema.order_created_schema import OrderCreatedValidationError, validate_order_created


def _load(name):
    return json.loads((ROOT / "samples" / name).read_text())


def test_old_shape_payload_validates_successfully():
    payload = _load("old_producer_payload.json")
    validate_order_created(payload)  # does not raise


def test_new_producer_payload_fails_with_observed_error():
    payload = _load("new_producer_payload.json")
    try:
        validate_order_created(payload)
        assert False, "expected OrderCreatedValidationError"
    except OrderCreatedValidationError as exc:
        assert "shipping_method" in str(exc)
        assert "field required" in str(exc)


def test_new_producer_payload_with_field_renamed_back_validates():
    payload = _load("new_producer_payload.json")
    corrected = dict(payload)
    corrected["shipping_method"] = "STANDARD"  # GROUND -> STANDARD, matching the old enum
    del corrected["fulfillment_method"]
    validate_order_created(corrected)  # does not raise


if __name__ == "__main__":
    test_old_shape_payload_validates_successfully()
    test_new_producer_payload_fails_with_observed_error()
    test_new_producer_payload_with_field_renamed_back_validates()
    print("all tests passed")
