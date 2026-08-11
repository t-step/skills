# next-best-product-slice — iteration 1 benchmark results

**Run date:** 2026-08-08 (initial suite); case 003 follow-up fix and
re-verification 2026-08-10, documented inline below rather than as a
separate iteration since it's a single-case wording fix, not a new pass
over the whole suite.
**Model under test:** claude-sonnet-5, fresh subagent per run, default settings
**Harness:** one read-only subagent per run, confined to the case directory
plus `skills/next-best-product-slice/SKILL.md`, blind to
`evals/next-best-product-slice/grading/`, `pressure-tests/`, and
`evals.json`. Graded by the orchestrating session against the assertion
lists in `evals.json` / `pressure-tests/pressure_evals.json`, 1 run per case.

This is the first iteration for this skill: 15 cases (4 regression,
11 pressure), built and run in the same pass per the accepted minimal-slice
plan. No with/without-skill baseline was run this iteration — the
divergence experiments (below) already established the skill's behavior
differs meaningfully from `next-best-slice`'s; this suite's job is
regression coverage and pressure-testing the new skill's own stated
contract, matching how `next-best-slice`'s own iteration 1 scoped its
first pass.

## Divergence experiments (pre-implementation gate)

Before writing `SKILL.md`, three fixtures were built to test whether
`next-best-slice` already covers product-value selection well enough that
a separate skill wouldn't be justified:

- **Fixture 1** (automation-rules visibility, explicit "core capability"
  framing): unmodified `next-best-slice` already picked the product-value
  candidate, using its strategic-continuity lens. No divergence — this
  fixture showed the boundary where the existing skill already succeeds.
- **Fixture 2** (technician schedule-change indicator, non-elevated
  framing, friction-reduction-vs-recovery-gap shape): unmodified
  `next-best-slice` picked the architecturally-leveraged candidate
  (`AvailabilityEngine`-based technician suggestion) over the evidenced,
  non-core product candidate. Real divergence, confirmed clean against the
  product-vs-reliability boundary (no violated contract, no incorrect
  behavior anywhere in the fixture).
- **Fixture 3** (Thicket landscaping, single strong architectural slice
  with no multi-slice tunneling chain): unmodified `next-best-slice` again
  picked the architectural continuation, explicitly because its
  anti-tunneling guard didn't trigger with only one prior same-subsystem
  slice — a second, structurally distinct confirmation of the same gap.

Both `next-best-product-slice` and `next-best-slice` were then run against
fixtures 1 and 2: on fixture 1 both skills agreed (visibility page); on
fixture 2 they diverged as predicted — `next-best-product-slice` picked
the technician-visibility indicator, explicitly reasoning that
friction-reduction on an already-functioning workflow is its weakest
signal and doesn't by default outrank a comparably-evidenced recovery gap,
even when the friction-reduction candidate is architecturally cheaper.
This is the direct empirical basis for building the skill. Fixtures live
in `next-best-product-slice-workspace/divergence-experiment/` (not
committed to `evals/`, per the instruction to keep eval suites physically
independent of the pre-implementation experiments).

## Regression suite (cases 001–004)

| Case | Scenario | Result |
|---|---|---|
| 001 | workflow completion vs. architectural continuation | 3/3 |
| 002 | clean single candidate (baseline sanity) | 3/3 |
| 003 | capability exists, no surface, zero recent-slice evidence | 3/3 (see follow-up below) |
| 004 | genuine tiebreak on size/reversibility | 3/3 |
| **Total** | | **12/12 (100%)** |

**Case 003 follow-up (post-iteration-1 fix):** iteration 1 scored this case
2.5/3 -- correct recommendation, correct grounding, correctly did not treat
the missing review/retro/backlog as blocking, but never explicitly stated
that no review, retro, or backlog exists for this repository. Flagged in
the original write-up (below, preserved) as a candidate wording addition
contingent on a second run reproducing the same gap, per this repository's
evidence-first convention.

A second independent run against the unmodified iteration-1 `SKILL.md`
reproduced the identical gap -- correct pick, correct reasoning, no mention
anywhere in the report that no review/retro/backlog exists. Two-for-two on
the same specific omission met the stated bar, so a fix was attempted:

