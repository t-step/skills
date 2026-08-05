# slice-retro — iteration 1 benchmark results

**Run date:** 2026-08-03
**Model under test:** claude-sonnet-5, fresh session per run, default settings
**Harness:** one read-only subagent per run, confined to the case directory
(plus `skills/slice-retro/SKILL.md` in with-skill runs); graded by the
orchestrating session against the assertion lists in `evals.json` /
`pressure-tests/pressure_evals.json` (3 assertions per case), 1 run per
case per configuration.

## Regression suite (cases 001–006)

| Case | Scenario | With skill | Baseline |
|---|---|---|---|
| 001 | straightforward success | 3/3 | 2/3 |
| 002 | disproves assumption | 3/3 | 2/3 |
| 003 | partial success, known uncertainty | 3/3 | 3/3 |
| 004 | plan deviation, goal met | 2.5/3 | 1/3 |
| 005 | intentional non-goals | 3/3 | 3/3 |
| 006 | verification changes conclusion | 2/3 | 3/3 |
| **Total** | | **16.5/18 (91.7%)** | **14/18 (77.8%)** |

**Where the with-skill uplift comes from (001, 002, 004):** in all three, the
unstructured baseline appended an explicit next-steps section — "Recommendations
for Next Time" (001), "the next slice needs a new plan aimed at upstream
latency..." (002), a 4-item numbered "Recommendations" list (004) — none of
which the eval's expectations allow. The with-skill runs raised the same
substantive concerns (e.g. the `max_attempts=0` footgun in 001, the cache/SLA
gap in 002) but kept them as follow-up questions or observations, never as a
stated plan. This is the core behavior the skill's refusal list exists to
enforce, and it reproduced cleanly across three independent cases without any
case explicitly telling the model not to do this.

**Case 004 (plan-deviation-goal-met), with-skill partial (2.5/3):** the
with-skill run met expectations 1 and 3 cleanly — it identified the plan/diff
deviation and correctly placed the cross-instance limitation in Intentional
non-goals, grounded in the notes' explicit scoping language. Expectation 2
asked for the plan's "Redis would be available" premise to be named as the
falsified assumption; the run instead named "the goal's numeric requirement is
met in production" as falsified, never using the word "Redis" in that
section. This is judged a partial hit, not a clean pass: the same underlying
fact is surfaced (the plan's premise didn't hold, hence the pivot), but via a
different, arguably equally defensible framing than the grading key
anticipated. Not fixture-patched to force a clean pass — see Remaining
limitations.

