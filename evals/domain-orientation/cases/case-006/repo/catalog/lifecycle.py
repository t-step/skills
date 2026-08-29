"""The only place Product.status is written. Kept separate from pricing
logic on purpose -- pricing and catalog lifecycle are reviewed by
different people."""

from .models import Product


class InvalidTransition(Exception):
    pass


def publish(product: Product) -> None:
    if product.status != "draft":
        raise InvalidTransition(f"cannot publish from {product.status}")
    product.status = "active"


def discontinue(product: Product) -> None:
    if product.status != "active":
        raise InvalidTransition(f"cannot discontinue from {product.status}")
    product.status = "discontinued"
