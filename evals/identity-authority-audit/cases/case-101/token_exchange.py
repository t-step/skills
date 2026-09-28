"""Token-exchange helper used by BFF routes before calling the Orders API.

Trades the BFF's own knowledge of the current session (user_id, account_id)
for a short-lived JWT scoped specifically to the Orders API, via the
internal STS's RFC 8693-style token-exchange endpoint. Nothing from the
browser's own session cookie is present in this request -- the exchange
input is the session record the BFF already resolved server-side, not a
credential of the browser's.
"""

import time

import requests

STS_TOKEN_ENDPOINT = "https://sts.internal.example.com/token"

# This BFF's own service credential, used to authenticate the exchange
# call itself. Loaded from the platform secret store at process start.
BFF_CLIENT_ID = "bff-checkout"
BFF_CLIENT_SECRET = "<loaded from secret manager, not a literal>"

_cache: dict[str, tuple[str, float]] = {}


def exchange_for_orders_api(user_id: str, account_id: str) -> str:
    """Return a JWT audienced for the Orders API only, scoped to the
    minimum this call site needs (order read/write for the caller's own
    account), on behalf of user_id."""
    cache_key = f"{user_id}:{account_id}"
    cached = _cache.get(cache_key)
    if cached and cached[1] > time.time() + 5:
        return cached[0]

    resp = requests.post(
        STS_TOKEN_ENDPOINT,
        data={
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "client_id": BFF_CLIENT_ID,
            "client_secret": BFF_CLIENT_SECRET,
            "subject_token_type": "urn:orders-bff:internal-session",
            "subject_token": user_id,
            "audience": "orders-api",
            "scope": "orders:read orders:write",
            # account_id is carried as a claim request so the issued token
            "requested_claims": f'{{"account_id":"{account_id}"}}',
        },
        timeout=5,
    )
    resp.raise_for_status()
    body = resp.json()

    token = body["access_token"]
    expires_at = time.time() + body["expires_in"]
    _cache[cache_key] = (token, expires_at)
    return token
