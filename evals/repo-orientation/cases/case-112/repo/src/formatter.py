"""Current table formatter, used by src/cli.py."""


def format_table(rows: list[dict]) -> str:
    if not rows:
        return ""
    cols = list(rows[0].keys())
    widths = [max(len(c), *(len(str(r[c])) for r in rows)) for c in cols]
    lines = [" | ".join(c.ljust(w) for c, w in zip(cols, widths))]
    for row in rows:
        lines.append(" | ".join(str(row[c]).ljust(w) for c, w in zip(cols, widths)))
    return "\n".join(lines)
