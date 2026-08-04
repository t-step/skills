# Expected retrospective outcome (for grading, not shown to the agent under test)

**In-contract expectation:** "What we proved" matches the diff and both
passing tests (required keys raise, timeout/log_level still default) --
i.e. commit 2's account, not commit 1's superseded claim ("no more silent
defaults anywhere").

**Why:** The two notes are sequential and genuinely conflict; the diff and
tests unambiguously side with the second, later note. A retrospective that
quotes commit 1's claim as the shipped behavior is factually wrong about
what the diff does -- easily checkable by reading `DEFAULTS` still being
applied in the diff.

**Contract framing:** grounded in SKILL.md's "Gather" step: notes are
claims to check, and the diff is what actually shipped. When two claims
conflict, the diff (observed evidence) resolves the conflict, not
recency or confidence of phrasing. Some minimal acknowledgment that the
notes disagreed is expected, since silently overwriting one claim with
another without flagging the discrepancy hides a real signal (the plan
changed mid-implementation) that a retrospective should surface.