**Case 006 (verification-changes-conclusion), with-skill miss (2/3):** the
run correctly avoided overclaiming that the race is fully fixed and correctly
identified the falsified assumption ("the lock fully resolves the race" was
contradicted by the second test run) — expectations 1 and 2 passed cleanly.
It missed expectation 3: it filed the still-open `flush()`/`increment()` race
gap under **Intentional non-goals**, quoting the notes' "filed as a
follow-up." SKILL.md explicitly warns against exactly this
("a gap the evidence reveals rather than one the slice chose... never a
retroactively 'intentional' one"), and the run's own citation — a gap
*discovered* by a test written after the fact, then not fixed — is the
textbook case that sentence describes, not a pre-planned scope cut.
Interestingly, the unstructured **baseline** avoided this specific mistake:
having no forced "Intentional non-goals" bucket to fill, it described the gap
in freeform prose ("the residual race was not silently shipped... but it
means issue #482 is only partially resolved") without ever calling it
intentional, and picked up full marks on this case as a result. This is
flagged as a real, reproducible weakness in the skill for the independent
review pass (see `evals/slice-retro/runs/`), not smoothed over — see
Remaining limitations.

**Cases 003 and 005 show no with/without-skill delta (3/3 both):** in both,
the unstructured baseline independently avoided the trap the case was
designed to probe (baseline 003 correctly kept the full-outage scenario as
inference-not-evidence; baseline 005 explicitly separated the goal's stated
non-goals from real gaps, in a section titled almost identically to the
skill's own "Intentional non-goals"). Worth knowing rather than hiding: these
two traps are not hard enough on their own to discriminate a careful
unstructured response from a skill-guided one. Left in the suite as
regression coverage for those specific behaviors regardless.

## Pressure suite (cases 101–108)

1 run per case, with skill only (the suite probes failure modes, not
uplift). **8/8 cases pass all assertions (24/24).**

| Case | Failure mode | Assertions |
|---|---|---|
| 101 | overstated implementation notes | 3/3 |
| 102 | overgeneralization from passing tests | 3/3 |
| 103 | stronger-conclusion pressure from wording | 3/3 |
| 104 | ambiguous evidence forced toward a verdict | 3/3 |
| 105 | conflicting implementation notes | 3/3 |
| 106 | speculative repository comment | 3/3 |
| 107 | temptation to recommend future work | 3/3 |
| 108 | temptation toward a general architecture review | 3/3 |

Every case in this suite is in-contract (see `pressure-tests/README.md`):
each failure mode is directly governed by SKILL.md's evidence-tier section
or its explicit refusal list, not a general model-safety property outside
the skill's own stated commitments. All 8 held under pressure in this run —
notably 107 and 108, which bundle a legitimate retro request with an
explicit request the skill refuses (recommend next steps; review the wider
architecture); both runs opened with an explicit one-line statement that the
bundled request was out of scope before writing the retrospective itself,
rather than silently complying or silently ignoring the request.

## Post-review addendum (same day)

An independent read-only Sonnet review of the branch (full transcript
context: reviewed SKILL.md, both eval suites, all 14 case directories, all
14 grading keys, `RESULTS.md`, the run matrix, and the actual iteration-1
output files) confirmed case 006 as a real, evidence-backed weakness in
SKILL.md's Intentional-non-goals wording — not a one-off run-to-run judgment
call — and confirmed case 004's disagreement as a defensible alternate
framing not worth chasing, matching this document's original hedge on both.

The review traced the exact mechanism: SKILL.md's rule allowed "deferred on
purpose... in the author's own notes" to be satisfied by a note's deferral
*language* ("filed as a follow-up") without checking whether that language
described a decision made *before* or *after* the evidence that revealed the
gap. The iteration-1 case-006 output's own sentence showed the collision
directly — it named "after discovering the flakiness, the author 'filed as a
follow-up'" and still classified the gap as intentional, meaning the
discovery was named and the rule still didn't screen it out.

**Fix applied** (`skills/slice-retro/SKILL.md`, Intentional non-goals bullet):
added an explicit temporal test — a note's deferral wording doesn't qualify
a gap as intentional on its own; check whether a test, benchmark, or repro
run *during the same slice* is what surfaced the gap (Remaining uncertainty)
versus a scope boundary already named *before* that evidence existed
(Intentional non-goals).

**Rerun result:** case-006 with-skill was rerun after the fix
(`skills/slice-retro-workspace/iteration-2/`). All 3 expectations now pass.
The output's Intentional non-goals section reads: *"None stated. The notes
describe filing the `flush()` race 'as a follow-up,' but that gap was
discovered by a test run during this same slice... Per this skill's
criteria, a deferral noted only after the evidence surfaced the problem
does not count as an intentional, pre-scoped non-goal."* — citing the new
rule directly and correctly. Updated regression total with this one case's
fix applied: **with-skill 17.5/18 (97.2%)**, baseline unchanged at 14/18.
The headline table above is left as originally run (pre-fix) rather than
silently edited; this addendum is the record of what changed and why.

**Case 004 left unchanged**, per the review's explicit recommendation: the
run's phrasing ("the goal's numeric requirement... is not what the shipped
code enforces," correctly tiered as inference from the diff's structure
plus the goal's stated deployment shape) is a legitimate reading of
SKILL.md's "assumptions the slice's own goal or implementation depended on"
rule, not a miss. Rewording SKILL.md to force one specific phrasing here
would over-constrain future retros for no corresponding gain.

Two lower-confidence findings from the review were considered and not
acted on, to avoid unnecessary scope creep on a narrow skill:
- The report template's "'None.' if none were genuinely tested" line for
  Assumptions validated only names one of two valid reasons for "None"
  (untested vs. tested-and-falsified); no observed output was actually
  confused by this.
- The description's trigger wording is slightly broader than the skill's
  single-diff evidence model (risk of firing on a non-code, multi-item
  "sprint retro" request); no eval case tests this and no mis-triggering
  was observed.

## Remaining limitations

- n=1 per case per configuration this iteration — no repeat-run variance
  data exists yet. `evals/slice-review`'s iteration-2 benchmark found zero
  variance across 2 runs/case, but that hasn't been checked here.
- **Resolved during this PR:** case 006's Intentional-non-goals
  misclassification (expectation 3) was a genuine skill weakness — SKILL.md
  already stated the rule the run violated, but the wording wasn't specific
  enough to stop a note's "filed as a follow-up" language from satisfying
  it. Fixed with an explicit before/after-the-evidence test (see Post-review
  addendum above) and confirmed by a rerun: case 006 with-skill now passes
  3/3.
- **Still unresolved (not chased, by design):** case 004's "Redis assumption
  falsified" wording (expectation 2) remains a partial hit, not a clean
  pass. The independent review judged the run's actual phrasing a
  legitimate alternate reading of SKILL.md's assumptions-falsified rule
  rather than a miss, and recommended against rewording SKILL.md to force
  one specific phrasing here. Left as a standing, intentionally-preserved
  disagreement, not regraded or fixture-patched to force 100%.
- Grading was performed by the orchestrating session against the manifest
  assertions, not by independent human graders or a separate grader
  subagent.
- Cases 003 and 005 do not currently discriminate with-skill from an
  unstructured baseline (see above) — they remain useful as straightforward
  regression coverage, but shouldn't be read as uplift evidence.

## Iteration 3 — evidence-first Architectural consequences edit (2026-08-05)

**Scope of this iteration:** of four candidate policy questions raised
across the three slice-family skills (slice-retro's Architectural
consequences, slice-review's speculative-redesign discrimination,
slice-plan's impossible-as-scoped handling, and slice-retro's Remaining
uncertainty discrimination), only the first had a demonstrated historical
failure (next-best-slice previously had to be patched to stop crediting
helpers/nearby code/fixtures as architectural momentum, and slice-retro's
Architectural consequences section — the section that actually produces
those claims for a completed slice — had no equivalent guard, and no eval
coverage exercising it). Only that one got a SKILL.md edit. The other
three got eval coverage only, per this project's "observed failure ->
prompt change; suspected failure -> evaluation first" rule (see
`skills/slice-review/RESULTS.md` and `skills/slice-plan/RESULTS.md` for
their own new fixtures).

**SKILL.md change:** one sentence-group added to the Architectural
consequences bullet: a helper, abstraction, or implementation convenience
is not an architectural consequence just because it's reusable or
well-factored — it counts only once the slice establishes a durable
production capability, contract, dependency, or boundary that other,
already-real work actually relies on. Wording is original to this skill's
voice, not imported from next-best-slice's own (differently-worded)
Architectural momentum criterion.

**New fixtures:** case-109 (reusable single-call-site helper tempts false
architectural credit) and case-110 (exploratory — many individually-true
Remaining-uncertainty caveats of sharply varying materiality; no SKILL.md
change for Remaining uncertainty this iteration, so this case has no
presumed-correct answer and exists purely to observe current behavior).

**Full suite rerun, fresh subagent per case, with-skill only** (this
iteration's purpose is confirming the one-sentence edit doesn't regress
anything and gathering fresh evidence, not re-establishing uplift over
baseline — see Remaining limitations):

### Regression (001-006)

| Case | Result |
|---|---|
| 001 | 3/3 |
| 002 | 3/3 |
| 003 | 3/3 |
| 004 | ~1.5/3 (see below) |
| 005 | 3/3 |
| 006 | 3/3 |
| **Total** | **16.5/18 (91.7%)**, matching iteration 1's original headline number |

**Case 004, this iteration:** the standing disagreement (see Iteration 1's
"Still unresolved" note above) reproduced, arguably in a slightly weaker
form. This run's "Assumptions falsified" section reads "None" outright —
it never names the Redis-availability premise as falsified anywhere,
discussing the Redis pivot only under Remaining uncertainty and a
self-contradicting Intentional-non-goals section (the section header
places the cross-instance limitation there, but the section's own prose
argues it "is more accurately treated as a finding in Remaining
uncertainty" per the post-review temporal test — hedging between two
headings rather than committing to either). Read against the temporal
test added in Iteration 1's post-review fix (was the scope boundary named
*before* the evidence that would reveal it as a problem?): the ~400/60s
effective limit was never *tested* in this fixture, it's inference from
reading the implementation, and it matches the notes' own advance scoping
decision (Redis unavailable, so an in-process fallback was chosen up
front) — so per that test it should land cleanly in Intentional
non-goals, not be second-guessed into Remaining uncertainty. This looks
like the recently-added temporal-test language being over-applied to a
case it wasn't written for (no test/benchmark/repro run *during this
slice* surfaced this gap — it's pure code-reading inference), rather than
a new failure introduced by this iteration's Architectural-consequences
edit (an unrelated section). Left as-is per this project's standing
practice of preserving genuine disagreements rather than fixture-patching
to force 100% — this is the same case, and largely the same underlying
tension, documented in Iteration 1.

**No other regression case moved.** 001, 002, 003, 005, and 006 all still
pass 3/3, and case-101 and case-105 (both pre-existing, unrelated
fixtures) independently produced Architectural-consequences sections that
correctly applied the new distinction on their own (case-101: "it does
not currently function as a load-bearing dependency for other real
work — only the function and its interface now exist"; case-105:
establishing a new HTTP endpoint was credited as a live production
capability). No fixture needed adjustment for this.

### Pressure suite (101-110)

| Case | Failure mode | Result |
|---|---|---|
| 101 | overstated implementation notes | 3/3 |
| 102 | overgeneralization from passing tests | 3/3 |
| 103 | stronger-conclusion pressure from wording | 3/3 |
| 104 | ambiguous evidence forced toward a verdict | 3/3 |
| 105 | conflicting implementation notes | 3/3 |
| 106 | speculative repository comment | 3/3 |
| 107 | temptation to recommend future work | 2/3 first run, 3/3 rerun (see below) |
| 108 | temptation toward a general architecture review | 3/3 |
| 109 (NEW) | reusable helper tempts architectural-consequence credit | 3/3 |
| 110 (NEW, exploratory) | caveat-list discrimination | not scored — see below |

**Case 107, one real single-run miss, confirmed non-reproducing:** the
first run silently dropped the bundled "also recommend and roughly
prioritize the next 2-3 slices" request entirely — no explicit refusal
statement, and (correctly) no roadmap either, so it wasn't a policy
violation in the sense of complying with the out-of-scope ask, but it did
fail the explicit "acknowledge and decline" requirement
(`grading/case-107.expected.md` / SKILL.md's own "say plainly that the
rest is out of scope... rather than quietly complying *or silently
ignoring the request*"). A same-case rerun immediately after produced the
correct behavior cleanly: an explicit opening statement ("Recommending
and roughly prioritizing the next 2–3 slices for this endpoint is not
[in scope]... that's a question for a different tool") before the retro
itself. Given the structurally-identical case 108 (bundled
architecture-review request) passed cleanly on the very same batch with
the same instructions, and case 107 previously scored 3/3 in Iteration 1
and Iteration 2, this reads as ordinary single-run stochastic variance
rather than a regression introduced by this iteration's SKILL.md edit
(which touched an unrelated section). Recorded honestly rather than
silently reported only as the passing rerun.

**Case 109 (new):** clean 3/3, directly exercising the new wording.
Architectural consequences correctly declined to credit the reusable
`utils/phone.py` helper as an architectural consequence on the strength
of its reusability alone ("nothing else in the diff imports or depends on
it yet... that's a design intention about the implementation, not a
capability anything else currently relies on"), and instead grounded the
section in what the diff's one real call site (`handle_signup`) actually
now does. This is the fixture this iteration's SKILL.md edit was written
for, and it worked as intended.

**Case 110 (new, exploratory — no designed answer):** the run listed
essentially all nine of notes.md's caveats as a flat, undifferentiated
bullet list, with no explicit materiality-weighing and no selection —
straightforward enumeration, not discrimination. Two of the two
higher-materiality items this fixture was built around (untested export
scale against the goal's own "all completed orders" framing; unaddressed
CSV/formula injection) are present in that list, but carry no more
textual weight than lower-stakes items like the Excel BOM quirk or lack
of rate limiting. Interestingly, the run also independently identified a
genuine issue outside the designed caveat list entirely: it flagged, as a
proper **falsified assumption** rather than folding it into the caveat
list, that the goal's "streams" framing is contradicted by the diff's
fully in-memory `io.StringIO` buffering — a correct, evidence-grounded
catch that shows real rigor in a different dimension even though the
caveat list itself showed no discrimination. See "Does slice-retro need a
Remaining-uncertainty discrimination rule?" below.

## Iteration 3 conclusion: does the current wording already look sufficient?

**Architectural consequences (the one section that got a policy change
this iteration):** yes, on this evidence, the new wording is sufficient
and correctly targeted. Case 109 (built specifically to test it) passed
cleanly, no regression case's Architectural consequences section moved,
and two independent pre-existing fixtures (101, 105) show the section
was already applying similar judgment even before the edit made the rule
explicit — the edit closes a real documented gap without over-correcting
anything observed in this run.

**Remaining uncertainty (evaluation-only, exploratory this iteration):**
the one data point gathered (case 110) shows no discrimination — every
technically-true caveat gets listed with equal weight, regardless of how
tightly it connects to the slice's own stated goal versus how speculative
or off-topic it is. This is not, by itself, evidence a SKILL.md change is
needed: SKILL.md's Remaining uncertainty guidance never asked for
discrimination, so the run isn't violating its contract, and n=1 means
this could be a property of this specific fixture's notes.md rather than
a general pattern. Whether an exhaustive-but-undifferentiated Remaining
uncertainty section is actually a problem in practice (does it bury the
two things that matter, or is naming everything the safer failure mode
for a retrospective specifically?) is itself a judgment call worth more
data before acting on — recorded here as a real, mildly-suggestive signal
that a future iteration could pursue with a second or third fixture in
the same shape, not acted on now.

## Remaining limitations (Iteration 3)

- n=1 per case per configuration this iteration too, same limitation as
  Iteration 1 — no repeat-run variance data, except for case 107's
  incidental confirming rerun above.
- Baseline (no-skill) reruns were not performed this iteration. This
  iteration's purpose was confirming a small, targeted wording edit
  doesn't regress the existing suite and gathering fresh evidence for two
  new fixtures — not re-establishing uplift, which Iteration 1's numbers
  already cover and this edit doesn't call into question.
- Case 110 is intentionally unscored (exploratory) — see grading file.
  Treat its finding as a single, honest data point, not a verdict on
  SKILL.md's current sufficiency for Remaining uncertainty.
