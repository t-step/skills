from app.orders.orders import get_order_by_charge_id, mark_order_confirmed


def handle_payment_confirmed(charge_id: str, status: str, final_total_cents: int) -> None:
    """Called when the gateway's webhook fires -- minutes after the
    original charge_async() call, on a separate request entirely."""
    order = get_order_by_charge_id(charge_id)
    if status == "succeeded":
        mark_order_confirmed(order.id, final_total_cents)
