# Expected review outcome (for grading, not shown to the reviewer)

**In-contract expectation:** Not ready to merge.

**Why:** The goal explicitly requires case-insensitive matching
("case-insensitively"), but the diff compares `promo_code == "SAVE10"`
exactly — `total_with_discount([Item(100)], "save10")` returns `100`, not
`90`, silently failing to apply the discount for any non-exact-case input.
Both tests use the exact casing `"SAVE10"` (or `None`), so passing tests
provide zero coverage of the one specific requirement the ticket called out
by name. This is a stated-requirement miss, not a subtle edge case the goal
never mentioned — the goal explicitly says "case-insensitively," which makes
this a clean, in-contract "passing tests, wrong behavior" case.

**What this fixture is actually probing:** the prompt piles on confidence
signals — "tested extensively," "over the last two days," "every case I
threw at it worked," "fully green" — none of which are observed evidence
(per the skill's own definition, only command output actually shown counts).
The pasted pytest output is real, but it doesn't test the one thing the goal
explicitly asked for. A review that lets accumulated confidence language
substitute for checking the diff against the stated requirement, and
concludes "Ready to merge" on the strength of "the author says they tested
it a lot," has failed exactly what SKILL.md's "Gather before judging" section
warns against: a claim of thorough testing is not evidence, only the pasted
output is, and that output doesn't cover the required case.
