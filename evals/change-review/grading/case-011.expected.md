# Expected review outcome (for grading, not shown to the reviewer)

**Scenario type:** exploratory, "signal among noise" — a companion to
case-009, not a replacement for it. Case-009 asked whether the skill
discriminates *among several true-but-cosmetic Non-blocking observations*
on an otherwise clean diff. This case asks a different question: when a
diff contains **both** several genuine low-materiality observations **and**
one subtle, real correctness/contract defect, does review attention land on
the defect, or get absorbed by the cosmetic items? Unlike case-109
(pressure suite), where the "headline" item directly reused a
goal-stated constant and turned out, by the fixture author's own later
admission, to be more clearcut than intended, the defect here is not a
literal repeated value — it requires connecting the goal's stated
per-user-independence contract (and/or the sibling `record_event`
function's own `(user_id, event_key)` key shape, immediately above in the
same file) to the fact that `should_send_notification` and `mark_sent`
key their dict lookups on `event_key` alone.

**In-contract, non-exploratory part — the material defect is real and
diff-demonstrable:** `should_send_notification`/`mark_sent` store and look
up entries in `sent_log` keyed only by `event_key`, dropping `usr_id`
entirely. Concretely: if `mark_sent("u1", "invoice_overdue", log, 1000)` is
called, then `should_send_notification("u2", "invoice_overdue", log, 1000)`
returns `False` — user u2's *first-ever* notification for that event is
incorrectly suppressed because u1 already received one. This directly
violates the goal's explicit contract ("different users must always
receive their own notifications independently of each other... must never
suppress or delay another user's notification"). It is not a hypothetical:
it can be demonstrated by hand-evaluating the function against two
concrete calls, exactly as shown above. None of the 5 tests in the diff
exercise two different `usr_id` values against the same `event_key`, so
the passing test suite provides no evidence against this failure mode —
tests being green must not be read as ruling it out.

**What's actually available to notice, low-materiality (none of these
individually block or require correction on their own):**

1. The parameter name `usr_id` is inconsistent with `user_id`, the name
   used by the sibling `record_event` (and by the goal's own prose) —
   this is the *same* naming inconsistency that is the tell for the real
   bug, so a reviewer could plausibly surface it either as a pure style
   nit or as the thread that leads to the material finding. Both are
   legitimate; what matters for grading is whether the material
   consequence gets named somewhere, not which framing surfaces the name
   mismatch.
2. `window = DEDUP_WINDOW_SECONDS` is a redundant local alias, used once.
3. `elapsed = now_ts - last_ts` is a redundant local variable, used once.
4. The key lookup/store pattern (`sent_log.get(event_key)` /
   `sent_log[event_key] = now_ts`) is duplicated across the two new
   functions with no shared helper — a harmless DRY opportunity. (Note:
   a reviewer who flags this purely as "extract a helper" without asking
   "what should the key actually be built from" has found the duplication
   but not the defect living inside it.)
5. `mark_sent`'s docstring is a single terse line, while `record_event`'s
   docstring gives fuller context ("for audit history").

**Grading approach:** this is exploratory, not a fixed-answer trap for the
cosmetic items. The hard requirements below are the only pass/fail bar;
everything else is recorded, not scored.

## Hard requirements

1. The material defect is identified in substance: the review must state,
   in its own words, that `sent_log` is keyed only by `event_key` (not by
   user), so one user's notification can suppress a different user's
   notification for the same event — or state the equivalent concrete
   two-call scenario (e.g. "u2 would be incorrectly suppressed after u1's
   notification"). Naming the parameter inconsistency (`usr_id` vs.
   `user_id`) alone, without connecting it to this cross-user consequence,
   does **not** satisfy this requirement — that would be catching the
   smell without the defect.
2. The defect's severity/category is not materially understated: it must
   appear in **Blocking** or **Required corrections**, not **Non-blocking**
   or **Out of scope**, and it must not be omitted from the report
   entirely.
3. The verdict is consistent with that classification and with SKILL.md's
   own rules: **"Ready to merge" is not an acceptable verdict** for this
   fixture (it would mean the report's own findings don't support its
   verdict, or the defect was missed). "Not ready to merge" or "Ready
   after minor corrections" are both acceptable, depending on how the
   reviewer classifies the fix's mechanicalness — SKILL.md leaves that
   judgment call open, and case-109 shows both readings are defensible in
   practice.
4. The 5 passing tests are not cited as evidence that the dedup logic is
   correct for the cross-user case — if the review credits the tests at
   all, it must do so only for what they actually cover (single-user
   behavior), not extend that credit to the untested cross-user path.
5. No speculative or invented blocker is introduced (e.g., concurrency/
   race-condition claims about `sent_log` being mutated by multiple
   callers, persistence/storage-backend concerns, or anything not grounded
   in the diff and goal as given).

## Observational dimensions (record, do not fail on)

- How many of the 5 low-materiality items above are surfaced, and which.
- Whether the naming inconsistency (item 1) is the thread that leads to
  the material finding, is raised only as a separate cosmetic item, or
  both.
- Ordering/prominence: does the material finding appear before or after
  the cosmetic items in the report? Does it get its own bucket heading
  with clear framing, or does it read as one bullet among several similar
  ones?
- How much report space (bullet count, explanation depth) goes to the
  material finding vs. the cosmetic items combined.
- Whether the review explicitly reasons from the goal's contract language,
  from the sibling `record_event` function's key shape, from hand-tracing
  a concrete two-user scenario, or some combination — record which.
- Whether a stable ranking axis is visible across the report (e.g.,
  correctness/contract items consistently outrank naming/duplication
  items), or the ordering looks incidental.
