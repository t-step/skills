"""Mints the access token the browser/BFF sends to API A.

Called once, at login, by the BFF's session layer (not shown -- out of
scope for this chain; the browser never sees this token, only API A does).
"""

import time
import jwt

SIGNING_KEY = "shared-hmac-secret"  # pulled from secret manager in prod


def mint_token_for_api_a(user_id: str, scopes: str = "orders:read orders:write") -> str:
    """Mints a token whose audience is API A specifically."""
    claims = {
        "sub": user_id,
        "aud": "api-a",
        "iss": "https://auth.example.com/",
        "scope": scopes,
        "iat": int(time.time()),
        "exp": int(time.time()) + 900,
    }
    return jwt.encode(claims, SIGNING_KEY, algorithm="HS256")
