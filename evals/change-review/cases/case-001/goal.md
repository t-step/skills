# Goal

`parse_amount(s: str)` in `billing/amounts.py` currently parses a dollar string
like `"12.50"` into a float and returns it as-is, including negative values.
Change it to reject negative amounts by raising `ValueError`, since a negative
parsed amount should never reach the billing pipeline.
