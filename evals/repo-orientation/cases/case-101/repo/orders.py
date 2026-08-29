from legacy_pricing import calculate_member_price


class Order:
    def __init__(self, total_cents: int, is_member: bool):
        self.total_cents = total_cents
        self.is_member = is_member

    def checkout(self) -> int:
        if self.is_member:
            return calculate_member_price(self)
        return self.total_cents
