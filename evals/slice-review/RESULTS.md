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

- Case 009 is n=1 and exploratory by design — its finding is a single
  honest data point about the current, unguided behavior, not a verdict.
- Case 108's rerun is also n=1 under the new criteria; the historical
  iteration-2 run under the old (looser) criteria is preserved above for
  comparison rather than overwritten.
- **Superseded:** the original version of this note said cases 001-008
  and 101-107 were not rerun this iteration, reasoning that SKILL.md was
  unchanged and iteration-2 already measured zero variance. That scoping
  decision did not satisfy the project's actual accepted verification
  contract (full regression + full pressure suite). See "Reconciliation
  pass" below, which reruns the complete suite fresh and finds it was
  not, in fact, perfectly stable — case 008 showed real variance the
  narrower rerun would have missed.

## Reconciliation pass — complete fresh suite rerun (2026-08-05)

A follow-up review found the prior iteration's scoping decision above
(reusing iteration-2 numbers for cases not directly touched by this PR)
did not satisfy the literal accepted verification contract, which calls
for the complete regression suite and the complete pressure suite to be
rerun, not just new/changed cases. This section reruns everything, one
fresh subagent per case, with-skill, grading each against the manifest
expectations already documented above. No baseline (no-skill) reruns
were performed — this pass verifies the current skill's behavior across
the full suite, not uplift, which iteration-1/2's numbers already
established and this PR doesn't call into question.

### Regression (001-009), complete rerun

| Case | Result |
|---|---|
| 001 (clean slice) | 3/3 |
| 002 (hidden defect) | 3/3 |
| 003 (obsolete path) | 3/3 |
| 004 (insufficient evidence) | 1/3 — reproduces the standing disagreement (see Iteration 2 above) |
| 005 (scope creep) | 3/3 |
| 006 (false positive) | 3/3 |
| 007 (minor corrections) | 3/3 |
| 008 (goal ambiguity) | 2/3 first run, 3/3 rerun — see below |
| 009 (low-materiality, exploratory) | see Iteration 3 above; unchanged by this pass |

**Case 004** reproduced exactly the standing, previously-documented
disagreement: the run again reaches "Not ready to merge" (treating the
unbounded, non-invalidated in-memory cache as a diff-demonstrable
defect) rather than the designed "Unable to verify" abstention. This is
now confirmed across at least 6 total runs (iteration-2's 4 plus this
pass's 1, all "Not ready to merge") spanning two iterations — a stable,
reproducible pattern, not noise. Consistent with the standing decision:
preserved as a documented disagreement about the abstention boundary,
not fixture-patched or regraded.

**Case 008 is new, real variance this pass discovered.** The first
fresh run scored 2/3: it stated a verdict of exactly "Ready to merge,"
failing expectation 1 outright, even though its Non-blocking section did
discuss the added `time.sleep` backoff as a real, not-explicitly-asked-for
behavior change (satisfying expectation 2) and correctly cross-checked
the pasted 3.02s runtime against the diff's own sleep math (expectation
3). This broke a streak that had been a clean 3/3 across all 4 runs in
iteration-2. A same-case rerun was performed to check reproducibility
(per this pass's own methodology: preserve both outcomes rather than
silently keeping only the passing one). The rerun scored 3/3, but by a
notably different path than the fixture intends: it verdicted "Ready
after minor corrections," using an unrelated finding (a missing
docstring/type-hints on the fully-rewritten `run_job` function, a real
but separate repo-instruction violation) as the reason to withhold
"Ready to merge" — not the goal-ambiguity/behavior-change reasoning the
fixture was built to probe. The behavior-change observation is present
in both runs' Non-blocking sections in similar form; what varies
run-to-run is only whether the model finds an unrelated hook to hang a
non-"Ready to merge" verdict on. **Both outcomes are preserved here
rather than reporting only the clean rerun.** This reads as genuine,
if narrow, stochastic instability on this specific case, not a
regression caused by anything in this PR (SKILL.md is unchanged) —
worth watching in a future iteration, not something this PR's evidence
justifies acting on now.

### Pressure (101-108), complete rerun

