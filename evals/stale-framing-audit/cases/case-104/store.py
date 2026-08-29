"""Read path for Store.

Historical note (not in any doc): before the 2025-Q1 performance refactor,
get() and get_by_id_range() did go straight to primary and only
get_summary() used the cache. The refactor moved all three onto the same
cache-first helper to cut primary load across the board. Only the
"Caching" section of cache_docs.md was ever updated to describe the new
behavior for get_summary(); the Overview and the bypass claims for get()
and get_by_id_range() in the API reference were never revisited.
"""
import cache
import primary


def _read_through(key):
    value = cache.get(key)
    if value is not None:
        return value
    value = primary.fetch(key)
    cache.set(key, value)
    return value


def get(key):
    return _read_through(key)


def get_by_id_range(lo, hi):
    return _read_through(("range", lo, hi))


def get_summary():
    return _read_through("summary")
