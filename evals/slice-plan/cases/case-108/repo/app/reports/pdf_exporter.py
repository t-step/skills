def export(rows: list) -> str:
    header = "PDF REPORT\n===========\n"
    body = "\n".join(f"{r['id']} | {r['name']} | {r['amount']}" for r in rows)
    return header + body
