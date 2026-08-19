class Balance:
    def __init__(self, amount):
        self.amount = amount

    def apply_delta(self, delta):
        self.amount += delta
