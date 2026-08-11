# Backlog — DocuVault document requests

1. **Add a "date range" field type.** Several customers have asked (10+
   support tickets over the last month) for a field where a recipient
   picks a start and end date instead of two separate date fields. Now a
   direct registration against `FieldValidator` — no changes to the shared
   submission handler.

2. **Recipient-visible validation errors.** Today, when a recipient submits
   a document request and any field fails validation, `FieldValidator`
   correctly rejects it and the page reloads with the recipient's
   previously-entered values preserved — but shows no message identifying
   which field was wrong or why. `docs/design-principles.md` describes
   helping recipients understand what's required of them as part of the
   product's intended experience. Support has logged 6 tickets in the last
   month from recipients who re-submitted the same rejected request
   three or four times, unable to tell what needed to change, before
   guessing the right fix or emailing the sender to ask what was wrong.
   A minimal first step: show which field(s) failed and the
   specific reason, using the validation-result data `FieldValidator`
   already produces internally but currently discards after a failed
   submission.

3. **Bulk document-request creation.** Let a sender create the same request
   for 50 recipients at once instead of one at a time. No ticket or usage
   signal on record.

4. **Custom branding on the request page.** No ticket or usage signal on
   record.
