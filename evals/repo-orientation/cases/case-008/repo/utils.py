def parse_records(text: str) -> list[dict]:
    records = []
    for line in text.splitlines():
        if not line.strip():
            continue
        key, _, value = line.partition("=")
        records.append({key.strip(): value.strip()})
    return records
