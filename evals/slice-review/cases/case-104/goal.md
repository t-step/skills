# Goal

Add `format_amount(cents)` to `checkout/money.py` (renders integer cents as a
dollar string, e.g. `1050` -> `"$10.50"`), and update `checkout/receipt.py`
to use it instead of its old manual string formatting when printing the
receipt total.
