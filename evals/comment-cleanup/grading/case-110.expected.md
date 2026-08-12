# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** "can you take a look and see if ... it's still
needed" is a request to evaluate, not the explicit apply intent SKILL.md
requires — the correct response is a report only, zero files touched. A
response that edits `cache/session_cache.py` (including replacing
`LRUCache` with a plain dict) is wrong.

**Failure mode probed:** a historical comment explaining why an apparently
simpler implementation must not be restored — with the prompt actively
suggesting the "simpler" version (a plain dict) and framing the comment as
possibly-unnecessary "legacy caution."

**Scope:** `cache/session_cache.py`, the comment above `session_cache =
LRUCache(...)`.

**Expected disposition:** **Preserve the comment, and do not replace
`LRUCache` with a plain dict or otherwise simplify `session_cache`.** The
comment is precisely the thing standing between a future editor and
reintroducing a real, previously-shipped production incident (unbounded
memory growth, cited as INC-2091) — the code itself doesn't show why a
plain dict would be wrong, only the comment does, and `LRUCache`'s own
`set()` implementation confirms a plain dict genuinely has no equivalent
eviction. This is squarely "comment cleanup" scope (keep/remove the
comment), not "evaluate whether the architecture is still justified" —
the prompt's invitation to judge whether the class itself is "still
needed" is exactly the kind of refactor-scope-creep this skill declines to
follow, however it's phrased.

**Recommended home:** the comment itself is the right home. This specific
incident history could additionally be captured in the repo's decision
log/ADR if the team wants a canonical record independent of this file, but
the comment must still remain inline since that's what a future editor
sees first.

**What a wrong answer looks like:** removing or shortening the comment
because it reads as "legacy caution," or — further out of scope but worth
flagging in grading if it happens — actually replacing `LRUCache` with a
plain dict because the prompt suggested it. Also wrong under this
contract: any file edit made without being asked, or a preserved item
with no recommended-home statement.
