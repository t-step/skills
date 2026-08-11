# case-002 — expected: billing-admin invoice download

**In-contract expectation:** the response recommends backlog item 1
(billing admins can download their own invoices), and explicitly declines
items 2 and 3 for lacking any ticket, request, or usage evidence.

**Grounded in SKILL.md:** "Discoverability and legibility of existing
capability" -- `generate_invoice()` is real, verified, and already used
internally; nothing exposes it to the role (billing admin) the
repository's own `docs/roles.md` names as responsible for retrieving
invoices. This is a baseline-sanity case: there is no serious competing
candidate, so the response should reach this pick cleanly and explain why
items 2/3 don't clear the evidence bar ("What counts as a product slice,
and what doesn't" -- a speculative idea is not enough evidence on its
own).
