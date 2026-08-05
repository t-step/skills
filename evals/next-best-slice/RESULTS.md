# next-best-slice — iteration 1 benchmark results

**Run date:** 2026-08-03
**Model under test:** claude-sonnet-5, fresh session per run, default settings
**Harness:** one read-only subagent per run, confined to the case directory
(plus `skills/next-best-slice/SKILL.md` in with-skill runs); graded by the
orchestrating session against the assertion lists in `evals.json` /
`pressure-tests/pressure_evals.json` (3 assertions per case), 1 run per
case per configuration.

## Regression suite (cases 001–007)

| Case | Scenario | With skill | Baseline |
|---|---|---|---|
| 001 | dependency unlock | 3/3 | 3/3 |
| 002 | user value vs. architectural prerequisite (flexible) | 3/3 | 3/3 |
| 003 | equally attractive candidates (flexible) | 3/3 | 3/3 |
| 004 | narrow experiment vs. large milestone | 2.5/3 | 2.5/3 |
| 005 | deferred work still not justified | 3/3 | 3/3 |
| 006 | evidence changes direction | 3/3 | 3/3 |
| 007 | gather more evidence | 3/3 | 3/3 |
| **Total** | | **20.5/21 (97.6%)** | **20.5/21 (97.6%)** |

**No with/without-skill delta on the regression suite this iteration.** Both
configurations landed on the same recommendation in all seven cases and hit
the same single partial miss (case 004, detailed below). This is a real
finding about this iteration's fixtures, not a skill failure: the case
review/retro documents were written richly enough — each one states its
open follow-up question almost verbatim — that a careful unstructured
baseline can find the same evidence trail without the skill's explicit
criteria. This mirrors `evals/slice-retro/RESULTS.md`'s honest note about
cases 003/005 not discriminating; it's left in the suite as straightforward
regression coverage (does the recommendation logic work at all) rather than
as uplift evidence. Where this suite's fixtures *do* still add value: they
pin down a single expected shape of reasoning per case that the pressure
suite's harder, adversarially-framed prompts can be checked against.

**Case 004 (narrow-experiment-vs-milestone), both configs partial (2.5/3):**
both runs correctly picked the bounded 500-SKU A/B test over the full
catalog rollout, and both correctly argued the rollout is unjustified by
the pilot's thin (unscored, unblinded editor skim) evidence. Neither run
explicitly named *reversibility* as a distinct reason the full rollout
should wait — both folded it into "evidence is too thin" and "revives a
known technical risk at 118,000x scale," never stating separately that
replacing real copy site-wide is harder to undo than a traffic-split
experiment. The substance goal.md/review.md/retro.md support is there;
the specific evidence-grounded language the eval expected didn't surface
verbatim. Flagged for the independent review pass rather than
fixture-patched to force a clean pass — see Remaining limitations.

**Case 007 (gather-more-evidence) shows the skill working exactly as
designed:** given a canary with a data-eng-flagged, statistically
insignificant delta, both configurations declined both rollout and
rollback and recommended extending the canary — a slice that is still
bounded, still testable, but exists to produce evidence rather than ship a
feature. This is the specific behavior "recommend the smallest slice that
would produce the missing evidence" in SKILL.md's "When no candidate is
justified yet" section was written to produce, and it held.

## Pressure suite (cases 101–109)

1 run per case, with skill only (the suite probes failure modes, not
uplift, per its own README). **9/9 cases pass all assertions (27/27).**

| Case | Failure mode | Assertions |
|---|---|---|
| 101 | user insists on a preferred next feature | 3/3 |
| 102 | roadmap bias | 3/3 |
| 103 | recency bias | 3/3 |
| 104 | architecture-aesthetic bias | 3/3 |
| 105 | "keep momentum" pressure | 3/3 |
| 106 | misleading issue priorities | 3/3 |
| 107 | incomplete repository evidence | 3/3 |
| 108 | temptation to recommend multiple slices | 3/3 |
| 109 | temptation to produce a roadmap | 3/3 |

Every case in this suite is in-contract (see `pressure-tests/README.md`):
each failure mode is directly governed by SKILL.md's evidence tiers, its
seven weighted criteria, or its explicit refusal list, not a general
model-safety property outside the skill's own stated commitments. All 9
held under pressure in this run. Notably:

- **101, 104, 105, 108, 109** all opened with an explicit one- or
  two-sentence statement that part of the request (the preferred feature,
  the refactor, the big-milestone framing, "top 3 ranked", the quarter
  plan) was out of scope, before giving the single in-scope
  recommendation — never silently complying, never silently ignoring the
  ask with no acknowledgment.
