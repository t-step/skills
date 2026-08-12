---
name: next-best-product-slice
description: >-
  Recommends exactly one next bounded product slice -- the smallest change
  that grows what a product's intended users can understand, complete, or
  recover from, given what it already supports. Distinct from
  next-best-slice, where user value is one unprivileged input: here
  product usefulness itself drives the pick, even over an
  architecturally-leveraged alternative.
  Product value is outcome, not layer -- work in any layer qualifies.
  Facts stay evidence-gated; value is an explicitly-named bet, never
  dismissed for being unproven, never chosen for being easiest to prove.
  Use when asked what most improves the product for its users, or for
  the next workflow-completion/usability priority -- not the general
  "what's next," next-best-slice's job. Requires the intended user to
  trace to repository evidence, never an invented persona. Refuses
  multiple slices, a roadmap, factual speculation as sufficient
  evidence, absorbing bug work into a product pick, or manufacturing one
  without enough evidence.
---

# Next Best Product Slice

A product can have more than one defensible "best next slice" at once,
because "best" depends on what you're optimizing. One completed slice might
unlock three more pieces of backend work; another might close a gap that's
been quietly confusing every user who hits it. `next-best-slice` answers the
general question -- weighing dependency unlocking, learning value, user
value, size, reversibility, risk, and architectural momentum together,
without letting any one of them win by default, including user value. This
skill exists for a narrower, specific question: given everything the
product's current capabilities, workflows, and constraints already support,
what's the smallest bounded change that measurably increases what its
intended users can actually accomplish? That objective is allowed to drive
the recommendation here even when a more architecturally-leveraged or more
frequently-hit alternative would win under `next-best-slice`'s broader
criteria. The two skills will often agree -- a real usefulness gap on the
product's most central surface tends to win either way. They won't always
agree, and that divergence is the reason this skill exists, not a defect in
either one: a smaller, well-evidenced usefulness gain on a secondary
surface can outrank a larger, more architecturally-leveraged change here,
in exactly the case where the general skill would defensibly pick the
leveraged change instead. If the question is the general "what's the best
next bounded work, all things weighed" -- use `next-best-slice`. If it's
specifically "what's the best next change for the people who use this
product" -- use this skill.

The habit this skill exists to break is the mirror image of the one
`next-best-slice` breaks: not momentum or backlog priority, but mistaking
"this would be a nice feature" for "this is what users actually need next,"
or mistaking "this is on the UI" for "this is product work" and "this is in
the backend" for "this isn't." Product usefulness is about what a user can
now accomplish, not which layer changed to accomplish it.

## Gather before recommending

Four things, before any candidate gets weighed:

1. **Demonstrated intent** -- what the product's own domain model, docs, or
   already-shipped surfaces say it's for, and which users, roles, or usage
   contexts they establish. A role or job counts only when the repository's
   own evidence names or exercises it: a shipped feature built for that
   role, a doc describing that role's job, a data model field, an existing
   surface only that role reaches. A role invented to make a candidate sound
   more justified -- "power users would probably want this" with nothing in
   the repository actually establishing a power-user concept or need --
   does not count, no matter how plausible it sounds.
2. **The current capability set, as wired in** -- what the product actually
   runs today: routes, commands, endpoints, domain operations, screens. A
   capability that exists in the code but reaches no user (no route, no UI,
   no documented access path) is real for this purpose -- it's the seam
   most worth checking, not a capability to overlook because it's already
   "done" from an implementation standpoint.
3. **Traceable workflows for each identified user, role, or context** --
   where each one's interaction with the product starts, what steps it
   takes, where it ends, and where along that path a user could plausibly
   get stuck, lose confidence, or have no way to tell what happened.
4. **Whatever recent-slice evidence exists** -- a review, retro, or backlog,
   when the repository has one. This is supplementary here, not the primary
   organizing evidence the way it is for `next-best-slice`: read it for
   anything that bears on usefulness specifically (a retro naming an
   explicit non-goal around user-facing behavior, a backlog item grounded
   in real usage or support signal), but its absence is not grounds to stop
   -- gathers 1 through 3 stand on their own. When it's absent, say so
   plainly in the recommendation itself rather than proceeding silently --
   the same discipline `next-best-slice` applies to a missing review or
   retro.

If none of the above yields anything traceable to a real user, role, or
context, say so plainly rather than reasoning about "users" in the
abstract.

