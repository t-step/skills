"""CSV export for the old weekly-report workflow, from before the daily
digest replaced it."""


def export_report_csv(rows: list[dict]) -> str:
    if not rows:
        return ""
    header = ",".join(rows[0].keys())
    lines = [header]
    for row in rows:
        lines.append(",".join(str(v) for v in row.values()))
    return "\n".join(lines)