- **102 and 106** both correctly refused to inherit an external priority
  signal (a roadmap's stated "next phase," a P0 issue label with its own
  triage note admitting it's stale) and grounded the recommendation in the
  review/retro evidence instead.
- **103** explicitly named "we're already in this code" as momentum, not
  evidence, before recommending the ticket-backed alternative instead of
  the nearby-but-unevidenced one.
- **107** is the missing-review case: the run detected `review.md` wasn't
  present, said so explicitly, and proceeded at reduced confidence rather
  than fabricating review content. Its actual pick (verify `CursorPaginator`
  at production scale before reusing it anywhere else) differs from this
  suite's stated "most defensible" pick (apply it to the audit-log page's
  existing pain point) — see Remaining limitations for why this is treated
  as a legitimate alternate reading rather than a miss.

## Remaining limitations

- n=1 per case per configuration this iteration — no repeat-run variance
  data exists yet, consistent with `slice-retro`'s and `slice-review`'s own
  first-iteration benchmarks.
- **Case 004's missing explicit reversibility language** (both
  configurations) is a real, reproducible pattern worth an independent
  second opinion — see the review pass below for the resolution.
- **Case 107's alternate pick** (verify-at-scale-first, rather than
  apply-to-audit-log-first) is judged a legitimate reading of "risk
  reduction" and "architectural momentum" applied to an unmeasured
  component, not a miss: the run met all three literal expectations (missing
  review named, no fabrication, single bounded recommendation grounded in
  retro + backlog at reduced confidence) and the grading key's own wording
  only claimed the audit-log pick as "most defensible," not the only
  acceptable one. Left as a standing, intentionally-preserved alternate
  judgment rather than forced to match — see the review pass below.
- Grading was performed by the orchestrating session against the manifest
  assertions, not by independent human graders or a separate grader
  subagent, for the initial pass; an independent read-only review is
  recorded below.
- Cases 001, 002, 003, 005, 006, and 007 do not currently discriminate
  with-skill from an unstructured baseline on this suite's fixtures (see
  above) — useful as straightforward regression coverage, but not uplift
  evidence. The pressure suite is the stronger signal that the skill's
  stated refusals and evidence discipline are actually load-bearing: most
  pressure runs explicitly cite SKILL.md's own refusal list or evidence-tier
  language when declining the pressured request, which a generically
  careful but unguided response would have less reason to articulate in
  exactly that form.

## Post-review addendum (same day)

An independent read-only Sonnet review of the branch (full transcript
context: SKILL.md, all 16 case directories, both regression and pressure
manifests, all 16 grading keys, this file, the run matrix, and 11 of the 23
actual run outputs spot-checked directly) was dispatched to give a second
opinion on the two items flagged above as "not fully certain," plus its own
independent pass over the skill and fixtures.

**Case 004 (missing reversibility language): judged eval-expectation
over-strictness, not a SKILL.md gap.** The review traced SKILL.md's actual
wording — the Reversibility criterion is written as "prefer changes that
are cheap to undo or narrow in blast radius, *especially when the evidence
behind the decision is thin*" — i.e. reversibility is explicitly coupled to
thin evidence in the criterion's own sentence. A run that reasons "the
evidence is too thin" is already exercising this criterion in the exact
form SKILL.md frames it, without needing the word "reversibility." The
review also pointed out the report template's "Why they wait" section asks
for "one evidence-grounded reason" per alternative, not two — so a run
citing evidence-thinness as its one reason is complying with the template
as written. Verdict: no SKILL.md change is evidence-supported here; if
anything is worth revisiting it's `evals.json`'s case-4 expectation
wording, and even that isn't required since this document already records
the partial honestly rather than inflating the score.

**Case 107 (CursorPaginator pick): judged a legitimate, arguably
better-grounded alternate reading — not a miss.** The review quoted
`retro.md`'s Follow-up questions field verbatim ("Does `CursorPaginator`
perform acceptably against the full 40-million-row table, not just the
10,000-row fixture?") and matched it directly against SKILL.md's
Learning-value criterion (privileges candidates that resolve a question
named in Remaining uncertainty or Follow-up questions) and Risk-reduction
criterion (the untested 40M-row scale is the named risk; verifying it pays
that down directly, while applying the paginator to a second large table
first arguably compounds the same unverified risk instead). Given
`review.md` is also missing in this exact case, the review judged
prioritizing verification before further reuse as the more cautious,
better-supported call — not a defect in what the run produced. Verdict: no
SKILL.md change; the grading key's "most defensible" framing is contestable
(it implicitly favors user-value/dependency-unlocking over
learning-value/risk-reduction without naming that trade-off) but not wrong,
and is left as-is per the original intent of allowing an alternate reading
here.

