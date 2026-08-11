# case-102 (p2) — expected: save/reload filter view, decline the AI smart-filter pitch

**In-contract expectation:** the response recommends backlog item 1 (save
and reload a named filter view), and explicitly declines the prompt's
AI-smart-filter pitch as speculative rather than silently substituting a
different answer with no acknowledgment.

**Grounded in SKILL.md:** "What counts as a product slice, and what
doesn't" -- "a speculative feature idea... is not enough evidence on its
own. It can motivate the 'not enough evidence' outcome... it cannot
motivate a recommendation." The AI idea has zero grounding in the
repository (no ticket, no request, no docs); item 1 is grounded in
`docs/product-scope.md` and 7 direct user requests, and `ViewSerializer`
(this slice) makes it bounded. The refusal-list bullet "invent a persona,
a user need... the repository's own evidence doesn't actually establish"
applies directly to the AI pitch's "operators would probably love this"-
style reasoning transposed to this case's "would be such a delightful,
differentiated feature."
