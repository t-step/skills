# state-ownership-audit — eval results

**Run date:** 2026-08-29
**Model under test:** claude-sonnet-5, fresh `general-purpose` subagent per
run, default settings.
**Harness:** one subagent per run, instructed not to read anything outside
the case's own scratch directory; with-skill runs additionally received
`skills/state-ownership-audit/SKILL.md` and were told to read and follow it
exactly, including its report structure; baseline runs received the same
case files and the same one-line task framing, with no skill file and no
imposed report structure. Raw transcripts are local, untracked artifacts;
`runs/2026-08-29-iteration-1-runs.md` and the `grading/*.expected.md`
files are the committed, auditable record every claim below cites.

This is iteration 1: the skill's first eval suite, authored and run in the
same session as the skill's own design. See "What this proves / what this
does not prove" before treating any of this as strong validation.

## Numeric summary

- Regression suite (`evals.json`), with-skill: **26/26** expectations met
  across 6 cases, one run per case (first run; two expectations in case 1
  were reworded post-run to credit a real finding the run surfaced -- see
  "Fixture and grading-key findings" below; no case was re-run).
- Pressure suite (`pressure-tests/pressure_evals.json`), with-skill:
  **16/16** expectations met across 4 cases (first run; expectations in
  cases 102 and 104 were reworded post-run for the same reason -- see
  below).
- Baseline (no skill) runs were collected for all 6 regression cases, for
  contrast, not for pass/fail grading against the skill's own vocabulary
  and report structure. Baseline reached the correct substantive
  conclusion in all 6 -- see "What the baseline comparison shows."
- Baseline was not run against the pressure suite, matching this skill
  family's convention (see `pressure-tests/README.md`): that suite exists
  to probe where the skill's own stated contract could fail under
  pressure, not to benchmark uplift.
- **Two grading-key corrections were made after the first run**, both
  because a with-skill run legitimately exceeded what the original key
  anticipated, not because it was wrong. See "Fixture and grading-key
  findings" below. No case was re-run against the corrected keys; the
  original transcripts already satisfy them.

## Per-case results

### Regression suite

| Case | Scenario | With-skill | Baseline (no skill) |
|---|---|---|---|
| 001 | Clean invalidate-on-write cache; ticket proposes an unneeded reconciliation job | 5/5 (revised) | Reached the same conclusion, independently found the same repopulation race |
| 002 | Two apparent writers of a materialized total, one is reconciliation against the true append-only authority | 5/5 | Reached the same conclusion; also went further and proposed two specific fix designs the skill's contract would refuse to offer |
| 003 | Legitimate partitioned/sharded authority; proposal to collapse to one global authority | 4/4 | Reached the same conclusion with comparably strong, specific pushback |
| 004 | Asynchronous, event-driven projection with a documented, intentional staleness window | 4/4 | Reached the same conclusion, citing the same SLA figure |
| 005 | Genuine, uncoordinated second-writer hazard, confirmed by an incident | 4/4 | Reached the same diagnosis; also prescribed two named remediation designs the skill's contract would refuse to offer |
| 006 | README claims one authority; executable evidence establishes another | 4/4 | Reached the same conclusion via an equivalent claim-vs-code comparison |

### Pressure suite

| Case | Failure mode | With-skill |
|---|---|---|
| 101 | Aspirational design-note text mistaken for current authority | 4/4 -- reported unresolved, explicitly declined to treat the note's stated future intent as current fact |
| 102 | Two writers under transferable, lifecycle-scoped authority; is the guard real? | 4/4 (revised) -- found the guard is check-then-act, not atomic, and named the resulting TOCTOU race |
| 103 | Bundled "also design the coordinator" request under stated team-consensus pressure | 4/4 -- did the audit correctly, explicitly declined the build request |
| 104 | Two representations reading each other -- circularity vs. two one-way reads | 4/4 (revised) -- named the circular dependency and correctly flagged that the fixture's stubbed promo data leaves "confirmed vs. merely permitted" open |

## Fixture and grading-key findings

Three with-skill runs (cases 001, 102, and 104) surfaced real subtlety in
the fixtures that the original grading keys did not anticipate, in every
case in the direction of *more* epistemic care, not less. Rather than
alter the fixtures to erase these subtleties (which would have required a
rerun to re-validate), the grading keys were revised to credit the
higher-quality answer the runs actually gave, following this skill
family's established precedent for a first-iteration key that turns out to
be more rigid than the skill's own correct behavior (see
`evals/lifecycle-audit/RESULTS.md`'s "Eval-spec fix" section for the
precedent this follows).

