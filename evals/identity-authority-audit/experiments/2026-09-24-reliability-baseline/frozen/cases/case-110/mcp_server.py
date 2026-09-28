"""Orders MCP server: tool registration and dispatch for the support-ops
agent platform. Each tool declares its own required scope, and dispatch
rejects a call before it ever reaches the tool implementation if the
authenticated delegation doesn't carry that scope."""

from auth_middleware import AuthError, authenticate
import orders_tools

TOOLS = {
    "list_orders": {
        "handler": orders_tools.list_orders,
        "required_scope": "orders:read",
    },
    "refund_order": {
        "handler": orders_tools.refund_order,
        "required_scope": "orders:refund",
    },
}
# orders:refund is a separately-granted, materially narrower scope than
# orders:read. Most delegations issued to the agent platform carry
# orders:read (needed for routine "look up my order" support flows) but
# not orders:refund, which the rep's session only picks up when refund
# capability has been explicitly authorized for that session. Read and
# destructive-write authority are never bundled under one scope here.


def handle_tool_call(bearer_token: str, tool_name: str, arguments: dict) -> dict:
    try:
        ctx = authenticate(bearer_token)
    except AuthError as e:
        return {"error": e.code, "message": e.message}

    tool = TOOLS.get(tool_name)
    if tool is None:
        return {"error": "unknown_tool", "message": f"no such tool: {tool_name}"}

    if not ctx.has_scope(tool["required_scope"]):
        return {
            "error": "insufficient_scope",
            "message": f"delegation does not carry required scope: {tool['required_scope']}",
        }

    return tool["handler"](ctx, **arguments)
