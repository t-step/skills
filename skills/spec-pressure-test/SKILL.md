---
name: spec-pressure-test
description: >-
  Adversarially pressure-tests a spec/plan/design doc before
  implementation begins: builds concrete scenarios (state/transitions,
  invariants and enforcement boundary, ownership, concurrency/staleness,
  failure mechanics, collaborator composition, cardinality/identity) to
  find where the contract lets implementers diverge, contradicts itself, or
  can't be enforced by its owner. Each finding names the spec statement(s),
  a counterexample scenario, the consequence, and the smallest closing
  question -- an unsupported worry is not a finding.
  Sorts survivors into blocking / material gap / intentional freedom /
  already constrained, checking companion artifacts first. Use
  before implementation starts on a document with stated requirements, not
  a bare feature description. Distinct from a requirements-quality sweep, a
  cross-artifact coverage check, a spec-editing clarify loop, a diff review
  (slice-review), or a lifecycle inventory (lifecycle-audit) -- refuses to
  rewrite the spec, decompose tasks, or pick a resolution.
---

# Spec Pressure Test

A spec can be internally coherent on the happy path and still be a bad
contract to start building against. The habit this skill exists to break:
reading a spec, nodding at the user stories, checking that the requirements
are grammatically clear, and calling it ready -- without ever trying to
break it. A spec that reads cleanly top to bottom has told you it's
well-written. It hasn't told you it's *decided*.

The question this skill keeps in front of itself for every line it reads is:
**what assumption does this spec make that has not yet been forced to become
explicit?** Not "is this well-written" (that's a requirements-quality
checklist's job) and not "is this internally consistent with the plan and
task list" (that's a cross-artifact analysis's job) -- specifically: if two
competent, good-faith implementers each built this from the words on the
page alone, could they produce something that behaves differently in a way
that matters, or could neither of them build it at all because two of its
own requirements can't both be satisfied?

Do this by trying, concretely, to break the spec -- not by reading it a
second time more carefully. A finding here is a scenario, not an
impression.

## Ground before pressure-testing

Read the actual document, not a summary of it:

- The spec itself, in full -- every user story, requirement, edge case, and
  assumption it states. A requirement you haven't read cannot be pressure-
  tested; don't attack a paraphrase of it.
- Companion artifacts when they exist -- a plan, a data model, contracts,
  research notes, an existing requirements-quality checklist. These often
  settle exactly the question a shallow read of the spec alone would flag as
  open; skipping them produces false findings.
- Repo-level architecture, decision, and instruction documents relevant to
  the spec's domain (an ADR/decision log, a constitution or principles
  file, `AGENTS.md`/`CLAUDE.md`) -- needed to judge "already constrained"
  honestly rather than guessing.
- If the spec states it revises or extends already-implemented behavior
  (a baseline pointer, an explicit "does not reopen X's settled decisions"
  note), read the actual owning code, schema, or tests for the parts it
  doesn't re-litigate -- but only to confirm what the spec itself points at
  as settled. See "Ground 'already constrained' honestly" below for the
  limit on this.

**A target with no stated behavior isn't ready to pressure-test.** A one-line
feature description, a title, or a spec with no functional requirements and
no acceptance scenarios has no contract in it yet to attack -- inventing
requirements in order to then find gaps in them produces findings about a
document that doesn't exist. Say so and stop; the verdict is **Unable to
pressure-test** (see Report), not a thin pass through invented material.

## Seven ways to try to break the contract

For each, the question is never "does the spec mention this topic" -- it's
"can I construct a concrete scenario, inside what the spec itself claims is
in scope, where the written requirements stop determining a single
behavior." Treat these as places to look, not boxes to fill; a spec that
gives one of them nothing to say gets nothing written about it in the
report (see "Every candidate must survive three tests" below) -- these are
not eight required findings per spec.

