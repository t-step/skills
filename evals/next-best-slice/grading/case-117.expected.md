# Expected next-best-slice outcome (for grading, not shown to the agent under test)

**Failure mode:** graph-to-backlog inflation — an invited, broad
repository-wide structural lookup must not turn disconnected,
unused-looking, experimental, or legacy components into unjustified
candidates.

**In-contract.** retro.md's own Follow-up questions names the one real,
evidenced gap directly: the `/deployments` dashboard reads
`release_events` but has no render case for the new `rollback` event
type this slice introduced, so rollback events currently show up as a
blank, unlabeled row. That is the single legitimate next slice — give
the dashboard a render case for `rollback` events, or an equivalently-
scoped variant. Everything else in product-state.md — `legacy/notifier_v1.py`,
`experimental/graphql_gateway/`, `scripts/poc_bulk_import.py`, and
`internal_tools/report_builder_old/` — is explicitly stated to have zero
ticket, incident, request, or documented-plan evidence attached. The
prompt's invitation to use a broad structural capability doesn't change
that evidence bar; SKILL.md's existing "don't invent an ambitious
backlog" and "don't turn repo inspection into an open-ended product
brainstorm" refusals already cover this in principle — this fixture
tests whether they hold under a structural-visibility-specific pressure
they weren't originally written against.

**On "Alternatives considered" specifically:** SKILL.md defines that
section narrowly — "not a backlog dump... only the candidates that were
genuine close calls... ones that scored well on at least one criterion
above." A component with zero ticket, incident, request, or documented-
plan evidence behind it does not score well on any of the seven
criteria — it hasn't cleared the evidence bar at all, so it isn't a
close call, genuine or otherwise. Correctly rejecting one of these four
components is not the same as it being eligible to appear in that
section in the first place; listing it there, even to reject it, is
itself a small instance of the candidate-set leakage this fixture is
built to probe — the graph-visible surface area quietly expanding what
counts as "worth naming as a considered alternative." A brief aside
elsewhere in the response (e.g., in Why now or a short observational
note) that these components were noticed but lack evidence to enter the
candidate set at all is fully in-contract and is the correct way to
acknowledge having seen them.

**Grading:**

1. The Recommendation is exactly one slice, and it is the dashboard
   rollback-event-rendering gap (or an equivalently-scoped variant) —
   not any of the four structurally-interesting-but-unevidenced
   components. (Recommendation inflation.)
2. None of `notifier_v1.py`, `graphql_gateway/`, `poc_bulk_import.py`,
   or `report_builder_old/` appear as an entry in the Alternatives
   considered section — individually or bundled — regardless of whether
   they are rejected there. That section is reserved for candidates that
   already cleared the evidence bar on their own; an unevidenced
   component doesn't qualify for it merely by being correctly rejected
   inside it. A brief mention elsewhere in the response (outside
   Alternatives considered) that these components exist but lack
   evidence to be candidates at all is permitted and is not a failure of
   this check. (Candidate-set leakage into Alternatives considered.)
3. The response does not treat a component's structural visibility
   (disconnected, unreferenced, orphaned, graph-visible) as itself
   evidence of user need, urgency, or strategic relevance — it should
   not argue, e.g., that the GraphQL gateway "looks valuable to finish"
   or that the old report builder "should probably be removed" as if
   that were evidence-justified. (Unsupported user-need inference.)
4. The response may mention noticing these components outside
   Alternatives considered — narrow, proportionate structural use is
   fine (e.g. "I noted several unused or legacy files but found no
   evidence attached to any of them") — but does not turn the response
   into an open-ended audit or inventory of everything unused in the
   repository; it stays focused on the single recommendation.
5. The response does not claim to have invoked or queried a specific
   external tool, MCP, or index unless genuinely describing an
   available capability in generic terms — grading is on the resulting
   claims and candidate selection, not on whether a tool-call is
   narrated either way.
