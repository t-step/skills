# Goal

`handle_signup()` in `signup_flow.py` currently stores whatever phone
number string a user typed, unvalidated and unformatted. Add validation
and normalization so `handle_signup()` stores phone numbers in a
consistent format (`+1XXXXXXXXXX`), and simply omits the `phone` field
when the input can't be parsed as a valid 10- or 11-digit US number.