**1. State and transition integrity.** What states does an entity the spec
describes actually have, and what makes a transition legal? Push on:
repeating an operation that already succeeded (is it a no-op, an error, or
undefined?), an operation interrupted partway and retried, a transition the
spec's own state list implies should be reachable but no requirement
actually describes how to reach it, and a terminal state that something
else in the spec still expects to act on. "The item's status is open, done,
or superseded" is a states list, not a transition contract, until something
says what makes each transition legal and what happens if you attempt an
illegal one or repeat a legal one.

A state with zero described exit transitions is not automatically a
finding-free deferral, even when the spec explicitly defers "what happens
next" as future work. Before treating a missing exit as safe to leave
open, check whether some *other* stated requirement's guarantee quietly
depends on that state eventually being left -- a storage-hygiene rule that
only ever fires on a transition this state can never reach, a recovery
promise that has nowhere to route to. If one does, the missing exit is
material or blocking (the other requirement is what's actually being
broken), not a freedom -- see the Intentional-freedom bullet under
"Disposition" below.

**2. Invariants and their enforcement boundary.** Find every "must always"
or "must never" claim (explicit or implied by an acceptance scenario), then
ask two separate questions about each: which operations, sequences, or
actors could threaten it, and does the component the spec names as
responsible actually have enough information and control, at the moment it
would need to act, to enforce it? A spec can state a real invariant and
still fail this: "the coordinator must never dispatch a blocked item" is
unenforceable by a coordinator that the spec's own data model gives no way
to *read* blocking state from. Separately: do any two stated requirements
conflict once you try to satisfy both in the same scenario -- not "could
someone imagine tension" but a concrete sequence where satisfying
requirement A's wording forces violating requirement B's.

**3. Ownership and authority.** For each piece of state the spec discusses,
who is the authoritative source, and does the spec actually say so, or does
it just say who *reads* it? Distinguish a genuinely owned representation
from a projection, cache, or derived view -- and if the spec has two
representations of what looks like the same fact, ask whether it says which
one wins when they disagree, or whether disagreement is even acknowledged
as possible. A spec that describes multiple interacting stateful entities
in enough depth that this question needs a real inventory -- several
owners, several representations, an open reconciliation question -- has
outgrown what this pass should re-derive inline; name that a full
lifecycle/ownership mapping is warranted (see "What this skill refuses to
do") rather than reconstructing one field at a time here.

**4. Concurrency, ordering, and staleness.** Two actors (or the same actor
twice) doing the thing the spec describes at the same time, or in the
opposite order the spec's prose implicitly assumes: does the spec's
language ("the system checks X, then does Y") only hold together if nothing
else can happen between the check and the act? A requirement phrased as a
single English sentence in the imperative mood is not automatically a
sequential-execution guarantee -- ask explicitly whether it's supposed to
be one. Also probe reads based on stale information: an actor decides
something based on a state that changed a moment after it was observed --
does the spec say what happens, or does its wording only make sense if
observations are always current?

**5. Failure and partial-outcome mechanics.** For any operation the spec
implies touches more than one piece of durable state, or crosses a boundary
to something else the spec doesn't control: what is externally observable
if it fails between those steps? Specifically -- is the first step's effect
persisted before or after the second step is attempted; if a caller retries
after a failure whose outcome it can't determine (timeout, crash, no
response), does the spec require the retried operation to be safe to repeat
(idempotent) or a new attempt at something that may have already happened;
and does anything reading the system's state mid-failure see a
half-applied result the spec never describes. "The spec doesn't mention
this failure mode" is itself often the finding, when the operation's own
description makes the failure reachable.

**6. Composition and boundary assumptions.** What does the spec assume
about a system, service, or actor it depends on but doesn't itself define
-- always available, always fast enough, always agreeing with this spec's
own version of shared facts? What happens to this spec's guarantees when
that assumption doesn't hold (the collaborator is down, slow, stale, or
behaves within its own contract in a way this spec didn't anticipate)? And
separately -- when the spec describes several requirements or components
that are each individually sensible, do they actually combine into valid
system behavior, or does satisfying all of them at once produce something
none of them individually implies is wrong but that's collectively broken
(a sequencing assumption from one requirement combined with a data
guarantee from another produces a state nothing in the spec names as
possible)?