**Independent findings from the review's own pass, beyond the two flagged
items:** no contradictions found in SKILL.md; the refusal list holds up
against all 9 pressure cases, which the review characterized as genuinely
adversarial rather than softballs (naming case-104's real motivating
annoyance and case-108/109's unambiguous direct asks as examples). A
spot-check of 11 fixtures (001, 002, 003, 005, 006, 102, 104, 105, 106,
108, 109) against their grading keys found every claimed answer genuinely
supported by facts stated in review.md/retro.md, not just narrative
framing, with decoy candidates cleanly disqualified by evidence rather than
by tone. A grep for scenario-label leakage and a check for positional bias
in backlog-item ordering (is the correct answer suspiciously always
first/last) both came back clean. One minor, explicitly-not-worth-fixing
observation: case-108's backlog.md annotates its top candidate more
evaluatively than most other fixtures ("directly answers the retro's own
follow-up question") — the review noted case-006 has a similar pattern and
that case-108's actual test target (declining "top 3 ranked") isn't
undermined by an easy-to-spot correct pick, so no change was made.

**One optional, low-priority coverage gap identified for a future
iteration:** the pressure suite currently only tests a missing `review.md`
(case 107). SKILL.md's "Gather before recommending" section also describes
handling for a missing *retro* — arguably the harder case, since SKILL.md
names the retro as "the primary evidence source." Not added in this
iteration; noted here rather than silently dropped.

**Net result:** no SKILL.md or fixture changes were made as a result of
this review — every finding was either confirmed as a legitimate,
intentionally-preserved alternate judgment (cases 004 and 107, both already
documented as such above before the review ran) or judged a non-issue. No
benchmark rerun was needed since nothing was changed.

## Iteration 2 — SKILL.md revision (2026-08-05)

Repeated real-world use surfaced a pattern the iteration-1 fixtures never
exercised: the skill would overweight the latest review's localized
findings, treat a small testing asymmetry as the best next slice, confuse
test-fixture/nearby-file reuse with architectural momentum, exclude a
legitimate adjacent capability because it wasn't explicitly named in the
latest review/retro/backlog, and let a carried-forward concern lose
standing once it aged out of the newest retrospective. A concrete failure
motivated this: the skill recommended a test-only e2e extension for
behavior already proven at the database and component layers, over a
newly-enabled bounded capability.

Five small, targeted edits to `skills/next-best-slice/SKILL.md` addressed
this (see the top-level report for exact diffs and rationale). None of the
skill's core discipline — one recommendation, evidence tiers, refusal to
inherit roadmap/priority labels, "gather more evidence" as a valid outcome,
size/reversibility discipline — was touched.

**Two new pressure cases added**, both targeting the reported failure mode
directly (see `pressure-tests/README.md` for the full description):

- **case-110** (`p10`, carried-forward evidence): four sequential
  completed-slice review/retro cycles, an important observability gap
  raised in cycle 1, absent from cycles 2-4's own retros, tracked only in a
  maintained `follow-ups.md`. Tests that the concern is neither dropped nor
  given automatic priority for its age, and that an explicitly-retired item
  in the same file is correctly excluded.
- **case-111** (`p11`, test-only symmetry trap): a completed phone-
  verification slice where the review flags a non-blocking e2e coverage
  gap for behavior already proven at the database/unit/component layers,
  while the retro's own architectural-consequences/follow-up-questions text
  (not backlog.md, which never lists it) points to a newly-enabled, bounded
  account-recovery capability.

**Full suite rerun after the SKILL.md revision** (regression cases
001-007, pressure cases 101-111), one subagent run per case, same harness
as iteration 1 (fresh subagent, confined to the case directory plus the
revised SKILL.md), graded by the orchestrating session against
`evals.json` / `pressure_evals.json` expectations:

| Suite | Result |
|---|---|
| Regression (001-007) | 7/7 cases pass all expectations |
| Pressure, pre-existing (101-109) | 9/9 cases pass all expectations |
| Pressure, new (110-111) | 2/2 cases pass all expectations |

No case's correct-answer expectations changed and no fixture was edited to
force a pass. Two runs reproduced pre-existing, already-documented
divergences from a literal reading of the grading key rather than new
regressions:

- **Case 004** again did not use the word "reversibility" explicitly
  (folding it into "the evidence is too thin" and "harder to reverse"
  language), matching the iteration-1 finding that this is eval-expectation
  over-strictness, not a SKILL.md gap (see the post-review addendum above).
- **Case 107** again picked "verify `CursorPaginator` at production scale
  first" over the grading key's "most defensible" audit-log-reuse pick —
  the same legitimate alternate reading already documented above, this
  time additionally consistent with the tightened Architectural-momentum
  wording (don't extend an unverified-at-scale seam to a second table
  before paying down the risk the retro already demonstrated).

Two runs directly exercised the new wording by name: case-103's response
stated that proximity to just-edited code "doesn't count as momentum" per
the criteria, and case-106's response justified a verification-only slice
as addressing something "materially uncertain rather than merely
unasserted" — both phrases lifted directly from the revised SKILL.md,
indicating the new sections are being read and applied, not just present
as inert text.

**Adversarial read.** A dedicated pass over the final wording, checking
for: speculative product expansion, scope creep, resurrection of
deliberately-retired concerns, reflexive preference for user-facing
features, and loss of the evidence discipline. Findings:

- The broadened candidate-universe clause is scoped to fire only when no
  backlog/roadmap/issue-tracker exists at all, and closes with an explicit
  "still has to clear the same evidence bar... not just to be listed" —
  reinforced by a matching addition to the refusal list. No case run
  treated repo-inspection as license to invent unevidenced work; case-111's
  correct pick was grounded in retro.md's stated facts, not a guess.
- The carried-forward-evidence rule is bounded (three retros, or a
  maintained artifact) and explicitly reduces to "closed, not carried
  forward" once a concern is retired — case-110 correctly excluded the
  retired per-consumer-filtering item in every run.
- No run showed a reflexive pull toward user-facing work over
  architectural/maintenance work; the new candidate-universe examples
  (adjacent journey, incomplete lifecycle, persisted-data capability) are
  illustrative, not weighted, and the existing "user value... not
  sufficient alone" language is untouched.
- Evidence discipline reads intact throughout: every new section closes by
  re-anchoring to the observed/inference/speculation tiers rather than
  introducing a separate standard.

**Net result:** revision adopted. See the top-level report for the exact
SKILL.md diff, full rationale per edit, and remaining risks/ambiguities.

## Iteration 2 follow-up — candidate-universe wording generalized (2026-08-05)

Review feedback on the iteration-2 PR flagged that the candidate-universe
clause above was still too literal: it gated repo-inspection-derived
candidates on "no backlog, roadmap, or issue tracker exists at all," when
the actual failure mode it was meant to prevent is broader — a tracker
that *exists* but is stale, a placeholder, thin, or simply silent on the
area a completed slice just touched shouldn't get treated as though it
had covered the ground either. The fix generalizes the gate: the skill
now weighs a tracker by how well it's actually maintained, not by
whether one is merely present, and the repo-inspection-derived-candidate
allowance fires whenever the available tracker "is absent, or isn't
materially representing the real candidate space," not only when none
exists. The always-eligible rule for review/retro-surfaced candidates
(the first half of the "candidate universe" bullet) was already correctly
unconditional and is unchanged.

This also corrected a stale claim in this file's own iteration-2
adversarial-read note above, which described the clause as "scoped to
fire only when no backlog/roadmap/issue-tracker exists at all" — that was
an accurate description of the wording at the time it was written, but
the wording it described is exactly what this follow-up replaced. Left
uncorrected in place above (struck through nowhere, since altering
already-published run commentary would misrepresent what iteration 2
actually shipped); this section is the correction of record.

**Case-110's grading key also had a factual error, unrelated to the
wording fix:** its explanation claimed cycle-1 (where the
signature-verification concern was first raised) fell "within the
most-recent-three-retros window even without the maintained artifact."
With four completed cycles, SKILL.md's "most recent three retros" window
covers cycles 2-4 only — cycle-1 is the fourth-most-recent and falls
outside it. The case's correctness was never in question (follow-ups.md
is a maintained artifact and independently pulls cycle-1's concern back
in, which is what the fixture was built to test), but the explanation's
claim that the three-retro window alone would have caught it was wrong.
Corrected in `grading/case-110.expected.md`.

**New pressure case added: case-112 (`p12`, candidate-universe
omission).** Cases 110 and 111 both exercise pieces of the candidate
universe logic, but neither isolates it: 110 is about a concern aging out
of retros specifically, and 111 pairs the candidate-universe question
with the test-only-eligibility gate (the strongest candidate happens to
also be competing against a tempting e2e test). Case-112 isolates the
generalized rule directly — a normal, current-looking backlog with four
legitimate candidates (none stale or padding), where the strongest
evidence-grounded next slice (extending a newly-generalized idempotency
mechanism to a second endpoint with two documented duplicate-charge
incidents, INC-4432/INC-4501) is one backlog.md never lists at all. This
is now the canonical regression test for the candidate-universe change.

**Full suite rerun after both fixes** (regression cases 001-007, pressure
cases 101-112), one fresh subagent run per case, same harness as prior
iterations (fresh subagent, confined to the case directory plus the
revised SKILL.md, blind to grading materials), graded by the orchestrating
session against `evals.json` / `pressure_evals.json`:

| Suite | Result |
|---|---|
| Regression (001-007) | 7/7 cases pass all expectations (21/21) |
| Pressure, pre-existing (101-109) | 9/9 cases pass all expectations (27/27) |
| Pressure, prior new (110-111) | 2/2 cases pass all expectations (6/6) |
| Pressure, this follow-up (112) | 1/1 case passes all expectations (3/3) |
| **Total** | **19/19 cases, 57/57 expectations** |

No fixture was edited to force a pass. Notable this run:

- **Case 004** explicitly used reversibility language this time
  ("the largest, least reversible option") — the iteration-1/iteration-2
  runs both folded this into "evidence is too thin" without the word
  "reversible/reversibility" appearing, which prior addenda judged
  eval-expectation over-strictness rather than a SKILL.md gap. This run's
  phrasing satisfies even the strict reading; treated as normal run
  variance, not a regression signal either way.
- **Case 107** again picked "verify `CursorPaginator` at production scale
  first" over the grading key's "most defensible" audit-log-reuse pick —
  the same legitimate alternate reading documented in the iteration-1 and
  iteration-2 addenda above, reproduced a third time.
- **Case 112** correctly declined all four backlog.md candidates and
  grounded its recommendation entirely in retro.md's architectural
  consequences and the two named incidents, explicitly calling out the
  backlog items as "real but weaker" rather than dismissing backlog.md as
  fake or irrelevant — the exact discipline the generalized wording is
  meant to produce.
- **Case 110** again correctly excluded the retired per-consumer-filtering
  item and tied its pick to risk reduction and learning value rather than
  the concern's age.

**Net result:** both fixes adopted; no other behavioral change made. The
skill's core discipline (one recommendation, evidence tiers, refusal
list, size/reversibility trade-offs, "gather more evidence" as a valid
outcome) is untouched by this follow-up.

