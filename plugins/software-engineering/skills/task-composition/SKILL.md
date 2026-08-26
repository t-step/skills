---
name: task-composition
description: >-
  Given an existing spec/plan and its decomposed tasks, partitions
  remaining work into agent-sized delivery slices: which tasks belong
  together and why, what each delivers end to end, dependencies on other
  slices, safe parallelism, and a verification checkpoint. Prefers
  vertical slices over layer-batching; allows a horizontal enabler only
  when it unlocks more parallel work; surfaces convergence points; runs
  only the minimal dependency check needed (cycles, numeric-order
  illusions, false-parallel work sharing an unmet prerequisite). Use once
  a plan/task list exists and someone asks how to split it into sessions,
  PRs, or agent assignments, or which tasks can run in parallel. Does not
  decompose a spec into tasks, choose what to build next or override
  priority (next-best-slice, next-best-change), plan one slice's
  implementation (slice-plan), or build a graph/scheduler/orchestration
  integration -- refuses to manufacture parallelism the dependencies
  don't support, reporting low or zero safe parallelism when honest.
---

# Task Composition

Somewhere between "here's the plan and its tasks" and "an agent is
actually executing something" sits a step nobody names: deciding what an
agent-sized unit of work actually is. Spec and planning tools produce a
numbered task list. Orchestrators can run several agents at once once
they're told what to run. Neither one decides which tasks belong in the
same session, which ones are actually independent, or where the plan's
real seams are versus where its task numbering just happens to fall.
Left unaddressed, the numbering itself quietly becomes the execution
plan -- one task per agent, in order -- which is usually wrong in both
directions: it splits work that has no useful checkpoint between its
parts, and it batches or serializes work that was actually independent.

This skill's only job is that missing step: take a plan and its tasks as
already decided, and shape them into delivery slices -- units sized for
one agent session, that deliver and verify one coherent piece of
behavior, that respect real dependencies, and that expose whatever
parallelism is actually safe. It does not decide what the plan should
contain, and it does not decide which slice runs first when priority is
someone's call -- it decides how the already-decided work should be cut.

A good delivery slice is defined by what becomes true once it lands and
passes verification -- an independently meaningful behavior, capability,
or system property that didn't exist before -- not by which files it
touches, which layer it lives in, or how conveniently its tasks happen
to batch together. Two tasks that touch the same directory are not
automatically the same slice; two that touch entirely different
directories are not automatically different slices. The question that
actually decides a slice's boundary is: what can someone now rely on,
verify, or build on top of, that they couldn't before this slice landed?

## Input boundary: the work is already decomposed

Assume the specification, planning, and task-decomposition work is
finished. Inputs may include a spec, an implementation plan, a task
list, explicit or inferable dependencies, stated priorities, and the
repository's current state. Do not re-run that process:

- Don't rewrite or second-guess the specification.
- Don't re-decompose a task that's too coarse into sub-tasks, or merge
  two tasks into one, in the source material itself -- slicing groups
  existing tasks into sessions; it doesn't edit the task list.
- Don't invent tasks the source material doesn't contain, even to fill a
  gap you can see. Name the gap as a topology problem instead (see
  "Minimal topology validation" below).

Only step outside this boundary when the source artifacts are
insufficient or internally inconsistent to the point that no credible
slice plan can be built from them at all -- and then say exactly what's
missing or contradictory, rather than quietly patching it by inventing
task content.

## Gather before slicing

1. **The tasks themselves** -- their IDs, descriptions, and whatever
   detail the plan gives about what each touches.
2. **Dependencies, stated or inferable.** A plan sometimes states them
   explicitly ("depends on #4"); more often they're inferable from what
   each task actually touches -- shared files, shared interfaces, a task
   that clearly can't work until another exists. Read the source
   material closely enough to tell the two apart from bare task-number
   order, which is not a dependency and often isn't even a hint of one.