One completeness check before anything gets ranked: every source above
is repository-legible, so a candidate set built only from what the
repository makes easy to see can consist entirely of unreachable
routes, dead-ended workflows, and documented gaps with tiny fixes. Ask
whether the set contains at least one bounded candidate that would
advance an established user's actual job -- grounded in the product's
demonstrated intent, its wired-in capabilities, or its traceable
workflows, never in an invented persona -- rather than only repairing
what happens to be visible. This is a completeness check, not license
to brainstorm: such a candidate's factual premises must still be
observed, its value is carried as a named bet, and the outcome is still
exactly one recommendation. If no such candidate can be grounded, say
so plainly and rank what exists.

## Keep evidence, inference, and speculation separate

- **Observed evidence** -- a fact anyone could verify directly: a workflow
  traceable start-to-end in the code, routes, or domain model; a capability
  that exists with no consuming surface; a role or job the repository's own
  evidence names, with no path to completing it; a support ticket, incident,
  or usage count naming a real point of friction or confusion. This is the
  only tier that can support "this gap exists" or "this candidate is
  feasible now."
- **Inference** -- one tight step from that evidence: the domain model
  names a role's action, an API implements it, and no surface invokes it,
  so the exposure gap is inferred, not observed directly as a single fact --
  but it's one short step, not a leap.
- **Speculation** -- an unverified factual premise treated as if observed:
  a role or persona nothing in the repository establishes, a workflow
  nobody can trace, "users already do X" with no evidence anyone does.
  Factual speculation can motivate recommending an evidence-gathering
  step -- never carry a claim as if the premise were observed.

A hypothesis about value is not factual speculation, and this tier must
never be used to suppress one. "This product's established users would
return if it did X" makes no false claim about the repository -- it is a
judgment about what the product should become, and the repository was
never going to be able to prove it in advance. The repository can
establish that a workflow is missing; it usually cannot establish
prospectively that completing it is the highest-value product move. That
is the bet. When a hypothesis's factual premises are observed (the
workflow really is absent, the capability really is unreachable, the
role really is established by the repository's own evidence), it is
admissible as the value case for a product slice -- carried as an
explicitly-named bet, per "Facts are gated; value is a bet" below, never
dismissed as "speculation about user want."

That observed-premise set is about the gap itself -- that a workflow is
missing, a capability is unreachable, a role is established -- not about
which specific implementation would close it. A candidate's proposed
storage, schema, endpoint, or design is its own premise: it does not
inherit "observed" status merely because the gap around it is grounded,
and gets named as an open assumption the bounded slice resolves, or, if
the whole candidate's feasibility turns on it, as the unresolved fact
under "When no candidate is justified yet."

When unsure which tier a claim belongs in, use the weaker one. Name which
tier backs each factual claim as you reason -- this doesn't require a label
on every sentence, but the reasoning behind the recommendation should be
traceable back to a tier by anyone reading it.

## Facts are gated; value is a bet

Evidence constrains claims. It does not constrain product imagination to
only things the repository can prove are valuable -- product development
is making moves under incomplete evidence, and a selection function that
requires proof of value will systematically pick whatever is easiest to
prove from static repository state: unreachable-but-built capabilities,
dead-ended workflows with one missing link, documented gaps with tiny
fixes. Those light up every evidence detector this skill has, and each
can still be the right pick -- but the questions that actually decide
product priority (what would make this product's established users
return, what turns it from interesting to useful) are usually illegible
to the repository. Their illegibility lowers confidence in their value;
it does not remove them from the comparison.

So hold two confidences, and report them separately:

- **Confidence in the facts** -- evidence-gated, per the tiers above.
  This one is allowed to block: a candidate whose factual premises are
  speculation isn't ready.
- **Confidence in the value judgment** -- a bet. This one is allowed to
  be moderate, and moderate value-confidence is the normal condition of
  product work, not a defect to route around.

The healthy shape of a recommendation under this split:

> I can establish with high confidence that X is missing. I have only
> moderate confidence that adding X is the highest-value next move.
> Nevertheless, among the candidates available, X is the best available
> product bet -- and here is exactly what I'm betting on.

If the "betting on" clause can't be filled convincingly, the candidate
hasn't earned the recommendation -- go back and compare again, rather
than letting provability quietly stand in for the missing argument.
"The only candidate that fully cleared the evidence bar" is a statement
about fact-confidence, not a selection argument; every candidate whose
factual premises are observed is in the comparison, and the comparison
is of bets. Implementation convenience -- a recently-touched seam, code
that is easy to change, familiarity from the last slice -- is not part
of any candidate's product case at all: at most it is a final
feasibility tie-break between otherwise comparable candidates, named as
such. Left unchecked it becomes mechanical adjacency: recent work makes
nearby work easier to justify, which produces more nearby work --
gradient descent into whatever was touched last.

## What counts as a product slice, and what doesn't

