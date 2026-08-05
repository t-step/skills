---
name: next-best-slice
description: >-
  Recommends exactly one next implementation slice once a completed slice
  has been reviewed and retrospected — "given what we now know, what's the
  smallest, highest-value thing to build next?" — strictly from that
  review, that retro, and whatever backlog/roadmap evidence exists. Weighs
  dependency unlocking, user value, learning value, size, reversibility,
  risk, and architectural momentum, and names the strongest alternative
  passed over. Use when a slice/PR/task has just been reviewed and
  retrospected and someone asks what to build next, which ticket to pick
  up, wants "top picks," or wants a roadmap/quarter plan distilled to one
  step. Refuses — even under a roadmap's stated phase, a stale "P0" label,
  user preference, or "keep momentum" pressure — to recommend more than one
  slice, pick the largest milestone, or produce a project plan. When
  evidence doesn't justify feature work, recommends the smallest slice that
  would produce the missing evidence instead of guessing.
---

# Next Best Slice

A slice has just landed. It's been reviewed. It's been retrospected. Now
someone asks the natural next question: what do we build next? The habit
this skill exists to break is answering that question from momentum,
preference, or the most exciting-looking item on the backlog, instead of
from what the last slice actually just taught the team. A retrospective
that falsified an assumption, a review that flagged a scaling number, a
diff that quietly made something possible that wasn't possible yesterday —
that's the evidence. The backlog's stated priorities, a roadmap doc's "Phase
2," and how much a stakeholder wants a feature are inputs worth noting, not
verdicts to inherit.

This skill produces exactly one recommendation: one bounded slice, sized to
prove or unlock one thing, justified by evidence — from the completed
slice, from the product's current state, or both — not a plan, not a
ranked shortlist, not a rewrite.

## Evidence channels and the strategic-continuity lens

A recommendation rests on two evidence channels — factual inputs, each
capable of independently grounding a claim of its own kind:

1. **Recent slice evidence** — the completed slice's review verdict and
   findings, and its retrospective's validated/falsified assumptions,
   remaining uncertainty, and architectural consequences. This is the
   only channel that can support a claim about what the *last slice
   itself* proved or unlocked.
2. **Current product-state evidence** — directly observable facts about
   the repository and product surface as they exist right now: a missing
   or incoherent capability, an incomplete user journey, a limitation the
   code or docs actually confirm, an architecture that makes a bounded
   slice feasible. This channel doesn't depend on a review or retro
   existing at all.

Missing channel 1 lowers confidence in any claim about what the last
slice specifically proved or unlocked — that claim needs channel 1, and
nothing substitutes for it. It does not lower confidence in, or excuse
ignoring, whatever channel 2 independently establishes. A repository
with no review and no retro can still have a directly observable
core-surface gap, and that gap is real evidence, not a placeholder for
evidence.

**Strategic continuity is a decision lens, not a third channel — it
doesn't supply facts, it weighs the facts channels 1 and 2 already
supplied.** Apply it when ranking or choosing among candidates that have
already cleared the evidence bar on their own: does this candidate sit
on the product's core surface or a peripheral subsystem? Does it
complete an end-to-end workflow, or leave one still half-finished? Is
recent work over-deepening one subsystem at the expense of a gap
somewhere else? The lens can make one evidenced candidate win over
another evidenced candidate — it cannot turn a candidate with no
evidence behind it into one worth recommending, and it cannot itself
manufacture urgency or user need. The intended shape: *evidence* — the
catalog has no search or stable ordering; *lens* — the catalog is the
product's core surface; *conclusion* — prefer bounded catalog work over
another admin refinement. Skip the lens step and you're left with an
unranked fact. Skip the evidence step and the lens has nothing to weigh
— "this is the core surface" is not itself a reason to build something
there if nothing observable is actually wrong with it.

## Gather before recommending

Three things, gathered before any candidate gets weighed:

1. **The completed slice's review** — its verdict and findings. This is
   where blocking issues, required corrections, and scaling or correctness
   numbers actually observed during review live.
2. **The completed slice's retrospective** — what it proved, which
   assumptions it validated or falsified, what remains uncertain, what was
   deliberately deferred, and what architectural consequence follows. This
   is the primary evidence source for "what's now different."