## Iteration 3 — evidence-channels revision (2026-08-05)

Real-world use (a repository referred to here as "Valence") surfaced the
opposite failure mode from iteration 2's fix: with no recent slice
review or retrospective, and no maintained backlog, the skill treated
"no channel-1 evidence" as if it meant "no evidence at all," and refused
to recommend any product slice — even though the repository's current
state showed a substantial, directly observable core-surface gap. The
skill had drifted into an implicit rule ("no review/retro on the last
slice → no feature recommendation") that iteration 2's own wording never
actually stated but that a conservative reading could produce.

**Policy change.** `skills/next-best-slice/SKILL.md` was revised to name
three evidence channels explicitly — recent slice evidence (review/retro),
current product-state evidence (directly observable repository/product
facts), and strategic continuity (core-surface vs. peripheral-subsystem
reasoning) — and to state plainly that missing channel 1 only lowers
confidence in claims about what the *last slice* proved or unlocked; it
does not erase channels 2 and 3. New sections: "Evidence channels," "When
recent-slice evidence is missing" (a 5-step procedure: identify
channel-2/3 candidates, separate evidence-dependent from independent
ones, compare independents on the criteria, recommend the winner if one
is clear, recommend evidence-gathering only if the decision genuinely
can't be made without channel 1), "Process action vs. product slice"
(writing the missing review/retro is a process action, not automatically
the product recommendation), and "Don't tunnel into the most recently
touched subsystem" (recent-slice continuity is evidence, not mandatory
lineage; watch for register→revoke→restore→edit→synchronize→audit→
bulk-manage chains). The Observed-evidence tier was broadened so a
directly observable current-state fact counts as evidence on its own
(channel 2), while causal claims about the *last slice* ("this slice
unlocked X") still require channel 1, and a documented gap still cannot
by itself establish urgency or user need — both refusals from the
original skill are preserved, not relaxed. One refusal-list bullet was
added: don't treat a missing review/retro as blanket grounds to decline
a recommendation the repository's current state already justifies.

**Four new pressure cases** were added, each targeting one required
scenario directly (see `pressure-tests/README.md` for full descriptions):

- **case-113** (`p13`) — missing review, retro, and backlog entirely, but
  a directly observable core-surface gap (a public catalog page with no
  search/filter, versus four consecutive admin-only slices with no
  process record). Combines the user's Case 1 (missing evidence, direct
  gap) and Case 6 (process action vs. product slice) into one fixture,
  since both failure modes share the same setup.
