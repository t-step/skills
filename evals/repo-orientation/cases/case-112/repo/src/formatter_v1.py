"""Original table formatter, from before column-width alignment existed."""


def format_table_v1(rows: list[dict]) -> str:
    if not rows:
        return ""
    cols = list(rows[0].keys())
    lines = [",".join(cols)]
    for row in rows:
        lines.append(",".join(str(row[c]) for c in cols))
    return "\n".join(lines)
