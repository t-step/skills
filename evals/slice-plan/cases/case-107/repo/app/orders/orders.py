class Order:
    def __init__(self, id: str, amount_cents: int):
        self.id = id
        self.amount_cents = amount_cents
        self.charge_id = None
        self.status = "pending"
        self.confirmed_total_cents = None


_orders: dict[str, Order] = {}


def create_pending_order(cart: dict) -> Order:
    order = Order(id=_new_order_id(), amount_cents=cart["amount_cents"])
    _orders[order.id] = order
    return order


def get_order_by_charge_id(charge_id: str) -> Order:
    for order in _orders.values():
        if order.charge_id == charge_id:
            return order
    raise KeyError(charge_id)


def mark_order_confirmed(order_id: str, final_total_cents: int) -> None:
    order = _orders[order_id]
    order.status = "confirmed"
    order.confirmed_total_cents = final_total_cents


def _new_order_id() -> str:
    import uuid
    return str(uuid.uuid4())
