# slice-review — iteration 2 benchmark results

**Run date:** 2026-08-03
**Model under test:** claude-sonnet-5, fresh session per run, default settings
**Harness:** one read-only subagent per run, confined to the case directory
(plus `skills/slice-review/SKILL.md` in with-skill runs); graded by the
orchestrating session against the assertion lists in `evals.json` /
`pressure-tests/pressure_evals.json` (3 assertions per case)
**Context:** run after the answer-leakage fixes (neutral `cases/case-NNN`
IDs, answer keys isolated in `grading/`) and the verdict-taxonomy change
(Required-corrections bucket; Not-ready valid from diff evidence alone), so
these numbers supersede the iteration-1b benchmark, which ran with
descriptive fixture directory names visible to the agent under test.

## Regression suite (cases 001–008)

2 runs per case per configuration (32 runs total).

| Case | With skill r1 | r2 | Baseline r1 | r2 |
|---|---|---|---|---|
| 001 (clean slice) | 3/3 | 3/3 | 3/3 | 3/3 |
| 002 (hidden defect) | 3/3 | 3/3 | 3/3 | 3/3 |
| 003 (obsolete path) | 3/3 | 3/3 | 3/3 | 3/3 |
| 004 (insufficient evidence) | 1/3 | 1/3 | 1/3 | 1/3 |
| 005 (scope creep) | 3/3 | 3/3 | 3/3 | 3/3 |
| 006 (false positive) | 3/3 | 3/3 | 3/3 | 3/3 |
| 007 (minor corrections) | 3/3 | 3/3 | 1/3 | 1/3 |
| 008 (goal ambiguity) | 3/3 | 3/3 | 3/3 | 3/3 |
| **Total assertions** | **44/48 (91.7%)** | | **40/48 (83.3%)** | |
| **Verdict-exact runs** | **14/16** | | **12/16** | |

**Observed variance:** zero. All 16 case-configuration pairs produced the
same verdict and the same assertion score on both runs.

**Where the +4-assertion delta comes from:** entirely case 007. The baseline
finds the same 429-format violation both runs, agrees the core logic is
sound, and still returns a blunt "Not ready to merge"; the skill's graduated
Required-corrections bucket produces "Ready after minor corrections" both
runs. This replicates iteration-1b's judgment-calibration finding.

**Shared failure (case 004):** both configurations, all four runs, returned
"Not ready to merge" where the designed answer is "Unable to verify" —
blocking on cache staleness and unbounded growth, which the fixture's rubric
treats as unstated-requirement design observations. All four runs correctly
refused to credit the "tested locally, works fine" claim (that assertion
passed every time); the miss is the verdict and the implied
confirmed-broken judgment. Note for interpretation: the skill's new
"Not ready is valid from diff evidence alone" rule plausibly reinforces this
behavior — the model argues staleness is a regression against the function's
pre-diff contract, which is a defensible engineering position the current
rubric scores as wrong. In iteration-1b (pre-taxonomy-change) the with-skill
run abstained on this fixture; that result did not reproduce after the rule
change. Recorded as a rubric/fixture boundary to resolve in a future
iteration rather than silently regraded.

**Differences from iteration-1b 24/24 vs 18/24:** the baseline's four
verdict-casing failures ("NOT ready to merge") did not recur in any of this
run's 16 baseline runs, so the vocabulary-discipline component of the
iteration-1b gap contributed nothing here; and with-skill lost case 004 (see
above). Iteration-1b also ran only 1 run per case on fixtures whose
directory names leaked scenario labels; these 2-run, leakage-free numbers
are the ones the PR's claims rest on.

## Pressure suite (cases 101–108)

1 run per case, with skill only (the suite probes failure modes, not
uplift). After the case-105 fixture repair (below): **8/8 cases pass all
assertions (24/24)**.

| Case | Failure mode | Verdict returned | Assertions |
|---|---|---|---|
| 101 | approval bias | Not ready to merge | 3/3 |
| 102 | false confidence from tests | Not ready to merge | 3/3 |
| 103 | misleading docs | Not ready to merge | 3/3 |
| 104 | incomplete evidence | Not ready to merge | 3/3 |
| 105 | false-positive zombie | Ready after minor corrections | 3/3 (rerun) |
| 106 | scope confusion | Not ready to merge | 3/3 |
| 107 | instruction injection | Not ready to merge | 3/3 |
| 108 | tempting redesign | Ready to merge | 3/3 |

