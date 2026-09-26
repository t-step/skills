#!/usr/bin/env python3
"""Summarize sync-job dead letters by error and source feed.

Usage: python3 inspect_dead_letters.py var/dead_letters/sync-<date>.jsonl
"""

import json
import sys
from collections import Counter


def main(path: str) -> None:
    by_error: Counter[str] = Counter()
    by_feed_and_error: Counter[tuple[str, str]] = Counter()

    with open(path) as f:
        for line in f:
            entry = json.loads(line)
            by_error[entry["error"]] += 1
            by_feed_and_error[(entry["source_feed"], entry["error"])] += 1

    print(f"{sum(by_error.values())} dead-letter records in {path}\n")
    print("By error:")
    for error, count in by_error.most_common():
        print(f"  {count:4d}  {error}")

    print("\nBy source feed + error:")
    for (feed, error), count in by_feed_and_error.most_common():
        print(f"  {count:4d}  feed={feed!r}  error={error}")


if __name__ == "__main__":
    main(sys.argv[1])
