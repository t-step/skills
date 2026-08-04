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