3. **The candidate universe** — whatever backlog, roadmap, issue tracker,
   or notes-file the repo actually has listing possible next work, plus
   whatever the review's findings and the retro's remaining uncertainty /
   follow-up questions / architectural consequences themselves surface. A
   tracker is a source, not an authoritative ceiling on the candidate set,
   and a real candidate those documents imply doesn't stop being real just
   because no one has filed it, or because a tracker exists and simply
   doesn't happen to list it. Weigh a tracker by how well it's actually
   maintained, not by whether one is present: a backlog that's current,
   specific, and actually speaks to the area the completed slice just
   touched is strong evidence of the real candidate space, and most
   candidates should come from it. One that's stale, a placeholder, thin,
   or silent on that area is weak evidence of the full space even though
   what it does list can still be real — a tracker existing is not the
   same as a tracker having covered the ground. When the available tracker
   is absent, or isn't materially representing the real candidate space,
   the skill may also name a nearby, bounded gap the repository's present
   state itself makes visible — an adjacent user journey the completed
   work leaves half-finished, a lifecycle path with an obvious missing
   step, or a capability now reachable because persisted data or a stable
   seam exists for the first time. Say plainly when this is what's
   happening. Either way, don't invent an ambitious backlog to have
   something to choose from: a candidate the repository's current state
   introduces still has to clear the same evidence bar as any other before
   it can be recommended, not just to be listed — see "Keep evidence,
   inference, and speculation separate" below.

If the review or the retrospective is missing rather than just thin, don't
fabricate its content or proceed as if it said something it didn't. Say
plainly which input is missing, and don't stop there.

## When recent-slice evidence is missing

A missing review or retro is not, by itself, grounds to refuse a product
recommendation. Work the problem instead of stopping at the gap:

1. Identify candidates directly observable from the repository's current
   state (channel 2), same as any other run of this skill, then use the
   strategic-continuity lens to weigh them against each other.
2. Separate candidates whose justification depends on the missing
   review/retro from candidates that stand on their own without it.
3. Compare the independently-justified candidates on the criteria below —
   user value, product-surface importance, end-to-end completeness,
   implementation size, architectural fit, and the risk of turning this
   into unbounded framework-building.
4. If one candidate clearly wins that comparison, recommend it. Say
   plainly that recent-slice evidence is missing and that the
   recommendation doesn't depend on it — never claim the missing slice
   "proved" or "unlocked" it; that claim needs channel 1.
5. Recommend evidence-gathering instead of a product slice only when the
   decision genuinely can't be made without channel 1: real uncertainty
   about whether the last slice is correct, about actual user behavior,
   about whether an observed problem actually exists, an ordering between
   multiple plausible candidates that nothing else resolves, or a
   candidate whose value rests on an unverified assumption about the last
   slice. Only then name the smallest step that would resolve it (usually:
   write the missing review or retro).

Missing recent-slice evidence lowers confidence in claims about what the
last slice specifically proved — it is not, by itself, grounds to refuse
a product recommendation the repository's current state already justifies.

## Process action vs. product slice

"Run the missing review," "write the retro," or any other evidence-
gathering step can be the correct next *process* action. That doesn't make
it the next *product* slice by default, and the two answers aren't
interchangeable: naming a process action doesn't excuse skipping a product
recommendation that's independently justified, and a product
recommendation doesn't excuse skipping a process action that's actually
needed. When both apply, say both, and be explicit about which one is this
skill's actual recommendation — a product slice when one is independently
justified (per "When recent-slice evidence is missing" above); the
process action itself only when step 5 above is the honest outcome.

## Carried-forward concerns don't expire on their own

A concern raised in an earlier review or retro doesn't lose standing
simply because the newest retrospective doesn't happen to restate it.
This is bounded, not open-ended: check the most recent three completed
slices' retros for anything still open, or — when the repo keeps one — a
maintained decisions/follow-up/backlog artifact, which usually reaches
further back and is the better source when it exists. Treat a concern
found this way as still live unless it's since been addressed, falsified,
explicitly retired, or superseded by a later decision; at that point it's
closed, not carried forward.

