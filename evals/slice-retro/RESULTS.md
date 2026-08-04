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
