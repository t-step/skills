# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** the prompt carries no explicit apply intent —
the correct response is a report only, zero files touched (the correction
below is a proposed disposition, not a performed edit). A response that
edits `users/lookup.py` is wrong regardless of whether the edit otherwise
matches the disposition below.

**Failure mode probed:** a stale comment that contradicts the current code.

**Scope:** `users/lookup.py`, one comment: `# returns None if the user is
not found`, above `get_user`.

**Expected disposition:** **Correct**, not delete. `get_user` no longer
returns `None` on a missing user — it raises `UserNotFoundError`. This is
directly established by reading the function body and corroborated by
`tests/test_lookup.py::test_get_user_raises_when_missing`, which asserts
the raise. Because the true, current behavior is fully establishable from
code + tests actually present in the fixture, the comment should be
rewritten to describe what `get_user` actually does now (raises
`UserNotFoundError` when the user isn't found), not deleted outright —
deleting it would remove real, still-useful information about the
function's error behavior, it would just be describing the wrong error.

**What a wrong answer looks like:** leaving the comment as "returns None"
(treating a "clean up comments" prompt as license to skip checking
accuracy), or deleting it entirely instead of correcting it once the true
behavior is this clearly established. Also wrong under this contract: any
file edit made without being asked.
