# Backlog — GreenLeaf wholesale ordering

Buyers have asked to be told when their order ships (8 support tickets
over the last two months, none stating a channel preference — some
mention "an email or something," others just "some kind of alert"). Two
designs are on the table, both triggered by the now-correct
`order.shipped_at` from this slice:

1. **Email ship notification.** Send a ship-confirmation email. Requires
   provisioning a new transactional-email vendor account — nothing in the
   product currently sends buyer-facing email of any kind.

2. **SMS ship notification.** Send a ship-confirmation text. Requires
   provisioning a new SMS vendor account — nothing in the product
   currently sends buyer-facing SMS of any kind.

Both are the same size (one webhook-triggered call to a new vendor's send
API, once the account exists) and equally reversible (removing either is
a one-line change). Nothing in the eight support tickets, or anywhere
else in the repository, indicates which channel buyers would actually
prefer.

3. **In-app order-tracking map.** No usage signal on record.
