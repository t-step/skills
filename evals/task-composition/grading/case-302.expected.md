# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** real-world-external-vs-internal-dependency (Apache
Cassandra CEP-7 / SAI, CASSANDRA-16052, snapshot at 2023-05-15)

**Source:** `evals/task-composition/provenance/case-302/` -- every
REQUIRED claim below cites a specific provenance file/fact, not general
familiarity with Cassandra or SAI.

## REQUIRED

1. **Recognizes CASSANDRA-18112 as blocked by something OUTSIDE the
   supplied task set, not by any other task in this list.** Per its own
   filed description, it needs an unresolved community mailing-list
   DISCUSS thread on CQL grammar before implementation can start, and the
   filer explicitly doubts the feature's own scope. No amount of
   engineering work inside this task set resolves that. A run that treats
   18112 as just another orderable/parallelizable task -- without naming
   this external blocker -- fails this expectation. *(Source:
   `cases/case-302/tasks.md` and `dependencies.md`, both quoting 18112's
   filed description directly.)*

2. **Recognizes CASSANDRA-18345 as reaching into shared, non-SAI-owned
   storage-engine machinery outside this task set** -- the SSTable
   format's fixed streamed-component set (`Components.STREAMING_
   COMPONENTS`), which every SSTable-based feature relies on, not
   something this task set owns or can unilaterally redefine without
   wider blast radius. A run does not need to use these exact words, but
   must distinguish this from an ordinary in-task-set dependency (e.g. by
   flagging it as a coordination/architectural-boundary concern, a risk
   requiring extra care, or similar). *(Source: 18345's own description
   in `tasks.md`; corroborated by the concrete, already-observed
   `SSTableFlushObserver` rebase coupling in `repository-state.md`.)*

3. **Does not treat CASSANDRA-18490 as independently completable/
   verifiable from CASSANDRA-18345.** 18490's stated goal includes
   checksum-validating SAI components "on... streaming," but 18345's own
   description establishes that streaming does not yet carry SAI's
   components at all. The report must name this as a real dependency or
   convergence point -- either by making 18490 explicitly depend on
   18345, or by naming a shared checkpoint/slice that covers both -- not
   by silently listing them as unrelated, independently schedulable
   tasks. *(Source: `dependencies.md`; strongly corroborated
   post-cutoff by the actual review history in
   `provenance/case-302/historical-outcome.md`, where reviewers
   explicitly linked the two and deferred checksum-validation failures
   from 18345's review into 18490 -- this corroboration is DIAGNOSTIC
   evidence the concern was real, not the basis for the requirement
   itself.)*

4. **Does not silently serialize CASSANDRA-18067 (on-disk numeric index,
   the stated active priority) behind the smaller cleanup/improvement
   tasks just because they share the SAI component/label.** None of
   18165, 18166, 18167, 18216, 18280, 18494, 18515, or 18521 state or
   imply a dependency on 18067 finishing; several explicitly target
   already-landed components (18216 modifies `MemtableIndex` from the
   already-merged 18058; 18165 is a review follow-up from the
   already-merged 18058). A run that blocks these behind 18067 "to be
   safe," without a stated reason grounded in the fixture, fails this
   expectation. *(Source: `dependencies.md`, "Not addressed by any of the
   above" section.)*

5. **Does not manufacture CASSANDRA-18166 (IndexContext code-model
   cleanup) as a horizontal enabler by claiming it unblocks two or more
   named downstream tasks.** Nothing in the record states or clearly
   implies any other task depends on 18166. It is fine to group it as a
   small standalone internal-cleanup slice, or fold it into general
   polish -- what's wrong is asserting enabler status (which the skill's
   own criteria require naming concrete unlocked downstream work for)
   when the source material doesn't support it. *(Source:
   `dependencies.md`, "IndexContext code-model cleanup" entry, explicitly
   framed as an open topology question, not a settled fact either way.)*

6. **Honors the one stated priority signal**: CASSANDRA-18067 (Phase 3 /
   on-disk numeric index) is named as the currently active priority item,
   distinct from the twelve other tasks, for which no relative priority
   is stated. A run does not need to schedule 18067 first, but it must
   not invent a different priority scheme, and must not claim priority
   information exists among the twelve smaller tasks where none is
   stated. *(Source: `source-notes.md`, "Stated priority" section, itself
   sourced from the epic's Nov 16, 2022 five-phase-plan comment.)*

## DEFENSIBLE EITHER WAY (must be stated, not silently assumed)

- **Whether CASSANDRA-18067, CASSANDRA-18345, and CASSANDRA-18490 are
  proposed as one convergence/integration slice, as three vertical
  slices with an explicit convergence dependency, or some other grouping
  that still names the interaction.** The actual historical record (see
  `historical-outcome.md`) shows the real Cassandra team developed these
  in parallel with a deliberated (and later revised) merge-order
  decision, not a strict "18067 must fully finish before 18345 or 18490
  start" gate. Do not require a specific sequencing choice here -- what's
  required is only that the convergence itself is named (see REQUIRED
  #3), not which specific slice shape resolves it.

- **Whether the CASSANDRA-18067/CASSANDRA-18494 (lucene-core) and
  CASSANDRA-18067/CASSANDRA-18280 (RAMIndexOutput) pairs are treated as
  parallel-safe or flagged as needing a closer look.** The record
  establishes a concrete shared-dependency/shared-utility fact for each
  pair (see `dependencies.md`) but does not state whether it actually
  creates a conflict. A run may reasonably call either pair parallel-safe
  or not -- what's required is that the shared exposure is at least
  named as a consideration, not asserted as settled independence without
  comment, and not used to fabricate a hard blocking dependency the
  record doesn't support either.

## Would be WRONG

- Treating CASSANDRA-18112 as resolvable by ordinary engineering work
  within this task set (assigning it to a slice with a normal
  implementation-and-test verification checkpoint, with no mention of the
  external design/DISCUSS blocker).
- Treating CASSANDRA-18345's fix as a self-contained, SAI-internal change
  with no wider architectural consideration.
- Listing CASSANDRA-18490 and CASSANDRA-18345 as fully independent,
  parallel-safe tasks with no dependency or shared-checkpoint relationship
  named between them.
- Fabricating a hard, stated dependency of the eight smaller tasks on
  CASSANDRA-18067 that the record does not support.
- Promoting CASSANDRA-18166 to enabler status while naming two or more
  specific downstream consumers the record does not actually support.
- Inventing a priority ordering among the twelve non-18067 tasks.
- Treating CASSANDRA-18167 as an equally concrete, ready-to-slice task
  when its own description offers no committed design and it remains
  unassigned -- a credible answer should at least note its scope is
  less settled than the others', though this is not separately scored
  beyond REQUIRED #4/#6 unless it drives a wrong claim there.

## DIAGNOSTIC / HISTORICAL COMPARISON (not pass/fail)

- The actual Cassandra team's June 19-20, 2023 review comments show they
  explicitly linked 18345, 18067, and 18490 in exactly the way REQUIRED
  #3 asks a report to recognize -- including deferring checksum-failure
  fixes from 18345's review into 18490's scope.
- The real merge order ended up 18345 (Jun 29) before 18067 (Jul 4)
  before 18490 (Jul 11) -- the reverse of the "wait for 18067" plan
  floated on Jun 19, 2023. No run should be scored against predicting
  this exact order.
- CASSANDRA-18112 remained unresolved for over two years past this
  fixture's cutoff (resolved Aug 2025), consistent with it needing
  external consensus rather than being an ordinary engineering task.
- CASSANDRA-18216 never merged (still "Review In Progress" as of
  2026-09-26) -- a real example of a concretely-scoped task stalling for
  reasons outside any dependency graph.
- The stated Phase 5 ("LIKE support") placeholder from cutoff
  (CASSANDRA-18493) was later restructured under an entirely different,
  later epic (CASSANDRA-19224) with child issues that didn't exist at
  cutoff -- corroborating this fixture's choice to exclude Phase 5 from
  the task list entirely rather than guess at its shape.
- SAI (including all thirteen tasks in this fixture) eventually shipped
  in Cassandra 5.0-alpha1/5.0, with the `cep-7-sai` branch merging to
  trunk on 2023-07-26.

## Why this fixture pressures the skill

This case is built from a real, messy, mid-flight open-source backlog
rather than an author-designed synthetic plan. It specifically targets:

- **External-vs-internal dependency discipline**: CASSANDRA-18112 (blocked
  by community process, not by anything in-set) and CASSANDRA-18345
  (reaching into shared, non-SAI storage-engine machinery) are both real,
  sourced examples the skill's own guidance calls out as something to
  "say so plainly" about rather than pretending the task set is
  self-contained.
- **A real convergence point** (18067 x 18345 x 18490) grounded in actual
  reviewer behavior, not invented for the fixture -- with the specific
  sequencing left appropriately open, since even the real team changed
  its mind about it.
- **Resisting layer-batching by label**: eight small, differently-shaped
  tasks share only the "SAI component" label; the skill should not
  serialize or bundle them together, or behind CASSANDRA-18067, purely on
  that basis.
- **Resisting manufactured horizontal-enabler status** for CASSANDRA-18166,
  which sounds architectural ("code model," "IndexContext") but has no
  stated downstream consumer -- exactly the failure mode the skill's own
  "sounding architectural is not the same as being shared" guidance
  warns against.
- **Respecting a stated priority signal** (Phase 3 / CASSANDRA-18067)
  without inventing a substitute ranking for the rest of the list.
