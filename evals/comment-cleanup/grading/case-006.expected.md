# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** this key grades the response's classification
*report*, not applied edits. The prompt carries no explicit apply intent,
so the correct response is a report only — zero files touched. A response
that edits `pricing/discount.py` is wrong regardless of whether the edits
otherwise match items 1–2.

**Scope:** `pricing/discount.py`, two candidate comments; `pricing/currency.py`
is supporting context (no candidate comments of its own — checking it is
what establishes that the minor-units convention isn't documented anywhere
else in the repo).

1. The minor-units comment above `apply_discount` — **Preserve.** At a
   glance it can look like it's just restating that `cents` holds a
   cent amount, but its actual content is a package-wide convention
   ("the API layer converts once at the boundary and never again") that
   isn't stated anywhere else in this repo — `pricing/currency.py` has no
   docstring, comment, or naming convention that establishes it, and
   nothing else does either. Removing it would delete the only place this
   invariant is written down, even though the specific line it sits next
   to doesn't obviously need it. **Recommended home:** `pricing/currency.py`'s
   module docstring (currently absent) would be a more discoverable home
   for a package-wide convention shared by every function in the package;
   until that documentation exists, the comment remains the only copy and
   should stay regardless.
2. `# convert cents to dollars` above `to_display_string` — **Remove.**
   Unlike (1), everything this comment says is fully reconstructable from
   the code beneath it (`cents / 100`) and the `$` / `.2f` formatting —
   there is no separate fact being carried.

**What this fixture is probing:** two comments that read similarly on the
surface (both are short, both mention "cents") but differ in whether their
specific informational content survives without them — checkable only by
looking at whether that information is written down anywhere else in the
repository, not by comparing the comments' wording to each other. Under
the report-first contract it also checks that the preserved item gets a
placement recommendation.

**What a wrong answer looks like:** the substantive misjudgments above,
plus — new under this contract — any file edit made without being asked,
or the preserved item reported with no recommended-home statement at all.