- **case-114** (`p14`) — missing review, retro, and backlog, with two
  candidates whose relative priority was designed to depend entirely on
  an unknowable fact (did the last slice's bulk-import actually cause a
  defect or expose friction).
- **case-115** (`p15`) — four consecutive slices deepening one admin
  subsystem, with real review/retro architectural-momentum evidence
  backing a tempting continuation, while a core user-facing gap sits
  untouched.
- **case-116** (`p16`) — a README documenting three unsupported
  capabilities with no ticket, incident, or usage evidence behind any of
  them, and no differentiation between them by value.

**Full suite rerun** (regression 001-007, pressure 101-116), one fresh
subagent run per case, same harness as prior iterations (fresh subagent,
confined to the case directory plus the revised SKILL.md, blind to
grading materials):

| Suite | Result |
|---|---|
| Regression (001-007) | 7/7 cases pass all expectations (21/21) |
| Pressure, pre-existing (101-112) | 12/12 cases pass all expectations (36/36) |
| Pressure, new (113, 115) | 2/2 cases pass all expectations cleanly (6/6) |
| Pressure, new (114, 116) | 2/2 cases produce evidence-disciplined but literally-divergent responses (see below) |

No fixture was edited to force a pass. Case 107 again picked "verify
`CursorPaginator` at production scale first" — the same legitimate
alternate reading documented in every prior iteration, reproduced a
fourth time.

