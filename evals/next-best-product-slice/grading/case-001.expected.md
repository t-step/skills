# case-001 — expected: recipient-visible validation errors

**In-contract expectation:** the response recommends backlog item 2
(recipient-visible validation errors), not item 1 (date-range field type),
despite item 1 having the stronger dependency-unlocking/architectural-
momentum evidence.

**Grounded in SKILL.md:** the "Workflow completion or trust" criterion
("usually the strongest signal: closing a dead end or restoring trust in a
broken loop outweighs making an already-working path faster") and the
"Convenience or friction-reduction" paragraph ("making a working path
faster does not by default outrank closing a path that's broken,
confusing, or untrustworthy, even when the friction-reduction candidate is
... more architecturally convenient to build"). Item 1 is real,
evidenced, cheap, and directly named in the retro's follow-up question --
exactly the kind of candidate a generic dependency-unlocking-weighted
selector would favor. Item 2 is the correct pick specifically because
recipients cannot currently tell why their submission was rejected and
therefore cannot reliably complete the request at all -- a workflow-
completion gap, which this skill's criteria explicitly rank above
friction-reduction on an already-functioning path.

A response that picks item 1, or that picks item 2 without engaging with
item 1's real evidence at all, does not meet the bar.
