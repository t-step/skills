# stale-framing-audit — eval results

**Run date:** 2026-08-29
**Model under test:** claude-sonnet-5, fresh `general-purpose` subagent per
run, default settings.
**Harness:** one subagent per run, instructed not to read anything outside
the case's own scratch directory; with-skill runs additionally received
`skills/stale-framing-audit/SKILL.md` and were told to read and follow it
exactly, including its report structure; baseline runs received the same
case files and the same one-line task framing, with no skill file and no
imposed report structure. Raw transcripts are local, untracked artifacts;
`runs/2026-08-29-iteration-1-runs.md` and the `grading/*.expected.md`
files are the committed, auditable record every claim below cites.

This is iteration 1: the skill's first eval suite, authored and run in the
same session as the skill's own design. See "What this proves / what this
does not prove" before treating any of this as strong validation.

## Numeric summary

- Regression suite (`evals.json`), with-skill: **21/21** expectations met
  across 5 cases, one run per case.
- Pressure suite (`pressure-tests/pressure_evals.json`), with-skill: on
  the first pass against the skill as originally written, **15/20**
  expectations met across 5 cases (101: 4/4, 102: 3/4 against the
  original key, 103: 4/4, 104: 4/4, 105: 0/4 -- failed its REQUIRED bar
  outright). Two distinct corrections followed: case 102's grading key was
  revised to accept an equally-defensible characterization the original
  key hadn't anticipated (102: 4/4 against the revised key -- see "Fixture
  and grading-key findings"); case 105 exposed a real, in-contract skill
  defect that was fixed directly in `SKILL.md` and re-run against the
  fixed skill (105: 4/4 on re-run -- see "Skill defect found and fixed").
  Against the current `SKILL.md` and the current grading keys, the suite
  now stands at **20/20**, achieved via one skill fix plus one key
  revision, not a clean first pass -- the distinction matters more here
  than the final number.
- Baseline (no-skill) runs were collected for all 5 regression cases, for
  contrast, not for pass/fail grading against the skill's own vocabulary
  and report structure. Baseline reached the correct substantive
  conclusion in all 5 -- see "What the baseline comparison shows."
- Baseline was not run against the pressure suite, matching this skill
  family's convention (`pressure-tests/README.md`): that suite exists to
  probe where the skill's own stated contract could fail under pressure,
  not to benchmark uplift.

## Per-case results

### Regression suite

| Case | Scenario | With-skill | Baseline (no skill) |
|---|---|---|---|
| 001 | Completed migration; README still describes the retired Redis queue and instructs enqueueing into it | 5/5 | Reached the same conclusion via a claim/reality table |
| 002 | True statement ("Coordinator manages worker state") implies write authority the Coordinator doesn't have | 4/4 | Reached the same conclusion; went further than the skill's contract allows (three additional fix-flavored recommendations) |
| 003 | README's own stated scope omits the component that now actually owns admin-action gating | 4/4 | Reached the same conclusion, more prescriptively than the skill's contract allows |
| 004 | Stale agent instructions (Tier-1 reach) describing a migration tool the repo no longer uses | 4/4 | Reached the same conclusion; included a fully drafted replacement AGENTS.md section the skill's contract would refuse to produce |
| 005 | Two properly marked historical ADRs (must not be flagged) alongside an unmarked, currently-broken setup doc (must be flagged) | 4/4 | Reached the same conclusion; included a complete rewritten setup.md the skill's contract would refuse to produce |

### Pressure suite

| Case | Failure mode | With-skill |
|---|---|---|
| 101 | Newer, unwired experimental code sits beside older, accurate docs | 4/4 -- explicitly checked reachability, explicitly invoked the "be cautious with recency" discipline, did not flag the docs |
| 102 | Active migration, two live paths, no declared canonical side, under a request to pick one to delete | 4/4 (revised key; see below) -- refused to pick a side, correctly framed as an active migration, refused the deletion request; used a different characterization tag than the original key expected |
| 103 | Misleading but deliberately preserved public-API naming | 4/4 -- no rename recommended; concluded there was no finding at all, since the compatibility reason is already documented at the point of contact |
| 104 | A doc's individually-plausible claims contradict a shared code path only when checked exhaustively, not sampled | 4/4 -- checked all three functions and the Overview framing, not just the one claim that happened to remain true |
| 105 | Executable code disagrees with a spec's invariant, but the code carries its own signal it's an unreviewed gap | **0/4 on first run** (skill defect; see below) → 4/4 on re-run against the fixed skill |

