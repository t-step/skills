# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** real-world-kafka-kip405-tiered-storage-spi (case-306)

**Nature of this case:** like cases 301-305, this is a real, messy
backlog pulled from the public Apache Kafka issue tracker and the KIP-405
wiki text (see `evals/task-composition/provenance/case-306/`), not an
author-designed fixture. It is graded on topology facts the record
actually supports, not on reproducing the historical PR/ticket grouping
or timeline. **This case is the deliberate mirror image of case-305.**
Case-305 pressured a run not to over-merge a large set of tickets that
shared a real, textually-established mechanism-level coupling into one
slice. This case pressures a run in the opposite direction: KAFKA-9548
(the tiered-storage SPI) is a real shared prerequisite with several
named, distinctly-owned downstream consumers — the question is whether a
run correctly recognizes that and gives it independent slice identity,
without either (a) inventing more or stronger multi-consumer evidence
than the record supports (two of the apparent "consumers," S3 and HDFS,
carry an explicit, primary-source caveat that they were never planned as
this initiative's own in-repo deliverables) or (b) using the real
coupling as an excuse to collapse everything into one indivisible
foundation slice. Several REQUIRED items below exist specifically to
catch a run that either under-credits or over-credits this enabler.

## REQUIRED

These are facts the record in `tasks.md`/`dependencies.md`/
`repository-state.md`/`source-notes.md` genuinely supports. A run that
violates one of these is wrong, not just less thorough.

1. **Does not treat KAFKA-9554 as an open, remaining task needing its own
   slice.** It was filed one day after KAFKA-9548 and closed the same day
   as a stated duplicate of it, with no remaining scope. A plan that
   lists it as a second, independent foundational task (its title,
   "Define the SPI for Tiered Storage framework," could tempt exactly
   this) is wrong.
   *(tasks.md, KAFKA-9554 entry; source-notes.md, "Already landed, not
   remaining work")*

2. **Recognizes KAFKA-9548 as a real, textually-established prerequisite
   for at least KAFKA-9549, KAFKA-9550, KAFKA-9555, and KAFKA-9579.**
   KAFKA-9549 and KAFKA-9555's own descriptions name the SPI directly;
   the KIP's own architecture text (quoted in `dependencies.md`)
   describes both KAFKA-9550's copy path and KAFKA-9579's fetch path as
   built on both SPI interfaces. A plan that treats KAFKA-9548 as an
   unrelated, independently-schedulable item with no stated connection to
   the rest of the set is contradicted by the record.
   *(dependencies.md, "Stated or clearly inferable")*

3. **Recognizes that the SPI has more than one real, distinctly-owned
   downstream consumer within this set, and gives it independent
   standing rather than treating it as a single-consumer prerequisite
   folded silently into someone else's slice.** At minimum, KAFKA-9549
   (one assignee, a distinct test-oriented subsystem) and KAFKA-9550/
   -9555 (a second assignee, the core production/framework track) both
   depend on the same interface shape — and KAFKA-9579 (RLM's fetch path)
   is a third real, textually-established consumer under yet a third
   assignee at cutoff (see REQUIRED #5's note on assignee overlap). A
   plan concluding "only one real consumer exists here, so the SPI
   doesn't need independent identity" is contradicted by this record —
   this is the sharpest instance of this case's central, mirror-image
   lesson from case-305.
   *(repository-state.md; dependencies.md, "Stated or clearly
   inferable")*

4. **Does not place KAFKA-9565 (S3) and KAFKA-9569 (HDFS) on the same
   in-scope-deliverable footing as KAFKA-9549/-9550/-9555/-9579 without
   naming the KIP's own stated intent for them.** The KIP's own text
   (quoted in `source-notes.md`) states directly that HDFS and S3
   implementations are planned to be hosted in external repositories,
   "inline with the approach taken for Kafka connectors" — not as part of
   this repository's own deliverable set — and KAFKA-9569's own
   description frames its purpose as verifying the SPI's sufficiency, not
   as a committed production backend. A plan may still list KAFKA-9565/
   -9569 (they are real, filed, assigned tickets) but must not use them,
   uncaveated, as the primary or sole evidence that "the SPI unlocks
   several parallel storage-backend teams," and must not present them as
   equivalent in kind to KAFKA-9549/-9555's clearly in-repo scope.
   *(source-notes.md, "The KIP's own text draws a line..."; tasks.md,
   KAFKA-9565/KAFKA-9569 entries)*

5. **Does not collapse all of KAFKA-9548, -9549, -9550, -9555, and -9579
   into one indivisible "tiered storage" slice on the strength of the
   shared SPI.** Recognizing real coupling (REQUIRED #2/#3) is not the
   same as concluding every SPI-consuming item must be composed as one
   unit — the record shows at least three genuinely separate
   assignees-at-cutoff across genuinely separate subsystems: KAFKA-9549
   (local/test implementation) under one, KAFKA-9550/-9555 (core RLM
   copy path and the production-default RLMM) under a second, and
   KAFKA-9579 (RLM's fetch path) under a third — the same one assigned to
   KAFKA-9569 (HDFS), the fixture's one genuine cross-scope assignee
   overlap. A plan must keep at minimum KAFKA-9549 visibly separable from
   KAFKA-9550/-9555, even if it also groups some subset of the SPI's
   consumers together.
   *(repository-state.md, assignee distribution; dependencies.md,
   "Shared-area signal, not a stated dependency")*

6. **Does not invent a merge-order or blocking dependency between
   KAFKA-9550 and KAFKA-9579.** The KIP's own text describes these as two
   separate thread pools triggered by different events (a scheduled copy
   interval versus an incoming consumer fetch), with no stated ordering
   between them and no cross-reference from either ticket to the other —
   and, at cutoff, no shared assignee either (see REQUIRED #5).
   *(dependencies.md, "Open questions the record does not resolve",
   second bullet; "Shared-area signal, not a stated dependency", second
   paragraph)*

7. **Does not overclaim the SPI's stability in either direction.** The
   record supports neither "the interface was already finished and
   settled at filing" (the KIP itself was still formally under
   discussion, not accepted, throughout this window and well beyond it)
   nor "downstream work here was blocked or unsafe until the interface
   was finalized" (the one piece of concrete implementation evidence —
   a linked work-in-progress fork PR — shows interface changes and a
   first consumer implementation being developed together, days after
   filing). A plan asserting either extreme as settled fact is wrong;
   treating this as a real, unresolved coordination question is correct.
   *(dependencies.md, "Open questions the record does not resolve", first
   bullet)*

8. **Does not treat KAFKA-9564 (the integration test framework) as a
   second independent horizontal enabler or foundation on the same
   footing as KAFKA-9548, merely because its title sounds architectural.**
   Nothing in the record shows any other item depending on KAFKA-9564's
   own completion; its only plausible relationship to the rest of the set
   is as a verification consumer of a concrete implementation (most
   plausibly KAFKA-9549's), not as something that itself unlocks further
   downstream production work. A plan that gives KAFKA-9564 the same
   "foundational/enabler" treatment as KAFKA-9548 is over-crediting an
   architectural-sounding name the way REQUIRED #1 warns against for
   KAFKA-9554.
   *(tasks.md, KAFKA-9564 entry; dependencies.md, "Open questions the
   record does not resolve", third bullet)*

9. **Does not invent a priority ranking, urgency signal, or deadline for
   any of the nine items beyond what the record states.** All nine carry
   the identical priority label; none carries a milestone, fix-version,
   or due date. A plan may note the assignee-based split described in
   `repository-state.md`, but must not turn that into a stated priority
   order, and must not invent one from filing date or issue number.
   *(dependencies.md, "No stated priority"; repository-state.md)*

10. **Does not invent concrete implementation detail beyond what a
    task's own text supports**, for any of the six items whose
    description is empty or a single line (KAFKA-9548, KAFKA-9550,
    KAFKA-9564, KAFKA-9565, KAFKA-9569, KAFKA-9579). A plan may
    reasonably describe what each is *for*, using the KIP's own
    architecture text where it exists (as `dependencies.md` does for
    KAFKA-9550/-9579), but must not present invented class names, method
    signatures, or design decisions beyond that as the ticket's own
    stated content.
    *(tasks.md, entries with no description text)*

11. **Does not treat "all nine items already appear under KAFKA-7739"
    as a curated, hand-sequenced roadmap signal.** `repository-state.md`
    states this linkage is a structural, automatic tracker feature (every
    subtask of an umbrella ticket appears there the moment it's filed),
    not a maintained checklist that implies review, ordering, or intent
    beyond "this has been filed." A plan that treats the umbrella's
    subtask list as evidence of a deliberate sequence or an implicit
    priority ranking overclaims what that link means.
    *(repository-state.md, last bullet)*

## DEFENSIBLE EITHER WAY

Genuine open questions the record doesn't resolve. Both answers are
acceptable as long as the choice is stated, not silently assumed, and
doesn't cross into a REQUIRED violation above.

- **Whether KAFKA-9548's two interfaces (`RemoteStorageManager` and
  `RemoteLogMetadataManager`) are composed as one slice (matching how
  they're actually filed, as a single ticket) or split into two
  conceptually distinct slices.** The KIP's own design text treats them
  as two separate contracts bundled into one ticket "since remote storage
  is separated from the remote log metadata store" — either grouping
  choice is defensible as long as it's stated.
- **Whether the SPI is treated as a hard, blocking prerequisite that must
  fully land before any of KAFKA-9549/-9550/-9555/-9579 begins, or as a
  convergence point that early/draft downstream work can proceed
  alongside** (per REQUIRED #7, neither extreme may be asserted as
  settled fact, but a plan must still choose *some* practical sequencing
  or concurrency stance to be useful) — both a conservative
  (interface-first) and a concurrent (co-develop, converge later)
  approach are defensible outcomes of this case's central, genuinely
  unresolved tension.
- **Whether the SPI (KAFKA-9548) is judged to pass this case's own
  independent-verifiability question on its own terms, or is folded into
  whichever slice first exercises it (most plausibly paired with
  KAFKA-9549).** The record supports a narrow verification bar for the
  SPI by itself ("package with interfaces and key objects available and
  published for review," per KAFKA-9554's own description of what "done"
  means) but no standalone runnable test suite independent of some
  implementation. A plan may reasonably keep the SPI as its own slice
  (citing its multiple named downstream consumers) or fold it into its
  first paired implementation (citing weak independent verifiability on
  its own) — either is a defensible resolution of this case's central
  question, not a REQUIRED-level fact either way.
- **Whether KAFKA-9549 (local implementation) and KAFKA-9564 (integration
  test framework) are composed as one slice or kept separate.** Both are
  assigned to the same engineer and plausibly form one natural delivery
  ("a local implementation, tested"), but nothing in the record states
  they must be combined.
- **Whether KAFKA-9550 (RLM copy path) and KAFKA-9579 (RLM fetch path)
  are composed as one "RemoteLogManager" slice or kept as two separate
  ones.** Both belong to the same new component named in the KIP, even
  though they do not share an assignee at cutoff (see REQUIRED #5) — the
  KIP's own text describes them as architecturally distinct thread pools
  (REQUIRED #6) — either grouping is defensible as long as no invented
  ordering between them is introduced.
- **How KAFKA-9565 and KAFKA-9569 are handled in the final slice plan**
  — as their own (externally-scoped-and-flagged) slices, folded into one
  "out of this initiative's direct scope" note, or omitted from the
  slice plan's main sequence entirely while still being named as tracked
  tickets that exist. Any of these is acceptable as long as REQUIRED #4's
  caveat is stated somewhere.

## DIAGNOSTIC / HISTORICAL COMPARISON (informational only — not pass/fail)

- KAFKA-9548 (the SPI) was not merged to the official Apache Kafka
  repository until **2021-03-03** — over a year after this fixture's
  cutoff — via a pull request that touched only interface/data-class
  files, no implementation code. This is the ticket's *eventual* shape,
  long after any plan built from this fixture would have run its course;
  it is not evidence that a cutoff-time plan should isolate the SPI into
  its own slice, nor evidence that it shouldn't.
- KAFKA-9549 (local implementation) was marked "Fixed" on 2020-04-27, but
  no pull request referencing it was ever opened against the official
  Apache Kafka repository — its resolution rests entirely on fork-only
  work. The package path used in that fork's SPI-and-implementation PR
  (`org.apache.kafka.common.log.remote.storage`) differs from the package
  path the interfaces eventually landed under on trunk
  (`org.apache.kafka.server.log.remote.storage`) — concrete, if narrow,
  evidence that the interface's own shape (down to its package location)
  was still moving between this fixture's cutoff and its eventual
  official landing.
- KAFKA-9565 (S3) was ultimately closed **Won't Fix** in 2023, on the
  explicit stated grounds that concrete `RemoteStorageManager`
  implementations were never going to be hosted in the Apache Kafka
  repository — directly confirming the KIP's own cutoff-time statement
  (REQUIRED #4) rather than contradicting it.
- KAFKA-9569 (HDFS) was marked "Fixed" in 2021, but no pull request
  referencing it was ever found against the official repository, and a
  2023 comment asking whether the resulting plugin was available
  anywhere went unanswered — consistent with REQUIRED #4's caution not
  to treat this ticket's existence as proof of a committed in-repo
  deliverable.
- KIP-405 itself was not marked "Accepted" until sometime between
  2021-02-15 and 2023-09-17 (the exact date wasn't pinned down further;
  it remained "Discussion" as late as one week before KAFKA-9548's own
  official merge) and the feature's GA announcement was added to the KIP
  text as late as 2025-04-01 — confirming this was a genuinely
  multi-year initiative, not something a Feb-2020 cutoff plan could have
  known the timeline for.
- A real, later, additional consumer of the same SPI did eventually
  appear — KAFKA-12458 (Azure Storage integration), filed 2021-03-12,
  thirteen months after this fixture's cutoff and nine days after the
  SPI's own official trunk merge. This is the closest real analogue to
  the mining pass's "multiple parallel storage-backend consumers"
  hypothesis, but it arrives well after the interface had actually
  stabilized on trunk — not during this fixture's own cutoff window —
  and is not something a plan built from this fixture's five files could
  have named.

## Why

This fixture is built to test the opposite failure mode from case-305.
Case-305 gave a run strong, textually-established coupling across a large
ticket set and tested whether it would resist collapsing all of it into
one slice. This case gives a run a real, if more modest and more
textured than the initial mining pass suggested, horizontal enabler
(REQUIRED #2/#3), embedded in a set that also contains:

- **A trap that looks like more of the same signal but isn't** (REQUIRED
  #4) — KAFKA-9565 and KAFKA-9569 are textually SPI-consuming, filed the
  same week, each with a named assignee, exactly like KAFKA-9549 — but
  the KIP's own design text states, in advance, that these two were never
  planned as this initiative's own in-repo deliverables. A run that
  counts these two uncritically toward "the SPI has many consumers"
  isn't wrong that they're SPI-consuming — it's wrong to treat that as
  equivalent evidence to KAFKA-9549/-9555's clearly in-scope status
  without reading past the ticket title to the KIP's own stated intent.
- **A trap that looks architectural but carries zero real scope**
  (REQUIRED #1) — KAFKA-9554, filed the day after the real SPI ticket
  with an almost identical title, closed as a duplicate the same day.
- **A trap that looks architectural but isn't a second enabler**
  (REQUIRED #8) — KAFKA-9564's "framework" naming invites treating it as
  another piece of shared infrastructure, when the record shows it's a
  verification consumer of one concrete implementation, not something
  that itself unlocks parallel work.
- **A genuine, unresolved tension the record does not settle** (REQUIRED
  #7, DEFENSIBLE) — whether the SPI needed to be finished before
  downstream work began. Real evidence exists on both sides (an
  unaccepted KIP; concurrent fork-based co-development), and this
  fixture does not force a resolution either way.
- **A genuine, unresolved tension about the SPI's own independent
  verifiability** (DEFENSIBLE) — the record supports a narrow
  "reviewed and published" bar but no standalone test suite, directly
  engaging SKILL.md's own vertical-grouping verifiability question
  without an unambiguous answer either way.

The central anti-overfit check applied while drafting this key: every
REQUIRED item above was checked against "would this still make sense if
SKILL.md did not exist?" — each traces to a specific primary-source fact
(a ticket's own stated scope, the KIP's own architecture or scope text, an
absence of stated links, an identical priority label across all nine
items), not to a restatement of SKILL.md's own three-part enabler test
dressed up as a historical fact. See
`provenance/case-306/cutoff-rationale.md`'s "Claim 10" for the specific
self-check performed on this point.

This case does not exercise, and should not be graded on, a numeric-order
illusion (the nine tickets file in essentially chronological order within
one narrow week, with no dependency riding on that order), a
community-external process gate comparable to case-302's mailing-list
DISCUSS block (nothing in the record shows any of these nine tickets was
formally *blocked* pending KIP acceptance — work proceeded regardless), or
a resource-manager-style "one discovered bug, several separately-fixable
instances" cluster shape identical to case-304's (this case's shared
prerequisite is a designed interface filed before its consumers, not a
bug discovered after several already-existing components shipped) — see
`provenance/case-306/cutoff-rationale.md` for why these aren't well
supported at this cutoff and should not be treated as something a correct
run was expected to surface.
