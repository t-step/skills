# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** real-world-fixture -- Apache Ignite's "move common classes
to ignite-commons" phase (IGNITE-24781 and its Sub-tasks), an early phase
of the same IEP-119 initiative that later produces the thin-client
extraction epics IGNITE-28717/IGNITE-28819. Cutoff: 2025-03-30.

**Why this fixture exists:** this is a real, formally-decomposed plan
(twelve genuine Jira Sub-tasks of one umbrella ticket, with real "blocks"
links between some of them) rather than an author-designed synthetic one.
Its distinctive pressure points are: a real horizontal-enabler judgment
call (does creating the `ignite-commons` module, IGNITE-24782, deserve
independent-enabler treatment, given it unlocks most of the other tasks
here?), a real "looks architectural but is actually gated, not gating"
task (IGNITE-24850, which is *blocked by* two siblings rather than
blocking them, despite "split IgniteUtils" sounding like foundational
work), a real same-class/shared-file ambiguity with no stated link
(IGNITE-24941 and IGNITE-24850 both touch `IgniteUtils`), and a real,
textually concrete pair of tasks (IGNITE-24957 and IGNITE-24851) whose
stated relationship does not resolve into one clean direction. A good
response should surface all of these using the fixture's own stated and
inferable detail, without manufacturing structure the record doesn't
support and without flattening the genuine tangle into false certainty.

## REQUIRED

- **Recognizes IGNITE-24846 blocks IGNITE-24850, and IGNITE-24848 blocks
  IGNITE-24850, as stated Jira dependencies** -- i.e. IGNITE-24850 depends
  on both, and is not proposed as independently startable in parallel
  with either of them.
  *Provenance:* `provenance/case-301/sources.md` (formal `issuelinks`
  fields, both directions).

- **Does not treat IGNITE-24850 as a horizontal enabler or foundational
  first step just because "split IgniteUtils" sounds architectural.**
  Within this task set, IGNITE-24850 has no forward-blocking relationship
  to anything -- it is itself gated by two siblings. A response that
  schedules it early, or as a prerequisite other tasks wait on, has
  inverted the fixture's actual stated topology.
  *Provenance:* `tasks.md`/`dependencies.md` (the only stated links on
  IGNITE-24850 are "is blocked by", not "blocks", within this set);
  `provenance/case-301/actual-prs.md` (historically, no code work
  happened on it until months after every other task in this set had
  already shipped -- DIAGNOSTIC corroboration only, not something the
  agent could know, but confirms the REQUIRED claim was the right call).

- **Identifies IGNITE-24782 ("Create ignite-commons module") as a real
  prerequisite for the other "Move X to ignite-commons" tasks in this
  set, via inference (no task/module can be moved into a module that
  doesn't exist yet) rather than a stated link** (none exists). A
  response that either ignores this dependency entirely, or asserts it
  as if the tracker stated it explicitly, has missed what kind of claim
  this actually is.
  *Provenance:* `dependencies.md` ("Inferable from concrete detail").

- **Given that IGNITE-24782 plausibly gates most of this task set, does
  not casually reject it as a standalone enabler.** Unlike the
  "absorbable pseudo-enabler" pattern this suite also tests (a shared
  piece with only one real consumer), IGNITE-24782 genuinely unlocks
  several separately-verifiable "Move X" tasks (at minimum IGNITE-24792,
  -24846, -24847, -24848, -24851, -24852, -24957, -24958) -- a real,
  multi-consumer case for independent-enabler treatment, not a borderline
  one. A response that folds it into one of the "Move X" tasks without
  comment, or dismisses it as "too simple to be an enabler," has
  under-weighted what the fixture's own text establishes.

- **Does not resolve the IGNITE-24957 / IGNITE-24851 relationship into a
  single confident order.** IGNITE-24957's own description both (a) says
  part of its own work should happen first to unblock IGNITE-24851, and
  (b) lists `IgniteException` (IGNITE-24851's target) among the classes
  `X` currently imports -- which pulls in the opposite direction. A
  correct response either names this as a genuine, only partly-resolved
  coupling (the fixture's own honest framing), or picks one reading while
  explicitly acknowledging the other exists and stating why it chose as
  it did. Silently picking one direction with no acknowledgment that the
  ticket's own text also points the other way is the failure this checks
  for.
  *Provenance:* `tasks.md` (IGNITE-24957's full quoted description);
  `dependencies.md` ("A genuinely tangled pair").

- **Does not invent a stated dependency between IGNITE-24941 and
  IGNITE-24850** (both touch `IgniteUtils`, no link exists) **or between
  IGNITE-24946 and IGNITE-24846** (both touch `F`, no link exists). A
  response may reasonably flag either pair as worth sequencing given the
  shared class, but must not present that as something the tracker
  states, and must not silently assume they're safe to run fully
  concurrently without at least naming the shared-file consideration.

- **Does not invent detail beyond what four terse tasks actually say.**
  IGNITE-24846, IGNITE-24847, IGNITE-24848, and IGNITE-24852 have no
  description beyond their titles in the source material. A response
  that adds specifics for these (e.g. inventing file paths, specific
  method signatures, or a rationale the ticket doesn't give) has violated
  this skill's own "don't invent detail" boundary.

## DIAGNOSTIC / HISTORICAL COMPARISON (not pass/fail)

- The real, delivered PR for IGNITE-24847 also covered IGNITE-24851 and
  IGNITE-24852 in the same change -- three separate Sub-tasks landed as
  one real unit. Nothing in the tracker predicted this at the cutoff, and
  a response is not expected to reproduce it; grouping these three
  together, keeping them separate, or any other defensible grouping
  consistent with the fixture's own stated content are all acceptable.
  (`provenance/case-301/actual-prs.md`)
- IGNITE-24850's real PR did not open until roughly four months after
  this cutoff, well after both of its stated blockers had their own PRs
  opened -- historical confirmation that the "is blocked by" links
  reflected a real execution constraint, not just paperwork.
  (`provenance/case-301/historical-outcome.md`)
- The umbrella ticket (IGNITE-24781) and IGNITE-24850 were both marked
  "Resolved" in Jira on the same day, 2026-01-12 -- roughly nine months
  after the actual code work on this phase had substantially finished --
  an administrative closeout, not a sign that work happened that late.
  (`provenance/case-301/historical-outcome.md`)

## Note on this fixture's history

An earlier draft of this case centered on IGNITE-28717/IGNITE-28819
directly and used a five-task fixture built around external-scope
ambiguity. That draft was superseded after a broader search of the same
IEP-119 initiative (using the tracker's actual parent/Sub-task field
rather than a shared label) found this richer, still-real, still-bounded
window instead. See `provenance/case-301/cutoff-rationale.md` for the
full comparison and the honest note about the original search's gap.