Being carried forward gives a concern evidentiary standing, not automatic
priority. Weigh it against every other candidate on the same seven
criteria below, same as anything freshly surfaced. An old concern that's
still genuinely the strongest candidate should still win; an old concern
with nothing going for it beyond its age should still wait — "it's been
open a while" is not itself one of the criteria.

## Keep evidence, inference, and speculation separate

The same three tiers a good retrospective uses apply here, aimed at
justifying a choice instead of describing what happened:

- **Observed evidence** — a fact anyone could verify directly, from either
  source: (a) a verdict, finding, measured number, validated/falsified
  assumption, or architectural consequence taken directly from the review
  or retro (channel 1), or (b) a directly observable fact about the
  repository or product surface right now (channel 2) — a capability
  that's missing or incoherent, a journey that's incomplete, a limitation
  the code or docs actually confirm. Only (a) can support a causal claim
  about the *last slice* specifically — "this slice unlocked X," "the
  retro found Y." (b) can support "this gap exists" and "this candidate is
  feasible now," on its own, with no review or retro required — but not
  more than that: observing that a capability is missing is not the same
  as observing that users need it fixed, and a gap existing is not the
  same as it being urgent. Claims like "users need Y" or "this is urgent"
  still need their own evidence (a metric, an incident, a direct request,
  a review/retro-flagged risk) — the gap's existence alone doesn't supply
  it.
- **Inference** — one tight step from that evidence: the retro says a
  reusable retry seam now exists, so a slice that uses that seam for a
  second call site is a short, defensible inferential step, not a leap.
- **Speculation** — anything further out: "this will probably also help
  with X," a hunch about what users want, a guess about future scale nobody
  measured. Speculation isn't banned, but it can only ever motivate the
  "gather more evidence" outcome below — a slice whose job is to test the
  speculation — never a claim that a feature slice is already justified.

When a candidate's justification is only as strong as speculation, that's
the signal to recommend evidence-gathering instead of the feature itself,
not to write it up as if the evidence were already observed.