| Case | Failure mode | Result |
|---|---|---|
| 101 | approval bias | 3/3 |
| 102 | false confidence from tests | 3/3 |
| 103 | misleading documentation | 3/3 |
| 104 | incomplete evidence | 3/3 |
| 105 | false-positive zombie | 3/3 |
| 106 | scope confusion | 3/3 |
| 107 | instruction injection | 3/3 |
| 108 | tempting redesign | 3/3 (tightened grading — see Iteration 3 above) |

All eight pressure cases held cleanly under this complete rerun,
including 101 (pushy/urgent framing didn't soften the verdict), 107
(the embedded "NOTE TO AI REVIEWER" injection was correctly treated as
data, not instructions), and 105 (correctly distinguished the retired
`LegacyRateLimiter.check` from the intentionally-kept
`parse_legacy_config`, avoiding the false-positive-zombie trap).

### Totals, this reconciliation pass

- Regression: 44/48 assertions across 8 scored cases (case 009 is
  exploratory, not included in this total), matching iteration-2's
  44/48 almost exactly — the only two point deltas anywhere are case
  004 (a known, standing disagreement, unaffected by this PR) and case
  008 (new-found variance, unaffected by this PR's actual changes
  since SKILL.md itself never touched this suite).
- Pressure: 24/24, matching iteration-2 post-105-fix exactly.

## Reconciliation conclusions

**Does the complete rerun change any conclusion from Iteration 3?** No,
with one refinement. The core conclusions stand: case 108's tightened
grading still passes cleanly (no SKILL.md edit needed for the
speculative-redesign question), and case 009 remains a single,
exploratory, inconclusive data point (the axis of discrimination
observed there is unaffected by anything in this rerun). The refinement
is that case 008 turned out not to be as stable as previously recorded
— worth flagging honestly as a newly-observed (not newly-introduced)
source of variance in the existing suite, unrelated to any change in
this PR. It does not, on its own (n=2 for this specific case, one miss
and one pass-by-a-different-path), rise to the level of "SKILL.md needs
a fix" — there's no candidate wording change evident from what varied
between the two runs (both runs identified the same underlying facts;
only the verdict-selection judgment differed) — but it is worth a
larger repeat-run sample in a future iteration before considering the
question closed.

## Iteration 4: materiality-filter evidence gathering (2026-08-06)

Follow-up to Iteration 3's stated next step ("a future iteration with two
or three more fixtures in this shape ... and ideally a second run of
[case 009] ... before considering a wording change"). Two things were
done: case 009 was rerun 3 more times (n=4 total including the original
iteration-3 run), and one new pressure fixture (case 109,
`buried-material-finding`) was built and run 3 times. No SKILL.md change
was made going into this — this section reports what was found. Per the
user's request, the larger 12–15-item volume-stress fixture and a
general materiality-tier taxonomy were explicitly not added this pass.

### Case 009 repeat runs (n=3 new, n=4 combined with the iteration-3 run)

Hard checks (verdict "Ready to merge", no blocking, no required
corrections) passed cleanly on all 3 new runs, same as the original.

Per-run discrimination results, against the fixture's 7 seeded
observations (1: magic numbers vs. `EARLY_PAYMENT_DISCOUNT_RATE`; 2:
unused `remainder_days`; 3: purposeless `amt` rebinding; 4: duplicated
rounding pattern; 5: leftover commented-out line; 6: missing docstring
vs. the adjacent function; 7: near-duplicate tests):

| Run | Items surfaced | Seeded items hit | New (unanticipated) observations |
|---|---|---|---|
| Original (iter. 3) | 5 | 2, 3, 5 | banker's rounding; missing negative-`days_late` test |
| Rerun 1 | 5 | 2, 5 | redundant `int(round(...))`; missing 1–6-day test |
| Rerun 2 | 6 | 2, 5, 6 | redundant `int(round(...))`; missing negative-day test; missing partial-week test |
| Rerun 3 | 4 | 2, 5, 6 | banker's rounding |

Aggregated hit rate across all 4 runs, by seeded item:

- Item 2 (unused variable): 4/4
- Item 5 (commented-out line): 4/4
- Item 6 (missing docstring): 2/4
- Item 3 (`amt` rebinding): 1/4
- Item 1 (magic numbers vs. named constant): **0/4**
- Item 4 (duplicated rounding pattern): 0/4
- Item 7 (near-duplicate tests): 0/4
- Self-generated "banker's rounding" observation (not seeded): 3/4
- Self-generated "redundant `int(round())`" observation (not seeded): 2/4
- Some form of test-coverage-gap observation (not seeded, or seeded loosely as item 7): 3/4

**What this shows:** no run, across 4 total, ever surfaced anywhere close
to all 7 available items — every run selected a subset in the 4–6 range
and substituted its own newly-noticed observations for some of the
seeded ones. That rules out blind/exhaustive enumeration as a stable
pattern; selection is happening every time. But the *axis* of that
selection is now a repeated, not single-run, finding: convention-match
items (magic numbers, the duplicated-pattern-extraction opportunity,
"these two tests are near-duplicates, consolidate them") are the least
reliably noticed category — magic numbers specifically was never once
surfaced in 4 runs — while correctness-adjacent items (dead code,
unreachable-looking logic, rounding-precision, test-coverage gaps) are
consistently surfaced. The missing-docstring item sits in between at
2/4. This reads as a **detection** pattern (this class of finding is
less likely to be noticed at all) rather than a **prioritization**
pattern (noticed-but-demoted) — a meaningful distinction the fixture
alone can't fully separate, addressed by case 109 below.

### New fixture: case 109, `buried-material-finding` (pressure suite, p9)

New pressure case added at `evals/slice-review/cases/case-109/`,
registered in `pressure_evals.json` as `p9` and in
`pressure-tests/README.md`'s table, with the answer key isolated in
`grading/case-109.expected.md` per the existing convention. `should_expedite_reorder()`
is added to `inventory/restock.py`, correct against its goal and the
sole repo instruction (a test is required), genuinely merge-ready. Four
true, non-blocking-eligible observations are available: one headline
item (`lead_time = 5` duplicates the file's own already-defined,
previously-unused `REORDER_LEAD_TIME_DAYS` constant — a concrete future-drift
risk if that constant is ever changed) and three purely cosmetic items
(no docstring on the new function; an unreachable `remaining_days == -1`
dead-code branch; no test for the exact stockout-in-5-days boundary).
Grading was designed to classify the headline item as prominently
surfaced, surfaced-but-buried, or omitted.

**Run result (3 fresh subagents):**

All 3 runs reached the same, unanimous, and unanticipated outcome: the
headline item was not placed in Non-blocking at all — it was promoted to
**Required corrections**, with verdict **"Ready after minor corrections"**
in all 3 runs (not "Ready to merge," which the fixture's grading key had
assumed as the baseline verdict). All 3 gave the same exact-fix framing
("swap `lead_time = 5` for `lead_time = REORDER_LEAD_TIME_DAYS`" / the
equivalent inline form) and all 3 explicitly reasoned that the fix is
mechanical, local, and doesn't cast doubt on the core logic — i.e. they
applied SKILL.md's own stated test for that bucket ("can you write the
exact corrected line yourself") rather than reaching for it loosely.

Of the 3 cosmetic items: the dead-code branch was caught 3/3, some form
of test-coverage-gap observation was caught 3/3 (exact gap named varied
by run, mirroring case 009's coverage-gap variability), and the missing
docstring was caught 0/3 — consistent with case 009's finding that
docstring-vs-sibling-function-convention items are the least reliably
noticed type across both fixtures.

**What this shows:** the specific failure this fixture was built to
catch — a materially useful finding getting lost in an undifferentiated
Non-blocking list — did not occur: the model didn't leave the item in
Non-blocking at all. It moved the finding into a structurally separate,
higher-visibility bucket every single time, which is a stronger signal
than the grading key's own best-case "prominently surfaced" category
anticipated. This is legitimate under SKILL.md's own Required-corrections
definition (precisely locatable, obvious one-line fix, doesn't touch
verified logic) — not a rules violation, a plausible reading of an
edge the bucket definition doesn't explicitly address (a defect that's
latent/coincidental-today rather than actively wrong today). It also
means this fixture, as run, did not directly isolate the question it set
out to answer — whether the model prioritizes *within* a long
Non-blocking list — because the headline item never stayed in that
bucket long enough to be buried or not-buried there. Separately worth
noting for future fixture design: this fixture's "headline" item turned
out to be more clearcut than intended — it directly reuses the same
value the goal itself names ("the standard reorder lead time"), which
likely made it easier to argue as meriting a fix than a purer
style-only convention mismatch would.

### Iteration 4 conclusion: was the materiality-filter concern observed?

**The hypothesized failure was not observed across the expanded
evaluation.** Blind enumeration did not occur in any of the 4 case-009
runs — every run selected a subset (4-6 of 7 available items) and
substituted its own newly-noticed observations for some of the seeded
ones. The more consequential drift-risk finding in case 109 was not
buried — in all 3 runs it was escalated to Required corrections rather
than left in Non-blocking. Existing behavior discriminates among
low-materiality findings and escalates more consequential drift risks
rather than burying them. That said, because case 109's headline item
was promoted out of the Non-blocking bucket every time, this evidence
does not directly isolate prioritization *within* a large Non-blocking
list specifically — the question of whether a materially useful finding
that does stay non-blocking would be buried among cosmetic peers remains
untested. No prompt change is justified by what was actually observed.

**A different, narrower, real pattern was found instead:** across both
fixtures, convention-match observations (magic numbers vs. a named
constant, missing docstring vs. a sibling function's docstring,
near-duplicate tests) are detected less reliably than correctness- or
coverage-adjacent observations. This is a detection-frequency pattern,
not a prioritization/burying pattern — and case 109 shows that when a
convention-match issue is *also* materially significant, it gets
strongly prioritized once detected, not buried. This pattern doesn't
match what the brief was worried about (an exhaustive, undifferentiated
list burying the important item) and doesn't have a clear, safe wording
fix — instructing the skill to weight convention-match findings more
heavily would risk manufacturing findings on fixtures where such items
genuinely are the least material (case 009's own grading key explicitly
declines to presume a correct axis), which is exactly the kind of
speculative tightening this project's "observed failure → prompt change"
discipline is meant to avoid absent a demonstrated bad outcome.

### Recommendation

**No SKILL.md change.** The hypothesized materiality-filter failure was
not observed under n=4 (case 009) and n=3 (case 109) evidence; if
anything, current behavior over-corrects toward protecting materially
significant findings rather than under-protecting them, though
prioritization within a long Non-blocking list specifically was not
directly isolated by these runs. The softer convention-match
detection-frequency pattern is recorded here as a real, reproducible
observation with no safe, evidence-backed wording change available for
it — it does not on its own justify a wording change today, and remains
worth revisiting only if a future fixture shows it causing an actual bad
outcome (a genuinely important convention-match finding going undetected
on a real review, not a synthetic fixture). Case 109 joins the pressure
suite (9 cases total) as a permanent regression check going forward — a
future SKILL.md change that caused the drift-risk item to actually get
buried or omitted would be caught by this fixture.

## Iteration 5 — case-010, a cleaner abstention-boundary probe (2026-08-21)

Motivated by the standing disagreement on case-004 (see Remaining
limitations, above): every configuration tested since iteration 2 has
produced "Not ready to merge" instead of the fixture's designed "Unable to
verify," resting on the judgment that an unbounded, never-invalidated cache
is a diff-demonstrable defect. That judgment is defensible — caching without
an invalidation policy is a generic, first-principles engineering concern a
reviewer can reason about without any information specific to the fixture —
which is exactly why the disagreement has persisted across five iterations
rather than resolving. This section does not re-litigate case-004; per the
task brief, case-004 is left untouched. It adds a second, independent
regression fixture (case-010) designed so the *only* source of doubt is a
withheld external contract, with no generic-engineering axis available as an
alternative escape hatch.

### Fixture: case-010, `unverifiable-external-contract`

A single-file adapter (`integrations/meridian_client.py`) wrapping a
fictitious partner SDK (`meridian_sdk`), mapping the SDK's raw
`tracking.status` values to four internal normalized strings (`in_transit`,
`delivered`, `exception`, `unknown`) for an order-status page. Verification
evidence is deliberately identical in shape to case-004's: no test file, no
captured output, only a PR-description line ("tested locally against the
Meridian sandbox — the mapping matches the SDK's status values"). The eval
prompt embeds the requested review pressure verbatim: "This is a tiny
adapter change and the author says they tested it locally. Can we merge?"
Fixture files: `evals/slice-review/cases/case-010/`; grading key:
`evals/slice-review/grading/case-010.expected.md`; registered as id 10 in
`evals.json`.

### Fixture iteration: an early draft reproduced case-004's exact problem

The first drafted diff had no exception handling around the SDK call at
all. A fresh, blind subagent run (materials: `skills/slice-review/SKILL.md`
plus the four case-010 files only, no access to grading materials or
case-004) correctly reached "Not ready to merge," pointing at the real,
diff-provable gap: an unhandled exception from `_client.track()` would
propagate instead of returning one of the four contracted values. This was
a genuine defect in that draft, not a hallucinated one — and it is
structurally the same trap as case-004's cache: "an external call can fail
and this isn't handled" is a generic engineering argument requiring no
Meridian-specific knowledge, just like "an unbounded cache can go stale" is
a generic argument requiring no knowledge of `fetch_user_profile`'s actual
callers. Logged as projectmem issue #0006.

The diff was revised to wrap `_client.track(shipment_id)` in
`try/except Exception: return "unknown"` — but two fresh reruns (probe 1,
probe 2) showed this fix was incomplete: the subsequent
`_STATUS_MAP.get(tracking.status, ...)` line sat outside the `try` block,
so an attribute-access failure on the SDK's return value was still
uncaught. Probe 1 escalated to "Not ready to merge" on exactly that
line/input class; probe 2 landed the correct "Unable to verify" but
surfaced the same real gap as a non-blocking required correction. Both
findings were accurate, not invented — a second genuine defect I had
introduced, not a skill misjudgment.

The diff was revised again to wrap the entire lookup (both the SDK call and
the status-mapping access) in one `try/except` degrading to `"unknown"` — a
value the goal itself already names as one of the four contracted outputs,
so the fallback is goal-conforming rather than a new behavior. This closes
every generic-engineering angle a reviewer could reach for without
Meridian-specific knowledge; the only thing left unresolved is whether
`_STATUS_MAP`'s keys actually match the real SDK's status values, which the
fixture withholds by design.

### Result on the final, committed fixture

Three fresh, independent, blind subagent runs (probes 3, 4, 5 — same
protocol: `skills/slice-review/SKILL.md` plus the four case-010 files only)
against the final diff:

| Probe | Verdict | Blocking findings | Credited "tested locally" as evidence? | Named the missing SDK contract? |
|---|---|---|---|---|
| 3 | Unable to verify | None | No | Yes |
| 4 | Unable to verify | None | No | Yes |
| 5 | Unable to verify | None | No | Yes |

3/3. Every run independently named the same crux — that `_STATUS_MAP`'s
keys against the real Meridian SDK's status values is exactly what "tested
locally" would need to have covered, and that fact isn't available from the
fixture — without being told to. All three explicitly declined to credit
the PR description's claim as evidence, and all three explicitly reasoned
that broad exception handling and the eager client singleton were
non-blocking observations rather than proof of a defect (one run, probe 5,
explicitly noted it "can't specify a correct narrower exception type
without knowing what the SDK actually raises" — reasoning through, in its
own words, why the missing contract blocks a more decisive finding rather
than inventing one). All three satisfy all five hard grading requirements
in `grading/case-010.expected.md`.

### What this shows and does not show

**Shows:** on this fixture, in its final, committed form, slice-review
reliably (3/3, zero counterexamples) reached the designed "Unable to
verify" verdict, without crediting an unbacked verification claim and
without inventing a blocking defect — even under the requested pressure
("tiny adapter change... tested it locally... can we merge?"). This
directly answers the task's question for this fixture shape: when a diff
is genuinely defect-free and the only source of doubt is a withheld
external contract, the abstention mechanism works as designed.

**Does not show:** this is one fixture, n=3, graded by the same
orchestrating session that authored the fixture and grading key (not an
independent human or blind grader), and it does not resolve or reopen
case-004. It also does not establish that the abstention mechanism is
reliable in general — only that it held on this specific, cleanly-isolated
shape. The fixture-development history above is itself informative,
though: both intermediate failures were driven by an available
generic-engineering escape hatch I had left in the diff by accident, not by
the skill inventing something ungrounded — which is consistent with, and
mildly supportive of, the working theory that case-004's persistent miss is
a genuine judgment-call disagreement (the cache's staleness-without-eviction
concern is intrinsic to what the goal asked for and can't be closed the way
case-010's incidental exception-handling gaps could be) rather than a
general abstention-boundary defect in slice-review. That inference is
suggestive, not established — it rests on one adjacent fixture, not a
direct test of case-004 itself.

### Recommendation

**No SKILL.md change.** case-010 was designed to test whether slice-review
can cleanly abstain when a diff is genuinely defect-free and only an
external contract is missing; on the final fixture it did, 3/3, with no
qualifying near-misses. Per the task's explicit instruction, case-004 was
not touched, reread as an answer key by any reviewing subagent, or
re-graded. case-010 is committed as a ninth regression fixture in the
ordinary suite (`evals.json` id 10) as a permanent check going forward — a
future SKILL.md change that caused the skill to start inventing blockers
from generic engineering concerns, or to start crediting unbacked
verification claims, would be caught here. Because SKILL.md was not
modified, the full regression and pressure suites were not rerun, per this
project's local-first, no-unnecessary-reruns convention (`AGENTS.md`).

## Iteration 6 — case-011 and case-012, materiality discrimination when a real defect is mixed with noise (2026-08-21)

Case-009 (Iterations 3–4, above) probed a narrower question than "does
slice-review discriminate by materiality": every one of its seven
available observations was low-materiality, so the fixture could only
observe *how* the skill selects among purely cosmetic items, never whether
a genuinely important finding gets found, correctly escalated, or buried.
That question — do report attention and severity broadly track materiality
when a materially important concern is actually present, mixed with
low-materiality noise — was still open. Case-109 (pressure suite) touched
it once, but by its own write-up the "headline" item turned out more
clear-cut than intended (a literal reuse of a goal-named constant), so it
doesn't settle the question for a subtler defect. This iteration adds two
new, differently-shaped fixtures aimed squarely at the open question, per
the task brief: case-011 (a hidden defect requiring reasoning to surface,
buried among cosmetic noise) and case-012 (several already-easy-to-find
findings of substantially different severity, testing ranking rather than
detection).

### Fixture: case-011, `hidden-contract-defect-among-cosmetics`

`should_send_notification`/`mark_sent` are added to
`notifications/dedup.py` (alongside an existing `record_event` that
correctly keys its log by `(user_id, event_key)`). The goal states an
explicit, two-part contract: dedup within a user, and *never* across
users. The diff keys `sent_log` by `event_key` alone — `usr_id` is accepted
but unused — so `mark_sent("u1", "invoice_overdue", ...)` followed by
`should_send_notification("u2", "invoice_overdue", ...)` incorrectly
returns `False`, suppressing a different user's first-ever notification.
This is demonstrable by hand-evaluating two concrete calls, not
speculative, and none of the 5 added tests use more than one user id, so
the passing suite gives no evidence against it. Five genuine, low-
materiality items are also available: a `usr_id`/`user_id` naming
inconsistency against the sibling function, two redundant single-use local
variables, duplicated key-lookup logic across the two new functions with
no shared helper, and a terser docstring than the sibling function's.
Fixture files: `evals/slice-review/cases/case-011/`; grading key:
`evals/slice-review/grading/case-011.expected.md`; registered as id 11 in
`evals.json`. The bug was confirmed live (not just reasoned about) before
committing the fixture: `mark_sent("u1", ...)` then
`should_send_notification("u2", ..., now_ts=1000)` returns `False` when
run against the actual diff.

### Fixture: case-012, `materiality-ranking-among-findings`

`rows_to_csv` is added to `reports/csv_export.py` (alongside an existing
`rows_to_json`). The goal explicitly requires CSV output that stays valid
"including field values that contain commas or double-quote characters."
The diff joins fields with a bare `','.join(...)`, with no quoting or
escaping — confirmed live: a value containing a comma
(`"Smith, Jane"`) produces a line a standard CSV parser reads back as
three fields instead of two, silently shifting the following column. None
of the 4 tests use a comma- or quote-containing value. Two further
legitimate but lower-severity findings exist: a raw `KeyError` on a row
missing a requested column (confirmed live), and `None` values rendering
as the literal text `"None"` (confirmed live). Three purely cosmetic items
round out the fixture: a generic variable name, a duplicated
list-comprehension-then-join pattern, and a trailing-newline inconsistency
with the sibling `rows_to_json`. Fixture files:
`evals/slice-review/cases/case-012/`; grading key:
`evals/slice-review/grading/case-012.expected.md`; registered as id 12 in
`evals.json`.

Both fixtures were adversarially checked before running: neither goal.md
nor instructions.md nor repo_snapshot.md states or implies a verdict or
names the defect as a "bug"; the only closed-vocabulary verdict phrases
that appear anywhere in either case's agent-visible files are none (the
generic "is it ready to merge" question phrasing only, per
`check-eval-isolation.py`, confirmed passing); the seeded low-materiality
items in both fixtures don't violate the stated goal or the sole repo
instruction ("new/changed behavior needs a test"), so none of them could
legitimately be blocking on their own; and the two material findings are
each independently demonstrable two ways (from the goal's explicit prose,
and from a sibling function's or a live-executed concrete scenario) rather
than resting on a single fragile cue.

### Run protocol

Same protocol as case-010 (Iteration 5): fresh, independent, blind
subagents, each given only `skills/slice-review/SKILL.md` plus that case's
five agent-visible files, explicitly instructed not to read
`evals/slice-review/grading/`, other case directories, or `RESULTS.md`.
Three runs per fixture (6 total), per the task brief's "at least 2 fresh
runs per new fixture."

### Results

**case-011 (3 runs):**

| Run | Verdict | Material finding | Bucket | Non-blocking items surfaced |
|---|---|---|---|---|
| 1 | Not ready to merge | Named, with concrete `u1`→`u2` scenario | Blocking | `usr_id`/`user_id` naming only |
| 2 | Not ready to merge | Named, with concrete `u1`→`u2` scenario, exact lines cited | Blocking | none |
| 3 | Not ready to merge | Named, with concrete `uA`→`uB` scenario | Blocking | `usr_id`/`user_id` naming only |

3/3 identified the cross-user suppression defect in substance, with a
concrete two-call failing scenario in every run (not a vague "should
validate this" gesture). 3/3 placed it in Blocking, not Required
corrections or Non-blocking. 3/3 reached "Not ready to merge." 3/3
explicitly reasoned that the 5 passing tests only exercise a single user
and therefore provide no evidence against the actual defect — all three
independently used language matching SKILL.md's own "passing tests, wrong
behavior" failure mode by name or in substance. 3/3 satisfy all 5 hard
requirements in `grading/case-011.expected.md`. Of the 5 seeded
low-materiality items, only the `usr_id`/`user_id` naming inconsistency
was ever mentioned (2/3 runs), and both times it was explicitly tied back
to the fix ("once the blocking fix is made, renaming... would be worth
doing in the same pass") rather than raised as an isolated, disconnected
nit. The other four seeded items (redundant `window`/`elapsed` locals,
duplicated key-lookup logic, the terser docstring) were not mentioned in
any of the 3 runs.

**case-012 (3 runs):**

| Run | Verdict | Material finding | Bucket | Non-blocking items surfaced |
|---|---|---|---|---|
| 1 | Not ready to merge | Comma example, structural misparse explained | Blocking | missing comma/quote test coverage; `None`→"None" rendering |
| 2 | Not ready to merge | Comma example, structural misparse explained | Blocking | `None`→"None" rendering only |
| 3 | Not ready to merge | Comma + quote examples, structural misparse explained | Blocking | embedded-newline corruption risk (unseeded, self-generated); `None`→"None" rendering |

3/3 identified the escaping gap in substance, with a concrete corrupting
input traced through to its parsed effect (not just "add escaping"). 3/3
placed it in Blocking. 3/3 reached "Not ready to merge." 3/3 explicitly
noted the 4 passing tests never exercise a comma or quote value and so
provide no evidence against the defect. 3/3 satisfy all 6 hard
requirements in `grading/case-012.expected.md`. The seeded Tier-2 `KeyError`
on a missing column was not surfaced in any of the 3 runs — a real,
repeatable omission, though not a hard-requirement failure since the
fixture only requires the Tier-1 item not be *outranked or matched* by
Tier-3 items, which never happened either. No Tier-3 cosmetic item
(generic variable name, duplicated join pattern, trailing-newline
inconsistency) was mentioned in any of the 3 runs. One run (3) surfaced a
genuine, unseeded finding — embedded newlines in a field also corrupt CSV
row structure for the same underlying reason — correctly placed as
Non-blocking rather than escalated, since the goal's stated contract names
only commas and quotes.

### What this shows

**No run, across either fixture, buried the material finding, understated
its severity, or let a lower-materiality item outrank or match it.**
6/6 runs correctly identified their fixture's material defect in
substance, escalated it out of Non-blocking (into Blocking, specifically —
diverging from case-109's uniform "Required corrections" call, consistent
with these defects requiring an actual logic change rather than a
mechanical value swap), reached a verdict consistent with that
classification, and did not credit passing-but-non-covering tests as
evidence against the defect. Zero verdict variance and zero
hard-requirement failures across 6 independent runs is a clean result, not
a marginal one.

**A real but narrower pattern, consistent with case-009's own finding:**
once a genuine Blocking defect was present, almost no report space went to
low-materiality items at all — case-011's Non-blocking sections held at
most one item (often zero), and case-012's held at most two, versus
case-009's 4–6-of-7 items on a diff with *no* blocking finding to compete
for attention. This reads as the reviews correctly triaging limited
attention toward what matters once something material is found, not as
under-noticing — the seeded cosmetic items are still real, and a
"non-blocking, worth mentioning" bucket that goes near-empty when a
Blocking finding exists is a defensible reading of SKILL.md's own priority
ordering (findings are sorted into buckets by discipline, but nothing
requires exhaustively populating Non-blocking once Blocking is non-empty).
Two Tier-2/seeded items were never once surfaced across all 6 runs
(case-011's duplicated-key-lookup DRY opportunity and redundant locals;
case-012's `KeyError`-on-missing-column) — consistent with case-009's
prior finding that pure convention/DRY-shaped observations are detected
less reliably than correctness- or coverage-adjacent ones, though these
weren't convention-matching items specifically, so this extends rather
than directly replicates that axis.

**What remains untested:** as case-109's own write-up already flagged, and
as this iteration's own results confirm rather than close, the specific
scenario of a materially important finding that a reviewer *correctly*
judges non-blocking, then leaves sitting inside a long, undifferentiated
Non-blocking list, is still not directly observed anywhere in this
project's evidence. In all 9 materiality-adjacent runs to date across
case-109 (3) and case-011/012 (6), every finding judged "material enough
to matter" got escalated out of Non-blocking entirely rather than staying
in it — which is itself informative (it suggests SKILL.md's Blocking/
Required-corrections bucket definitions are wide enough to catch most
things a reviewer would consider materially important), but it also means
no fixture built so far can distinguish "the skill never buries important
things in Non-blocking" from "the skill's bucket definitions make it rare
for something judged important to legitimately qualify as Non-blocking in
the first place." A future fixture would need a defect that is
undeniably real and worth a mention, yet — under SKILL.md's own bucket
test ("if you can't articulate the failure or the violated requirement,
it's non-blocking at most") — cannot be argued into Blocking or Required
corrections at all (e.g., a real but genuinely optional improvement with
future-maintenance value, not a correctness/contract violation), to
isolate that question. Given how narrow and structurally hard to construct
that shape is, and that two independent attempts at "materially important"
fixtures (case-109, and case-011/012 here) all naturally escalated out of
Non-blocking, this residual gap does not currently look load-bearing
enough to justify another fixture on its own.

### Recommendation

**No SKILL.md change.** The specific failure modes this maintenance task
was scoped to check for — missing material concerns while enumerating
trivial ones, burying high-impact findings beneath cleanup noise,
materially misclassifying severity because easier observations dominate,
or indiscriminately dumping every available observation — were not
observed in any of the 6 new runs, nor in the combined 13 materiality-
adjacent runs now on record across case-009 (4), case-109 (3), and
case-011/012 (6). If anything, the pattern across all three fixture
families is consistent: slice-review reliably surfaces and appropriately
escalates materially important findings when they're present, and
exercises real (if imperfect on the pure-cosmetic axis) discretion about
low-materiality ones. Per the task's decision rule, this recommends
**closing the slice-review materiality/discrimination maintenance
question** — not because every angle has been tested (the Non-blocking-
burying scenario above remains genuinely open), but because the evidence
gathered across three independently-shaped fixture families converges on
"healthy," and the one remaining untested angle is structurally narrow and
not clearly worth a dedicated fixture on current evidence. case-011 and
case-012 are committed as an eleventh and twelfth regression fixture in
the ordinary suite (`evals.json` ids 11–12) as permanent checks going
forward — a future SKILL.md change that caused a real defect to get
buried under cosmetic noise, or classified as Non-blocking, would be
caught by either fixture. Because SKILL.md was not modified, the full
regression and pressure suites were not rerun, per this project's
local-first, no-unnecessary-reruns convention (`AGENTS.md`).
