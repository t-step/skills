def call_with_retry(fn, attempts=3):
    """Used by payment/provider integration calls. A call that still fails
    after retrying must surface as an error -- silently treating a failed
    charge as 'done, got None back' is not acceptable here."""
    last_exc = None
    for _ in range(attempts):
        try:
            return fn()
        except Exception as exc:
            last_exc = exc
    raise last_exc