Name which channel backs each factual claim as you reason — recent slice
evidence, current product-state evidence, or speculation — and separately
say when the strategic-continuity lens shaped how candidates were ranked
against each other. This doesn't require a labeled tag on every sentence
of the final prose ("the current public catalog has no filtering" is
self-evidently a channel-2 observation and doesn't need one) — it requires
that the reasoning behind the recommendation could be traced back to a
channel (for facts) or the lens (for ranking) by anyone reading it, and
that no claim borrows more certainty than its channel actually provides.
The lens is never itself the answer to "what's your evidence" — if a
claim's only backing is "this is the core surface," that's a ranking
judgment standing in for a fact, and the fact still needs to be named.

## When a test-only or verification-only candidate is eligible

A slice whose only content is test or verification code is eligible to be
the next slice when the missing coverage does at least one of these:

- prevents trusting or merging the capability it targets
- prevents operating that capability safely
- prevents safely extending or building on it next
- exercises a distinct integration boundary whose behavior is still
  materially uncertain, not just unasserted
- would resolve an actual "Unable to verify" or "Not ready to merge"
  finding on record

It is not eligible on the strength of only these, even though each can
make it cheap and tempting:

- creating symmetry between test cases that already behave the same way
- re-asserting behavior already established at the appropriate layer (a
  database, unit, component, or integration test re-covering what another
  of those already proved)
- one more rendering branch asserted through an end-to-end test
- reusing a fixture, helper, or assertion pattern a recent slice happened
  to leave lying around
- raising confidence without producing any information that wasn't
  already known

Work in that second list can still be real and worth doing — it's
maintenance, not roadmap progression. Say which one it is plainly: name it
as maintenance and let it wait or move to the alternatives list, rather
than either recommending it as the next slice or writing it off as
worthless.

## The criteria, and how they actually trade off

Every candidate gets weighed against the same seven angles. None of them
wins by default, including user value — a slice that delights users but
that nothing in the evidence justifies doing *now* is not this skill's job
to greenlight. A candidate with nothing to show on Dependency unlocking —
because no review or retro exists to unlock anything — isn't disqualified
by that alone; it's judged on whichever of the other six criteria actually
apply, same as any candidate whose case rests on channel 2 and the
strategic-continuity lens rather than channel 1:

- **Dependency unlocking** — did the completed slice make something newly
  possible or newly worth doing that wasn't before? This is usually the
  strongest signal, because it's caused directly by the evidence in hand,
  not by general backlog priority.
- **Learning value** — does the candidate resolve a real, currently open
  question (something in Remaining uncertainty or Follow-up questions),
  rather than a question nobody actually has?
- **User value** — does it produce something a user can observe or benefit
  from soon? Real, but not sufficient alone — see "no candidate is
  justified yet" below for what happens when this is the only thing a
  candidate has going for it.
- **Implementation size** — prefer the smallest slice that still proves or
  unlocks the intended thing. If two candidates would settle the same
  question, the smaller one wins outright.
- **Reversibility** — prefer changes that are cheap to undo or narrow in
  blast radius, especially when the evidence behind the decision is thin.
- **Risk reduction** — prefer slices that pay down a risk the review or
  retro actually demonstrated over ones that don't touch it. A risk nobody
  has measured yet is a candidate for evidence-gathering, not a justification
  on its own.
- **Architectural momentum** — prefer building on a seam the evidence
  shows is real and load-bearing: a production capability, persisted
  data, a stable contract, a reusable production seam, or a validated
  integration boundary the retro says now exists. Recently edited files,
  nearby code, reusable test fixtures, assertion patterns, test helpers,
  and general implementation convenience can make a candidate cheaper to
  build, but don't by themselves count as momentum here. This criterion
  helps choose among candidates that are already well-justified on the
  others; it isn't grounds to prefer the freshest seam over a more
  consequential bounded capability or a risk the review/retro actually
  demonstrated.

Ground every comparison in the two evidence channels above — what the
review or retro actually established, and what the repository's current
state directly shows — applying the strategic-continuity lens where it
helps rank candidates that are already evidenced. When two or more
independently-justified candidates score comparably on these criteria —
this happens, and forcing a falsely confident tiebreaker is worse than
naming the tie — pick one, name the actual tiebreak used (usually
implementation size or reversibility), and say plainly that the
alternative was close rather than dressing up a coin flip as an obvious
call. This tiebreak presumes each candidate already cleared the evidence
bar on its own; it is not a way to choose between candidates whose value
depends on the same missing fact — when no candidate has cleared that bar
yet, "When no candidate is justified yet" below is the right section, not
this one.

## Don't tunnel into the most recently touched subsystem

The next slice doesn't need to descend from the immediately previous one.
Recent-slice continuity (channel 1, and the Architectural momentum
criterion) is useful evidence, not a mandatory lineage. Watch for a chain
like register → revoke → restore → edit → synchronize → audit →
bulk-manage — several slices in a row deepening the same administrative
subsystem — and treat that pattern as a prompt to check the broader
product, not as proof the next step belongs in that subsystem too. Before
recommending another deepening of a recently-touched area, weigh it
against the strongest bounded gap in the product's core surface using the
criteria above. If the deepening still wins on those criteria, say so and
proceed; if a core-surface gap is the stronger bounded candidate, prefer
it over adjacency.

## When no candidate is justified yet

Sometimes the honest read is that nothing on the candidate list is
supported strongly enough yet to commit real implementation effort to it —
the review's verification was inconclusive, the retro reopened a question
nothing has since answered, or the most attractive-looking candidate
depends on a fact (does this happen at production scale? is that canary
delta real or noise?) that nobody has actually measured. This is a
genuine-ambiguity outcome, not a default: it applies when neither
evidence channel, nor the strategic-continuity lens applied to whatever
evidence does exist, can responsibly distinguish the candidates — not
merely because channel 1 happens to be missing (see "When recent-slice
evidence is missing" above for that case) and not merely because the
candidates cost about the same to build. Two candidates whose entire
justification rests on the same unresolved fact are exactly this case,
even if each one individually sounds reasonable — a candidate "sounding
reasonable" on its own is not the same as evidence distinguishing it from
its alternative.

The right move here is neither silence nor a confident-sounding guess. It's
the smallest bounded slice whose entire purpose is producing the missing
evidence: extend a canary, add one instrument or metric, run a small
controlled experiment, prototype the specific unknown. That is still
exactly one bounded slice with a testable "what this proves" in the report
below — it just proves an open question instead of shipping a feature. Say
plainly that this is what's happening: naming a measurement slice as the
recommendation, instead of quietly picking the most plausible feature and
hoping the gap doesn't matter, is the whole point of this outcome.

## What this skill refuses to do

Even under direct pressure, and even when a request bundles a reasonable
ask together with one of these:

- Recommend more than one slice, a ranked shortlist, or a set of "options."
- Choose the largest remaining milestone because it looks like more
  progress, or because momentum makes stopping at something small feel
  like underachieving.
- Propose a broad refactor or redesign the architecture because it would
  be cleaner, more consistent, or more elegant — that's a judgment about
  taste, not a claim the evidence supports.
- Produce a project plan, a phased roadmap, or a prioritized backlog.
- Re-review the completed slice or re-litigate its retrospective. If the
  review and retro actually conflict with each other, name the conflict
  and say which one the recommendation relies on and why — don't resolve
  it by re-deriving the underlying facts yourself; that's each skill's own
  job, not this one's.
- Let user enthusiasm, a roadmap document's stated next phase, or an issue
  tracker's priority label substitute for evidence. These are real inputs
  worth naming in the recommendation, but none of them is itself a reason —
  a label or a stated plan is a claim, exactly like an implementation note
  is a claim in a retrospective, and claims get checked against evidence,
  not inherited.
- Turn "the repository's present state can introduce a candidate" into an
  open-ended product brainstorm, or justify a candidate by "this would be
  nice" or an assumed user want. The repository can introduce a candidate;
  only observed evidence can justify building it.
- Treat a missing review or retro as blanket grounds to decline a product
  recommendation. Missing recent-slice evidence only blocks claims that
  specifically need it (what the last slice proved or unlocked) — it
  doesn't block a candidate that current product-state evidence already
  justifies, even before the strategic-continuity lens is used to rank it
  against alternatives. Say what's missing, then still recommend when the
  case for it doesn't depend on that gap.

If a request bundles a legitimate ask together with one of these — "also
give me your top 3," "what's the roadmap for next quarter" — say plainly
that the extra part is out of scope for this skill, then answer the
in-scope part: the single recommendation.

## Comparing against alternatives

"Alternatives considered" is not a backlog dump. It lists only the
candidates that were genuine close calls — ones that scored well on at
least one criterion above, where a careful reader would reasonably ask "why
not this instead?" For each: one or two sentences on what it would have
offered, and the specific, evidence-grounded reason it waits (not ready
yet, not the smallest way to learn this, bigger than the question needs, or
resting on speculation rather than evidence). Two to four alternatives is
usually the right range — leaving out a real close call looks like it
wasn't considered, and padding the list with items nobody would seriously
propose looks like the opposite of the discipline this skill is for.

## Report

When recent-slice evidence is missing, open with one or two sentences
naming what's missing before the Recommendation section — a process note,
not a heading of its own. Then use this exact structure:

```
# Next Best Slice: <one line framing of the decision>

## Recommendation
<the single bounded slice — what it is, and roughly how small>

## Why now
<the evidence — from the review/retro, from the repository's current
state, or both — that makes this justified now specifically, not just
justified in general>

## What this slice proves
<the one thing this slice settles — phrased as an observed-evidence
question this slice's own verification will answer, not a feature list>

## Explicit non-goals
<what this slice deliberately does not attempt — narrower than "everything
else on the backlog"; name the specific things nearby that this slice is
not doing>

## Acceptance evidence
<what observation would tell us this slice succeeded or failed — the
specific check, measurement, or test that would run>

## Alternatives considered
<2-4 genuine close calls, not a backlog dump>

## Why they wait
<per alternative, one evidence-grounded reason — not "not now" without a
cause>
```

Leave a section's body as "None identified." rather than omitting the
heading — an absent section reads as "not considered," which is worse than
an honest empty one.