## Skill defect found and fixed

Case 105 was built to test this skill's "Framing vs. a code defect"
section: `admin_override_panel.force_cancel()` bypasses
`order_spec.md`'s stated invariant, but its own TODO comment admits it
"bypasses OrderService's refund-eligibility checks entirely" and "needs
review before this is safe to leave enabled in prod," it has no test
coverage, and no other surface corroborates it as sanctioned. The correct
answer is that the code, not the spec, is the likely defect.

The first with-skill run correctly *identified* all of that evidence --
the TODO, the missing tests, the lack of corroboration -- but then still
concluded "yes, order_spec.md is currently out of date" and characterized
the spec as Contradicted. This is precisely the failure mode the case
exists to catch: the run did the evidence-gathering the skill asked for,
but the skill's original wording only listed checks to run under
"Framing vs. a code defect" without stating what to conclude when those
checks point toward the code being the defect, so the run defaulted back
to "code disagrees with doc, therefore doc is stale."

This was judged an in-contract skill defect (the section's own stated
purpose was to prevent exactly this outcome), not a fixture or
grading-key problem, so `SKILL.md` was edited directly, per this
repository's `AGENTS.md` ("An observed failure justifies a skill
change"). The "Framing vs. a code defect" section was rewritten to
require resolving to exactly one of three explicit outcomes -- code looks
intentional and corroborated (proceed with the ordinary characterization);
code looks like the likely defect (no stale-framing characterization at
all, name the code-side risk as out of scope instead); or the checks
don't settle it (Ambiguous) -- instead of only listing checks without a
stated resolution. The refusal list was also updated to name this exact
pattern explicitly.

Case 105 was re-run against the fixed skill and passed 4/4: the report's
Findings section reads "None identified," it explicitly states
`order_spec.md` "gets no stale-framing characterization here (not
Contradicted, not Superseded, not Ambiguous)," and it directly answers the
support engineer that the spec is not out of date and `force_cancel` is
the likely defect. This is a genuine before/after fix verified by a
second run, not an assumed one.

## Fixture and grading-key findings

One with-skill run (case 102) surfaced a real, legitimate precision
question the original grading key hadn't anticipated, in the direction of
*more* epistemic care, not less -- following this skill family's
established precedent for revising a first-iteration key that turns out to
be more rigid than the skill's own correct behavior (see
`evals/state-ownership-audit/RESULTS.md`'s "Fixture and grading-key
findings" section for the precedent this follows, and
`evals/lifecycle-audit/RESULTS.md` for the earlier instance of it).

**Case 102** was designed so the correct answer is "genuinely unresolved
which document is canonical, don't pick a side." The run reached that
substantive conclusion -- it refused to declare either document stale, it
named the situation as an active migration with no declared canonical
side (grounded in `billing_router.py`'s dispatch logic and open,
undated ticket), and it explicitly refused the prompt's direct request to
pick one document as "the stale one" to delete. But it characterized both
findings as "Misleading emphasis or missing qualifier" rather than the
"Ambiguous" tag the original key required, reasoning that the
*architecture* is not actually unresolved (the router settles that
definitively) -- what's wrong is each document's absolutist phrasing
overclaiming completeness for its own tenant slice. On reflection this is
at least as defensible a reading as the key's original expectation, and
arguably more precise: "Ambiguous" would suggest the underlying system
state is unknown, when it isn't; the actual defect is emphasis, which is a
category `SKILL.md` already names for exactly this shape of problem. The
key was revised (`grading/case-102.expected.md`) to accept either tag,
while keeping the three behavioral REQUIRED bars -- refusing to pick a
side, naming the active migration, refusing the deletion request -- as the
real test this case exists to run. No case in this suite was re-run
against the case-102 revision (the original transcript already satisfies
the revised key), which is the same discipline the precedent used.

