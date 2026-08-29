---
name: lifecycle-audit
description: >-
  Maps lifecycle-bearing entities in an implementation, subsystem, spec,
  or design -- owner, authoritative state, states, transition triggers,
  invariants, persistence, side effects, failure behavior -- only where
  evidence supports each field. For every interaction, separately answers
  how they connect (independent, sequencing-only, observation,
  projection/derivation, transition-triggering, or ambiguous) and whether
  a consistency requirement is real (no joint constraint, tolerable
  disagreement, or reconciliation) -- weakest supported answer per axis,
  never one label for both. Use when several stateful concepts appear
  together and there's a risk of inventing a coordinator, sync job, or
  orchestration layer before checking whether the lifecycles need
  coupling, or when asked to map lifecycles or vet a design's consistency
  claims. Refuses to propose a state-machine framework, recommend
  orchestration just because lifecycles exist, assume reconciliation is
  necessary, or treat every status field as its own lifecycle.
---

# Lifecycle Audit

When a design or an existing codebase surfaces more than one stateful
concept -- a job and a worker, a subscription and a payment, a document and
its search index, a task and its verification record -- there's a strong
pull toward reconciliation machinery: a coordinator, a sync job, a combined
state machine, an event bus, a "source of truth" table nobody quite owns.
Sometimes that machinery is genuinely necessary. Often it isn't -- the
lifecycles were never actually coupled, one was only ever observing the
other, or what looked like two lifecycles was one lifecycle and an
attribute wearing a costume. This skill's only job is to answer, with
evidence, which situation is actually in front of you, before anyone builds
something to solve a problem that doesn't exist.

It does not implement lifecycles, does not propose a framework for managing
them, and does not treat reconciliation as the default answer just because
reconciliation is the usual reflex here. On a system whose lifecycles turn
out to be independent or only loosely coupled, the correct output is "these
don't need to be coupled" -- stated plainly and left there, not softened
into a design recommendation nobody asked for.

## How this composes with the rest of this skill family

Reuse grounding that already exists rather than re-deriving it from
scratch -- but treat a sibling skill's report as grounding to build on, not
as an authority that decides this skill's own questions for it:

- **`repo-orientation`** may already show where a candidate entity's code
  and persistence actually live. If it exists for this target, use it as a
  pointer to where to look -- entry points, systems of record, executable
  paths -- not as a source of lifecycle facts; it doesn't characterize
  states, transitions, or invariants.
- **`domain-orientation`** may already establish what a concept means and
  note its own "Observed invariants / business rules." If a report exists
  for this target, reuse that as a starting point for this audit's own
  Invariants field rather than re-reading the same validation code cold --
  but confirm a reused rule actually constrains this entity's transitions
  before reporting it as a lifecycle invariant. A domain-level business
  rule and a lifecycle's own transition invariant (an illegal transition, a
  required precondition) are not automatically the same claim; a
  domain-orientation finding is evidence to check against this entity's
  actual transitions, not a lifecycle invariant already proven.
- **`state-ownership-audit`** may already determine a fact's authority and
  its consistency requirement with other representations, using the same
  mechanism/consistency vocabulary this skill defines. If a report exists
  for the fact in question, reuse its authority and consistency findings
  as evidence instead of re-tracing every write path this audit already
  traced. Authority over a fact is a different axis from lifecycle
  transition semantics: knowing who may write a value doesn't by itself
  decide what makes a transition legal, or which mechanism (independent,
  sequencing, projection, transition-triggering) connects two lifecycles --
  that classification, and the separate consistency-requirement judgment
  built on it, remain this skill's own to make.

Reused sibling output is grounding, not a verdict this skill inherits.
Keep mechanism and consistency evaluated independently of each other
exactly as "Characterize interactions" describes below, never inferring
one from a label a sibling report attaches to the other -- collapsing
mechanism into consistency (or the reverse) by inheritance is exactly the
mistake "Characterize interactions" exists to prevent when it happens
internally, and reusing another skill's conclusion is not an exemption
from that same discipline. If fresh evidence gathered for this audit
conflicts with a reused sibling finding, report the conflict explicitly
rather than silently preferring whichever report ran first; an earlier
report is prior grounding, not a settled fact this skill defers to.

If a target's complexity means one of these hasn't been run and would
materially change this audit's answer, say so and point at it, rather than
reconstructing a shallow version of its analysis inline.

## Ground before characterizing anything

