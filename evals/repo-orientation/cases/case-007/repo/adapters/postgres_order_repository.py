from boundary.order_repository import OrderRepository
from domain.order import Order


class PostgresOrderRepository(OrderRepository):
    def save(self, order: Order) -> None:
        ...  # INSERT/UPDATE against Postgres

    def get(self, order_id: str) -> Order:
        ...  # SELECT from Postgres
