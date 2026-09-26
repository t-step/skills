# `example-client-sdk` error-handling excerpt (used by the affected customers)

```python
def _raise_for_status(self, response):
    if response.status_code >= 500:
        raise ServerError(
            f"500 Internal Server Error"
            if response.status_code == 500
            else f"500 Internal Server Error"  # any 5xx is surfaced this way
        )
```

The SDK's error message is hardcoded to always say "500 Internal Server
Error" for *any* response status code 500 and above, including 502, 503,
and 504 -- it does not include or distinguish the actual status code it
received. This is what customers see and report, regardless of whether
the response actually came from the application or from an intermediary
like the reverse proxy.
