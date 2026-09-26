import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from checkout_service import SoldOutError, init_db, reserve_and_confirm


def _seed(conn, available=3):
    init_db(conn)
    conn.execute(
        "INSERT INTO inventory (sku, available, last_updated_by) VALUES (?, ?, ?)",
        ("SNK-4471", available, None),
    )
    conn.commit()


def test_serial_reservations_never_oversell():
    conn = sqlite3.connect(":memory:")
    _seed(conn, available=3)

    reserve_and_confirm(conn, "SNK-4471", "ORD-1", "checkout-app-01", "2026-09-20T14:00:00Z")
    reserve_and_confirm(conn, "SNK-4471", "ORD-2", "checkout-app-01", "2026-09-20T14:00:01Z")
    reserve_and_confirm(conn, "SNK-4471", "ORD-3", "checkout-app-01", "2026-09-20T14:00:02Z")

    remaining = conn.execute(
        "SELECT available FROM inventory WHERE sku = ?", ("SNK-4471",)
    ).fetchone()[0]
    confirmed = conn.execute(
        "SELECT COUNT(*) FROM orders WHERE sku = ? AND status = 'confirmed'", ("SNK-4471",)
    ).fetchone()[0]

    assert remaining == 0
    assert confirmed == 3


def test_serial_fourth_reservation_is_rejected():
    conn = sqlite3.connect(":memory:")
    _seed(conn, available=1)

    reserve_and_confirm(conn, "SNK-4471", "ORD-1", "checkout-app-01", "2026-09-20T14:00:00Z")

    try:
        reserve_and_confirm(conn, "SNK-4471", "ORD-2", "checkout-app-01", "2026-09-20T14:00:01Z")
        assert False, "expected SoldOutError"
    except SoldOutError:
        pass


if __name__ == "__main__":
    test_serial_reservations_never_oversell()
    test_serial_fourth_reservation_is_rejected()
    print("all serial tests passed")