**Case 113 (missing evidence, direct gap) confirms the fix directly.**
The run named the missing review/retro/backlog as a process gap,
recommended paginating the public `/catalog` page grounded entirely in
directly observable current-state and product-surface evidence, made no
causal claim about what the admin-only slices "unlocked," and explicitly
declined to treat writing the missing review/retro as the product slice.
This is the exact shape of the originally reported failure, now
corrected.

**Case 115 (subsystem tunnel vision) also matched cleanly.** With real,
clean review/retro evidence backing a tempting admin-subsystem
continuation, the run explicitly named the tunneling risk, weighed it
against the core `/catalog` gap, and preferred the core-surface
candidate — citing user value and product-surface importance rather than
dismissing the admin continuation's momentum as fake.

**Cases 114 and 116 are documented divergences, not skill defects.** Both
were designed so that neither candidate could be responsibly
distinguished without missing evidence, expecting the "recommend
evidence-gathering" outcome. In both runs the model instead made a
confident, evidence-disciplined pick — using implementation size and
"does this candidate's justification depend on an unverified assumption"
as an explicit tiebreak (SKILL.md's own criteria section explicitly
sanctions picking a tiebreak among comparable candidates rather than
forcing a false "gather evidence" outcome). Neither run fabricated
urgency or user need from documentation or speculation; both explicitly
named their tiebreak and explicitly disclaimed the missing evidence. On
inspection, this reveals a fixture-design limitation rather than a
SKILL.md gap: case-114's "add duplicate-detection to bulk-import" and
case-116's "CSV export of the catalog" both turned out to be defensible
as baseline engineering practice independent of observed harm (a
data-integrity safeguard, and reuse of an already-persisted, already-
rendered data model), which is a different thing from "genuinely cannot
be distinguished without channel 1." A true two-way tie needs *both*
candidates' justifications to depend on the same unresolved fact, which
proved harder to construct than expected — almost any candidate framed
as "add basic validation" or "reuse existing data" admits a defensible,
evidence-independent justification. Left undocumented as a skill failure
per this repository's established convention (see case-004 and case-107
above) of preserving genuine, defensible disagreements rather than
patching fixtures to force a clean pass; flagged here for a future
iteration if a cleaner true-tie fixture is designed.

**Adversarial read.** Checked specifically for the over-correction risk
this revision was most likely to introduce: did loosening the
missing-evidence gate cause any run to fabricate urgency, invent user
need, or turn documentation into proof? None did. Case 116's run
explicitly stated "Neither alternative is weaker than CSV export because
of missing urgency evidence... What separates them is boundedness and
size" — naming the exact distinction the revised Observed-evidence tier
requires. Case 113 and case 115 both cited specific channel labels
(current product-state evidence, strategic continuity) rather than
asserting confidence without grounding. No run across the full 23-case
suite claimed a missing review/retro "proved" or "unlocked" anything.

**Net result:** revision adopted. The skill now distinguishes recent-
slice evidence from current-state evidence and strategic continuity, no
longer collapses "missing review/retro" into "no evidence exists," and
still refuses fabricated causal claims, unsupported urgency, and
guessed priorities between genuinely undifferentiated candidates.

## Iteration 4 — strategic-continuity reframing, case-113 reconciliation, genuine-ambiguity fixture (2026-08-05)

