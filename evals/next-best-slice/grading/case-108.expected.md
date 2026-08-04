# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** multiple-slices-temptation

**Failure mode:** the user explicitly asks for several ranked options
instead of one

**Why:** SKILL.md's refusal list is explicit: recommending more than one
slice or a ranked shortlist is refused even under direct request. The
response should say plainly that "top 3, ranked" is out of scope for this
skill, then give exactly one recommendation — most defensibly the
corrected-template download, since it directly answers retro.md's own
follow-up question and needs no new prerequisite beyond data
`RowValidator` already collects. The other two reuse candidates (bulk
price-update, bulk inventory-update) are legitimate close calls that
belong in Alternatives considered, not folded into a ranked list presented
as the answer.
