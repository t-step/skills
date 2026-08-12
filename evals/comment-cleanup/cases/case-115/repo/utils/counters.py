"""Small helpers for tracking per-key counts."""


def increment(counter: dict, key: str) -> None:
    # increase the count for key by 1
    counter[key] = counter.get(key, 0) + 1


def reset_all(counter: dict) -> None:
    # clear all keys from the counter
    counter.clear()


def merge_counts(a: dict, b: dict) -> dict:
    # b's counts win on collision because b represents the more recent
    # batch; merging the other way silently drops late-arriving increments
    # that b is specifically meant to override (see incident where a's
    # stale batch overwrote same-day corrections)
    merged = dict(a)
    merged.update(b)
    return merged