3. **Priority, if the source material states one.** Carry it forward;
   don't derive a substitute.
4. **Current repository state.** What's already built changes what
   "remaining work" actually is -- a task the plan lists may already be
   done, partially done, or blocked by something the plan didn't
   anticipate.

If dependency information cannot be established with reasonable
confidence from what's actually there -- not stated, and not inferable
from a concrete shared file, interface, or precondition -- say so
plainly as an open topology question. Do not invent a plausible-sounding
topology to avoid an unsatisfying answer; a wrong invented dependency is
worse than an honestly flagged unknown, because it looks like it was
checked.

## Task IDs are not session boundaries

A task list's numbering is an accounting and decomposition artifact, not
an execution plan. Two failure modes to avoid symmetrically:

- **One slice per task**, just because the source plan enumerated tasks
  individually. This fragments coherent work into sessions with no
  independent checkpoint between them and multiplies review/merge
  overhead for no benefit.
- **One slice per feature area**, just because several tasks happen to
  concern the same feature. This can hide a real internal seam --
  a risk boundary, a natural parallel split, a place where a smaller
  checkpoint would have caught a problem earlier -- inside one
  oversized batch.

The right size is whatever causes one independently meaningful behavior,
capability, or system property to become true and verifiable in one
agent session -- not the numeric grouping the source plan happened to
use, not the largest batch that shares a feature name, and not the
tidiest pile of similarly-shaped work.

## Prefer vertical slices

Default to vertical delivery slices: a slice crosses whatever layers are
necessary -- data, logic, interface, tests -- to deliver and verify one
independently meaningful behavior, capability, or system property.
Implementation and its directly associated tests normally belong in the
same slice when there is no useful learning or checkpoint boundary
between writing the code and proving it works; splitting them apart
usually just adds a handoff with nothing gained.

### The vertical grouping test

For any proposed grouping, ask:

1. What new behavior, capability, or system property becomes true once
   this grouping lands and passes verification?
2. Can that become-true claim be verified independently of the other
   groupings in the plan?
3. Would a reviewer reasonably understand why this grouping matters from
   that answer alone, without being told only which technical layer or
   files changed?

If none of the three can be answered, the proposed grouping is probably
not a real vertical delivery unit yet -- it's a pile of related edits
still waiting to be shaped into one. Answering the test does not require
inventing product or UI language: "the runtime can now select and reject
execution-provider configuration correctly," "a coding-agent run can
invoke its bound tools without reaching another run's state," and "an
operator can perform an action through the API and get the expected
persisted result" are all valid answers to question 1, and none of them
is a technical-layer description like "adds config schema and
validation," "adds API and tests," or "implements an MCP server."

A grouping that fails question 2 -- nothing in the plan actually verifies
its become-true claim on its own, only "inspection" or "this will be
exercised indirectly once something else lands" -- is not a real slice
yet, even if it's a clean, self-contained diff. Fold it into whichever
grouping actually establishes and verifies the combined behavior, rather
than letting it stand alone with a note that verification is implicit or
manual. This also tightens the horizontal-enabler test below: a shared
prerequisite only earns independent status by unlocking two or more
separate downstream slices when each of those downstream groupings can
independently pass the vertical grouping test on its own. A piece that
can't be independently verified doesn't count as a second consumer --
it's still part of the one grouping that can be verified, and the
prerequisite's status as a standalone enabler should be judged against
that smaller, real set of consumers.

This question is about whether the plan specifies a verification path
for a grouping, not about whether that verification is predicted to
pass. If the plan pairs certain tasks with a test that would exercise
them together, compose the slice normally even when something about the
described implementation looks likely to fail once built -- name that as
a risk (see "Risk and checkpoint boundaries") rather than refusing to
produce a slice plan over it. Diagnosing or fixing a suspected defect in
already-decomposed tasks is out of this skill's scope; a defect that
would only surface once code is written and run is not the same thing as
tasks that cannot be composed into a slice plan at all.

