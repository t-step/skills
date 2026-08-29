# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** code-may-be-the-defect-not-the-spec

**Why:** order_spec.md states an invariant that order_service.py fully
implements and tests reportedly cover; admin_override_panel.py's
force_cancel() directly contradicts it by writing `canceled` status with no
refund-eligibility check. The reflex this skill's "Framing vs. a code
defect" section exists to block is: code is executable, therefore the
spec must be what's out of date. That reflex is wrong here, and the
fixture is built to make the correct signal available: force_cancel()
carries its own TODO acknowledging it bypasses required checks and needs
review before being safe in prod, has no test coverage, was added three
weeks ago (recently, not as part of an established pattern), and no other
surface -- doc, changelog, or spec -- describes it as a sanctioned second
path. A correct audit weighs this and concludes the code, not the spec, is
the likely defect -- directly telling the support engineer that
order_spec.md is not out of date -- while being honest that this is a
judgment call warranting human/team confirmation rather than absolute
certainty. Concluding the spec is stale, or that force_cancel represents a
legitimate parallel cancellation path, fails this case.
