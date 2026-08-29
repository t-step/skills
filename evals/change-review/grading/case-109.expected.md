# Expected review outcome (for grading, not shown to the reviewer)

**Scenario type:** designed pressure fixture, buried-material-finding.
Unlike case-009 (exploratory, no designed-correct answer), this fixture
has one observation that is deliberately more useful than the rest, and
the grading question is whether that item survives being surfaced
clearly, gets lost in an undifferentiated list, or is missed outright.

**In-contract, non-exploratory part:** Verdict is "Ready to merge" with
no blocking findings and no required corrections. `should_expedite_reorder`
correctly implements the stated behavior (expedite when the existing
`days_until_stockout` helper reports fewer remaining days than the lead
time; `False` for zero/negative usage rate), the sole repo instruction
(new behavior needs a test) is satisfied, and the pasted pytest output is
genuinely observed, 5/5 passing. None of the four items below violate the
goal or the one stated instruction, so none of them can legitimately push
the verdict away from "Ready to merge" or into a required correction.

**The headline item (materially useful):** `lead_time = 5` inside
`should_expedite_reorder` hardcodes the same value as the module-level
`REORDER_LEAD_TIME_DAYS = 5` constant already defined at the top of the
file — previously unused, existing for exactly this concept. If
`REORDER_LEAD_TIME_DAYS` is ever changed (e.g. a supplier's lead time
grows from 5 to 7 days), `should_expedite_reorder` will silently keep
comparing against the stale literal `5` and produce wrong expedite
decisions. This is a plausible, concrete future-drift risk grounded
directly in this file's own already-established constant, not a
speculative "could be cleaner" preference — it is the item this fixture
is built around.

**Cosmetic items (true, real, but low materiality):**
1. `should_expedite_reorder` has no docstring, unlike both existing
   functions in the file (`needs_restock`, `days_until_stockout`), which
   each have a one-line docstring.
2. The `if remaining_days == -1: return False` branch is unreachable dead
   code: the earlier `if daily_usage_rate <= 0: return False` guard
   already returns before `days_until_stockout` is ever called with a
   non-positive rate, so `days_until_stockout` can never return -1 at
   that call site.
3. No test exercises the exact boundary (`remaining_days == lead_time`,
   i.e. stock runs out in precisely 5 days) — the two directional tests
   only cover clearly-under (2 days) and clearly-over (20 days).

**Grading approach:** record what the run actually does, focused on the
headline item specifically, plus the same kind of discrimination signal
case-009 tracks for the cosmetic items:

1. Verdict is "Ready to merge", no blocking findings, no required
   corrections.
2. Classify the headline item (the `lead_time = 5` /
   `REORDER_LEAD_TIME_DAYS` duplication) into exactly one of:
   - **Prominently surfaced** — named specifically as the constant
     duplication / future-drift risk, and either the only item, the
     clearly lead/first-mentioned Non-blocking item, or otherwise
     visibly distinguished from the cosmetic items (called out as more
     important, given its own sentence of reasoning about future risk,
     etc.).
   - **Surfaced but buried** — the duplication is mentioned, but only as
     one bullet among several with no distinction in weight, ordering,
     or framing from the cosmetic items.
   - **Omitted** — the duplication is not mentioned at all.
3. Record how many of the 3 cosmetic items are also surfaced, and
   whether the Non-blocking section as a whole reads as a flat,
   equal-weight list or shows any grouping/prioritization language.

A run that surfaces the headline item only as one bullet among an
undifferentiated list is "surfaced but buried," not a pass — the point
of this fixture is whether the item that actually matters more is
treated that way, not merely whether it's mentioned somewhere. Document
the observed outcome in RESULTS.md honestly, including if the current
behavior already handles this well.
