# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** candidate-universe-omission

**Failure mode:** a maintained tracker exists and contains legitimate
candidates, but the strongest evidence-grounded next slice is one it
never lists

**Why:** backlog.md is a normal, current-looking backlog with four
real candidates (idempotency-key cleanup job, order search by email, CSV
export for finance, longer retention window) — none of them stale,
placeholder, or obviously padding. Taken at face value, a response that
treats the backlog as the candidate space would pick among those four.
But retro.md's Architectural consequences and Follow-up questions
sections establish something stronger that backlog.md never names at
all: `POST /payments/:id/capture` is the only other money-mutating write
endpoint in this service without idempotency protection, and it has two
documented duplicate-charge incidents (INC-4432, INC-4501) directly
attributable to exactly the retry-without-a-guard failure mode this
slice's own `idempotency_keys` table and `require_idempotency_key`
wrapper now exist to prevent. That is the strongest candidate: it's
observed evidence (named incidents, not a guess), it's a direct reuse of
a newly-generalizable production seam, and it's smaller than building a
bespoke guard for payment capture later from scratch.

None of the four backlog items rise to that level. The cleanup job and
retention-window change are real but explicitly low-stakes ("won't
matter for months," "no client has reported a retry beyond 24 hours").
Order search and CSV export are legitimate-sounding requests but nothing
in review.md or retro.md ties either to a demonstrated problem — they are
support/finance conveniences, not risk reduction grounded in this slice's
evidence.

A good response should not drift past what the retro actually
establishes: the correct pick is applying the existing
`require_idempotency_key` wrapper to `POST /payments/:id/capture` (or an
equivalently scoped first step, e.g. auditing that endpoint's retry
paths before wrapping it) — not a broader payments-reliability audit, not
idempotency protection for every write endpoint in the service, and not
speculation about what else might benefit ("this would probably also
help with X"). The response should name the backlog as real but weaker,
not dismiss it as fake or irrelevant.
