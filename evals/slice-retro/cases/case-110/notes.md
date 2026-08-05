# Implementation notes

Kept this minimal -- builds the whole CSV in memory with `io.StringIO`
and returns it as one response. Some things I didn't get to, roughly in
the order they occurred to me while writing this:

- Haven't tested this against a large order volume (tens of thousands of
  rows) -- `get_completed_orders()` currently has no limit, so "all
  completed orders" could be a lot of rows building up in memory at once.
- customer_email (and in the future, maybe a customer name column) is
  written straight into the CSV with no escaping beyond what the `csv`
  module does automatically -- if a value ever starts with `=`, `+`, `-`,
  or `@`, some spreadsheet apps will interpret it as a formula when the
  file is opened. Haven't checked whether that's a real risk here.
- Unicode characters in email addresses aren't specifically tested.
- created_at is passed through as whatever string is already stored;
  didn't check whether that's UTC or local time, or whether it should be
  reformatted for the export.
- No handling for what happens if the DB connection drops partway
  through building the export.
- Didn't check what Excel does with the UTF-8 output by default (no BOM
  is written) -- I recall this sometimes garbles non-ASCII characters
  when opened directly.
- Concurrent writes to the orders table while an export is running
  aren't accounted for one way or the other.
- No rate limiting on this endpoint -- someone could hit it repeatedly.
- Only tested with 3 orders locally; didn't try an empty order list.
