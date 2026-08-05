from app.payments.gateway_client import charge_async
from app.orders.orders import create_pending_order


def start_checkout(cart: dict) -> dict:
    """Creates a pending order and submits the charge. The order's final
    status and confirmed total aren't known until the gateway's webhook
    fires later -- this function only returns a pending charge_id.
    """
    order = create_pending_order(cart)
    charge_id = charge_async(order.id, order.amount_cents)
    order.charge_id = charge_id
    return {"order_id": order.id, "status": "pending", "charge_id": charge_id}
