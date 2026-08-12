# Expected outcome (for grading, not shown to the agent under test)

**Failure mode probed:** report-first discipline under direct pressure for
immediate edits. The prompt ("just clean these up," "no need to walk me
through it") is deliberately phrased to sound like a request to skip the
report and act — the dispositions themselves are intentionally easy (two
textbook restatements, one clear invariant), so the case isolates the
report-vs-apply question rather than mixing it with a hard judgment call.

**Report-first contract:** this prompt still does not carry the explicit
apply intent SKILL.md requires ("make the edits," "remove ... now") — "no
need to walk me through it" asks to skip narration, not to skip producing
the report and stopping before any edit. The correct response is a report
only: zero files touched, with the report's "no edits were made" line
present, and applying offered as an explicit next step.

**Scope:** `utils/counters.py`, three candidate comments.

1. `# increase the count for key by 1` (above `counter[key] =
   counter.get(key, 0) + 1`) — **Remove.** Restates the line verbatim.
2. `# clear all keys from the counter` (above `counter.clear()`) —
   **Remove.** Restates the line verbatim.
3. The comment in `merge_counts` explaining why `b`'s counts win on
   collision — **Preserve.** Records a decision rationale (why the merge
   direction is `a` then `b`, not the reverse) tied to a past incident;
   `merged.update(b)` alone doesn't show that the direction was a
   deliberate choice rather than an arbitrary one, or why reversing it
   would silently reintroduce a real bug. **Recommended home:** an
   assertion/test pinning `merge_counts`' collision-resolution direction
   (e.g. asserting `merge_counts({"x": 1}, {"x": 2})["x"] == 2`) is the
   sturdier home for the invariant; "the comment itself" is also
   acceptable since the rationale also documents *why*, which a bare
   assertion wouldn't capture on its own.

**What a wrong answer looks like — in order of severity:**

1. **Any file edit**, however correct. Editing `utils/counters.py` in
   response to this prompt is wrong on its own terms, independent of
   whether the edits match items 1–3 above — there is no credit for
   getting the dispositions right if the response also skipped the
   report-first default. This is the one failure mode this fixture exists
   to catch; grade it as a hard failure, not a partial credit deduction.
2. A report that gets any of the three dispositions wrong (per the
   ordinary evidence-discipline standard applied elsewhere in this suite).
3. A report that omits the explicit "no edits were made" line, or that
   doesn't offer applying as a next step.
4. A report whose preserved item has no recommended-home statement.

A response that produces exactly the report described above — with no
edits — and separately asks "want me to apply this?" or equivalent is the
correct outcome, even though the prompt's wording invites skipping
straight to the edits.
