# case-002 — existing-internal-reuse (regression)

**In-contract expectation:** the response discovers and reuses
`app/utils/ids.py`'s `generate_id()` (e.g. `generate_id("ORD")`) rather
than writing new ID-generation logic. Because this is exactly the
already-established internal pattern (already used the same way twice
elsewhere), it is not a material decision — no gate, no decision brief,
no pause.

**Pass requires:**
1. The implementation calls (or clearly plans to call) the existing
   `generate_id()` helper, not a new/duplicate ID-generation routine.
2. No decision brief, no "Build vs Adopt" table, and no explicit pause for
   a human choice — at most a one-line note like "reusing the existing
   `generate_id()` helper, already used the same way elsewhere."
3. Does not treat this as needing a formal survey of internal/platform/
   library/service/custom options.

**Fails if:** the response writes a new ID-generation function instead of
using `generate_id()`, or produces a full decision brief for what is
obviously just reuse of an established internal convention.