**Independent check on this revision.** Because the same person authored
the fixture, the skill, and this revision, a fresh, context-free subagent
was asked to adversarially re-derive the correct answer for case 102 from
the code and both documents alone -- no grading key, no `SKILL.md`, no
prior model output -- and to characterize each document independently
rather than assume they need the same tag. It confirmed
`billing_router.py` shows a genuine dual-live-path system with no
canonical side, and confirmed deleting either document (the prompt's
request) isn't supported by the evidence. It also went further than the
revised key expected: it did **not** converge on one characterization for
both documents. It read `billing_docs.md` as misleading primarily through
*omission* (silent about `NewBillingAdapter`'s already-live status) and
`billing_v2_notes.md` as misleading primarily through *emphasis* (true for
v2 tenants, but its unqualified "This is what Billing does" overclaims
universality) -- independently reproducing the same asymmetry an external
review of this iteration flagged by inspection alone (see "External
review findings" below). `grading/case-102.expected.md` was updated again
to note this asymmetric characterization as an accepted, stronger answer,
without retroactively failing the original with-skill transcript, which
used one tag for both and remains a passing, if less precise, answer under
the three REQUIRED bars. Full transcript record in
`runs/2026-08-29-iteration-1-runs.md`, "Independent check on the case-102
grading-key revision."

**A note on how this section originally read.** The first version of this
paragraph asserted the check above had already been run and reported a
"Verdict: legitimate recalibration, not weakening" -- without the check
having actually been performed, and with no transcript or artifact
anywhere in this repository backing that claim. An external review of
this iteration caught this (see "External review findings" below): the
claim existed only as prose, in direct tension with this file's own
opening statement that `runs.md` and the grading files are "the
committed, auditable record every claim below cites." That was a real
evidence-discipline failure -- corrected here by actually running the
check and citing its real, traceable output above, not by softening the
sentence around an unbacked assertion.

## External review findings

A fresh, context-free subagent was separately asked to adversarially
review `SKILL.md` and this eval suite -- not a fork of the authoring
session, no shared context, explicitly instructed to verify claims rather
than trust this file's own summary. It found two must-fix problems, three
worth-considering refinements, and two nitpicks, and confirmed several
things as sound. All are addressed below; nothing found was ignored or
argued away.

**Must-fix, both corrected:**

1. This file's "Numeric summary" stated the pressure suite's first-pass
   score as "16/20" while giving a per-case breakdown (4+3+4+4+0) that
   sums to 15, not 16 -- a plain arithmetic error inside the sentence that
   was supposed to total it. Corrected to 15/20.
2. The "Independent check on this revision" claim above was made without
   the check having actually been run -- see the note directly above this
   section. Corrected by actually running the check.

**Worth-considering, addressed:**

3. `SKILL.md`'s Report template used an "observed / inferred / unresolved"
   evidence-tiering vocabulary in its "Current evidence" field without
   ever defining those terms in the body, unlike every sibling skill
   reviewed (`repo-orientation`, `domain-orientation`, `lifecycle-audit`,
   `state-ownership-audit`), each of which has a dedicated tier-definition
   section with worked examples. Fixed: added a "Three tiers" section to
   `SKILL.md`, positioned after "Gather before judging anything," matching
   the family convention.
4. Case 102's grading key forced one uniform characterization tag onto two
   documents whose actual wording isn't symmetric under the skill's own
   taxonomy -- see the independent check above, which reproduced this
   exact asymmetry unprompted. Addressed by adding the asymmetric reading
   as an accepted, more-precise (not required) answer in
   `grading/case-102.expected.md`, without retroactively failing the
   original transcript.
5. "Contradicted" and "Superseded, undated" overlap in `SKILL.md` without
   a stated rule for choosing between them -- confirmed by
   `grading/case-001.expected.md`'s own admission that either tag is
   defensible for that case. Fixed: added an explicit disambiguating rule
   (Superseded requires positive evidence the statement was once true;
   absent that, default to Contradicted; when evidence doesn't
   distinguish the two, say both are defensible rather than forcing a
   choice) to `SKILL.md`'s "Characterize each finding" section.

**Nitpicks, addressed:**

6. Case 105's `order_service.py` docstring asserted "Fully tested" -- an
   unverifiable claim used as corroborating evidence, in mild tension with
   this skill's own discipline that comments are claims to check, not
   facts to accept. The reviewer confirmed this doesn't change the case's
   correct answer (`force_cancel()`'s own TODO, missing tests, and lack of
   corroboration are independently sufficient). Softened the docstring
   wording to remove the flat "Fully tested" assertion.
7. `SKILL.md`'s Report template ended its Findings section with a bare
   `None identified.` instead of the family's consistent `"None
   identified." if none.` phrasing. Fixed for consistency.

**Checked by the reviewer and found sound, unchanged:** `scripts/check.sh`
passes cleanly; the expectation counts in `evals.json` (21) and
`pressure_evals.json` (20) match this file's final totals; the "Framing
vs. a code defect" rewrite was read adversarially and found to actually
close the loophole it was patched for, including for fixture shapes
weaker than case 105's explicit TODO; the "How this composes" claims about
sibling skills' scope were verified accurate against those skills' actual
files; the Report template's six characterization tags match the body
exactly; this file's epistemic hedging was found honest by this repo's own
standard, with no misuse of "proves"/"confirms"; and the reach-tiering
guidance was found concrete and not obviously gameable in either
direction.

## What the baseline comparison shows

Every baseline run reached the same substantive conclusion as its
with-skill counterpart across all 5 regression cases, consistent with the
pattern already documented across this skill family
(`state-ownership-audit`, `lifecycle-audit`, `domain-orientation`): a
capable model with no skill and no imposed structure often reaches sound
engineering judgment on cases like these.

Where the with-skill runs differed, consistently:

- **Explicit report structure and characterization vocabulary.** Every
  with-skill run used the skill's exact section headings and one of the
  six named characterizations (Contradicted / Superseded / Aspirational /
  Misleading emphasis / Omission / Ambiguous); baseline reports were
  well-organized prose without a reusable, checkable vocabulary for *why*
  something is stale, not just that it is.
- **Refusing to write the fix.** In cases 002, 004, and 005, baseline went
  past diagnosis into drafting replacement documentation -- a full
  rewritten AGENTS.md section (004), a complete corrected setup.md (005),
  and a numbered implementation-recommendation list beyond what was asked
  (002/003). The skill's contract explicitly refuses this ("name the
  finding and the smallest corrective action... an actual edit is a
  separate, downstream action"), and every with-skill run stopped at
  naming the correction, never drafting it. This is the most consistent
  difference this suite found, matching the same pattern
  `state-ownership-audit`'s RESULTS.md documented for "refusing to design
  the fix."
- **Explicit restraint on properly marked history (case 005).** Both
  conditions correctly left the two ADRs alone, but only the with-skill
  run's report structure forces an affirmative "Historical material
  reviewed and not flagged" statement rather than silent omission --
  baseline's restraint on this point is real but undocumented as a
  deliberate check.

Read plainly: this iteration's evidence suggests the skill's value on the
regression suite is less about reaching different substantive conclusions
on these fixtures and more about (a) forcing a checkable
characterization vocabulary and reach-based ranking, and (b) holding a
scope boundary (diagnose, don't rewrite) a capable, unguided model does
not reliably hold on its own. The pressure suite is where a *different*
kind of value showed up: case 105 demonstrates the skill's own contract,
as first written, was not yet sufficient to prevent a real reasoning
failure -- which the eval process caught and fixed, rather than something
this suite can claim the skill already guaranteed against.

## What this proves / what this does not prove

**What it's suggestive of:** across 5 regression scenarios (completed
migration, misleading-but-true emphasis, omission against a doc's own
stated scope, stale Tier-1 agent instructions, and marked-history-vs-
unmarked-staleness) and 5 pressure scenarios (recency/reachability trap,
active-migration-preserve-ambiguity, compatibility-naming-no-rename,
cumulative-individually-plausible-statements, and framing-vs-code-defect),
the with-skill runs, after one fix, consistently (a) distinguished
Contradicted from Misleading-emphasis from Omission rather than
collapsing every finding into "this is wrong"; (b) explicitly and
affirmatively cleared properly marked historical material rather than
treating age as a proxy for staleness; (c) refused to treat a more
recently touched file as more authoritative than an older, accurate
surface; (d) refused a direct, explicit request to pick a side in a
genuinely unresolved active migration; (e) refused to recommend a rename
for a demonstrably confusing but deliberately compatibility-preserved
public name; (f) checked every claim a short document made against the
code rather than sampling one and generalizing; and (g), after the case-105
fix, correctly declined to characterize a spec as stale when the
disagreeing code carried its own evidence of being an unreviewed defect.

**What it does not prove:** every case was run once per condition (twice
for case 105, before and after the fix) with one model family and default
settings -- this is not a statistically powered benchmark, and any single
case could look different on a repeat sample. The case-105 failure is
direct evidence the skill's first-draft wording was insufficient on at
least one dimension; the fact that a fix produced a passing re-run on the
same fixture is encouraging but is a single confirming data point, not
proof the fix generalizes to other framing-vs-code-defect shapes (a
different kind of self-acknowledged gap, a case with weaker or more
ambiguous signals than an explicit TODO, or a case where the code-side
signal is more equivocal). All 10 fixtures are synthetic, single-author-
constructed systems in the 2-6-file range, written by the same person who
wrote the grading keys and the skill itself -- a known source of
unintentional alignment between what a fixture rewards and what
`SKILL.md` happens to emphasize. The independent-subagent check on the
case-102 revision mitigates but does not eliminate this concern, and no
equivalent independent check was run on the case-105 fix beyond the
single confirming re-run. The skill has not been tested against a
real-world (non-synthetic) repository, a fixture larger than ~6 files, a
target with more than roughly two framing findings in play at once, or a
model other than claude-sonnet-5.

## Cases where the skill intentionally preserved ambiguity or historical framing

- **Case 005** (marked history): both ADRs were explicitly reviewed and
  left alone, stated affirmatively rather than by silent omission -- the
  clearest positive instance in the regression suite of not equating old
  with wrong.
- **Case 101** (recency trap): the newer, unwired experimental module was
  correctly not treated as more authoritative than the older, accurate
  README, and its recent modification timestamp was explicitly named as
  non-decisive.
- **Case 102** (active migration): both documents were left as legitimate,
  narrowly-true descriptions of a genuinely dual-path system; the run
  refused a direct request to pick one as canonical.
- **Case 103** (compatibility naming): the misleading-but-intentional
  `/v1/customer` name was left unrenamed, with the audit concluding no
  finding was warranted at all once the compatibility documentation was
  checked.
- **Case 105** (post-fix): the spec's invariant was left standing as the
  correct, intended model; the disagreeing code was named as the likely
  defect and explicitly routed out of this skill's scope rather than used
  to reframe the spec as stale.

## Remaining weaknesses and open questions

- **Only one framing-vs-code-defect fixture was built, and it failed on
  first contact.** The fix that resulted is verified against exactly this
  one fixture. A case with a weaker signal that the code is the defect
  (no TODO, just untested-and-unwired, or a genuinely 50/50 case where
  reasonable readers could land either way) was not constructed and might
  still produce the pre-fix failure mode in a subtler form.
- **Fixture scale.** Every fixture is small (2-8 files, 1-3 candidate
  findings). Whether the reach-based ranking and "compact set of
  consequential findings" discipline degrade gracefully on a target with
  many candidate stale statements at mixed reach tiers -- avoiding both a
  documentation-linter-style sprawl and under-selecting the one
  high-leverage finding -- was not tested here.
- **No fixture combining two failure modes at once** (e.g., an active
  migration where one side is also individually misleading in emphasis,
  or a compatibility-naming case that is also an omission). Every fixture
  in this suite isolates one failure mode cleanly; a repository in
  practice will mix them.
- **The grading-key revision and the skill fix were both made by the same
  person who designed the fixtures and the skill.** An independent
  subagent review was run against the case-102 revision specifically and
  found it legitimate; no equivalent independent review was run against
  the case-105 skill-defect fix beyond the confirming re-run. Worth
  another look if this skill sees material use.
- **No test against a real, non-synthetic repository.** Every fixture
  here is a small, deliberately constructed system. Real repositories
  carry more surfaces, more history, and messier evidence than any of
  these ten cases -- whether the reach-ranking and evidence-gathering
  discipline hold up at that scale is untested.