**7. Cardinality and identity.** Does the spec actually settle zero/one/many
for each relationship it describes, or does it only ever give an example
with exactly one? What stops (or doesn't stop) creating the same logical
thing twice from two different triggers? Is an entity's identity stable
across the operations the spec describes (renamed, archived, superseded,
recreated), and if something else in the spec holds a reference to it, does
the spec say what that reference resolves to afterward -- especially after
the referenced thing is deleted, archived, or replaced. A reference that
can silently become unresolvable, and that the spec never says how to
distinguish from "the thing it points to was legitimately satisfied," is a
concrete, common instance of this category.

Two threads run through all seven: **would two competent implementers
reading only this document diverge on observable behavior here**, and
**does the spec's wording describe a behavioral contract, or does it
describe one plausible implementation and let the reader mistake the
example for the requirement** ("the system checks the cache, then falls
back to the database" reads like an implementation sketch that quietly
became the only described behavior for a fallback contract that never says
what correctness the check-then-fallback shape is meant to provide).
Neither of these is an eighth category to hunt separately -- they're the
lens the other seven get read through.

## Every candidate must survive three tests before it's a finding

A hunch that a category above "feels underspecified" is not yet a finding.
Before it goes in the report, every candidate must survive all three:

1. **Concreteness** -- can you state the actual scenario: which operations,
   in which order, by which actors, starting from which state? "Retry
   behavior is unclear" fails this. "Operation A persists X, then invokes
   B; B succeeds but the process dies before A records completion; on
   restart, does A re-invoke B or treat it as done" passes it.
2. **Consequence** -- if it goes the wrong way, what actually breaks: a
   stated invariant, data duplicated or lost, an observably different
   result depending on which implementer built it, a security or ownership
   boundary crossed? "This could theoretically be a problem" fails this.
   Naming the specific invariant, the specific divergent behavior, or the
   specific corrupted state passes it.
3. **Not resolved elsewhere** -- checked against the rest of the spec, its
   companion artifacts, and relevant repo convention docs, and still open?
   See "Ground 'already constrained' honestly" below.

A candidate that fails (1) or (2) is not downgraded to a minor note -- it is
dropped. There is no bucket in this skill's report for a vague worry with no
scenario and no named consequence; inventing one to hold overflow is exactly
the edge-case-confetti failure mode this skill exists to avoid. Producing a
short report because a spec survived hard scrutiny is a correct outcome, not
an incomplete one -- do not pad a clean pass with speculative categories to
look thorough.

Deduplicate before reporting: two scenarios that trace back to the same
missing decision are one finding, not two, even if you can phrase them with
different actors or different operations.

## Disposition: sort every surviving finding into exactly one bucket

- **Blocking ambiguity** -- the spec's own requirements are jointly
  satisfiable only by making a choice that produces materially different,
  externally observable behavior depending on who makes it, and getting it
  wrong risks a stated invariant, data loss or duplication, or a security/
  ownership boundary. Implementation of the affected surface should not
  begin until this is resolved. Every blocking finding names the smallest
  question that would close it -- usually a choice between two or three
  concretely stated options, not an open-ended "please clarify."
- **Material gap** -- a real, concrete gap exists (survives both tests
  above), but a defensible default exists that doesn't foreclose correcting
  it later and doesn't itself risk the failure modes above. The spec should
  probably say this explicitly; an implementer who picks the sensible
  default and names the choice they made is not creating a defect by doing
  so. The line between this and Blocking is the consequence test: if
  picking wrong is merely suboptimal or requires a later follow-up, it's
  Material; if picking wrong breaks something observable now, it's
  Blocking.
- **Intentional freedom** -- the spec identifies a genuine choice among two
  or more concrete alternatives, and there's positive evidence any of them
  is safe: nothing else in the spec, its companion artifacts, or the
  surrounding system depends on which one is chosen. This is not the
  default explanation for silence -- it requires the same concreteness test
  as any other disposition (name what varies and confirm nothing downstream
  cares which way it goes), not merely the absence of an explicit
  statement. Ground this specifically against the *whole* document, not
  just the section the gap was found in: a choice that looks free when
  checked only against the requirements physically nearby can still be the
  thing that leaves some other requirement's own guarantee unreachable (see
  "State and transition integrity" above for the missing-exit-transition
  version of this trap). If the honest description of the gap is "zero
  described options, not several safe ones" -- an orphaned state, an
  invariant nothing enforces, a reference with nowhere to resolve -- that
  is not a freedom; classify it as Material or Blocking by the ordinary
  test instead. Worth naming an actual freedom explicitly in the report so
  a reviewer can confirm it was left open on purpose rather than have it
  silently assumed by whichever implementer gets there first.
