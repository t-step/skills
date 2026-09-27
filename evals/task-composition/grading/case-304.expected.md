# Expected outcome (for grading, not shown to the agent under test)

**Scenario:** real-world-kep753-sidecar-containers (case-304)

**Nature of this case:** like cases 301-303, this is a real, messy plan
pulled from public Kubernetes GitHub history (see
`evals/task-composition/provenance/case-304/`), not an author-designed
fixture. It is graded on topology facts the record actually supports, not
on reproducing the historical PR grouping or timeline. Several points
below are intentionally left open in the fixture itself — a correct run
should surface that openness, not resolve it with invented confidence.
**The central design lesson for this case (see `RESULTS.md`'s
introduction to this case): historical evidence can constrain a slice
topology without determining a unique one.** Ticket identity, PR identity,
component identity, chronological adjacency, thematic similarity, and
historical execution grouping are none of them, by themselves, a mandatory
delivery-slice boundary. Several REQUIRED items below are written as "does
not do X" for exactly this reason — the record rules out specific wrong
moves without mandating one specific right topology.

## REQUIRED

These are facts the record in `tasks.md`/`dependencies.md`/
`repository-state.md` genuinely supports. A run that violates one of these
is wrong, not just less thorough.

1. **Does not treat already-landed work as remaining work.** The base
   SidecarContainers implementation (referenced in `repository-state.md`
   as "a single already-merged pull request"), the kubectl describe-nodes
   fix, and the LimitRanger fix (both named in `source-notes.md` under
   "Already landed, not remaining work") must not appear in the plan as
   open tasks needing a slice.
   *(source-notes.md, "Already landed, not remaining work";
   repository-state.md)*

2. **Does not invent a concrete implementation design for MEM-119442,
   DEV-119442, or TOPO-119407.** As filed, MEM-119442 and DEV-119442 are
   each only a maintainer's comment naming a code location with the same
   coalescing pattern as CPU-119447 — no proposed fix, no PR. TOPO-119407
   is even thinner: a two-sentence TODO with a self-assignment and no
   further discussion. A correct run treats these as named-but-unscoped,
   not as fully specified implementation tasks with invented file names,
   function signatures, or a design mirrored wholesale from CPU-119447's
   (not-yet-merged, not-yet-visible-as-a-diff) approach.
   *(tasks.md, MEM-119442/DEV-119442/TOPO-119407 entries;
   dependencies.md, "Open questions")*