The target can be broad -- an existing implementation, a feature or
subsystem, a specification or design doc, a proposed change, or a named set
of interacting entities. Whatever it is, read the actual code, schema,
spec text, or design doc for it before writing a single field. Do not
characterize a lifecycle from a plausible guess about how systems like this
"usually" work.

Use the same three evidence tiers as an orientation pass, applied per
field, not just per finding:

- **Observed** -- a state you can point to in code (an enum, a status
  column, a constant), a transition you can point to (the function/handler/
  event that performs it), or a spec sentence that states it directly.
- **Inference** -- one short, defensible step from something observed:
  "every write to this table happens inside the same handler that also
  flips `status`, so this table is that lifecycle's persistence" is
  inference. "This was probably designed to eventually support X" is not a
  short step from anything observed -- that's speculation, not inference.
- **Unknown** -- the evidence doesn't settle it. Say so. A field left
  unknown is a correct, useful output, not an incomplete one.

When a claim could go either way, use the weaker tier. An audit that
under-claims costs a reader a few minutes double-checking; one that
over-claims can send someone off building reconciliation machinery for an
interaction that was never actually there.

## What counts as a lifecycle

Not every field that holds more than one value is a lifecycle. Before
inventorying something as a lifecycle-bearing entity, check whether it
clears this bar:

- It has more than one state that matters to something other than display
  formatting.
- Something identifiable -- an event, an action, a handler, a state-machine
  definition -- causes it to move between states; it isn't just derived by
  re-computing a value from other data every time it's read.
- It has at least one invariant or legitimate-transition rule of its own
  (a state it can't reach directly from another, a precondition a
  transition requires).

If a "status" clears none of these -- it's just a computed label, or its
only legitimate values are entirely determined by another entity's own
state with no independent trigger or rule -- it's an **attribute of that
other entity**, not a separate lifecycle. Say so explicitly rather than
giving it its own inventory entry: "`Order.paymentStatus` is not an
independent lifecycle; it's a read-through projection of `Payment.state`,
recomputed on read, with no transition of its own" is a real, useful
finding, and a much smaller claim than a full lifecycle entry would imply.

The same discipline applies in the other direction: two things sharing a
name or a status vocabulary ("pending", "active", "closed") are not
automatically one lifecycle. Check whether they're actually the same state
machine (one owner, one authoritative representation, transitions that
affect both) or two distinct state machines that happen to use similar
words because the domain overlaps.

## Characterize each lifecycle-bearing entity

For each entity that clears the bar above, capture what the evidence
actually supports -- omit or mark **Unknown** any field it doesn't:

- **Entity** -- what it is, in the target's own terms.
- **Owner** -- the component, service, or module that decides its
  transitions. Not "who reads it" -- who has the authority to change it.
- **Authoritative representation & persistence** -- where the real state
  lives (a table, a document, an in-memory structure, a file) and whether
  that's the only place it's stored, or whether other locations hold
  copies/projections of it (flag those explicitly -- they matter for the
  interaction analysis below).
- **States** -- only the ones you can actually point to.
- **Transitions & triggers** -- what event, action, or condition causes
  each transition. A state diagram implied by code you haven't read is not
  evidence.
- **Invariants** -- rules the lifecycle must never violate (illegal
  transitions, required preconditions, uniqueness/ordering constraints).
- **Side effects** -- what else happens when it transitions (writes,
  notifications, downstream triggers) -- this is often where a second
  lifecycle turns out to be entangled with the first.
- **Failure / interruption behavior** -- what happens if a transition is
  interrupted partway, retried, or fails. "Unknown -- not addressed
  anywhere in the target" is common and worth stating exactly that way,
  since an unhandled partial-transition case is itself a finding.

Don't force a field that isn't there. A lifecycle with three clean states,
one owner, and no documented failure behavior is fully and honestly
characterized by saying exactly that.

## Characterize interactions -- this is the actual point

Enumerating lifecycles is preparation. The finding that matters is what
happens where two or more of them meet. For every pair (or small group)
that actually touches -- shares data, shares a trigger, or one's transition
visibly affects the other -- answer two separate questions, and keep them
separate. How two lifecycles connect and how tightly they must agree are
different facts: a transition-triggering connection can still tolerate
disagreement during its window, and a merely-sequenced pair can carry a
real shared invariant once both are running. Collapsing "how do they
connect" and "how tightly must they agree" into one label is exactly how
an interaction ends up sounding like it needs reconciliation when only the
connection, not any consistency requirement, actually turned out to be
real.