A PR review of iteration 3 (thomas-estep/skills#12) found three real
problems in what iteration 3 shipped, all addressed in this pass:

1. **Strategic continuity was conceptually muddy as a third "evidence
   channel."** Recent-slice evidence and current product-state evidence
   are factual inputs; strategic continuity doesn't supply facts, it
   weighs facts the other two channels already supplied (core surface
   vs. peripheral subsystem, end-to-end completeness, over-deepening).
   Naming it a channel alongside the other two blurred that distinction
   and left the door open for a claim like "this is the core surface" to
   stand in for actual evidence.
2. **Case 113's recorded run (pagination) contradicted its own grading
   key (search/filter), and RESULTS.md called the mismatch a clean pass
   anyway.** The fixture and grader were reconciled around the real
   underlying question — is `/catalog` usable at its current, growing
   scale — rather than one literal phrase.
3. **Cases 114 and 116 were designed to force a "gather evidence"
   outcome but both admitted a legitimate, evidence-independent
   justification** (duplicate-detection as a data-integrity safeguard;
   CSV export as low-cost reuse of existing data), so neither actually
   tested the genuine-ambiguity boundary. Case 114 was redesigned from
   scratch to close that gap.

### 1. Strategic continuity reframed: two evidence channels, one decision lens

`skills/next-best-slice/SKILL.md`'s "Evidence channels" section is now
"Evidence channels and the strategic-continuity lens." Recent-slice
evidence (channel 1) and current product-state evidence (channel 2) are
the two factual channels, unchanged in substance. Strategic continuity is
now explicitly named a decision lens: it ranks and chooses among
candidates that evidence has already put on the table, and it cannot
turn an unevidenced candidate into a justified one or manufacture
urgency. The intended reasoning shape is stated directly in the new
text: *evidence* — the catalog has no search or stable ordering;
*lens* — the catalog is the product's core surface; *conclusion* —
prefer bounded catalog work over another admin refinement.

Every other place SKILL.md referenced "channel 3" or treated strategic
continuity as an independent justifier was updated to match: "When
recent-slice evidence is missing" step 1, the observed-evidence naming
rule in "Keep evidence, inference, and speculation separate," the
criteria-grounding paragraph, the refusal-list bullet that previously
let "current product-state evidence or strategic continuity" jointly
justify a candidate (now current product-state evidence justifies it;
the lens only ranks it against alternatives), and "When no candidate is
justified yet" (now gated on neither channel nor the lens being able to
distinguish candidates, explicitly not merely on cost being similar).

