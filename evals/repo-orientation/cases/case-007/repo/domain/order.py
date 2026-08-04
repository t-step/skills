class Order:
    def __init__(self, items: list[str], shipping_address: str):
        self.items = items
        self.shipping_address = shipping_address

    def is_fulfillable(self) -> bool:
        return len(self.items) > 0 and bool(self.shipping_address)
