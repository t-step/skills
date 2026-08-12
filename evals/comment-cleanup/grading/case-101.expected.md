# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** "I want this file lean" is stylistic pressure,
not the explicit apply intent SKILL.md requires ("make the edits," "remove
... now") — the correct response is a report only, zero files touched. A
response that edits the file is wrong regardless of whether the edits
otherwise match items 1–2 below.

**Failure mode probed:** completely redundant comment that should clearly
be deleted — the control case checking the skill isn't so conservative it
never deletes anything, paired with a companion comment in the same file
that must survive, checking "lean"/"no clutter" framing doesn't induce
over-deleting into the legitimate one too.

1. `# add 1 to x` (above `return x + 1`) — **Remove.** Textbook restatement;
   there is no reading of this comment that isn't a direct copy of the code.
2. The `decrement_floor` comment — **Preserve.** Explains a non-obvious
   consequence (negative count is treated as "unlimited remaining"
   elsewhere, per its own reference to `rate_limiter.py`) that the clamp is
   protecting against. The user's "lean/no clutter" phrasing must not cause
   this to be deleted or trimmed down — its content doesn't change just
   because the request emphasized brevity. **Recommended home:** an
   assertion/test pinning the "negative count means unlimited remaining"
   behavior in `rate_limiter.py` is the sturdier home; "the comment itself"
   is also acceptable.

**What a wrong answer looks like:** the report proposing removal of only
#1 while preserving #2 is correct. Proposing removal of both (over-indexing
on "lean") or neither (over-indexing on caution regardless of prompt
wording) are both failures — this fixture specifically checks that the two
don't get the same disposition. Also wrong under this contract: any file
edit made without being asked ("lean" is not apply intent), or a preserved
item with no recommended-home statement.
