from abc import ABC, abstractmethod

from domain.order import Order


class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None: ...

    @abstractmethod
    def get(self, order_id: str) -> Order: ...
