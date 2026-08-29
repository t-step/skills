# case-104 (p4) — expected: distinct past_due label, decline the wrapper-unification refactor

**In-contract expectation:** the response recommends backlog item 1 (show
`past_due` status distinctly, with an update-payment link), and explicitly
declines item 2 (unifying the three payment-provider wrappers) for lacking
a concrete, near-term product-value connection, despite the prompt framing
it as "good engineering hygiene."

**Grounded in SKILL.md:** "Product value isn't a layer" and "Pure
technical or architectural cleanup is not eligible here unless there's a
concrete, near-term, evidence-traceable connection... not 'this will
probably help eventually.'" Item 2's own backlog description states
plainly that "no customer-facing behavior is affected either way" and "no
ticket, incident, or product note connects this to anything a customer has
experienced" -- the response should cite exactly this. Item 1's underlying
data (`subscription.status`) is already correct; the gap is purely a
state-transition legibility issue (past_due renders identically to
active), grounded in 8 tickets from customers surprised by a cutoff with
no warning.
