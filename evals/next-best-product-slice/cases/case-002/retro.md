# Slice Retrospective: Add generate_invoice() PDF renderer to the billing-admin console

## What we proved
`generate_invoice(invoice_id)` produces a correctly-formatted PDF from an
invoice record, verified by hand against 12 real invoices spanning every
line-item shape currently in use.

## Assumptions validated
None specifically tested beyond rendering correctness.

## Assumptions falsified
None.

## Remaining uncertainty
None material to this slice.

## Intentional non-goals
This slice only added the renderer used internally by the admin console
when support staff need to pull a copy of an invoice. It did not add any
way for a billing admin (a customer-side role) to generate or retrieve an
invoice themselves — that was explicitly out of scope.

## Architectural consequences
Invoice PDFs can now be generated on demand from any invoice record,
without the manual export script staff used before. Any future feature
that needs an invoice PDF can call `generate_invoice()` directly.

## Follow-up questions
None.
