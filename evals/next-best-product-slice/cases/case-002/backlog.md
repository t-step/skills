# Backlog — Ledgerline invoicing

1. **Let billing admins download their own generated invoices.** Today,
   only internal support staff can generate or retrieve an invoice PDF,
   using `generate_invoice()` through the internal admin console. A
   billing admin (a customer-side role `docs/roles.md` describes as
   responsible for "retrieving and archiving any invoice their account has
   generated") has no way to get a copy of their own invoice without
   filing a support ticket. Support has logged 12 such tickets in the last
   month. A minimal first step: a "download PDF" button on the invoice's
   existing detail page in the customer-facing billing area, calling the
   already-verified `generate_invoice()`.

2. **Multi-language invoice templates.** No ticket or usage signal on
   record.

3. **Custom invoice numbering schemes.** No ticket or usage signal on
   record.
