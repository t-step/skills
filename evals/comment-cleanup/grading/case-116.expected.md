# Expected outcome (for grading, not shown to the agent under test)

**Failure mode probed:** the "better home" recommendation requirement.
This fixture's disposition itself is a fairly ordinary
invariant-corroborated-by-a-second-file case (similar in shape to
case-003/case-102 elsewhere in this suite); what's new here is grading
whether the report gives a *concrete, specific* recommended home for the
preserved invariant, not just a correct preserve/remove call.

**Report-first contract:** the prompt carries no explicit apply intent —
the correct response is a report only, zero files touched. A response
that edits `registry/plugins.py` is wrong regardless of whether the edit
otherwise matches the disposition below.

**Scope:** `registry/plugins.py`, the comment above `register()`.

**Expected disposition:** **Preserve, not trimmed.** The comment reads on
its face like it could be explaining ordinary call order ("call this
before that"), which is exactly what the prompt's framing invites treating
it as. Its actual content is an ordering *invariant with a silent-failure
mode*: `initialize()` snapshots `_plugins` into an immutable tuple and
never re-reads the dict, so a late `register()` call doesn't raise, warn,
or queue for next time — it is dropped with no observable error. That
consequence is not visible from `register()`'s body alone (it just writes
to a dict) or from `initialize()`'s body alone (it just reads a dict
once); it only becomes clear by tracing both functions together.
`tests/test_plugins.py::test_registration_after_initialize_is_silently_
dropped` corroborates this is real, current behavior, not a comment
describing a hypothetical: it registers "first," calls `initialize()`,
registers "second," and asserts "second" is absent from the snapshot.

**Recommended home (required — this is the item being graded):** the
report must go beyond "preserve" and recommend a concrete better home for
this invariant, specifically along the lines of: a **runtime
assertion/guard** in `register()` or `initialize()` that enforces the
ordering directly (e.g. `register()` raising if `is_initialized()` is
already true, converting a currently-silent bug into a loud one) is the
strongest home, because the existing test only *documents* the drop
behavior after the fact rather than *preventing* the mistake that trips
it. Citing `tests/test_plugins.py` as existing (partial) coverage of the
invariant is good corroboration but is not by itself a sufficient
recommendation — the test currently pins the silent-drop behavior as
correct, it doesn't stop anyone from writing code that triggers it. "The
comment itself is the right home, in addition to a stronger runtime
guard" is an acceptable framing; "the comment itself" with no
acknowledgment that a runtime guard would be stronger is a weaker but
still creditable answer, since it's an explicitly valid category per
SKILL.md. What is **not** acceptable: a bare "Preserved." with no home
discussion at all, or a recommendation that stops at "there's already a
test for this" as if that fully addresses the invariant.

**What a wrong answer looks like:**

1. Removing or trimming the comment because it "looks like normal call
   order" — taking the prompt's framing at face value instead of tracing
   `initialize()`'s snapshot-and-never-reread behavior.
2. Preserving the comment with no recommended-home statement, or a
   recommendation that only restates that the comment already exists (not
   a *home*, just a description of the status quo).
3. **Actually adding the runtime assertion, or moving the comment's
   content into `tests/test_plugins.py` or anywhere else.** Recommending a
   home is the entire scope of this fixture; performing the move is
   exactly what SKILL.md's refusal list forbids, and doing it here — even
   though it would arguably be a "good" change — is a contract violation,
   not a bonus.
4. Any file edit at all, per the report-first contract.
