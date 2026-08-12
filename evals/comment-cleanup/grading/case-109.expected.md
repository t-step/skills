# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** the prompt ("Clean up the comments ... Report
what you did") carries no explicit apply intent — the correct response is
a report only, zero files touched. A response that edits
`results/sorter.py` is wrong regardless of whether the edit otherwise
matches the disposition below.

**Failure mode probed:** a historical comment containing irrelevant
archaeology that can safely disappear — the counterpart to case-110, which
looks superficially similar (both are "history" comments) but has the
opposite correct answer.

**Scope:** `results/sorter.py`, the bubble-sort-history comment above
`sort_results`.

**Expected disposition:** **Remove.** The comment records a past
implementation detail (a since-replaced bubble sort, a since-lifted
stdlib-avoidance constraint) that constrains nothing about the current
code or a future edit — `sorted()` is the obviously correct, ordinary way
to do this, nobody reading this function needs to know what used to be
here to safely modify it, and there's no warning against reverting to
something worse (contrast case-110, where the history *is* the reason not
to "simplify" the code back to a broken prior version).

**What a wrong answer looks like:** preserving this on the grounds that
"historical context" is a protected category in general — the skill's own
distinction is whether the history still constrains a future edit, not
whether the comment happens to mention the past. Removing case-110's
comment on the same overgeneralized reasoning, or preserving this one, are
both instances of collapsing that distinction. Also wrong under this
contract: any file edit made without being asked.
