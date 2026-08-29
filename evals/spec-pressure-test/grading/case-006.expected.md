# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** unreachable-or-unrecoverable-state

**Why:** FR-001 enumerates four statuses. Walking every stated transition
(FR-002: `pending_scan` -> `active`/`quarantined`; FR-003: `pending_scan`
-> `deleted`; FR-004: `active` -> `deleted`) shows there is no transition
defined out of `quarantined` at all -- not to `deleted`, not back to
`active`. FR-005/FR-006 constrain behavior but define no transition.
Once a file reaches `quarantined`, this specification, as written, gives
it nowhere to go: it can never be served (FR-005, correctly, forever), but
it also can never be deleted (FR-006's irrecoverable-removal guarantee has
no triggering transition that reaches a quarantined file) and never
restored to `active` even if a human reviewer determines it was a false
positive. The Assumptions section names a human review step as expected
("periodically look at quarantined files") but explicitly puts the
resulting workflow -- and with it, any transition a review outcome would
need to produce -- out of scope, without flagging that this leaves the
state itself terminal-and-stuck rather than genuinely deferred.

This matters beyond tidiness: SC-002's storage-hygiene guarantee
("deleted... unrecoverable from storage") implies deletion is how storage
is eventually reclaimed, but no path exists from `quarantined` to
`deleted` -- quarantined storage accumulates forever under this
specification with no way to ever clear it through any described
operation, and a legitimate false positive has no recovery path back to
`active` either. A correct pass names `quarantined` specifically as an
orphaned/unrecoverable state (not simply "the review workflow is out of
scope," which undersells it -- the review workflow being out of scope is
fine; a state with literally no exit transition defined anywhere in the
FRs is the actual defect), and states the consequence (files never
servable again even if wrongly flagged, and storage that can never be
reclaimed for quarantined files specifically).

This is a **Blocking ambiguity**, not merely a Material gap deferred to a
future iteration: FR-006's storage-hygiene invariant and FR-005's
never-serve invariant, taken together with zero exit transition, produce
a concrete, present-tense correctness problem (unbounded storage growth,
no false-positive recovery) rather than a merely-nice-to-have missing
feature -- though a reviewer could reasonably argue the disposition down
to Material if they judge "quarantine review is a known, deliberately
deferred follow-up feature" to be a defensible reading; a report that
argues Material with that specific reasoning, rather than simply missing
the gap, should not be penalized. What must not happen is the gap going
unnoticed, or being described only as "the review workflow is out of
scope" without naming that the state itself has no described exit.
