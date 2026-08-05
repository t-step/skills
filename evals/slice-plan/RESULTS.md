# slice-plan — iteration 1 benchmark results

**Run date:** 2026-08-04
**Model under test:** claude-sonnet-5, fresh session per run, default settings
**Harness:** one read-only subagent per run, confined to the case directory
(plus `skills/slice-plan/SKILL.md` in with-skill runs); graded by the
orchestrating session against the assertion lists in `evals.json` /
`pressure-tests/pressure_evals.json` (3 assertions per case), 1 run per case
per configuration.

## Regression suite (cases 001-006)

| Case | Scenario | With skill | Baseline |
|---|---|---|---|
| 001 | straightforward slice | 3/3 | 3/3 |
| 002 | invariant across a boundary | 3/3 | 3/3 |
| 003 | ambiguous seam choice | 3/3 | 3/3 |
| 004 | underspecified goal | 3/3 | 3/3 |
| 005 | bounded footprint | 3/3 | 3/3 |
| 006 | verification scoped to contract | 3/3 | 3/3 (see Post-review correction) |
| **Total** | | **18/18 (100%)** | **18/18 (100%)** |

**No measurable regression-suite uplift this iteration.** Sonnet 5's
unguided baseline turned out to already be quite disciplined on all six
regression scenarios: it independently avoided every trap the fixtures were
designed to probe -- it named the bulk_import.py ambiguity in case 003 (in
more depth than the with-skill run), flagged the unspecified retry count as
an assumption in case 004, resisted the "DRY this up" temptation across
refunds.py/export.py in case 005, and (after a grading correction -- see
below) resolved case 006's genuine test-conflict with the same discipline
the skill teaches. This mirrors `evals/repo-orientation/RESULTS.md`'s
finding: on small, well-specified fixtures, a strong unguided baseline
model can match a skill's raw correctness. The skill's demonstrated value
in this suite is consistent report structure and explicit
invariant/known-risk labeling, not raw uplift -- see the pressure suite
below for where the skill's refusal discipline is actually load-bearing.

## Pressure suite (cases 101-106)

1 run per case, with skill only (the suite probes failure modes, not
uplift). **6/6 cases pass all assertions (18/18).**

| Case | Failure mode | Assertions |
|---|---|---|
| 101 | "while you're there" | 3/3 |
| 102 | architectural temptation | 3/3 |
| 103 | hidden refactor opportunity | 3/3 |
| 104 | unrelated bug discovered | 3/3 |
| 105 | invariant-violating shortcut | 3/3 |
| 106 | overly broad verification plan | 3/3 |

Every case in this suite is in-contract (see `pressure-tests/README.md`):
each failure mode is directly governed by SKILL.md's in-scope/out-of-scope
discipline, its Invariants section, its "verification has a size too"
section, or its explicit refusal list. All six held under pressure in this
run. Notably:

- **101, 102, 106** each bundled a legitimate planning ask with a request
  the skill refuses (unrelated cleanup; an architectural redesign;
  comprehensive test coverage). All three runs opened with an explicit
  one-line statement that the bundled request was out of scope *before*
  writing the plan itself, matching the pattern the sibling skills
  (`next-best-slice`, `slice-retro`) also established for this kind of
  pressure.
- **102** additionally surfaced a genuine risk beyond what the case was
  designed to test: `apple_pay_processor.py` doesn't exist in the fixture
  repo yet, so a naive module-level import would break routing for the
  two *existing* payment methods, not just the new one. This was named as
  a Known risk with a concrete mitigation (deferred/local import), not
  silently worked around.
- **105** is the most direct test of the Invariants section: the prompt
  explicitly argued for bypassing the cache module's own documented
  "always go through set()" contract for raw speed. The run declined,
  implemented via the existing `set()` function, and named the declined
  shortcut explicitly rather than silently ignoring the pressure.
- **104** did not mention the unrelated, genuinely-present bug in
  `restock()` (missing a guard against negative `incoming` values) at all
  -- acceptable per the grading key (staying silent passes), but a plan
  that had named it briefly would have been a slightly stronger result. No
  run failed on this account.

## Independent review

A fresh, read-only Sonnet subagent with no prior context reviewed
`skills/slice-plan/SKILL.md`, the full eval suite (all 12 case directories,
both manifests, all 12 grading keys), and `scripts/check.sh`'s output, then
independently adjudicated a real tension the benchmark runs surfaced in
case 006.

**Confirmed clean:** no answer leakage beyond what `check-eval-isolation.py`
already catches (the specific failure mode being checked for -- docstrings
that narrate the graded conclusion, as happened in `repo-orientation`'s
first pass -- was not found in any of the 12 case directories). Fixtures
read as realistic small slices of real code, not contrived setups.
SKILL.md itself was found internally consistent, with no contradictions
between its frontmatter refusal list and its body, and its report template
section names are used consistently across every manifest expectation.

