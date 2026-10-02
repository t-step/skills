# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** real-world-hudi-metadata-table (case-303)

**Nature of this case:** unlike cases 1–15/101, this is a real, messy
plan pulled from public Apache Hudi Jira history (see
`evals/task-composition/provenance/case-303/`), not an author-designed
fixture. It is graded on topology facts the record actually supports, not
on reproducing the historical PR grouping. Several points below are
intentionally left open in the fixture itself — a correct run should
surface that openness, not resolve it with invented confidence.

## REQUIRED

These are facts the record in `tasks.md`/`dependencies.md` genuinely
supports. A run that violates one of these is wrong, not just less
thorough.

1. **Does not invent tasks or resolve missing detail by fabricating scope.**
   In particular, HUDI-2436 is filed as an open investigation ("will
   follow up... to confirm the exact scenario") and HUDI-2459/HUDI-2460
   are filed as open-ended strategy questions ("need to come up with a
   strategy") — a correct run treats these as unscoped/uncertain, not as
   fully specified implementation tasks with an invented concrete fix.
   *(dependencies.md, "Open questions"; source: HUDI-2436, 2459, 2460
   descriptions in tasks.md)*

2. **Names HUDI-2432 and HUDI-2477 as dependent on HUDI-2422**, not as
   independent of it. HUDI-2422 introduces the `rollback.requested`
   instant; HUDI-2432's restore-plan design is explicitly built on that
   mechanism, and HUDI-2477's failure is explicitly triggered by that
   mechanism existing. Treating either as free-standing, unrelated work to
   HUDI-2422 is a topology error the fixture's own task text rules out.
   *(dependencies.md, "Stated or clearly inferable"; source: HUDI-2422,
   2432, 2477 descriptions)*

3. **Does not present a confident, singular execution order between
   HUDI-2432 and HUDI-2477** (e.g. "2432 must land before 2477" or vice
   versa) as if the record settles it. HUDI-2432 was filed a week before
   HUDI-2477 (2021-09-14 vs. 2021-09-21), but both concern restore's
   handling of pending rollbacks, and nothing in either ticket states
   which comes first in implementation or whether they're the same
   underlying problem — filing order alone does not establish an
   implementation or dependency order. A correct run either surfaces this
   as an open question or proposes handling them together while naming
   the ambiguity — not a confident one-directional order presented as
   fact, and not an order derived solely from which ticket was filed (or
   numbered) earlier.
   *(dependencies.md, "Open questions," first bullet)*

4. **Does not silently treat HUDI-2458 and HUDI-2459 as either the same
   fix or as strictly sequential** (e.g. "2459 can't start until 2458
   lands") without naming that this isn't stated. Both tickets address the
   same underlying metadata-table-compaction-fencing constraint from
   different angles (relax the fencing vs. go async instead), and neither
   ticket says whether they're complementary, redundant, or competing.
   *(dependencies.md, "Open questions," second bullet; source: HUDI-2458,
   2459 descriptions)*

5. **Does not elevate HUDI-2474 ("refresh timeline for every operation")
   into a standalone horizontal enabler for the whole plan.** Its own
   description names exactly one concrete consumer (delta-streamer's
   continuous mode) and a general "some tests fail without it" — not two
   or more separately-verifiable downstream slices. Per the skill's own
   horizontal-enabler test, a shared-sounding fix with only one real named
   consumer should fold into that consumer's slice, not stand alone.
   *(source: HUDI-2474 description in tasks.md; skill's "unlocks two or
   more separate downstream slices" criterion)*

6. **Does not confidently declare HUDI-2476 fully independent of
   HUDI-2285 with no caveat.** HUDI-2476's retried-compaction bug and
   HUDI-2285's synchronous design describe the exact same
   delta-commit-before-data-commit retry mechanics. The record does not
   settle whether 2476 is a standalone fix or a sub-problem inside
   implementing 2285 that isn't independently verifiable until 2285
   exists — a correct run names this connection or the uncertainty about
   it, rather than listing 2476 as a clean, unrelated parallel item.
   *(dependencies.md, "Open questions," third bullet)*

7. **Does not fabricate a dependency connecting HUDI-2452 to the rest of
   the plan.** It's an externally reported bug with no stated link to any
   other ticket in this set. A correct run may treat it as independent
   (defensible) but should not invent a shared cause or shared file with
   the rollback/restore cluster just because it was filed in the same
   window and shares the same "Blocker" priority label.
   *(dependencies.md, "Open questions," last bullet)*

8. **Does not conflate HUDI-2459 (async compaction) and HUDI-2460 (async
   cleaning) into the same fix, or invent a unified concrete
   implementation for both from thematic similarity alone.** They are
   stated as two distinct concerns (compaction vs. cleaning are different
   table services), and neither ticket states a dependency or shared
   mechanism between them — 2459's stated connection is to HUDI-2458 (the
   compaction-fencing constraint), not to 2460; 2460 states no link to
   either. Grouping them into one slice or tracking step is acceptable,
   and so is keeping them separate; both remain open-ended strategy
   questions per REQUIRED #1, and neither was ever implemented, separately
   or jointly, as of the most recent check (`provenance/case-303/
   actual-prs.md`), so no historical topology precedent corroborates a
   mandatory separation either. What's required is that a run not present
   them as the same problem, and not silently invent a shared design
   neither ticket supports, while naming whichever grouping choice it
   makes rather than assuming it needs no comment.
   *(source: HUDI-2459, 2460 descriptions in tasks.md; dependencies.md,
   "Open questions," second bullet, which connects 2458↔2459 only; a task
   count being two, filed the same day, is a task-identity fact, not by
   itself a slice-identity fact — see the skill's own "distinct source
   tasks are not automatically distinct delivery slices" framing)*
   *(NOTE — corrected 2026-09-26: this item originally required these to
   remain in two separate slices, treating separate-ticket-filing as
   sufficient evidence of a mandatory slice boundary. That was a grading-
   key defect found by adversarial review, not a response to either
   run's score: the original wording mandated a topology the source
   material doesn't establish, and was inconsistent with REQUIRED #10's
   correct treatment of a comparable, better-evidenced situation
   (naming a shared-area signal, not requiring a specific resolution of
   it). See RESULTS.md for the corrected scoring this produced.)*

9. **Does not treat the Jira "Blocker" priority label as a discriminating
   priority order.** 11 of the 19 tasks share the Blocker label; a run
   that picks an execution order and justifies it by "X is Blocker
   priority" without acknowledging that most of the list shares that same
   label is manufacturing a priority signal the source material doesn't
   actually provide. Per the skill's own "priority" rule, no priority was
   meaningfully stated here, and the report should say so rather than
   deriving a substitute from an undifferentiated label.
   *(source-notes.md; tasks.md's stated-priority footnote)*

10. **Surfaces, in some form, that HUDI-2422, 2432, 2477, 2468, and 2476
    describe touching the same rollback/restore/bootstrap-check
    mechanism** (the "compare last-synced instant to the active data
    timeline, decide whether to re-bootstrap" logic recurs by description
    in 2468 and 2477, and 2432 names the same rebootstrap mechanism as an
    alternative it considered; 2476's retry/clobber scenario and 2285's
    design describe the same delta-commit timing). This does not have to
    result in one giant slice — the correct response could reasonably keep
    several of these separate — but a plan that asserts all of this
    correctness-bug cluster is safely, fully parallel with no discussion
    of shared-area risk is missing a signal the tickets' own text
    supports. Per the skill's own parallelism guidance, a shared area is a
    signal to look closer, not an automatic serialize-or-allow verdict —
    what's required is that the signal gets named, not a particular
    resolution of it. HUDI-2478 is deliberately excluded from this list:
    despite superficially sounding like it belongs (it also touches
    metadata-table writer internals), its own filed text is about
    crash-recovery during bucket initialization, an unrelated mechanism —
    a run that lumps 2478 into this cluster on vibes rather than its
    actual text is making the same category of error this item exists to
    catch, just in the opposite direction (manufacturing a shared-area
    signal instead of missing one).
    *(dependencies.md, "Shared-area signal"; confirmed in practice by
    actual-prs.md's cross-cutting file overlap)*

11. **Treats HUDI-2303 and HUDI-2472 as functionally tied to HUDI-2276's
    own work, not as independent, freely-parallel items — even though
    neither ticket is formally linked to 2276 via a "blocks" relationship.**
    HUDI-2303 was filed as a bug discovered specifically while enabling
    metadata table in tests for 2276, and resolving it is functionally
    required before 2276 can be defaulted; HUDI-2472 exists only because
    2276's default-enablement work exposed the test failures it tracks,
    and its own text names HUDI-2468 as the known cause of part of what
    it's tracking. A plan that lists 2276 as safely parallel with 2303 or
    2472, with no mention of this consequence relationship, is missing a
    dependency the record actually states plainly (not just infers).
    *(dependencies.md, "Stated or clearly inferable," third and fourth
    bullets; source: HUDI-2276, 2303, 2472 descriptions)*

## DIAGNOSTIC / HISTORICAL COMPARISON (informational only — not pass/fail)

- Historically, HUDI-2285 and HUDI-2476 were actually implemented and
  merged together in one PR (#3590). This is consistent with REQUIRED #6
  above but is not itself required — a defensible plan could keep them
  separately tracked as long as the connection is named.
- A genuine multi-writer concurrency bug (HUDI-2573, a double-locking
  deadlock introduced by the synchronous metadata patch's new locking)
  was discovered about four weeks after this fixture's cutoff, during
  exactly the kind of end-to-end multi-writer verification work
  (HUDI-2567) that was just getting underway. Neither ticket is in the
  fixture; this is background on how the concurrency dynamic actually
  played out, not something the plan under test could have known.
- The "enable by default" effort (HUDI-2276) did not succeed cleanly on
  its first real attempt: 0.10.0 shipped with it defaulted on, but a
  production regression (HUDI-3066, existing large tables got *slower*
  file listing) surfaced eleven days later, and defaulting had to be
  re-planned more conservatively for 0.11.0 (HUDI-3208) a month after
  that.
- HUDI-2459 and HUDI-2460 (async compaction/cleaning for the metadata
  table) both remained open and unresolved for years past this window in
  real life — the record's own open-endedness (REQUIRED #1) held up.
- The rollout/upgrade design question (HUDI-2475) took roughly 2.5 years
  to formally close.

## Why

This fixture pressures the skill along axes the synthetic cases (1–15,
101) mostly can't reach, because real Jira tickets don't hand you a clean
task list with unambiguous file names and one stated priority:

- **Genuine, stated ambiguity that the tickets themselves don't resolve**
  (REQUIRED #3, #4, #6) — the synthetic cases' ambiguity is usually
  designed to have one intended resolution (e.g. case-006's revised key);
  here, several ambiguities are real open questions in the primary sources
  with no available resolution at all as of the chosen cutoff. The
  standard being graded is "did the run notice and say so," not "did it
  pick the historically correct side."
- **An undifferentiated priority signal** (REQUIRED #9) that looks like
  real information (every ticket has a Priority field) but doesn't
  actually rank anything, unlike case-011's "no priority stated at all" —
  a subtler trap than an absent field.
- **A correctness-bug cluster with a real, textually-recoverable shared
  mechanism but no formally declared shared file** (REQUIRED #10) — this
  is harder than the synthetic shared-file cases (008/009), which state
  the shared file outright; here the signal has to be read out of
  multiple tickets' independently-written failure descriptions.
- **A horizontal-enabler trap with a named-but-singular consumer**
  (REQUIRED #5), similar in shape to case-014 but drawn from a real
  ticket's own wording rather than authored to be clean.
- **Two ops-track tasks that are easy to either conflate into one
  invented fix, or to quietly merge under an unstated shared design**
  (REQUIRED #8) just because they're filed the same day and both concern
  "async metadata table operations" — the trap here is fabricating a
  connection or a unified implementation the tickets don't state, not
  which side of the grouping question a run lands on; distinct source
  tickets are not by themselves evidence that two delivery slices are
  required, any more than they'd be evidence that one merged slice is
  required.

This case does not exercise, and should not be graded on, a numeric-order
illusion (the real Jira IDs here roughly track real filing chronology, so
there isn't a strong instance of that dynamic in this window) or a
benchmarking/performance-verification task (the closest real candidate,
HUDI-2395, is test-infrastructure cleanup, not benchmarking) — see
`provenance/case-303/cutoff-rationale.md` for why those two target
dynamics from the design brief aren't well supported at this cutoff, and
should not be treated as something a correct run was expected to surface.