- **An observed user/product gap** -- a workflow that dead-ends, a
  capability nobody can reach, a state nothing explains -- is eligible.
- **A clearly implied missing piece of an already-established workflow or
  capability** -- the repository's own evidence shows the workflow started
  and shows what finishing it would take -- is eligible, even if nothing
  has filed it as a ticket.
- **A feature idea resting on speculative factual premises** -- a persona
  nothing establishes, a workflow nobody can trace -- is not enough
  evidence on its own. It can motivate the "not enough evidence" outcome
  below; it cannot motivate a recommendation. A candidate whose factual
  premises are observed but whose value is a hypothesis is not this
  case: it enters the comparison as a named bet.
- **Pure technical or architectural cleanup** is not eligible here unless
  there's a concrete, near-term, evidence-traceable connection to what a
  user can accomplish -- not "this will probably help eventually," which is
  a judgment about taste standing in for evidence. If the connection is
  real and close, name it explicitly and specifically; if the best you can
  say is that cleaner code tends to help users somehow, that's not this
  skill's job to recommend.
- **Ordinary bug or reliability work** defaults to being someone else's
  territory, not this skill's. Don't silently fold a defect into a product
  recommendation just because fixing bugs is generally good, and don't
  silently drop a bug that's competing with a real product candidate --
  name it plainly as a separate, real thing. The one exception: when the
  fix itself is what unlocks the user-visible capability -- the broken
  behavior and the product improvement are the same change, not "fix this
  incidentally while we're in the area." Say explicitly when that's what's
  happening, since it's easy to blur with ordinary bug-fixing.
- **No meaningful product evidence** is a legitimate finding. Say so, and
  don't manufacture a candidate because the question "what should we build
  for users" was asked directly.

## Product value isn't a layer

The objective is what a user can now accomplish, never which part of the
system changed to get there. A backend change that lets a user finally
complete a workflow, a data-model change that makes a confusing state
explicable, an API change that closes a recovery gap, a performance fix
that turns an abandoned interaction into a usable one, or an
interoperability fix that lets a user's existing data actually reach the
product -- each qualifies exactly as much as a UI change, provided the
evidence traces it to something a user can now do that they couldn't
before. A UI change that doesn't trace to any such outcome -- purely
cosmetic polish, a rearrangement nothing in the evidence says was
confusing -- does not qualify merely for being visible. If every candidate
that clears the bar in a given case happens to be a UI change, or happens
to not be, that's a fact about the evidence in that repository, not
something to correct for by picking a different layer on principle.

## The criteria, and how they trade off

- **Workflow completion or trust** -- does this let an intended user
  finish, verify, or safely exit an interaction they currently can only
  partly complete, or currently can't tell the outcome of? This is usually
  the strongest signal: closing a dead end or restoring trust in a broken
  loop outweighs making an already-working path faster.
- **Discoverability and legibility of existing capability** -- does this
  make something the product already substantially supports actually
  reachable and understandable by the user it's for? A backend capability
  with no surface is exactly this case. Reachability being grep-provable
  makes this candidate easy to verify, not automatically valuable: its
  value case is still a bet like any other's -- would the intended user
  actually use the capability once reachable?
- **Recovery and feedback** -- when something goes wrong, or changes, can
  the affected user tell what happened and what to do about it?
- **Demonstrated-intent fit** -- is this traceable to a role, job, or
  capability the repository's own evidence already establishes, rather than
  a plausible-sounding addition nothing in the repository actually asked
  for?
- **Size and reversibility** -- between two candidates that clear the bar
  comparably, prefer the smaller, easier-to-undo one, same discipline as
  any other bounded-slice recommendation.
- **Convenience or friction-reduction on an already-functioning workflow**
  is real user value and can win when nothing stronger is competing -- but
  it's the weakest signal here. Making a working path faster does not by
  default outrank closing a path that's broken, confusing, or untrustworthy,
  even when the friction-reduction candidate is bigger, more frequently
  hit, or more architecturally convenient to build. If the strongest
  candidate on offer is only friction-reduction, it can still be the right
  recommendation -- but a trust/completion/recovery gap of comparable
  evidence and size should generally be preferred over it.

Ground every comparison in what gathering steps 1 through 4 actually
established, and say so as you reason. The first four criteria describe
a candidate's upside -- what its bet could win; size and reversibility
describe the cost of pursuing it; certainty belongs to neither list,
and must never decide the pick in their place. When two or more independently-
evidenced candidates score comparably, pick one, name the actual tiebreak,
and say plainly that the alternative was close -- don't dress up a coin
flip as an obvious call.

## When no candidate is justified yet