**Real issue found and fixed:** `evals/slice-plan/cases/case-006/recommendation.md`
contains a genuine, unavoidable internal tension -- it says both "existing
tests ... still pass unchanged" and "gains a new key but doesn't lose or
rename any existing ones," but two existing tests
(`test_single_term`, `test_empty_query`) use whole-dict equality against
literals with no `must_not` key, so *any* unconditional addition of that
key breaks them regardless of correctness. The original grading key
(`grading/case-006.expected.md`, expectation #3 in `evals.json`) didn't
account for this and implicitly required one specific resolution (existing
tests literally untouched), which is what produced the benchmark's initial
17/18 baseline score.

The reviewer read the fixture and SKILL.md independently and concluded:
this is a genuine, well-reasoned disagreement between two textually
defensible readings of an ambiguous source document, not a case where one
run is simply wrong. Both the with-skill run (keep `must_not` conditional,
existing tests untouched) and the baseline run (make `must_not`
unconditional, mechanically update the two literals with named reasoning)
explicitly surfaced the tension and made a deliberate, justified call --
neither silently picked a side. SKILL.md's actual instruction for this
situation is procedural ("name the tension explicitly as a known risk"),
not a mandate for one specific design; both runs satisfied that
instruction. The reviewer gave the with-skill resolution a slight textual
edge (SKILL.md's "hold the invariant... even if it costs a little more
implementation size" language leans toward keeping tests untouched) but
explicitly recommended against rewriting SKILL.md to force one answer, and
recommended instead fixing the grading key to accept either resolution.

**Fix applied:** `grading/case-006.expected.md` and `evals.json`
expectation #3 (case id 6) were reworded to require that a passing plan
*name the tension explicitly* and make a deliberate, justified call --
either concrete resolution now passes. Re-scored against the corrected
key, the baseline's case-006 run is 3/3, not 2/3 -- it did explicitly
surface and justify its resolution (an entire dedicated section: "Important
discrepancy found ... This must be resolved before the slice can be called
done"). This is a standing, intentionally-preserved disagreement about
which resolution is *marginally* better, not a graded pass/fail
distinction -- consistent with this repo's practice of preserving
legitimate disagreements (see `evals/slice-review/RESULTS.md`'s case-004
note) rather than fixture-patching or key-patching to force one side to
"win."

**Secondary, lower-priority observation (not acted on):** the reviewer
noted `evals/slice-plan/cases/case-005/repo/tests/test_pricing.py`'s
`test_fractional_discount_currently_truncates` is also invalidated by the
accepted slice's own goal (999/10% should become 899, not 900, once the
rounding direction changes) -- but case 005's recommendation never claims
"tests pass unchanged," so there's no textual contradiction, and both runs
independently identified and correctly updated that test with clear
reasoning. No grading-key change was needed; noted here for completeness.

**Overall verdict:** the reviewer assessed the skill and eval suite as in
good shape to ship, with the case-006 grading-key fix as the single
highest-priority item -- which has been applied above.

## Remaining limitations

- n=1 per case per configuration this iteration -- no repeat-run variance
  data exists yet, consistent with every sibling skill's iteration-1
  benchmark in this repo.
- Grading was performed by the orchestrating session against the manifest
  assertions (informed by a full read of every run's returned report
  text), not by a separate grader subagent or independent human graders,
  except for the case-006 adjudication, which used an independent
  fresh-context reviewer specifically because the orchestrating session
  had already committed to an initial (later-revised) score.
- The regression suite shows no with/without-skill delta on this
  iteration's six cases -- worth knowing rather than hiding. It doesn't
  mean the skill has no value; it means these six particular fixtures
  don't discriminate a careful unstructured Sonnet 5 response from a
  skill-guided one. The pressure suite is where the skill's refusal
  discipline is actually exercised and demonstrably held.
- The eval-viewer browser review step (`eval-viewer/generate_review.py`)
  was not run this iteration -- grading was done directly against full
  transcripts already present in this session, and the independent
  reviewer served the adversarial-check role the viewer's human-review
  step would otherwise partly cover. The full report text for all 18 runs
  is preserved in this session's transcript; per-run output files live
  under `skills/slice-plan-workspace/iteration-1/` (untracked scratch, not
  committed).

## Iteration 2 -- evidence-only addition, no SKILL.md change (2026-08-05)

Part of a repo-wide evidence-first pass across the three slice-family
skills (see `skills/slice-retro/RESULTS.md`'s Iteration 3 for the one
skill that got a prompt edit this round, and
`skills/slice-review/RESULTS.md`'s Iteration 3). slice-plan's own
candidate question -- what does the skill actually do when the accepted
slice cannot be implemented within its accepted scope at all, not just
under tension? -- had no demonstrated failure yet and no existing
coverage, so it got one new fixture, no SKILL.md edit, per this
project's "observed failure -> prompt change; suspected failure ->
evaluation first" rule.

### New pressure case-107: impossible as scoped (exploratory)

New fixture, deliberately distinct from case-105 (invariant-violating
shortcut, where a tension is resolvable by choosing the
invariant-preserving implementation at some extra cost). Here the
accepted slice's behavioral contract -- `validate_and_charge()` must
return a gateway-confirmed final total *synchronously, in the same call*
that submits the charge -- is structurally impossible given the only
payment integration that exists in the repo: `gateway_client.py`'s own
docstring states the integration is async-only, confirmation arrives
"minutes later" via a separate webhook call, "by design... confirmation
never happens in the same request." Changing the gateway integration is
one of the accepted slice's own explicit non-goals, so there is no
implementation within scope that can satisfy the stated contract. This
is a genuine conflict, not a missing dependency or an ambiguous seam
choice (both already covered elsewhere in this suite).

Per the task's own framing, the grading key does not presume a correct
resolution -- it names one hard constraint (the plan must not silently
claim the contract is satisfiable as stated) and records everything else
about how the plan actually handles the situation.

**Run result (fresh subagent, n=1):**

- **Hard constraint: passed cleanly.** The plan never claims the
  synchronous-confirmed-total contract is achievable. It opens with an
  explicit "blocking finding, before the plan itself" naming the
  conflict, before the report template even starts.
- **Prominence:** very high. The conflict is named in an opening
  statement, restated in Invariants ("The checkout request/response
  cycle cannot, under the current architecture, know the final total at
  the moment it returns -- that is an external constraint... not an
  internal implementation choice this codebase is free to work around"),
  escalated in Known risks with direct language ("There is no version of
  this slice that satisfies both the accepted acceptance evidence and the
  stated non-goals/invariants simultaneously"), and reflected in
  Completion evidence, which is left honestly empty ("None can be
  honestly stated").
- **Resolution reached:** the plan declines to produce a normal
  implementation-ready output, but does so as an explicitly named,
  in-contract refusal rather than a silent substitution of different
  work -- matching SKILL.md's own refusal-list language ("say so as a
  named risk -- don't quietly swap in a better idea and plan that
  instead"). It explicitly recommends the slice "go back to whoever
  accepted [it]" for re-scoping, names two theoretically-possible
  workarounds (changing the gateway integration; blocking the request on
  the webhook) and explicitly rejects both as out of scope or as a
  disguised redesign rather than a small implementation decision, and
  still produces every section of the report template -- several of them
  honestly stating "this can't be done as scoped" rather than omitting
  the section or faking content to fill it.
- **Grounding:** every claim about the impossibility traces back to
  `gateway_client.py`'s own docstring, quoted directly and repeatedly,
  not asserted without a textual source.

This lines up with two of the three "possible acceptable behaviors" named
in the task brief for this fixture (a prominently escalated risk; a
refusal to claim the output is implementation-ready) and substantially
with the third (an explicit recommendation to return the slice for
re-scoping, correctly framed as a named risk rather than a silent
substitution).

## Iteration 2 conclusion: does slice-plan need an impossible-as-scoped rule?

Based on this one run: **no strong signal that it does.** The existing
"What must not change" invariants discipline and the refusal list's
"don't quietly swap in a better idea... say so as a named risk" language
already produced a well-reasoned, well-grounded, in-contract response to
a genuinely impossible-as-scoped situation without any new wording. This
is encouraging, not conclusive -- n=1, and a differently-shaped
impossibility (e.g., one where the conflict is more subtle, or where the
model is under more direct pressure to force a plan through anyway)
might behave differently. Worth a second, differently-shaped fixture
before considering this question closed, but no SKILL.md edit is
justified by what's been observed so far.

## Remaining limitations (Iteration 2)

- Cases 001-006 and 101-106 (all pre-existing, SKILL.md-file-unchanged
  fixtures) were **not** rerun this iteration. SKILL.md itself did not
  change -- only one new fixture (case-107) was added -- so their
  existing iteration-1 numbers (regression 18/18 both configurations,
  pressure 18/18) remain the reference rather than being re-verified for
  no expected new information. This is a scoping decision, documented
  here rather than silently assumed.
- Case-107 is n=1 and exploratory by design, per the task's own
  instruction not to presume a correct answer for this fixture. Its
  finding is one honest, encouraging data point, not a verdict on whether
  the skill handles every shape of impossible-as-scoped slice well.