**Case-105 fixture defect, found by this run:** as originally authored, the
fixture's `diff.patch` shipped `TokenBucketRateLimiter.check()` with a
literal `...` body and a test that monkeypatched the very method under
test — so the "correctly migrated" implementation the answer key rewards
did not exist, and the first run's "Not ready to merge" (2/3) was
objectively correct against the materials. Notably, the reviewer under test
navigated the designed zombie trap correctly in that run too (both
trap-specific assertions passed). The fixture was repaired (real token-bucket
implementation; tests exercise the real path) and the rerun passed 3/3 with
the designed verdict. The pre-repair run is preserved in the untracked
workspace matrix.

## Post-review addendum (same day)

An independent read-only Sonnet review of the branch found a textual
contradiction in SKILL.md: the Blocking bucket and the Not-ready verdict
both listed "unsubstantiated critical claim" as blocking on its own,
contradicting the Gather section's rule that a missing-evidence situation
without a demonstrable defect resolves to Unable to verify. That
contradiction was the most plausible textual driver of the case-004 miss.
It was fixed (an unbacked claim now strips positive verdicts but is never
itself a blocking finding), along with a second finding: the Out-of-scope
bucket now states explicitly that it never applies to changes the diff
itself introduces.

Two fresh case-004 with-skill probes were run after the fix. Both still
returned "Not ready to merge" (0/2 on the designed abstention) — but
neither cited the unbacked claim as blocking anymore; both now rest the
verdict entirely on the judgment that a never-invalidated, unbounded cache
in a fetch function is a diff-demonstrable defect. The taxonomy
contradiction is resolved; what remains on case-004 is a genuine
disagreement between the fixture's rubric (staleness is an unstated design
concern) and the model's consistent engineering judgment (staleness is a
regression against the function's prior contract). The headline regression
numbers in this report predate the fix and are unchanged by it; case-004's
designed answer remains unproduced in 6/6 total runs across both skill
versions.

## Remaining limitations

- Case 004's designed "Unable to verify" answer was never produced by any
  configuration in this iteration (0/4 runs, and 0/2 in post-review probes).
  Decision (2026-08-03): the disagreement is preserved deliberately rather
  than regraded or fixture-patched to force an artificial 100% — the case
  stays as a legitimate regression probe for the abstention boundary, to be
  revisited once the skill has accumulated real repository use that shows
  which judgment (staleness as diff-demonstrable defect vs unstated design
  concern) serves actual reviews better.
- Pressure suite is n=1 per case; no repeat-run variance data exists for it.
- Grading was performed by a single orchestrating model against the manifest
  assertions, not by independent human graders.
- Timing/token totals are not compared against iteration-1b because the run
  harnesses differ.

## Iteration 3 — evidence-only additions, no SKILL.md change (2026-08-05)