- **Case 001** was designed as a clean, no-hazard invalidate-on-write
  cache. The run correctly identified that `update_price()`'s `UPDATE` and
  `r.delete()` are non-atomic, so a concurrent `get_price()` cache-miss
  read can repopulate the cache with a stale price *after* the delete has
  already run -- a real, narrow race the fixture actually contains,
  self-correcting only via the 300s TTL. The run reported this plainly,
  without recommending a new mechanism to fix it (correctly treating it as
  a design judgment call outside this audit's scope). The grading key was
  revised to require correct authority/derivation characterization and no
  invented fix, rather than "zero hazards found," which this fixture does
  not actually guarantee. Baseline independently found the same race,
  which is further evidence this is a real property of the fixture, not
  an artifact of the skill's own framing pushing the model toward finding
  something.
- **Case 102** was designed to test whether the skill checks for a guard
  before calling "two writers of one field" a hazard, with the guard
  intended to be airtight. As written, the guard is a `SELECT status`
  followed by a status-blind `UPDATE` -- check-then-act, not atomic -- so a
  stale-authority write genuinely can land after a transfer. The run
  found this precisely, which is exactly what the skill's own instruction
  to "check for a fencing or validity guard on every write path that could
  execute under a stale claim to authority" exists to catch. The grading
  key was revised to require reading and reporting on the guard logic
  (not flagging on field-name overlap alone) and to treat finding the
  TOCTOU gap as the correct, higher-quality answer, rather than requiring
  a flat "no hazard" conclusion the fixture's actual code doesn't support.
- **Case 104** was designed to show a definite circular-authority
  relationship. Because `_load_promo_for` (where a same-pair validation
  check would live) is deliberately stubbed out of the fixture as "not
  relevant to this audit," the evidence available doesn't actually confirm
  whether two products are ever configured to price-match each other --
  only that the code contains no guard preventing it. The run correctly
  reported this distinction: a real hazard the code permits, not a
  confirmed live occurrence. The grading key was revised to credit this
  more precise framing rather than expect an unqualified "there is a
  cycle" claim the stubbed data doesn't support.

None of these three required a code change to the fixtures and none
required a rerun -- in each case the original transcript already satisfies
the revised expectations. This differs from a defect fix: nothing here
indicates the skill reasoned incorrectly; the keys were calibrated to a
"clean" scenario slightly cleaner than what was actually written.

**Independent check on the revisions themselves.** Because the same
person authored the fixtures, the skill, and these three revisions, a
fresh, context-free subagent was asked to adversarially re-derive the
correct answer for each of the three fixtures from the code alone --
before reading the model's output or the current grading key -- and then
judge whether each revision was a legitimate recalibration or a quiet
weakening. Verdict on all three: **legitimate recalibration**, not
weakening -- the reviewer independently arrived at essentially the same
finding in each case before seeing the model's output, confirmed the
pre-existing REQUIRED bars were left intact (a wrong-authority or
invented-fix answer would still fail all three), and for case 001 noted
that the baseline (no-skill) run's independent discovery of the same race
is corroborating evidence the finding is a real fixture property, not an
artifact of one run's specific phrasing. The review did surface two
wording flaws, both fixed: case 102's expectation #3 had a self-
contradictory escape clause (rewritten to require the report state the
SELECT/UPDATE non-atomicity as a structural fact, regardless of whether it
labels the gap a "hazard"), and case 104's grading-key prose had a
muddled description of which product's promo depends on which product's
cached price (rewritten to name product A/B explicitly). Neither fix
changed any expectation's substance or required a rerun.

## What the baseline comparison shows

Every baseline run reached the same substantive conclusion as its
with-skill counterpart across all 6 regression cases, consistent with the
pattern already documented across this skill family (`lifecycle-audit`,
`domain-orientation`): a capable model with no skill and no imposed
structure often reaches sound engineering judgment on cases like these.
This suite's evidence does not show the skill producing conclusions a
strong baseline misses.

Where the with-skill runs differed, consistently:

- **Explicit report structure and evidence tiering.** Every with-skill run
  used the skill's exact section headings and tagged authority claims
  observed/inferred/unresolved/conflicting; baseline reports were
  well-organized prose without a reusable, checkable vocabulary.
- **Refusing to design the fix.** In cases 002 and 005, baseline went past
  diagnosis into prescribing specific remediation designs (a CAS update or
  row lock in case 002; a named choice between two remediation models in
  case 005). The skill's contract explicitly refuses this ("name the
  hazard; the remedy is a human design decision"), and every with-skill
  run stopped at the hazard. This is the clearest, most consistent
  difference this suite found -- not a different conclusion, but a
  different, deliberately narrower scope.
- **Declining bundled out-of-scope work under social pressure (case
  103, pressure suite only, no baseline counterpart).** The with-skill run
  performed the audit and explicitly declined to design the requested
  coordinator service despite the prompt's and Slack thread's repeated
  claims of team consensus. This case has no baseline analogue since it is
  part of the pressure suite.

Read plainly: this iteration's evidence suggests the skill's value is
less about reaching different substantive conclusions on these fixtures
and more about (a) forcing a checkable evidence-tiered structure and (b)
holding a scope boundary a capable, unguided model does not reliably hold
on its own -- refusing to design a fix once a hazard is found. That is a
real but more modest claim than "the skill finds things baseline misses,"
and the case-count here does not yet establish how consistently the
scope-discipline difference would replicate.

## What this proves / what this does not prove

**What it's suggestive of:** across 6 regression scenarios (clean
single-writer cache, reconciliation-not-a-hazard, partitioned authority,
safe async lag, a genuine hazard, and a docs/code conflict) and 4 pressure
scenarios (aspirational-doc-as-authority, guarded-vs-unguarded transfer,
bundled-request-under-social-pressure, and circular authority), the
with-skill runs consistently (a) correctly distinguished derived/cached
representations from independent authorities, including in the harder
reconciliation-is-not-a-second-writer case; (b) named the one confirmed,
incident-backed hazard as the centerpiece finding without diluting it or
proposing a fix; (c) preserved genuine uncertainty rather than resolving
it toward a tidier-sounding architecture, in both a documented-conflict
case (006) and a no-evidence-either-way case (101); (d) correctly named a
legitimately partitioned authority and pushed back on a proposal that
would have silently traded away its availability guarantee (003); (e)
checked guard logic rather than accepting a status check at face value,
finding a real TOCTOU gap when one existed (102); and (f) held its scope
boundary against direct, socially-framed pressure to design a
reconciliation mechanism (103).

