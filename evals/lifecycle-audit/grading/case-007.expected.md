# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** underspecified-approval-ownership

**Why:** The doc itself names its own biggest gap in the hallway-
conversation note: whether approval state lives in expense-reports or
in the existing generic Approvals service is explicitly undecided, with
both live in a meeting and no one having checked what the existing
service's data model even supports. The doc's own "open questions"
section additionally leaves resubmission, SLA/escalation, decision
reversal, and edit-while-pending all unanswered. This is a case built to
punish invention: a plausible-sounding answer is easy to write for any
of these (e.g. "approval state lives in expense-reports, in a new
approvals table" or "rejected requests can be resubmitted") but nothing
in the doc supports picking one option over the other. A correct audit
resists that pull -- it marks owner/persistence as Unknown, carries the
doc's own open questions into its own report as unresolved, and still
manages to say what IS established (submit -> approval stages -> approved/
rejected -> reimbursement handoff) rather than treating the whole audit
as impossible just because ownership is unsettled.
