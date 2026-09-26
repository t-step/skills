# expense-ocr-poc

Extracts line items from receipt photos using a third-party OCR API,
for expense report pre-fill.

## Deployment

Runs as a single container inside the corporate VPN, behind the
company's existing internal ingress, which requires SSO login for every
request before it reaches this service -- the same ingress every other
internal tool uses. This service has never been, and is not currently
planned to be, exposed outside the VPN.

## Data

Uploaded receipt images are processed synchronously and then deleted
immediately after the OCR result is parsed and written to a local SQLite
file (`results.db`). We don't keep the original images around once
we've extracted the line items -- didn't want to accumulate a pile of
receipt photos with financial and possibly personal detail on them
longer than necessary.

## Scale

Expected usage: the pilot group is ~40 employees submitting a handful of
receipts a week each. No autoscaling or queueing infrastructure is
currently in place; the service runs as one instance.
