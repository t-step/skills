# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** ownership-authority-of-derived-status-once-set

**Why:** FR-003 makes `review` eligibility an OR of two independently
owned facts: FR-001's computed readiness (a live, continuously-derived
projection of children's statuses -- "MUST compute... exactly when...")
and FR-002's manual-ready flag (an independently settable field). FR-003
itself is unambiguous as an *entry* gate. The gap is what a bundle's own
`review` status *is*, once set, relative to those two facts: is it a
fresh, independently authoritative fact from the moment of transition
onward (entry gate only, never re-checked), or does the spec intend it to
keep agreeing with "FR-001 OR FR-002 is currently true" for as long as it
remains `review`? FR-004 is the tell: it explicitly states that clearing
the manual-ready flag "MUST NOT affect any child task's own status" --
carefully scoping what clearing does *not* touch -- but says nothing about
whether clearing it affects the *bundle's own* `review` status when the
bundle only qualified via the manual path and computed readiness is still
false. The document never states whether `review` status is itself
authoritative once reached, or remains a live derivation that could
become "wrong" relative to its own qualifying conditions.

Concrete scenario: a bundle has one open child. A lead sets the
manual-ready flag; the bundle moves into `review` (FR-003, satisfied only
via the manual path, per FR-005's own path-recording language). The lead
then clears the manual-ready flag (FR-004) before the open child finishes.
At this instant, neither FR-001 (still one child open) nor FR-002 (flag
now cleared) holds -- yet FR-003 only speaks to *moving into* review, never
to what happens when a `review`-status bundle's qualifying condition
disappears. One implementer reasonably treats `review` status as sticky
and independently authoritative once set (the bundle stays in `review`);
another reasonably treats FR-003's OR condition as an ongoing invariant
the bundle's status must continue to satisfy, and reverts it (perhaps back
to `open`, though no such reverse transition is defined anywhere either).
These are observably different, both textually defensible, and the
second reading has nowhere to go (no reverse transition is specified),
which itself compounds the gap.

This is defensibly a **Blocking ambiguity**: which behavior is correct
materially changes what a reviewer sees (a bundle legitimately still under
review that the other reading would silently kick back out, with no
defined target state for the kickback), and the spec's own SC-002/SC-003
language doesn't resolve it either way. It is also a defensible **Material
gap** if reasoned explicitly (no stated invariant or data-corruption risk
is at stake here, unlike the FR-005 finding below, and "review status is
sticky once set" is a reasonable default the document's own one-way-gate
language supports) -- either disposition is acceptable for this case as
long as the finding itself is present and concrete. The smallest closing
question either way: is a
bundle's `review` status, once reached, authoritative and independent of
FR-001/FR-002 afterward (an entry gate only), or must it continue to
satisfy FR-003's condition for as long as it remains `review` -- and if
the latter, what happens to a bundle whose qualifying condition lapses?

A secondary, smaller and optional point a thorough pass may also raise:
FR-005's "via the manual-ready flag rather than ordinary computed
readiness" phrasing assumes the two paths are mutually exclusive at the
moment of transition, but nothing prevents both being true simultaneously
(the Edge Cases section even names this as an explicitly harmless case),
leaving which "path" gets recorded underdetermined. This is a legitimate,
lower-stakes **Material gap** (an audit-trail nicety, not a correctness or
invariant risk) if raised, but is not required for the case to pass --
the required finding is the entry-gate-vs-ongoing-invariant ambiguity
around `review` status itself.