### Not every grouping needs to be user-facing

Meaningful behavior is not synonymous with user-facing behavior. Do not
default to product or UI wording just because that's the easiest kind of
become-true claim to write. Isolation guarantees, validated
configuration behavior, provider dispatch capability, lifecycle
correctness, authorization boundaries, compatibility guarantees,
integration contracts, and recovery behavior are all independently
observable system properties that satisfy the vertical grouping test
just as well as an end-user-facing feature does -- what makes a grouping
valid is that its completion establishes something independently
observable or relied upon by the system, not that it happens to be
visible in a product UI. Forcing artificial product wording onto
genuinely internal work is its own failure mode, not a safer default.

The goal is delivered, verifiable behavior -- not maximum task count per
agent, and not organizing the plan by technical layer (all the schema
work in one slice, all the API work in another, all the UI work in a
third) merely because that's how the codebase's directories are
arranged or because the tasks happen to look natural to batch together.
Layer-batching is the specific anti-pattern this section exists to name:
it produces groupings whose completion means only "this technical layer
is done," not that any independently meaningful behavior became true --
it optimizes for tidy piles of similar work, not for anything an agent
can independently deliver or a reviewer can independently evaluate.

## Allow horizontal enablers, narrowly

Some work is genuinely shared infrastructure that several vertical
slices would otherwise need to duplicate, or that creates unsafe
coupling if left inside each of them separately. A horizontal enabling
slice is legitimate when keeping that work distributed across the
vertical slices it serves would cause real duplication, unsafe shared-
state coupling, or a structure that only exists because the work was
split arbitrarily rather than for a reason.

Every proposed horizontal enabler must state three things, or it doesn't
belong in the plan:

1. **Why it should exist independently** -- what would go wrong (not
   merely "feel less tidy") if it stayed embedded in the vertical slices
   instead.
2. **What downstream work it enables** -- named slices, not "future
   work in general."
3. **Whether completing it increases the amount of useful parallel work
   available.** An enabler that unblocks two or more vertical slices to
   run concurrently is earning its place. One that unblocks exactly one
   downstream slice is often just that slice's own prerequisite step,
   not a separate enabler worth naming.

A single diagnostic question ties these together: could this work be
absorbed into one downstream vertical grouping without duplication,
unsafe coupling, or materially reducing useful parallelism? If yes, it
probably should not be a standalone horizontal enabler -- fold it into
whichever vertical slice actually needs it. This is judgment guidance,
not a hard graph rule: a small foundation task that only one downstream
grouping will ever use, and that unlocks no additional concurrency, does
not earn independent status merely because it sounds architectural (an
interface, an abstraction, a shared module) -- sounding architectural is
not the same as being shared.

Keep every horizontal enabler narrowly bounded to what the downstream
slices actually need. Do not default to organizing work by technical
layer and calling the result "enablers" -- that's layer-batching wearing
a different name.

## Represent convergence explicitly

When independent slices must integrate before subsequent work is valid
-- two vertical branches that both touch a shared interface, a dispatch
layer that needs both sides finished -- name that convergence as its own
dependency, not an implicit assumption left for whoever runs the plan to
notice. A slice that can only start once two others are both done should
say so, listing both.

Integration or verification work earns its own slice when it represents
a real correctness boundary -- the first point where two independently
built pieces are actually exercised together and something could
genuinely be wrong. Purely mechanical final verification (a lint pass, a
build check, a changelog bump) does not need its own slice when
separating it from the last substantive slice would only add ceremony
with nothing to independently check; combine it with whatever slice it
mechanically follows.

## Assess safe parallelism, not maximum parallelism

For every pair of slices that don't depend on each other, decide whether
they can actually run concurrently -- not whether the dependency graph
merely permits it. Weigh:

