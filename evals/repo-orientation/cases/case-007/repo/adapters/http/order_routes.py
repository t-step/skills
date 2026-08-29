from boundary.order_repository import OrderRepository


def register_routes(app, repo: OrderRepository):
    @app.get("/orders/<order_id>")
    def get_order(order_id):
        order = repo.get(order_id)
        return {"items": order.items, "fulfillable": order.is_fulfillable()}
