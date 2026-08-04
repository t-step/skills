# Repo snapshot: display/formatting.py (full file, AFTER the diff below is applied)

```python
SYMBOLS = {"USD": "$", "EUR": "€"}


def format_currency(amount: float, currency: str) -> str:
    symbol = SYMBOLS[currency]
    if amount < 0:
        return f"-{symbol}{abs(amount):.2f}"
    return f"{symbol}{amount:.2f}"


def format_date(dt) -> str:
    # TODO: this assumes the server's local timezone; doesn't account for
    # user timezone preference. Known issue, tracked separately, not part of
    # this change.
    return dt.strftime("%Y-%m-%d")
```
