# Repo snapshot: reports/csv_export.py (full file, AFTER the diff below is applied)

```python
"""Row-oriented export helpers for admin report downloads."""

import json


def rows_to_json(rows: list[dict], columns: list[str]) -> str:
    """Render `rows` as a JSON array, keeping only `columns` per row, in order."""
    projected = [{c: row[c] for c in columns} for row in rows]
    return json.dumps(projected)


def rows_to_csv(rows: list[dict], columns: list[str]) -> str:
    """Render `rows` as CSV text, using `columns` as the header and field order."""
    lines = [','.join(columns)]
    for row in rows:
        values = [str(row[c]) for c in columns]
        lines.append(','.join(values))
    return '\n'.join(lines) + '\n'
```
