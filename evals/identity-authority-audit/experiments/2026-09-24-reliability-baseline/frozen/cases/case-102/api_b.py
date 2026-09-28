"""API B -- receives whatever API A forwards it.

No infrastructure/gateway configuration for this service exists anywhere
in this repository -- api_b.py's own request handling, below, is the only
evidence available about what happens to a request before it reaches this
code.
"""

import jwt
import requests

SIGNING_KEY = "shared-hmac-secret"


def validate_incoming_token(token: str) -> dict:
    """Checks signature and expiry only. Does not check `aud`."""
    claims = jwt.decode(
        token,
        SIGNING_KEY,
        algorithms=["HS256"],
        options={"verify_aud": False},  # audience is not checked here
    )
    return claims


def get_line_items(request):
    token = request.headers["Authorization"].removeprefix("Bearer ")
    claims = validate_incoming_token(token)  # aud="api-a" is accepted as-is

    order_id = request.view_args["order_id"]
    items = load_line_items_from_db(order_id, account_id=claims.get("sub"))

    # API B calls the internal MCP server to look up a supplier note for
    # each line item. Same pattern as the previous hop: whatever token
    # arrived is the token that goes out, unchanged.
    resp = requests.get(
        "https://mcp.internal/tools/supplier_notes",
        headers={"Authorization": f"Bearer {token}"},
        params={"order_id": order_id},
    )
    for item in items:
        item["supplier_note"] = resp.json().get(item["sku"])
    return items


def load_line_items_from_db(order_id, account_id):
    ...  # not relevant to this audit