- Shared files or interfaces both slices would touch -- a signal to look
  closer, not an automatic verdict either way. Two slices that touch the
  same file in clearly independent, stable regions or extension points,
  with no semantic dependency between their changes and a predictable
  way to combine them, can still be parallel-safe. Two slices that touch
  the same file or contract where the interface is still unsettled, the
  changes overlap in meaning, or one slice's edit would plausibly
  conflict with or invalidate the other's are not parallel-safe,
  regardless of whether the agents work in isolated branches. Working in
  separate workspaces and planning a later merge does not by itself make
  concurrent execution safe -- it only moves the conflict from write-time
  to merge-time. Isolation plus a merge step is worth naming as a
  coordination detail once parallelism is otherwise justified; it is
  never the reason parallelism is justified. What decides safety is
  semantic independence and a manageable convergence path, not pathname
  overlap and not workspace isolation.
- Architectural boundaries that keep the two genuinely separate versus
  ones that are separate on paper but share an implementation detail.
- Lifecycle or concurrency behavior either slice changes.
- Security or authorization boundaries either slice touches.
- How much uncertainty either slice's own scope still carries -- a slice
  whose boundary might shift once someone is in the code is a worse
  parallel-execution bet than one that's fully settled.
- Where the two would eventually need to integrate, and whether that
  integration point is already accounted for as convergence.

Two independent, cleanly bounded slices that can genuinely proceed
without touching each other are worth more than five slices that look
parallel on paper but actually share a file, an assumption, or an
interface neither has finished settling. It is a legitimate, useful
conclusion that available parallelism is currently low, or zero -- say
that plainly rather than inflating the count of "parallel" slices to
look more productive.

## Minimal topology validation

Check only enough to confirm the proposed slice plan can actually run --
not to build a standalone audit. Look for:

- Missing or ambiguous dependencies (see "Gather before slicing" above).
- Dependency cycles.
- Sequencing that the source plan's task numbering implies but nothing
  else actually supports -- a task numbered later that has no real
  dependency on an earlier one, or one numbered earlier that actually
  depends on something numbered later.
- Slices proposed as parallel that in fact share an unmet prerequisite
  neither has flagged.
- Convergence ordering that's actually invalid -- a slice scheduled to
  start before everything it converges on is done.
- Contention obvious enough to make proposed concurrent execution unsafe
  or counterproductive, even if nothing above formally forbids it.

This is a credibility check on the specific plan being proposed here,
not a durable dependency-management system. Do not build a graph
database, a scheduler, or persistent topology state to do it. A small
diagram or dependency list may be shown inline when it genuinely
clarifies the slice plan -- it is a byproduct of explaining the plan,
not a deliverable of its own.

## Risk and checkpoint boundaries

Some work deserves its own slice -- and its own verification checkpoint
before anything is built on top of it -- even when it could technically
be batched with adjacent work. Consider isolating a slice when it:

- Establishes a new architectural boundary.
- Changes concurrency or lifecycle semantics.
- Touches an authorization or security boundary.
- Establishes an API or contract that substantial downstream work will
  consume.
- Carries meaningful, currently unresolved uncertainty.
- Would benefit from real verification before anything depends on the
  assumptions it makes.

The purpose is reducing rework and protecting correctness by giving
dependents something verified to build on -- not adding isolation as
process for its own sake. A boundary that doesn't carry one of these
properties doesn't need its own slice just because it sounds important.

## Priority

If the source material states an explicit priority or ordering, respect
it as given. Do not invent a priority system, a scoring formula, or a
queue discipline to substitute for one that's missing, and do not decide
that a stated priority should be overridden for throughput or
theoretical-efficiency reasons -- that call belongs to a human or to
whatever capability owns prioritization, not to this one. When no
priority is stated, the recommended execution grouping in the report
(below) is a dependency-respecting default ordering, not a
prioritization -- say so plainly so it isn't mistaken for one.

## What this skill refuses to do

Even when a request bundles a reasonable slicing ask together with one
of these:

