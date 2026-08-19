def with_retry(fn, attempts=3):
    """Used by internal batch jobs. A job that still fails after retrying
    should not take the whole batch down -- log and move on."""
    for _ in range(attempts):
        try:
            return fn()
        except Exception:
            continue
    return None