1. **First attempt** -- appended a sentence to "Gather before recommending"
   step 4 ("its absence is not grounds to stop... When it's absent, say so
   plainly..."). A third independent run against this version *still* did
   not name the absence anywhere in its report. The instruction lived in
   the gather/reasoning phase; the model correctly internalized "don't
   treat this as blocking" but the "say so" clause didn't survive into the
   written report. Recorded as a failed fix attempt, not discarded
   silently.
2. **Second attempt** -- instead added the instruction directly to the
   Report template's "Why this clears the evidence bar" field: "If no
   review, retro, or backlog exists for this repository, say so explicitly
   in this section, and that the recommendation doesn't depend on one
   existing." A fourth independent run against this version explicitly
   stated: "No review, retro, or backlog exists in this repository -- the
   case materials say so directly. This recommendation doesn't depend on
   one..." -- closing the gap.

This matches the pattern already visible in `next-best-slice`'s own design
(a reasoning instruction alone under-specifies what must appear in the
*written report*; the instruction needs to be anchored at the point of
generation, not just the point of gathering). The original miss, the
reproduction, the failed first fix, and the working second fix are all
recorded here rather than only keeping the final state, per this
repository's evidence-first convention of not silently overwriting a
disconfirmed attempt. `next-best-slice` was not read for this fix beyond
the one confirmatory grep already cited in iteration 1 (its "When
recent-slice evidence is missing" section, step 4) and was not modified.

<details>
<summary>Original iteration-1 write-up (preserved for record)</summary>

Case 003, partial (2.5/3): the run correctly recommended exposing
`ReportScheduler.subscribe()` to team leads, correctly grounded the pick in
demonstrated intent and the capability's real, production-verified
existence, and correctly did not treat the missing review/retro/backlog as
blocking. It never explicitly stated that no review, retro, or backlog
exists for this repository, though — it simply proceeded straight to
product-state reasoning without naming the absence. `SKILL.md`'s "Gather
before recommending" section states recent-slice evidence's absence "is
not grounds to stop," but doesn't explicitly instruct naming the absence
the way `next-best-slice`'s own missing-evidence handling does. This is a
real, reproducible gap in the eval's literal expectation, not a
fabrication or a wrong pick — flagged per this repository's convention of
recording a partial honestly rather than inflating the score, and named
below as a candidate wording addition if a second run reproduces it.

</details>

## Pressure suite (cases 101–111)

1 run per case, with skill only (per this suite's own stated purpose —
probing failure modes, not uplift). **11/11 cases pass all assertions
(33/33).**

| Case | Failure mode | Assertions |
|---|---|---|
| 101 | discoverability under direct pressure | 3/3 |
| 102 | existing capability vs. speculative feature | 3/3 |
| 103 | stored info not surfaced vs. cosmetic polish | 3/3 |
| 104 | state-transition legibility vs. weak refactor | 3/3 |
| 105 | demonstrated intent vs. invented persona | 3/3 |
| 106 | bug vs. genuine product slice (boundary case) | 3/3 |
| 107 | technical work with concrete connection vs. vague cleanup (boundary case) | 3/3 |
| 108 | backend/algorithmic value vs. superficial UI | 3/3 |
| 109 | insufficient product evidence | 3/3 |
| 110 | genuine product-candidate tie | 3/3 |
| 111 | roadmap/list request | 3/3 |

Notable runs:

- **101 and 103** (the two fixtures redesigned mid-build after the
  product-vs-reliability audit) both passed cleanly, and both runs
  explicitly kept the underlying capability described as already
  correct/working — 101's run stated the reopen mechanism "already works
  correctly today," 103's run stated the change was "display-only" reading
  "a value ops already computes correctly." Neither run framed its pick as
  fixing something broken, confirming the redesigns closed the
  contamination risk they were built to close.
- **106 and 107**, the two deliberate bug/cleanup-vs-product boundary
  cases, both passed with unusually explicit reasoning: 106's run
  proactively separated the unrelated email-duplication bug from the
  product pick, marking it "should be tracked on its own" rather than
  silently folding it in or dropping it; 107's run proactively named the
  ambiguity itself ("this could be read as 'just a bug fix'... the fix and
  the product improvement are the same change here") before correctly
  applying `SKILL.md`'s stated exception. This is the strongest evidence in
  this iteration that the skill's classification discipline is legible and
  applied deliberately, not just landing on the right answer by luck.
- **108** confidently recommended the backend/algorithmic fix (token-based
  search matching) without any hedging for it being a non-UI change,
  cleanly declining the cosmetic decoy for having zero evidence trace —
  the direct test of "product value isn't a layer."
- **110** produced a more elegant answer than the grading key's suggested
  example: instead of simply asking the 8 ticket-filers which channel they
  prefer, it proposed a forward-looking preference-capture field at an
  existing touchpoint, which resolves the same open fact for all future
  buyers, not just the 8 who already complained. Graded as a full pass —
  the assertions require naming the tie and recommending a bounded
  evidence-producing step, not a specific mechanism.

## Remaining limitations

- n=1 per case this iteration — no repeat-run variance data exists yet,
  consistent with every other skill in this family's own first-iteration
  benchmark.
- No with/without-skill baseline comparison was run — the divergence
  experiments already demonstrate the skill's behavior differs from
  `next-best-slice` on real fixtures; a baseline-vs-skill comparison on
  this suite's own cases would be a reasonable follow-up but wasn't part
  of the accepted minimal slice.
- Case 003's wording gap was resolved post-iteration-1 (see the case 003
  follow-up above) after a second run reproduced it. Only one `SKILL.md`
  change resulted from this iteration's evals; the first fix attempt was
  tried, found ineffective on a fresh run, and replaced rather than kept
  alongside the working one.
- Cases 001, 002, and 004 were each re-run once against the patched
  `SKILL.md` to confirm the fix caused no regression (the new Report-
  template clause is conditional on no review/retro/backlog existing, so
  it shouldn't fire for these three, which all have one -- but this was
  verified rather than assumed). All three reproduced their iteration-1
  results: 001 recommended recipient-visible validation errors over the
  date-range field, explicitly weighing and setting aside its dependency-
  unlocking evidence; 002 recommended the billing-admin invoice download,
  declining items 2/3 for no usage signal; 004 recommended the status
  badge over the timeline page on the same size/no-new-route tiebreak,
  naming item 2 as a genuine close call. Regression suite is 12/12 (100%)
  post-fix, all four cases re-verified against the current `SKILL.md`.
- Grading was performed by the orchestrating session against the manifest
  assertions, not by an independent grader subagent or human reviewer —
  consistent with `next-best-slice`'s own iteration-1 first pass, which
  later added an independent review; the same could be done here in a
  follow-up iteration.

## Repository checks

`bash scripts/check.sh` passes: `check-skill-frontmatter` (6 skill files,
strict YAML clean, including the new skill), `check-eval-isolation` (111
case dirs across 6 skills, no leakage), `check-skill-deps` (6 skill files,
0 local dependency edges — `next-best-product-slice` declares no
cross-skill dependency, consistent with this repository's established
convention), and the `skill-usage-report` test suite. No changes were made
to any check script; all three auto-discover `skills/*/SKILL.md` and
`evals/*/` and required no modification to pick up the new skill and suite.

## Net result

15/15 cases built and run; all 15 pass all expectations after the case 003
follow-up fix (see above): 12/12 regression, 33/33 pressure, 45/45 overall.
Case 003's original 2.5/3 was a real, reproduced gap (2/2 runs against the
unmodified iteration-1 `SKILL.md` omitted the same explicit statement), not
a fabrication or a wrong pick, and it was closed only after reproduction --
not patched off a single suspected miss. The fix itself took two attempts:
a first edit to the gather-phase prose was verified and found ineffective
before being replaced by a second edit anchored in the Report template,
which verified successfully. Cases 001, 002, and 004 were re-verified
against the patched `SKILL.md` with no regression. No fixture was weakened
or patched to force a pass, and the two fixtures redesigned during the
pre-run audit (101, 103) were rebuilt from scratch around clean product-
capability-gap shapes before this suite ran, not adjusted afterward to fix
a failing grade. `next-best-slice` was not modified at any point in this
work.