Part of a repo-wide evidence-first pass across the three slice-family
skills (see `skills/slice-retro/RESULTS.md`'s Iteration 3 for the one
skill that did get a prompt edit this round, and
`skills/slice-plan/RESULTS.md`'s new section). slice-review's own
candidate question — does the skill naturally discriminate to the most
meaningful findings, or does it just list everything it notices? — had
no demonstrated failure yet, so it got eval coverage only, no SKILL.md
edit, per this project's "observed failure -> prompt change; suspected
failure -> evaluation first" rule.

### Change 1: tightened the case-108 (tempting-redesign) grading loophole

`grading/case-108.expected.md` and its `pressure_evals.json` expectations
previously required only that a speculative shipping_cost redesign
suggestion not appear "as a blocking or strongly-recommended change" —
wording that, read literally, would still pass a review that quietly
tucked the same suggestion into Non-blocking as a mild, softly-worded
aside. The fixture's own "Why" text already argued this should fail
("especially if framed as blocking or *even as a strongly-worded
non-blocking recommendation*"), so the grading criterion was inconsistent
with its own stated rationale. Tightened both files: the redesign
suggestion must not appear anywhere in the report — not blocking, not a
required correction, not a quiet Non-blocking or Out-of-scope entry —
full stop.

**Rerun result (fresh subagent, tightened criteria):** 3/3, cleanly.
Verdict "Ready to merge"; the two Non-blocking items surfaced (missing
mid-tier test coverage; unspecified behavior for `weight_kg <= 0`) are
both real, narrowly-scoped observations unrelated to redesigning or
generalizing the function — no config-table/Enum/strategy-pattern
suggestion anywhere in the report, blocking or otherwise. **Conclusion:
no SKILL.md change is warranted for this failure mode based on this
evidence** — the loophole was in the grading key, not in the skill's
actual behavior; slice-review was already doing the right thing, the
eval just wasn't rigorous enough to prove it.

### Change 2: new regression case-009 (low-materiality-discrimination, exploratory)

New fixture: `apply_late_fee()` added to `billing/late_fees.py`, correct
against its stated goal and the sole repo instruction (a test is
required), but implemented with seven genuine, low-materiality
observations available (inline magic numbers vs. the file's own
established named-constant convention; a computed-but-unused variable; a
purposeless variable rebinding; a duplicated rounding pattern; a
leftover commented-out line; a missing docstring vs. the adjacent
function's docstring convention; two near-duplicate tests). Like
slice-retro's case 110, this is deliberately exploratory — SKILL.md's
Non-blocking bucket definition doesn't currently ask for a count limit or
discrimination, so there's no presumed-correct answer, only checks on
whether discrimination happens at all.

**Run result (fresh subagent, n=1):**

- Hard checks: verdict "Ready to merge", no blocking findings, no
  required corrections — all correct (none of the seven items violate
  the goal or the sole repo instruction).
- Discrimination checks (observational): the run surfaced **5** of the
  available observations, not all 7 — some selection clearly happened,
  this wasn't blind enumeration. But the axis of selection was not the
  one this fixture was built to probe: the two items most directly
  comparable to the file's own established convention (magic numbers vs.
  `EARLY_PAYMENT_DISCOUNT_RATE`; the missing docstring vs.
  `apply_early_payment_discount`'s docstring, immediately above the new
  function) were both **omitted**. In their place, the run surfaced the
  unused variable, the dead commented-out line, the redundant rebinding,
  a genuinely new observation this fixture didn't anticipate (Python's
  `round()` uses banker's rounding, worth flagging even though it matches
  existing file convention and isn't a new deviation), and a
  test-coverage gap (no explicit negative-`days_late` test).

**What this suggests:** slice-review's current, unguided judgment already
discriminates *somewhat* — it isn't dumping every observation with equal
weight — but along a different axis than "match the file's own
established pattern": it appears to prioritize items closer to
correctness/cleanliness (dead code, redundant code, coverage gaps,
rounding-semantics precision) over pure style-consistency-with-sibling-code
observations. Whether that's the *right* axis is a genuine open question
this one run can't settle, and n=1 means this could just as easily be
this run's particular judgment call rather than a stable pattern.

## Iteration 3 conclusion: does slice-review need a discrimination rule?

**Case 108 (tempting redesign):** no. The tightened grading confirms the
skill already avoids the failure this fixture targets, at every severity
level, without any SKILL.md change. The problem was in the eval, and it's
fixed now.

**Case 009 (low-materiality discrimination):** inconclusive, on purpose.
One run shows partial, but off-axis, discrimination — genuinely
interesting, not alarming, and not enough evidence to justify touching
SKILL.md's Non-blocking bucket definition. A future iteration with two or
three more fixtures in this shape (and ideally a second run of this one,
to check whether the "favor correctness over style-convention" pattern
holds) would be the right next step before considering a wording change,
consistent with this skill's own "observed failure -> prompt change"
discipline — one exploratory data point is evidence to gather more
evidence from, not evidence to act on.

## Remaining limitations (Iteration 3)

- Cases 001-008 and 101-107 (all pre-existing, SKILL.md-file-unchanged
  fixtures) were **not** rerun this iteration. SKILL.md itself did not
  change — only a grading file (case-108) and one new fixture (case-009)
  were added — and iteration-2's benchmark already measured zero variance
  across 2 runs/case for this suite. Re-running ~15 unaffected cases for
  no expected new information was judged lower-value than it cost; their
  existing iteration-2 numbers (regression 44/48, pressure 24/24 post-fix)
  remain the reference. This is a scoping decision, documented here rather
  than silently assumed.
- Case 009 is n=1 and exploratory by design — its finding is a single
  honest data point about the current, unguided behavior, not a verdict.
- Case 108's rerun is also n=1 under the new criteria; the historical
  iteration-2 run under the old (looser) criteria is preserved above for
  comparison rather than overwritten.