3. **Does not present CPU-119447, MEM-119442, and DEV-119442 (or
   TOPO-119407) as fully independent/parallel-safe with no mention of
   their shared discovered root cause.** All three (and, more weakly,
   the fourth) trace to one comment thread identifying the same
   AddContainer-style coalescing pattern across managers. A plan may
   still choose to slice them separately (see DEFENSIBLE below) — what's
   required is that the shared-area signal gets named somewhere, not a
   particular resulting topology.
   *(dependencies.md, "Stated or clearly inferable" and "Shared-area
   signal, not a stated dependency")*

4. **Does not invent a merge-order or blocking dependency *among*
   CPU-119447, MEM-119442, and DEV-119442** (e.g. "memory/device manager
   fixes can't start until CPU-119447 merges"). `repository-state.md`
   states plainly that each lives in its own kubelet package with no
   shared file and no import relationship for this logic. Sharing a root
   cause is not the same as one blocking the others; over-serializing
   this cluster on that basis is a topology error the record doesn't
   support, distinct from item 3's shared-area-signal requirement.
   *(repository-state.md; dependencies.md, "Shared-area signal")*

5. **Recognizes TOPO-119407 as materially different in stage/commitment
   from MEM-119442 and DEV-119442, not simply a fourth instance of the
   same status.** It is tracked in a separate issue, has no maintainer
   naming a specific code fix (only the reporter's own vague TODO, plus a
   maintainer's triage acceptance with no code-location analysis), and has
   had no further discussion beyond the day after it was opened. A plan
   that lists "CPU, memory, device, topology manager fixes" as four
   uniformly-staffed, uniformly-scoped items is missing a distinction the
   record draws directly.
   *(tasks.md, TOPO-119407 entry; dependencies.md, "Open questions",
   first bullet)*

6. **Shows E2E-119014 as depending on both E2E-119019 and E2E-30281**, not
   as parallel-safe with either. The umbrella e2e issue's own checklist
   states this order explicitly (recovered from the issue's pre-cutoff
   edit history, not its current, later-edited body — see
   `provenance/case-304/sources.md`).
   *(dependencies.md, "Stated or clearly inferable", first bullet)*

7. **Does not claim E2E-119019 or E2E-30281 are nearly finished, or assign
   them a specific expected landing time.** Both are open, in-review pull
   requests with no stated ETA anywhere in the record; treating "has an
   open PR" as "almost done" overclaims what open-and-under-review
   actually establishes at this cutoff.
   *(tasks.md, E2E-119019/E2E-30281 entries)*

8. **Does not fold HPA-119991 into the CPU/MEM/DEV/TOPO cluster, and does
   not invent a dependency between it and any of them.** It lives in a
   different binary (`kube-controller-manager`, not the kubelet),
   addresses the same *conceptual* gap through a completely separate code
   path, and nothing in either record references the other.
   *(dependencies.md, "Shared-area signal, not a stated dependency",
   second paragraph; repository-state.md)*

9. **Does not present REGR-120247 as already resolved, or present either
   of its two same-day draft pull requests (or either reviewer's preferred
   approach on them) as the settled fix.** As of cutoff, `#120267` (marked
   "DO NOT MERGE," an e2e reproduction) is open and unreviewed; `#120269`
   (a candidate restart-order fix) received same-day review comments with
   an active, unresolved disagreement between the assignee and a senior
   reviewer over whether that fix is sufficient or a broader feature-gate
   restoration is needed instead. Either way, the record explicitly states
   it isn't settled whether one fix or more than one will be needed.
   *(tasks.md, REGR-120247 entry; dependencies.md, "Open questions",
   third bullet)*

10. **Does not fabricate a dependency linking REGR-120247 to the
    CPU/MEM/DEV/TOPO resource-manager cluster.** Both are post-alpha
    kubelet bugs discovered in the same general window, but REGR-120247's
    stated root cause (insufficient feature-gate guarding in the base PR)
    is a different mechanism from the managers' coalescing bug. A plan
    that lumps them together as "the fifth manager issue" because both
    are 1.28 kubelet regressions from the sidecar work is manufacturing a
    connection the record doesn't state.
    *(dependencies.md, "Stated or clearly inferable", third bullet;
    repository-state.md)*

11. **Does not invent a priority ranking or a "must land before beta"
    urgency for any task, and does not extend REGR-120247's own priority
    labels to any other item.** REGR-120247 is the one exception to an
    otherwise unprioritized backlog: it carries `priority/important-soon`
    then `priority/critical-urgent`, both applied the day it was filed. No
    other issue or pull request in the cutoff-visible record carries a
    priority label or a stated deadline; the KEP's own alpha/beta milestone
    targets are context, not a per-task priority signal. A plan may treat
    REGR-120247 as more urgent than the rest (the record supports that),
    but must not claim the reverse (that nothing here has any priority
    signal) or apply REGR-120247's urgency to the resource-manager cluster
    or the e2e-coverage items.
    *(dependencies.md, "No stated priority (one exception)"; source-notes.md,
    "Stated milestones")*

## DEFENSIBLE EITHER WAY

Genuine open questions the record doesn't resolve. Both answers are
acceptable as long as the choice is stated, not silently assumed, and
doesn't cross into a REQUIRED violation above.

- **Whether CPU-119447, MEM-119442, and DEV-119442 (and/or TOPO-119407)
  are composed as one grouped "resource-manager restartable-init-container
  fix" slice (naming each manager as a named sub-item) or as three-to-four
  separate slices.** The record supports either: it establishes a shared
  discovered root cause (REQUIRED #3) without establishing a merge-order
  dependency between them (REQUIRED #4) or a stated commitment that they
  ship together. This is the sharpest instance of this case's central
  lesson — a shared root cause is real evidence, but it doesn't by itself
  select a unique slice count.
- **Whether TOPO-119407 is grouped into that same slice/cluster (with its
  thinner status called out) or kept as its own, clearly-flagged, lower-
  confidence item.** Either is fine as long as REQUIRED #5's distinction
  is preserved.
- **Whether E2E-119019 and E2E-30281 are treated as two separate slices
  feeding into E2E-119014, or folded together into one "e2e harness
  prerequisites" slice with E2E-119014 as a following convergence step.**
  Either is fine as long as REQUIRED #6's dependency direction is
  preserved.
- **Whether REGR-120247 is scoped as a single "investigate and fix" task
  or explicitly flagged as "possibly more than one fix."** Either is fine
  as long as REQUIRED #9 isn't violated by presenting one draft as
  settled.

## DIAGNOSTIC / HISTORICAL COMPARISON (informational only — not pass/fail)

- Historically, REGR-120247 needed a third, separate pull request
  (`#120281`, opened the day after cutoff) distinct from both same-day
  drafts; `#120269` (one of the two drafts open at cutoff) also
  eventually merged, months later, alongside the CPU-manager fix. Neither
  draft turned out to be a dead end, and more than one fix really was
  needed — consistent with REQUIRED #9, not a contradiction of it.
- Historically, three of the four "manager" items (CPU, device, memory)
  merged within about 24 hours of each other two months after this
  fixture's cutoff (2023-10-31/11-01), while the topology-manager item saw
  no PR at all for roughly 18 months, well after the umbrella issue that
  named all four had already been closed as "fixed." This is offered as
  background on how asymmetric the four items' actual paths turned out to
  be — not something a cutoff-time plan could have predicted, and not a
  basis for requiring a specific slice count (see DEFENSIBLE above).
- A stated priority ("I'd like this to be addressed before SidecarContainers
  graduates to the beta") appears in the real record, but not until
  2023-09-16 — over two weeks after this fixture's cutoff. It is
  DIAGNOSTIC only and must not be treated as something the cutoff-visible
  record already established (see REQUIRED #11).
- The e2e kubelet-restart test (E2E-119019) took nearly a year past cutoff
  to merge (2024-07-24), far longer than any of the manager fixes it
  shares only a thematic "sidecar hardening" connection with.

## Why

This fixture pressures the skill along an axis the other real-world cases
(301-303) approach from different angles but don't isolate as sharply:
**a historically real, textually-grounded shared root cause that does not,
by itself, determine how many slices the resulting work should become.**

- **Cases 301-303 each have their own version of "don't overclaim
  parallel safety"** (case-301's same-class shared-file pairs, case-302's
  CASSANDRA-18345 shared-machinery risk, case-303's rollback/restore
  bootstrap-check cluster). This case sharpens that same axis to its
  purest form: three (arguably four) tickets that share one *named,
  quoted, comment-thread-traceable* root cause, live in verifiably
  separate files/packages, and have zero stated merge-order or ownership
  relationship to each other. Historical outcome (three landing within a
  day, one stalling 18 months) shows the record's own ambiguity was real,
  not a fixture-construction artifact — the four items really weren't on
  one track.
- **An asymmetric-readiness trap inside what reads as one checklist**
  (REQUIRED #2, #5): the umbrella issue's title names four managers
  side by side, but the four are not equally staffed, scoped, or
  committed as of cutoff — a subtler version of case-301's
  "IGNITE-24850 sounds foundational but is actually gated" trap, applied
  to a horizontal cluster instead of a single ticket.
- **A same-day, same-author, multi-draft investigation that must not be
  fragmented into invented separate tasks** (REQUIRED #9, #10) — a new
  dynamic not present in cases 301-303, testing the opposite failure mode
  from over-serialization: manufacturing task identity from PR identity
  when the underlying investigation hasn't yet resolved into one.
- **A real cross-binary independence claim that must not be
  under-credited by proximity** (REQUIRED #8): HPA-119991 sits right next
  to the manager cluster in the issue tracker's timeline and shares
  vocabulary ("restartable init container... resource... calculation")
  but has zero code or file relationship to it.

This case does not exercise, and should not be graded on, a numeric-order
illusion (issue/PR numbers here track filing chronology closely enough
that there's no strong instance of this dynamic), a community-external
blocker comparable to case-302's mailing-list DISCUSS gate, or a
benchmarking/performance-verification task — see
`provenance/case-304/cutoff-rationale.md` for why these aren't well
supported at this cutoff and should not be treated as something a correct
run was expected to surface.
