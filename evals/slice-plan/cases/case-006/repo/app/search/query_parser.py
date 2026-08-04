"""Parses a simple search query string into a structured filter."""

import shlex


def parse_query(raw: str) -> dict:
    tokens = shlex.split(raw)
    filters = {"must": [], "or": [], "fields": {}}
    mode = "must"
    for token in tokens:
        if token.upper() == "OR":
            mode = "or"
            continue
        if ":" in token:
            field, value = token.split(":", 1)
            filters["fields"][field] = value
            continue
        filters[mode].append(token)
    return filters
