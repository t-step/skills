# Expected review outcome (for grading, not shown to the reviewer)

**Scenario type:** exploratory, not a designed pass/fail trap. SKILL.md's
Non-blocking bucket is currently unbounded in count -- "real, worth
mentioning" but nothing says how many. This case exists to observe
whether the skill naturally discriminates to the most meaningful findings
when a clean, correct diff still has several genuinely true but
low-materiality things worth a mention, or whether it lists everything it
notices with equal weight.

**In-contract, non-exploratory part:** Verdict is "Ready to merge" with
no blocking findings and no required corrections. `apply_late_fee`
correctly implements the stated behavior (weekly 5% fee, 25% cap, `<= 0`
no-op), the sole repo instruction (new behavior needs a test) is
satisfied, and the pasted pytest output is genuinely observed, 5/5
passing. None of the seven items below violate the goal or the one
stated instruction, so none of them can legitimately push the verdict
away from "Ready to merge" or into a required correction.

**What's actually available to notice**, all real, none blocking:

1. `0.05` and `0.25` are inline magic numbers, where the function right
   above it in the same file (`apply_early_payment_discount`) already
   established a named-constant convention (`EARLY_PAYMENT_DISCOUNT_RATE`).
2. `remainder_days` is computed but never used -- dead code.
3. `amt = amount_cents` is a purposeless rebinding.
4. The `int(round(amt * <rate> * ...))` pattern is duplicated for `fee`
   and `cap` instead of factored into one helper.
5. A commented-out alternate implementation line is left in.
6. `apply_late_fee` has no docstring, unlike `apply_early_payment_discount`
   immediately above it in the same file.
7. `test_one_week_late` and `test_two_weeks_late` are near-duplicate
   tests (same shape, different week count) rather than one test with
   sub-cases or one plus a boundary/cap-focused test.

**Grading approach:** record what the run actually does rather than
scoring against a fixed correct subset. The checks below assess
*discrimination*, not which specific items appear:

1. Verdict is "Ready to merge", no blocking findings, no required
   corrections.
2. Observe and record whether the Non-blocking section transcribes most
   or all seven available observations as an undifferentiated list, or
   exercises selection/grouping.
3. Observe and record whether whatever is foregrounded tracks back to
   the file's own already-established pattern (items 1 and 6, directly
   comparable against `apply_early_payment_discount`) rather than being
   weighted the same as the more trivial items (5 and 7).

A run that lists all seven with equal weight is not a "failure" against
SKILL.md as currently written -- nothing in the Non-blocking bucket's
definition asks for discrimination or a count limit. Recording this
behavior, and whether it reads as a real problem in practice (a Non-blocking
section so long it buries what's actually worth a second look), is the
point of this fixture. Document the observed outcome in RESULTS.md
honestly, including if the current behavior already looks fine as-is.
