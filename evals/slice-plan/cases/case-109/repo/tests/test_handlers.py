from app.api.handlers import create_order
from app.audit.logger import all_events


def test_create_order_writes_audit_event():
    create_order("u1", [{"sku": "abc", "qty": 1}])
    assert all_events()[-1]["event_type"] == "order_created"
