# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** "can you sort it out?" is a vague request, not
the explicit apply intent SKILL.md requires — the correct response is a
report only, zero files touched (the removal below is a proposed
disposition, not a performed edit). A response that edits
`pricing/calc.py` is wrong regardless of whether the edit otherwise
matches the disposition below.

**Failure mode probed:** a misleading comment where deletion is safer than
attempting to guess the intended replacement.

**Scope:** `pricing/calc.py`, the `TODO: ... old_price ...` comment above
`compute_final_price`.

**Expected disposition:** **Remove — do not rewrite or "fix" it into a
guessed replacement.** The comment references `old_price`, a variable that
does not exist anywhere in this function (the parameters and locals are
`base_price`, `tax_rate`, `discount_pct`, `price_after_discount`, `final`),
strongly suggesting the comment predates a rewrite and was never updated.
It also references an unreachable ticket (`JIRA-1123`, not accessible) and
an undefined "edge case Z." `tests/test_calc.py` exercises a spread of
discount percentages without failure, giving no evidence of a live,
locatable bug this TODO could be describing. Because there's no way to
determine what the comment was ever actually trying to say — correcting it
would mean inventing a plausible-sounding but unverifiable bug description
— deletion is the correct action per the skill's own rule: a wrong comment
invented from a guess is worse than none.

**What a wrong answer looks like:** rewriting the comment into a new,
invented TODO (e.g. guessing what "edge case Z" might mean, or fabricating
a description of a tiered-discount bug that isn't demonstrated anywhere in
the fixture) instead of removing it. Also wrong: leaving it completely
untouched — this is a case where inspection produces enough evidence
(mismatched variable name, unreachable reference, passing tests across
several discount tiers) to act with confidence, not a "needs judgment" one.
Also wrong under this contract: any file edit made without being asked —
including deleting the comment outright in direct response to "can you
sort it out," which is not explicit apply intent.
