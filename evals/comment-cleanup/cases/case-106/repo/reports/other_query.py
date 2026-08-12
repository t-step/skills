"""Other report queries — already paginated, unlike fetch_all_results."""


def fetch_page(db, report_id: str, offset: int, limit: int = 500) -> list[dict]:
    return db.query(
        f"SELECT * FROM results WHERE report_id = '{report_id}' "
        f"ORDER BY id LIMIT {limit} OFFSET {offset}"
    ).all()
