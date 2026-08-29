# Backlog — Cargofy shipping

1. **Show document-attachment status on the shipper's booking history.** A
   shipper can already complete and book a shipment whether or not they
   attach customs paperwork at booking time — attaching documents later by
   emailing support is a normal, fully-supported path, and every booking
   completes correctly either way. Internally, ops already tracks, per
   shipment and correctly, whether the required documents have been
   received (`shipment.docs_received`) — it's how ops decides which
   shipments still need paperwork follow-up. Nothing on the shipper's own
   booking-history page shows this, though: a shipper who wants to check
   whether their last shipment's documents went through has no way to
   tell from the product itself. Support has fielded 9 "did my documents
   go through" messages in the last month from shippers checking, and ops
   has separately noted shippers occasionally re-sending documents that
   were already received, creating duplicate paperwork to reconcile. A
   minimal first step: show each shipment's document status on the
   existing booking-history page, reading directly from
   `shipment.docs_received`.

2. **Bulk shipment import from CSV.** No usage signal on record.

3. **Saved shipper preferences (default pickup address, etc.).** No usage
   signal on record.