### 1. Mechanism -- how do they actually connect, if at all?

Pick the weakest mechanism the evidence actually supports:

- **Independent** -- no real interaction; they were only ever adjacent in
  the same workflow or the same file.
- **Sequencing / dependency only** -- B can't usefully start until A
  reaches some state, but nothing about B's own states or transitions
  changes because of A once that precondition is met. This is workflow
  ordering, not lifecycle coupling.
- **One-way observation** -- B reads A's state to decide something, but A
  never reads or reacts to B. This describes direction only: whether that
  read also happens to enforce a joint correctness property (versus merely
  informing B's own behavior) is a separate question, settled by the
  consistency axis below -- not implied by the direction itself. A live
  status check performed at the moment of a transition is a one-way read
  that can still be exactly what enforces a real shared invariant.
- **Projection / derivation** -- what looked like B's own state is actually
  computed or copied from A and carries no independent authority. Per
  "What counts as a lifecycle" above, B isn't really a second lifecycle
  here -- name it as a projection and stop; the consistency question below
  doesn't apply to it.
- **Transition-triggering** -- a transition in A directly causes a
  transition in B (or vice versa) as a side effect.
- **Ambiguous** -- the evidence doesn't establish how, or whether, they
  actually connect. Say what's missing rather than guessing.

### 2. Consistency requirement -- given that connection, how tightly must they agree?

Only ask this when the mechanism is something other than Independent or
Projection/derivation -- an independent pair has nothing to agree on, and a
projection has no independent state of its own to disagree with its
source. Otherwise, pick the weakest requirement the evidence actually
supports:

- **No joint constraint** -- nothing about correctness depends on the two
  staying in agreement.
- **Shared invariant, tolerable disagreement** -- some rule genuinely spans
  both (e.g., B can't reach "active" while A is "cancelled"), but observed
  or momentary disagreement doesn't break anything -- the system recovers
  the next time either side is read or acted on. This is a legitimate,
  common, often-correct design, not a bug to flag.
- **Requires active reconciliation** -- the two must be brought back into
  agreement by some active mechanism, because a specific correctness or
  safety property -- not general tidiness -- actually depends on
  convergence.
- **Ambiguous** -- the target implies two things should agree (a spec says
  "in sync," a comment says "should match") but never states which side is
  authoritative, when disagreement is acceptable, or what resolves it.
  Naming this precisely is more valuable than guessing an answer the
  target doesn't give.

These two questions are a starting vocabulary, not a rigid form to force
every interaction into. If the target's own evidence suggests a cleaner
description for either axis, use that instead and say why the vocabulary
above didn't fit.

### The central question, asked explicitly for every interaction

**Interaction does not imply shared ownership, synchronization, or
reconciliation.** Before concluding anything past "these touch," work
through these in order:

1. Is this actually one state machine described from two vantage points,
   rather than two lifecycles that interact? If merging the concepts loses
   no real distinction the target's own evidence draws, say that plainly
   instead of writing up a two-entity interaction at all -- see "What
   counts as a lifecycle."
2. Is one side already authoritative with the other a cache, index, or
   projection? If so, mechanism is Projection/derivation and the
   consistency question doesn't apply -- stop there.
3. Does B's own state ever need to *change* because A transitioned, or does
   B only ever *read* A? If B only reads A, the mechanism is One-way
   observation -- but mechanism and consistency are independent axes, so
   that alone settles nothing about consistency. Ask separately: does the
   read merely inform B's own behavior with no correctness property riding
   on it (No joint constraint), does it enforce a shared invariant that
   tolerates momentary disagreement, or does it participate in something
   stronger? A one-way read performed at the moment of a transition (a
   live check before proceeding) is a common way a one-way observation
   turns out to carry a genuine shared invariant, not evidence there's
   nothing to agree on.
4. If a joint constraint genuinely exists, would anything be operationally
   required to fix a disagreement, or would the system recover on its own?
   If the latter, the answer is Shared invariant / tolerable disagreement
   -- say so and stop.

Only past all four does "requires active reconciliation" become a
defensible answer -- and even then, name the specific invariant or
correctness property at risk, not a general sense that things "should"
stay in sync.

## Separate mechanical findings from design judgment

Some things this audit establishes are structural facts, checkable against
the target directly:

- "There are two persisted status fields: `Order.status` and
  `Fulfillment.state`."
- "The transition in `mark_shipped()` writes both records in the same
  function, no transaction."
- "No retry or dead-letter path exists for a failed `Fulfillment` write
  after `Order.status` has already moved to `shipped`."
- "`ProjectSummary` is regenerated from `events.jsonl` on every write; it
  has no independent persistence."

These carry high confidence and belong in the audit without much hedging --
they're either true of the target or they aren't.

Some conclusions require architectural or domain judgment past what the
target's evidence alone proves:

- "These should be one lifecycle."
- "This disagreement is semantically invalid."
- "This entity should own the authoritative state instead."
- "This workflow requires reconciliation."

State these as judgments, with the structural evidence that motivates them
named explicitly, not as facts with the same confidence as the mechanical
findings above. When the evidence doesn't clearly settle a judgment call,
say that too, and leave it for a human decision rather than picking a side
to sound conclusive.

## What this skill refuses to do

Even when a request bundles it in:

- Propose a generic state-machine framework, library, or runtime.
- Recommend orchestration, a coordinator, or a message bus merely because
  more than one lifecycle exists in the same system.
- Assume eventual consistency or reconciliation is necessary without
  identifying the specific invariant or correctness property that would
  break without it.
- Merge two lifecycles because doing so would be simpler to implement,
  when the target's own evidence shows they have distinct owners,
  invariants, or persistence.
- Invent states, transitions, or failure behavior the target doesn't show,
  to make an inventory entry feel complete.
- Confuse workflow ordering ("B can't start until A finishes") with
  lifecycle coupling that needs synchronization.
- Confuse a projection, cache, or materialized view with an authoritative
  lifecycle carrying independent state.
- Treat every status field, flag, or enum as its own lifecycle.
- Automatically recommend a new persistent entity, coordination table, or
  reconciliation job as the fix for a found interaction.
- Produce diagrams or elaborate artifacts when a concise prose analysis
  says the same thing.
- Redesign the subsystem, unless one specific finding directly requires a
  correction -- and then propose only that correction, not a broader
  rework.

If a request bundles a legitimate lifecycle audit with one of these --
"map the lifecycles and design the sync mechanism," "find the state
machines and build a coordinator" -- say plainly that the second part is
out of scope for this skill, then deliver the audit itself.

## Report

Use this exact structure. Omit no heading; use "None identified." or
"Not established from available evidence." rather than dropping a section
that came up empty -- an absent section reads as "not considered."

```
# Lifecycle Audit: <target>

## Scope and evidence inspected
<What was actually read (files, spec sections, schema) to ground this
audit. Name any existing repo-orientation/domain-orientation/
state-ownership-audit output reused, and anything relevant that could not
be inspected.>

## Lifecycle inventory
### <entity>
- Owner: <...>
- Authoritative representation / persistence: <...>
- States: <...>
- Transitions & triggers: <...>
- Invariants: <...>
- Side effects: <...>
- Failure / interruption behavior: <...>
(Any field: "Unknown -- <why the evidence doesn't settle it>" when it
doesn't. Omit the entity entirely, with a one-line note in "Findings," if
it turned out to be an attribute rather than a lifecycle -- see "What
counts as a lifecycle.")

## Lifecycle interactions
### <A> <-> <B>
- Nature of the interaction: <what actually touches, and how you know>
- Mechanism: <independent / sequencing-dependency-only / one-way
  observation / projection-derivation / transition-triggering / ambiguous,
  or a stated alternative>
- Consistency requirement: <not applicable (independent or projection) /
  no joint constraint / shared invariant with tolerable disagreement /
  requires active reconciliation / ambiguous -- with the specific
  invariant or correctness property at stake if reconciliation is
  required>

## Findings
### Structural (mechanical, high confidence)
<Facts checkable directly against the target.>

### Judgment calls (semantic, human decision needed)
<Conclusions that go past what the evidence alone proves, each with the
structural finding that motivates it.>

## Unresolved questions
<Real open questions the target's evidence doesn't settle -- who should own
X, whether disagreement between Y and Z is acceptable, what the intended
failure behavior is. These are for a human to decide, not to guess past.>
```

A target with one clean lifecycle and no meaningful interaction is fully
served by a short report that says so and stops -- padding it with
speculative interactions or hypothetical risks is a worse outcome than a
short, honest "nothing more to say here."
