"""CSV parsing for tablefmt."""

import csv


def parse_csv(path: str) -> list[dict]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))
