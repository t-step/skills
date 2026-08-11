# case-103 (p3) — expected: surface document-attachment status, decline the cosmetic refresh

**In-contract expectation:** the response recommends backlog item 1 (show
each shipment's document-attachment status on the shipper's existing
booking-history page), and explicitly declines the prompt's visual-refresh
request as not connected to any observed gap.

**Grounded in SKILL.md:** "Discoverability and legibility of existing
capability" and "useful stored information that is not yet surfaced" --
booking already completes correctly with or without documents attached at
booking time (no failure, no blocked completion anywhere in this fixture),
and `shipment.docs_received` is already tracked correctly and used
internally by ops. The gap is purely that this already-correct, already-
stored fact isn't shown to the shipper it's about, evidenced by 9 "did my
documents go through" messages and ops's own note about shippers
re-sending already-received documents.

A response that recommends the dashboard refresh, or that frames item 1 as
fixing a broken upload/booking flow rather than surfacing already-correct
stored data, does not meet the bar.