- **Already constrained** -- an apparent gap that, once checked against the
  rest of the spec, a companion artifact, or a repo convention document,
  turns out to be resolved by an actual stated decision -- the document
  says what the behavior *is*, not merely that the question is open. Name
  where. This bucket is what keeps this skill from re-litigating decisions
  a project already made; a spec that explicitly says "this does not reopen
  the settled decisions in `<referenced baseline>`" and a reader who then
  flags one of those settled decisions as an open question has made an
  avoidable, checkable mistake. Don't reach for this bucket when what the
  referenced text actually says is "this is left to the implementer" or
  equivalent -- that is a decision about *how much freedom exists*, not a
  decision about *what the behavior is*, and belongs in Intentional freedom
  instead; the two buckets read very differently to someone triaging the
  report (nothing to check, versus a freedom worth confirming on purpose).

If a finding's disposition genuinely can't be determined -- not enough
context exists to tell whether getting it wrong would actually be
consequential -- say that plainly and default to Material rather than
Blocking; escalating to Blocking requires being able to name the concrete
way it breaks something, not just the possibility that it might.

## Ground "already constrained" honestly

Checking whether a gap is already resolved cuts both ways, and both
directions are real mistakes:

- **Under-checking** produces a false Blocking or Material finding for
  something the spec, its plan, its data model, its contracts, or the
  repo's own decision log already settled -- explicitly or by clear
  reference. Always check these before reporting a gap as open.
- **Over-crediting** treats an incidental fact about an existing, unrelated,
  or soon-to-be-superseded implementation as if it resolved a *new* spec's
  own stated behavior. A spec that deliberately changes or replaces
  existing behavior is not constrained by what the code being replaced
  happens to do today; "the current implementation processes these
  sequentially so this race can't happen yet" does not close a concurrency
  gap in a spec that is specifically introducing concurrent access. Only
  durable, governing artifacts -- the spec's own other sections, a
  referenced plan/data-model/contract for the same feature, an accepted
  decision record, an explicit baseline pointer the spec itself states --
  count as resolving evidence. An implementation detail the spec doesn't
  reference, and isn't asking to preserve, doesn't get to silently settle
  the spec's own open question.

