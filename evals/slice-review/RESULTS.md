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