- Re-run specification, planning, prioritization, or task decomposition.
  If the task list looks wrong, thin, or internally inconsistent, name
  that as a blocker to a credible slice plan -- don't quietly rewrite,
  split, merge, or invent tasks to compensate.
- Choose which slice should be built first, override a stated priority,
  or decide what the project should work on next -- that's
  `next-best-slice` or `next-best-change`.
- Produce an implementation plan for any one slice -- behavioral
  contract, seams, invariants, verification detail. That's `slice-plan`,
  scoped to one already-chosen slice; this skill stops at proposing the
  slice boundaries themselves.
- Build a durable dependency graph, a graph database, a scheduler, a
  coordination ledger, a telemetry system, or any orchestration
  integration. A graph shown inline to explain the plan is fine; a
  system to maintain one is not this skill's job.
- Maximize the number of parallel slices for its own sake, or dress up
  speculative, contention-heavy splitting as safe parallelism to look
  more productive. Reporting low or zero safe parallelism is a valid,
  sometimes correct, outcome.
- Treat branch or workspace isolation, plus a later merge step, as
  sufficient justification on its own for parallelizing slices whose
  changes are semantically overlapping or touch an unsettled interface.
  Isolation defers a conflict; it doesn't remove one.
- Fabricate a dependency topology when the source material doesn't
  support one. Say plainly what's missing or ambiguous instead.
- Invent scheduling optimality, a durable work ontology, or a metrics/
  diagnostics layer on top of the slice plan. The plan is the
  deliverable; measuring it belongs elsewhere.

If a request bundles a legitimate slicing ask together with one of
these -- "slice this up and also tell me which one to do first," "and
build me a dependency tracker for it" -- say plainly that the extra part
is out of scope for this skill, then deliver the in-scope part: the
slice plan itself.

## Report

Use this exact structure. Slice IDs should be short and stable (`S1`,
`S2`, ...) so dependencies between slices can reference them plainly.

```
# Delivery Slices: <one line naming the plan/feature being sliced>

## Slices

### <slice id>: <name>
- Kind: <vertical delivery | horizontal enabler | convergence/integration
  -- omit this line entirely when no category adds useful information>
- Includes: <task IDs / work items in this slice>
- Delivers: <the independently meaningful behavior, capability, or
  system property that becomes true once this slice lands and passes
  verification -- phrased as what can now be relied on or verified, not
  which technical layer or files changed>
- Why grouped: <why these tasks belong together, and -- when relevant --
  why they don't belong with a neighboring slice instead>
- Depends on: <other slice IDs this slice needs finished first, or "None">
- Parallel-safe with: <slice IDs it can run alongside right now, or
  "None currently" -- with the reason if that's non-obvious>
- Verification checkpoint: <what establishes this slice is actually done
  and correct>
- Risk / uncertainty: <material risk, unresolved dependency information,
  or "None identified.">

<repeat per slice>

## Recommended execution grouping
<the dependency-respecting order or waves this implies, referencing
slice IDs -- explicitly not a priority call unless the source material
stated one (see "Priority" above)>

## Available parallelism
<which slices can safely proceed concurrently right now, and how many
independent branches that actually represents -- say plainly if this is
currently low or zero>

## Bottlenecks to more parallelism
<what would need to resolve -- a convergence point, an enabler, missing
information -- before more concurrent work opens up, or "None identified.">

## Topology issues
<missing/ambiguous dependencies, cycles, numeric-order assumptions that
don't hold up, false-parallel slices sharing an unmet prerequisite, or
invalid convergence ordering -- or "None identified.">

## Out of scope
<a one- or two-line reminder of what this plan deliberately does not
settle: no re-decomposition, no priority override, no scheduling or
graph infrastructure>
```

Leave a section's body as "None identified." rather than omitting the
heading -- an absent section reads as "not considered," which is worse
than an honest empty one.
