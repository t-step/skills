"""The internal MCP server's tool dispatch.

Reached only from API B, above -- nothing else in this repository calls
it.
"""

import jwt

SIGNING_KEY = "shared-hmac-secret"


def validate_incoming_token(token: str) -> dict:
    """Same pattern as API B: signature and expiry only."""
    return jwt.decode(
        token,
        SIGNING_KEY,
        algorithms=["HS256"],
        options={"verify_aud": False},
    )


def handle_tool_call(request):
    token = request.headers["Authorization"].removeprefix("Bearer ")
    claims = validate_incoming_token(token)  # still aud="api-a", still accepted

    tool_name = request.json["tool"]
    if tool_name == "supplier_notes":
        order_id = request.json["order_id"]
        return supplier_notes_tool(order_id, acting_as=claims["sub"])
    raise ValueError(f"unknown tool: {tool_name}")


def supplier_notes_tool(order_id: str, acting_as: str) -> dict:
    ...  # queries the supplier catalog; not relevant to this audit
