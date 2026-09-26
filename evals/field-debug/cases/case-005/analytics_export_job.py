"""Nightly analytics export job.

Pages through the orders table and writes each page to the export file.
Written when daily order volume was a fraction of what it is today; the
page-count cap below was generous headroom at the time.
"""

PAGE_SIZE = 5000
MAX_PAGES = 50  # generous headroom when written -- see note below


def export_orders(db, output_file) -> None:
    for page in range(MAX_PAGES):
        rows = db.fetch_orders(offset=page * PAGE_SIZE, limit=PAGE_SIZE)
        if not rows:
            break
        output_file.write_rows(rows)
    else:
        # Loop exhausted MAX_PAGES without ever getting an empty page --
        # there was more data than the cap allowed for, and the job
        # simply stops here without writing the remainder or raising.
        raise TimeoutError(
            f"export exceeded MAX_PAGES={MAX_PAGES} without finishing"
        )
