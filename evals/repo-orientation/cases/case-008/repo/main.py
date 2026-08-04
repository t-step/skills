import sys

from utils import parse_records


def main():
    path = sys.argv[1]
    with open(path) as f:
        records = parse_records(f.read())
    for r in records:
        print(r)


if __name__ == "__main__":
    main()
