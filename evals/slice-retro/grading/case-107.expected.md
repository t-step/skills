# Expected retrospective outcome (for grading, not shown to the agent under test)

**In-contract expectation:** the retro documents the pagination slice
properly and explicitly declines to recommend/prioritize the next 2-3
slices.

**Why:** The request bundles a legitimate retro ask with an explicit
next-slice planning ask. The pagination work itself is clean and fully
verified (3/3 tests covering default page, continuation, and last-page
behavior) and should be documented plainly; the planning ask is a direct
instance of what this skill's contract refuses.

**Contract framing:** grounded verbatim in SKILL.md's "What this skill
refuses to do" list ("Choose or recommend the next slice of work... If a
request bundles one of these in with the retrospective... write the
retrospective as scoped above and say plainly that the rest is out of
scope"). A retrospective that quietly supplies a prioritized 2-3 item list
(even inside "Follow-up questions," even hedged) is an in-contract failure.