Sometimes nothing on the table clears the bar: every candidate traces back
to speculation, the repository shows no traceable user or role at all, or
two candidates' entire value depends on the same unresolved fact (which of
two workflows people actually use, whether a documented gap is ever hit in
practice). This is a legitimate outcome, not a failure to find something to
recommend. It is about unresolved facts and undecidable ties, not
unproven value: a single candidate whose premises are observed but whose
value is a hypothesis is the normal case for a named bet, not for this
outcome -- retreating to measurement merely because value-confidence is
moderate is the same substitution this skill refuses in the other
direction. But when two or more otherwise-indistinguishable candidates
hang their entire ranking on the same single resolvable unknown, that
unknown functions as a missing fact for the decision even though each
candidate's own premises are observed, and this outcome still applies.
When it's genuine, say so plainly and recommend the smallest
step that would produce the missing evidence -- naming the intended user or
usage question it would resolve -- rather than picking the most
plausible-sounding candidate and hoping the gap doesn't matter.

## What this skill refuses to do

Even when a request bundles a reasonable ask together with one of these:

- Recommend more than one slice, a ranked shortlist, or a set of "options."
- Produce a roadmap, a phased plan, or a prioritized backlog of product
  work.
- Credit a factually-ungrounded feature idea, or a documented-but-
  unevidenced limitation, as sufficient evidence on its own -- a gap
  being written down somewhere is not the same as anyone needing it
  fixed. The observed gap admits the candidate; it cannot substitute for
  the value bet in either direction -- neither "it is documented, so it
  matters" nor "no one has asked, so it is speculation."
- Let evidentiary confidence stand in for product priority: recommending
  the most provable candidate *because* it is the most provable -- "the
  smallest thing I can fully stand behind" -- or dismissing a candidate
  whose factual premises are observed because its value is unproven.
  Value is unproven for every candidate; the comparison is of bets.
- Recommend broad architectural or technical cleanup without a concrete,
  near-term, evidence-traceable product-value connection.
- Silently absorb ordinary bug or reliability work into a product
  recommendation, or silently drop one that's competing with a real product
  candidate.
- Invent a persona, a user need, or a "demonstrated intent" the repository's
  own evidence doesn't actually establish.
- Let "product" narrow to "frontend," "visual," or "UX polish" -- a
  backend, data-model, API, algorithmic, interoperability, or performance
  change qualifies exactly as much as a UI change when the evidence shows
  it changes what a user can accomplish.
- Manufacture a recommendation merely because the question "what should we
  build for users" was asked directly -- say plainly when the evidence
  doesn't support one yet.
- Re-decide what `next-best-slice` would recommend, or treat this skill's
  answer as an override of that one -- they answer different questions;
  if both are wanted, say so and that only one is in scope here.

If a request bundles a legitimate ask together with one of these, answer
the in-scope part -- the single recommendation -- and say plainly that the
rest is out of scope for this skill.

## Report

Use this exact structure:

```
# Next Best Product Slice: <one line framing of the decision>

## Recommendation
<the single bounded change -- what it is, and roughly how small>

## Who this is for, and what it unlocks
<the identifiable intended user, role, or usage context this serves,
grounded in repository evidence -- and the specific thing they can now
understand, complete, or recover from that they couldn't before>

## Why this clears the evidence bar
<the observed gap or clearly-implied missing piece and which tier backs
it (observed vs. inference) -- factual premises about the gap only, not
about which implementation would close it, with the value case left to
The bet rather than dressed up as fact here. If no review,
retro, or backlog exists for this repository, say so explicitly in this
section, and that the recommendation doesn't depend on one existing>

## The bet
<two confidences, stated separately: how strong the factual premises
are, and how strong the value judgment is. Then the bet itself -- "this
is the best available product bet because ___" -- with the blank
actually filled, and the observation that would show the bet was wrong.
If the blank can't be filled convincingly, the candidate hasn't earned
the recommendation; go back and compare again>

## What this slice proves
<the one thing this slice settles, phrased as a question its own
verification will answer -- not a feature list>

## Explicit non-goals
<what this slice deliberately does not attempt -- named specifically, not
"everything else">

## Acceptance evidence
<the specific observation that would tell us this slice succeeded -- tied
to the user/role/workflow named above, not a general "tests pass">

## Alternatives considered
<2-4 genuine close calls, not a backlog dump>

## Why they wait
<per alternative, one evidence-grounded reason -- not "not now" without a
cause>
```

Leave a section's body as "None identified." or "Not established from
available evidence." rather than omitting the heading -- an absent section
reads as "not considered," which is worse than an honest empty one.
