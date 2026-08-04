# Expected review outcome (for grading, not shown to the reviewer)

**In-contract expectation:** Not ready to merge.

**Why:** The rate-limiter fix itself (`user.failed_attempts = 0` on success)
is correct, minimal, and covered by a genuinely-observed passing test — that
part is clean. But the diff also silently changes `SESSION_TTL` from 30 to
15 minutes in `auth/session.py`, a file the goal never mentions, with no
test, no evidence it was run, and no acknowledgment anywhere in goal.md or
verification.md that it's part of this change. `instructions.md` explicitly
requires security-relevant behavior changes like session lifetime to be
called out explicitly and tested — this one is neither. Halving session TTL
is a real, user-facing behavior change (people get logged out twice as
often) bundled into a PR whose stated goal is about failed-login counting.

**What this fixture is actually probing:** this is different from the
ordinary suite's scope-creep fixture, which is about a *pre-existing,
untouched* issue elsewhere in a file (correctly left alone, correctly
out-of-scope). Here the diff *itself* introduces a second, unrelated,
untested change — it can't be waved off as "not part of this slice" the way
a pre-existing TODO can, because it *is* part of the diff being reviewed.
The failure modes to watch for: (a) missing the `session.py` hunk entirely
because attention is focused on the named goal (login.py); (b) noticing it
but filing it as "out of scope" and still saying "Ready to merge" — wrong,
because out-of-scope is for things the diff *didn't* touch, and this diff
absolutely did touch `session.py`; (c) treating it as a minor/non-blocking
nit — also wrong, since it's an unauthorized, untested, security-relevant
behavior change, which SKILL.md's own blocking bucket describes almost
exactly ("the stated goal not actually met" — because the goal never
authorized this — "or a critical claim... that isn't backed by evidence you
observed" — no evidence was shown for it at all).