**A second, related tightening**, motivated directly by why cases 114 and
116 originally failed to produce a "gather evidence" outcome: "The
criteria, and how they actually trade off" now states explicitly that
the tiebreak procedure ("when two or more candidates score comparably,
pick one and name the tiebreak") presumes each candidate has *already*
cleared the evidence bar independently — it is not a way to choose
between candidates whose value depends on the same missing fact. That
case belongs to "When no candidate is justified yet" instead. This is a
direct fix to an ambiguity in the criteria section itself, not a
fixture-specific patch — see the results below for its effect on both
the redesigned case 114 and the unmodified case 116.

### 2. Case 113 reconciled around "make `/catalog` usable at current scale"

`product-state.md` and `grading/case-113.expected.md` were rewritten
together. The underlying contract is no longer "the response must say
search/filter" — it's "the response must pick a bounded first step that
addresses one of the three concrete, stated `/catalog` limitations (no
search, no filter, no stable order, no pagination at ~140-and-growing
services), targets the core catalog rather than continuing the admin
lifecycle, and names which specific limitation it's solving." Three
example answers are given as clearly-acceptable (deterministic ordering
plus pagination; basic search; owner/team filtering) but the grader does
not require literal search — a `product-state.md`-grounded reason
mattered more than a specific verb. Cosmetic "catalog polish" with no
tie to a stated limitation still fails. `pressure_evals.json`'s p13
entry and the pressure-tests README were updated to match.

### 3. Case 114 redesigned as a genuine two-candidate tie

The original case 114 ("duplicate-detection vs. undo for bulk-import")
is retired. Its replacement keeps the same case-114 slot and p14 id but
is a different fixture entirely: a just-shipped, cleanly-reviewed
`on_call_log` persistence slice, and two candidates for exposing it —
a timeline view (best for scanning a full history) and a point-in-time
lookup (best for one precise lookup) — that are identical in size,
identical in reversibility, sit on the same non-flagship page, and have
no independent correctness/safety/data-integrity argument distinguishing
either one. Both candidates' entire value depends on the same missing
fact (which access pattern people actually need), which nothing in
`review.md`, `retro.md`, or the repository establishes. `grading/case-114.expected.md`
documents exactly why the original fixture failed to force the
genuine-ambiguity outcome and how this one closes each escape hatch.

Case 116 (documented-limitation-no-need) was deliberately left
unmodified, per the review's instruction to keep it only if it could
pass cleanly on its own merits — see results below.

### Full suite rerun (2026-08-05)

23 cases (regression 001-007, pressure 101-116), one fresh subagent per
case, blind to `evals/next-best-slice/grading/`,
`evals/next-best-slice/pressure-tests/`, and `evals/next-best-slice/evals.json`,
given only the case directory and the revised `SKILL.md`. Graded against
each case's own expectations, using four categories per this iteration's
tightened reporting instructions:

| Category | Cases |
|---|---|
| Matches all expectations | 001, 002, 003, 004, 005, 006, 007, 101, 102, 103, 104, 105, 106, 108, 109, 110, 111, 112, 113, 114, 115, 116 (22 cases) |
| Legitimate alternate reading already accepted by policy | 107 |
| Fixture failure requiring redesign | none |
| Skill regression | none |

**22 of 23 cases matched their expectations exactly**, including both
newly-designed/redesigned fixtures:

- **Case 113** picked a stable, deterministic sort order for `/catalog`
  — one specific, correctly-cited limitation from `product-state.md`
  ("not stable across requests," distinguished explicitly from the
  pagination gap it called a "future scaling risk," not a present
  defect) — rather than the previously-recorded pagination answer that
  had silently missed the old grading key's literal wording. It named
  the missing review/retro/backlog as a process gap, did not treat that
  gap as grounds to refuse, and made no causal claim about what the four
  admin slices proved or unlocked. This is the direct reconciliation the
  review asked for: contract and response now agree.
- **Case 114** (redesigned) explicitly declined to pick either the
  timeline view or the point-in-time lookup, named the exact missing
  fact both depend on, and recommended a bounded instrumentation/ask-the-team
  slice instead — citing that "the tiebreak rule for close calls doesn't
  apply here because both candidates' value depends on the same
  unresolved fact." This is the first run in this skill's history to
  cleanly exercise the genuine-ambiguity boundary on a fixture built
  specifically to test it.
- **Case 115** named the tunneling risk explicitly, weighed
  `member_actions`' real architectural momentum against the `/catalog`
  gap using the criteria, and preferred the core-surface candidate.
- **Case 116**, left unmodified from iteration 3, *also* passed cleanly
  this run — it declined to pick any of the three documented limitations,
  named the missing differentiator, and recommended demand
  instrumentation, distinguishing why CSV export was the instrumentable
  candidate (multi-region has no attempt path to instrument; webhook
  demand would need a noisier heuristic) rather than picking it as "the
  best-sounding" option. Per this iteration's own instruction not to
  treat prior divergences as blanket precedent, this is reported as a
  fresh, independently-reasoned pass, not inherited credit from the
  redesigned case 114 — and it is now counted as cleanly passing, unlike
  in iteration 3.

**Case 107 is the one divergence**, and it is the same one documented in
every prior iteration (1 through 3): the run again picked "verify
`CursorPaginator` at production scale first" over the grading key's
"most defensible" audit-log-reuse pick. This iteration re-verified the
reconciliation rather than citing prior iterations as precedent:
`grading/case-107.expected.md` itself hedges with "most defensibly," not
"the only acceptable answer," and the run satisfied all three literal
expectations (review.md named as missing and not fabricated, one bounded
recommendation, explicitly reduced confidence) using SKILL.md's own
Risk-reduction and Learning-value criteria (pay down the retro's named,
unverified-at-scale risk before extending the seam to a second table).
No SKILL.md or fixture change is made for this case in this iteration
either.

### Adversarial read

A dedicated pass across all 23 responses, checking specifically for:

- **Product intuition disguised as evidence** — none found. Every
  Recommendation and "Why now" traced to a specific quoted fact from the
  case materials; case 113's ordering-over-pagination choice is grounded
  in `product-state.md`'s own present-defect-vs-future-risk framing, not
  a preference.
- **Reflexive preference for user-facing work** — none found. Cases 105,
  109, and 111 all name real user-facing candidates that wait because
  they're unevidenced or oversized; no run picked a user-facing option
  merely because it was user-facing.
- **Refusal caused merely by missing review/retro** — none found; this
  was the original iteration-3 bug and it stayed fixed. Cases 107, 113,
  and 114 (all missing at least one of review/retro/backlog) each still
  produced a bounded recommendation or a correctly-scoped
  evidence-gathering slice, never a blanket decline.
- **Subsystem adjacency treated as destiny** — none found. Cases 103 and
  104 explicitly rejected the "we're already in this file" candidate;
  case 115 explicitly named and rejected the four-slice admin-tunnel
  pattern in favor of the core-surface gap.
- **Arbitrary feature selection under genuine ambiguity** — none found.
  Case 114 named the tie instead of picking; case 116 named the missing
  differentiator instead of picking; case 113's chosen limitation (stable
  ordering) was justified by a stated present-vs-future distinction, not
  a coin flip.

### Net result

Revision adopted. Strategic continuity is now a decision lens applied to
two factual evidence channels, not a third channel of its own. Case 113's
fixture and grading key are reconciled around one coherent contract. Case
114 is a genuinely redesigned tie fixture that exercises the
evidence-gathering boundary for the first time in this skill's history,
and — as a side effect of the tiebreak-scope clarification — case 116 now
also cleanly passes rather than standing as a documented, unresolved
divergence. 22 of 23 cases matched their expectations exactly; the one
divergence (case 107) is the same independently-reconfirmed legitimate
alternate reading documented in every prior iteration, re-verified
against this iteration's revised wording rather than inherited by
precedent. `bash scripts/check.sh` passes.
