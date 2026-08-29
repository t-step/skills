"""Result-set queries against the reports table."""


def fetch_all_results(db, report_id: str) -> list[dict]:
    # TODO: paginate this — returns the full unbounded result set, which
    # will not scale once a report has more than a few thousand rows
    return db.query(
        f"SELECT * FROM results WHERE report_id = '{report_id}'"
    ).all()