**What it does not prove:** every case was run once per condition with one
model family and default settings -- this is not a statistically powered
benchmark, and any single case could look different on a repeat sample,
especially the two pressure cases that most depend on resisting a bundled
request (103) or preserving uncertainty under a plausible-sounding
distractor (101). All 10 fixtures are synthetic, single-author-constructed
systems in the 2-3-file range, written by the same person who wrote the
grading keys -- a known source of unintentional alignment between what a
fixture rewards and what `SKILL.md` happens to emphasize, and the same
person revising two grading keys after seeing the with-skill output (even
in the direction of crediting a stronger answer) is a similar bias to
disclose plainly rather than paper over. No case in this suite combines
more than two of the requested failure categories from the original design
brief at once; a fixture layering, say, partitioned authority together
with a documentation conflict was not constructed and might behave
differently. The skill has not yet been pressure-tested against a
real-world (non-synthetic) codebase, a materially larger fixture (more
than ~4 files or more than 2-3 facts in scope), or a model other than
claude-sonnet-5.

## Cases where the skill intentionally refused to determine ownership

Two cases in this suite specifically reward refusing to name a winner:

- **Case 006** (docs vs. code): the run named the README-vs-code conflict
  explicitly rather than silently overriding the README, even while
  correctly concluding the executable evidence favors `auth`. This is
  "Conflicting," not "Observed," in the skill's own vocabulary -- the
  disagreement is preserved in the report, not erased once a side is
  picked.
- **Case 101** (aspirational doc): the run reported current authority as
  genuinely unresolved and explicitly declined to treat a stale design
  note's stated future intent as settling the present question -- the
  correct answer here is "unknown," not a guess in either direction.
- **Case 104** (circular authority, after the key revision): the run
  declined to assign resolving authority to either Pricing or Promotions,
  and further declined to claim the cycle is confirmed to execute given
  that the promo-configuration data needed to confirm it is outside the
  evidence provided.

## Remaining weaknesses and open questions

- **Fixture scale.** Every fixture is small (2-4 files, 1-2 facts in
  scope). Whether the skill's "what earns a full entry" admission bar
  degrades gracefully on a fixture with many candidate facts -- avoiding
  both a schema-audit-style sprawl and under-selecting a real hazard
  buried among clean facts -- was not tested here.
- **No adversarial pressure on the evidence-tier vocabulary itself.**
  `lifecycle-audit`'s own iteration 1 found and fixed a real internal
  contradiction in its mechanism/consistency wording under close reading
  of one case's own output. This suite's cases did not surface an
  equivalent contradiction in `state-ownership-audit`'s vocabulary, but
  the absence of a finding is not strong evidence of its absence --  a
  case specifically designed to stress the "authority scope" vocabulary
  (e.g., a fact that is simultaneously scoped *and* transferable, or where
  the partition dimension itself is ambiguous) was not constructed.
- **Baseline was not sampled on the pressure suite at all**, per this
  family's convention that the pressure suite isn't a benchmarking
  exercise -- but this means there is no direct evidence of whether an
  unguided baseline would also resist the case-103 social-pressure request
  or correctly preserve case-101's uncertainty. `lifecycle-audit`'s own
  pressure case did sample baseline and found it also resisted a
  comparable request; this suite did not check whether that pattern holds
  here.
- **The grading-key revisions were made by the same person who designed
  both the fixtures and the skill.** A fresh, independent subagent review
  was run against this specific concern (see "Fixture and grading-key
  findings" above) and found all three revisions legitimate, fixing two
  wording flaws in the process. That review was itself a single pass by
  one subagent instance, not a second independently-recruited human --
  worth another look if this skill sees material use.
- **No test of a fact with three or more representations**, or of a fact
  spanning more than two components with genuinely different write
  authority for different sub-parts of what looks like one row (the "one
  store, several facts" case named in `SKILL.md`'s "Unit of analysis"
  section) -- both are named as scenarios the skill should handle but
  neither was directly exercised by a fixture.
