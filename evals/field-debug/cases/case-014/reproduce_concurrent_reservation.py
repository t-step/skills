"""Deterministically reproduces the oversell using the real
reserve_and_confirm() code path from checkout_service.py, run from two
threads against a shared on-disk sqlite database.

Two threading.Event objects force the exact interleaving described by
the audit history: both workers read `available` before either one
writes, so both decide the sale is valid from the same stale value.
Nothing here is a re-implementation of the production logic -- both
"workers" call the identical function two real app instances would call.
"""

import os
import sqlite3
import tempfile
import threading

from checkout_service import init_db, reserve_and_confirm

DB_PATH = os.path.join(tempfile.gettempdir(), "case-014-repro.sqlite3")

t1_read_done = threading.Event()
t2_read_done = threading.Event()

results = {}


def worker_one():
    conn = sqlite3.connect(DB_PATH, timeout=10)

    def after_read():
        t1_read_done.set()
        t2_read_done.wait()

    results["ORD-88841"] = reserve_and_confirm(
        conn,
        "SNK-4471",
        "ORD-88841",
        "checkout-app-03",
        "2026-09-20T14:03:21.184Z",
        after_read=after_read,
    )
    conn.close()


def worker_two():
    t1_read_done.wait()
    conn = sqlite3.connect(DB_PATH, timeout=10)

    def after_read():
        t2_read_done.set()

    results["ORD-88842"] = reserve_and_confirm(
        conn,
        "SNK-4471",
        "ORD-88842",
        "checkout-app-07",
        "2026-09-20T14:03:21.199Z",
        after_read=after_read,
    )
    conn.close()


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    seed_conn = sqlite3.connect(DB_PATH)
    init_db(seed_conn)
    seed_conn.execute(
        "INSERT INTO inventory (sku, available, last_updated_by) VALUES (?, ?, ?)",
        ("SNK-4471", 1, "seed"),
    )
    seed_conn.commit()
    seed_conn.close()

    t1 = threading.Thread(target=worker_one)
    t2 = threading.Thread(target=worker_two)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    check_conn = sqlite3.connect(DB_PATH)
    available = check_conn.execute(
        "SELECT available FROM inventory WHERE sku = ?", ("SNK-4471",)
    ).fetchone()[0]
    confirmed = check_conn.execute(
        "SELECT order_id FROM orders WHERE sku = ? AND status = 'confirmed' ORDER BY order_id",
        ("SNK-4471",),
    ).fetchall()
    check_conn.close()

    print(f"starting stock: 1 unit of SNK-4471")
    print(f"both workers' results: {results}")
    print(f"final inventory.available: {available}")
    print(f"confirmed orders against SNK-4471: {[r[0] for r in confirmed]}")
    print(f"confirmed order count: {len(confirmed)}")

    assert available == 0, f"expected available to end at 0, got {available}"
    assert len(confirmed) == 2, f"expected 2 confirmed orders from 1 unit of stock, got {len(confirmed)}"
    print("\nREPRODUCED: 1 unit of stock, 0 SoldOutError raised, 2 confirmed orders.")


if __name__ == "__main__":
    main()
