"""API A -- the first hop the BFF calls directly."""

import jwt
import requests

SIGNING_KEY = "shared-hmac-secret"


def validate_incoming_token(token: str) -> dict:
    """Full validation: signature, expiry, AND audience."""
    claims = jwt.decode(
        token,
        SIGNING_KEY,
        algorithms=["HS256"],
        audience="api-a",  # rejects anything not minted for API A
        issuer="https://auth.example.com/",
    )
    return claims


def get_order_summary(request):
    token = request.headers["Authorization"].removeprefix("Bearer ")
    claims = validate_incoming_token(token)  # raises on bad aud/exp/sig

    order_id = request.args["order_id"]

    # API A needs line-item detail from API B to build the summary. It
    # forwards the exact same token it received -- no exchange, no new
    # token minted for this hop.
    resp = requests.get(
        f"https://api-b.internal/orders/{order_id}/line-items",
        headers={"Authorization": f"Bearer {token}"},
    )
    return {"user": claims["sub"], "order_id": order_id, "line_items": resp.json()}
