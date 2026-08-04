# Goal

`fetch_with_retry(url, max_attempts=3)` in `net/client.py` currently makes a
single HTTP GET and raises immediately on any failure. Add retry with
exponential backoff: on a failed GET, wait `0.1 * (2 ** attempt)` seconds and
retry, up to `max_attempts` total attempts, then re-raise the last exception
if all attempts fail. Only GET requests are in scope for this change.
