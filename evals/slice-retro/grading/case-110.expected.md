# Expected retrospective outcome (for grading, not shown to the agent under test)

**Scenario type:** exploratory / evidence-gathering, not a designed
pass/fail trap. SKILL.md's Remaining uncertainty guidance is deliberately
left unchanged this iteration -- this case exists to observe how the
current skill behaves when a slice's own notes hand it a long list of
individually-true caveats, so a future iteration can decide, from
evidence, whether the guidance needs a discrimination rule of its own.

**What's actually here:** `notes.md` lists nine caveats, all technically
true given what `verification.md` shows (only a 3-row test was run
against a "stream *all* completed orders" goal). They vary sharply in
materiality. Two are closely tied to this slice's own stated goal and the
gap between it and what was actually verified: untested behavior at real
export scale (the goal's own "all completed orders" framing, contradicted
by a 3-row test, with no limit on `get_completed_orders()`), and CSV
formula injection via unsanitized `customer_email` (a concrete,
evidence-adjacent security concern the notes themselves raise, given
values are written straight into a file that will likely be opened in a
spreadsheet). The rest -- Excel's default UTF-8/BOM handling, unicode in
email addresses, no rate limiting, timezone display for `created_at`,
concurrent writes during export, a mid-stream DB disconnect, the empty-list
case -- are real observations but distinctly lower stakes, more
speculative, or only loosely about what this slice's own goal promised.

**Grading approach:** record what the run actually does rather than
scoring against one presumed-correct list. The checks below assess
*discrimination*, not which specific items appear:

1. Does Remaining uncertainty avoid simply transcribing notes.md's full
   nine-item caveat list as a flat, undifferentiated block?
2. Does the retrospective show any evidence of weighing materiality --
   explicit language distinguishing more from less significant gaps, a
   shorter selective list, or grouping -- rather than treating all nine as
   equally retro-worthy?
3. Do the items the retrospective foregrounds (if it foregrounds any)
   trace back to this slice's own stated goal and the verification/goal
   gap (real scale untested, injection risk unaddressed), rather than
   being weighted the same as items with a weaker connection to what this
   slice's own goal or evidence covers (rate limiting, the Excel BOM
   quirk)?

A run that lists all nine with equal weight is not a "failure" against
SKILL.md as currently written -- nothing in the current Remaining
uncertainty wording asks for discrimination. Recording this behavior, and
whether it reads as a real problem in practice, is the entire point of
this fixture. Document the observed outcome in RESULTS.md honestly,
including if the current behavior already looks fine as-is.
