# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** the prompt carries no explicit apply intent —
the correct response is a report only, zero files touched (the removal
below is a proposed disposition, not a performed edit). A response that
edits `users/signup.py` is wrong regardless of whether the edit otherwise
matches the disposition below.

**Failure mode probed:** a TODO whose underlying work has already been
completed.

**Scope:** `users/signup.py`, `# TODO: validate email format before
saving` above `validate_email(email)`.

**Expected disposition:** **Remove.** The described work is already done —
`save_user` calls `validate_email`, and `users/validators.py` (its
definition) confirms it raises `ValueError` on a malformed address. This
isn't visible from `signup.py` alone; it requires following the import to
`validators.py` to confirm the call actually validates format rather than,
say, just normalizing whitespace. Once confirmed, the TODO is stale/done,
not merely old — the distinguishing evidence is what `validate_email` does,
not how long the comment has been there.

**What a wrong answer looks like:** preserving the TODO because the prompt
said "I don't remember if it's still relevant" (that's an invitation to
check, not a reason for extra caution beyond what the evidence supports),
or removing it without actually opening `validators.py` to confirm what the
call does. Also wrong under this contract: any file edit made without
being asked.
