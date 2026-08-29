"""Entry point for tablefmt."""

import sys

from src.parser import parse_csv
from src.formatter import format_table


def main(argv: list[str]) -> int:
    rows = parse_csv(argv[1])
    print(format_table(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
