# Goal

Bug: `format_currency` in `display/formatting.py` drops the currency symbol
for negative amounts (`format_currency(-5, "USD")` returns `"-5.00"` instead
of `"-$5.00"`). Fix just that.
