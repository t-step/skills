# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** user-to-workload-authority-frozen-at-enqueue

**Why:** This is the user-to-workload transition named in `SKILL.md`: an
interactive action (`generate_report`) creates execution
(`report_worker.py`'s job) that outlives the request, the session, and
potentially the user's continued access. `permission_service
.get_accessible_project_ids(user_id)` is called exactly once, at enqueue
time in `report_request_handler.py`, while the user's session is active.
`report_worker.py` runs later, under the worker's own broad service
credential (`reporting_service_client`, not scoped to the user at all),
and treats `job.payload["project_ids"]` -- fixed at enqueue time -- as
still valid, with no second permission check anywhere in the execution
path.

The correct answer names this precisely as a transition question, not a
vague "async is scary" comment: **who owns re-authorization for data
included in a report finished after enqueue time -- the frozen snapshot
taken at enqueue, or a live check against the user's access at the moment
the workload actually reads the data?** As implemented, authority is
frozen at enqueue and never revisited -- if the customer's revocation
scenario in context.md occurs, the worker has no code path that would
notice.

This should be reported as a **Likely issue, MEDIUM-to-HIGH consequence**
(the exact severity depends on how sensitive project data is, which the
fixture doesn't fully establish -- HIGH is defensible given the customer's
own framing is about post-revocation data exposure, but MEDIUM is also an
acceptable call if the report reasons explicitly about the uncertainty).
It is "Likely" rather than flatly "Confirmed as currently exploited"
because the fixture doesn't show revocation actually occurring in this
data -- what's confirmed is the structural gap (no re-check exists in the
code); what's likely is that the gap has real consequence given the
scenario described. A report that flatly says "this is broken" with no
acknowledgment that it's answering "what does the code structurally
allow" rather than "here is a proven incident" is overclaiming; a report
that shrugs this off as "workers are always trusted, that's normal" fails
to engage with the actual question asked. Do not accept a report that
proposes a specific remediation design (e.g., "add a live permission
recheck before rendering") as the *point* of the finding -- naming the
gap and the transition question is this skill's job; a proposed fix
belongs in Design mode, not required here.

**Update after first with-skill run:** the graded run correctly identified
the transition, the enqueue-time freeze, and answered the customer's
scenario directly without proposing a fix -- the substance above was met
in full. It did, however, exhibit the exact calibration gap this key
warns against for its second finding ("No destination-side
re-authorization..."), rating it Confirmed/HIGH while its own "Unresolved
uncertainty" and "Unknowns" sections named that the data warehouse might
independently enforce a project-level ACL the code doesn't show -- an
observed instance of blending a directly-observed structural fact
(no re-check visible in this code) with an unresolved consequence
(whether that's the *only* enforcement layer) under one Confirmed label.
This is an in-contract failure against `SKILL.md`'s own evidence
discipline, not a substance error, and it motivated a small clarifying
addition to `SKILL.md`'s tier-selection guidance (a finding whose own
Unresolved-uncertainty line names something that could change its stated
consequence should not carry Confirmed-level certainty for that
consequence). Not re-run against the revised wording -- this remains the
first and only run of this case.
