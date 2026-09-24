"""Tool implementations for orders-mcp. Every handler receives the
caller's AuthContext (delegating user + agent identity + granted scopes)
already established by auth_middleware -- never a raw token -- and is
responsible for its own destination-side resource authorization and
audit logging."""

import logging

import db  # internal Postgres access layer

audit_log = logging.getLogger("orders_mcp.audit")


def list_orders(ctx, **_):
    orders = db.query(
        "SELECT id, status, total_cents FROM orders WHERE account_id = %s",
        [ctx.claims["account_id"]],
    )
    audit_log.info(
        "tool=list_orders delegating_user=%s agent=%s account=%s result_count=%d",
        ctx.delegating_user_id, ctx.agent_id, ctx.claims["account_id"], len(orders),
    )
    return {"orders": orders}


def refund_order(ctx, order_id: str, amount_cents: int):
    order = db.query_one("SELECT * FROM orders WHERE id = %s", [order_id])
    if order is None:
        return {"error": "not_found", "message": f"no such order: {order_id}"}

    # Destination-side resource authorization: the scope check in dispatch
    # only established that this delegation carries *some* orders:refund
    # grant. It says nothing about whether this particular order belongs
    # to the account that grant was actually issued for -- a valid token
    # with the right scope is not sufficient on its own.
    if order["account_id"] != ctx.claims["account_id"]:
        audit_log.warning(
            "tool=refund_order denied delegating_user=%s agent=%s order=%s reason=account_mismatch",
            ctx.delegating_user_id, ctx.agent_id, order_id,
        )
        return {"error": "forbidden", "message": "order does not belong to the delegating user's account"}

    if amount_cents > order["total_cents"]:
        return {"error": "invalid_amount", "message": "refund exceeds order total"}

    db.execute(
        "UPDATE orders SET status = 'refunded', refunded_cents = %s, updated_at = now() WHERE id = %s",
        [amount_cents, order_id],
    )

    # Preserved actor attribution: both the human whose authority this
    # refund executes under and the agent that invoked it are recorded on
    # every call, not just "a valid token called this."
    audit_log.info(
        "tool=refund_order delegating_user=%s agent=%s order=%s amount_cents=%d",
        ctx.delegating_user_id, ctx.agent_id, order_id, amount_cents,
    )
    return {"status": "refunded", "order_id": order_id, "amount_cents": amount_cents}
