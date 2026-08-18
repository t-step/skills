# Scenario

You're working in a Python service. `pyproject.toml` lists `tenacity` as
a dependency. It's already used for exactly this purpose in
`app/clients/payment_client.py`:

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
def charge_card(payload: dict) -> dict:
    return http_client.post("/charges", json=payload).json()
```

A new outbound call to a shipping-rate API is being added in
`app/clients/shipping_client.py` and needs the same kind of retry-on-
transient-failure behavior.
