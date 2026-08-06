def export(rows: list) -> str:
    header = "id,name,amount\n"
    body = "\n".join(f"{r['id']},{r['name']},{r['amount']}" for r in rows)
    return header + body