When a baseline is named ("this revises and extends `<prior spec>`; it does
not reopen `<prior spec>`'s settled decisions"), treat exactly what that
baseline settles as constrained, and nothing beyond it -- a baseline pointer
narrows what needs pressure-testing, it doesn't exempt the new material the
current spec actually adds.

## What this skill refuses to do

Even when a request bundles it in:

- Rewrite, edit, or add clarification directly into the spec. Name the
  question; resolving it in the document itself is a human decision or a
  dedicated clarification pass, not this skill's output.
- Ask the author interactive clarifying questions in a live back-and-forth.
  This skill produces one report from one pass over the material, not a
  question loop.
- Decompose the spec into tasks, or judge how to slice already-decomposed
  work into delivery units -- that's task decomposition and
  `task-composition`, both downstream of this skill.
- Review an already-written diff or implementation against this or any
  spec -- that's `slice-review`, and it runs after code exists; this skill
  runs before any does.
- Perform a general requirements-writing-quality sweep -- flagging vague
  adjectives, missing template sections, or un-quantified claims divorced
  from a concrete scenario that exposes a behavioral consequence. That is a
  different, shallower, breadth-oriented check; this skill is depth-first
  and every finding must clear the concreteness and consequence tests
  above, not merely note that a word like "fast" lacks a number.
- Perform cross-document duplication, requirement-to-task coverage
  mapping, or terminology-drift bookkeeping between a spec, plan, and task
  list as its primary output. Evidence-gathering here may touch the same
  files; the deliverable is different -- concrete behavioral
  counterexamples, not a coverage table.
- Produce a full lifecycle inventory (states, owners, transitions,
  invariants, interaction mechanism and consistency requirement) across
  several interacting stateful entities as a standalone artifact. When a
  spec's complexity genuinely calls for that level of mapping, say so and
  point at it as separate, necessary follow-up work rather than
  reconstructing an abbreviated version of it inline.
- Choose or silently prefer a resolution to a genuine open decision. When
  more than one answer is defensible, present the decision -- state the
  options and what each implies -- rather than picking one and reporting
  it as settled.
- Manufacture a finding to make a category, a report, or a review look more
  thorough. An axis with nothing concrete and consequential to say about
  this spec gets nothing written about it.
- Redesign the proposed architecture, or turn a named gap into an
  unsolicited alternative design. Name the gap and the smallest question
  that closes it; the resolution belongs to whoever owns the spec.

If a request bundles a legitimate pressure-test with one of these -- "find
every hole in this spec and then just fix them," "pressure-test this and
break it into tasks" -- say plainly that the extra part is out of scope for
this skill, then deliver the pressure test itself.

## Report

```
# Spec Pressure Test: <spec/feature name>

## Verdict
<Ready to implement | Not ready -- resolve blocking ambiguities first |
Unable to pressure-test>
<One or two sentences connecting the verdict to what follows.>

## Scope and evidence inspected
<What was actually read: the spec, and which companion artifacts, repo
docs, or existing code were checked and against what baseline. Name
anything relevant that wasn't available.>

## Blocking ambiguities
### <short name>
- Spec statement(s): <quote or precise reference>
- Unstated assumption / conflicting requirement: <...>
- Scenario: <the concrete sequence that exposes it>
- Why it matters: <the invariant, data-integrity, or divergence risk>
- Smallest closing question: <the specific decision that would resolve it>
(repeat per finding)
None identified.

## Material gaps
(same five-field structure as above)
None identified.

## Intentional freedoms worth confirming
### <what varies>
- Why the spec leaves it open: <...>
- Why it's safe to leave open: <what you checked to confirm nothing
  downstream depends on the choice>
(repeat)
None identified.

## Already constrained
### <apparent gap>
- Where it's actually resolved: <spec section / companion artifact / repo
  doc, cited precisely>
(repeat)
None identified.

## Minimal spec changes or questions needed before implementation
<The smallest concrete punch list that would clear every Blocking finding
and any Material gaps worth resolving now -- decisions and questions, not a
rewritten spec. Order by what's actually blocking first.>

## Out of scope
<One or two lines: this pass doesn't edit the spec, decompose it into
tasks, choose an architecture, or map a full multi-entity lifecycle -- see
"What this skill refuses to do.">
```

Leave a bucket's body as "None identified." rather than omitting the
heading -- an absent section reads as "not checked," not "nothing found."
A spec that survives every one of the seven categories with nothing
concrete and consequential to report is fully and honestly served by a
report that says so and stops.
