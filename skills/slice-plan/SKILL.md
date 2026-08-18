---
name: slice-plan
description: >-
  Turns one already-accepted implementation slice into an
  implementation-ready plan: behavioral contract, likely implementation
  seams, invariants, a verification strategy scoped to the slice, explicit
  non-goals, known risks, and completion evidence. Assumes the repo is
  oriented, the slice already chosen and justified -- does not pick,
  re-justify, or redesign the work, only plans how to build the one slice
  agreed on. Use when a slice/ticket has just been accepted and someone wants
  an implementation plan, "how should I build this", seams/files identified
  before writing code, or a spec turned into something executable without
  guessing. Refuses -- even under "while you're at it" pressure, a tempting
  refactor nearby, an unrelated bug found nearby, a shortcut that breaks an
  invariant, or a request to widen verification into a test-everything pass
  -- to recommend different work, redesign the feature, expand scope, produce
  a roadmap, review an implementation, rewrite architecture, or plan an
  already-shipped slice.
---

# Slice Plan

A slice has already been chosen. The repository has already been
oriented, the case for doing this work over other work has already been
made, and someone has said yes to it. What's still missing is the part
that turns "build X" into something an implementer can actually execute
without guessing: which behavior is actually being promised, which files
it will touch, what must not break, how small a change proves it, and
what "done" looks like. That's this skill's only job.

The habit this skill exists to break: a plan that quietly becomes a
second decision about what to build, instead of a plan for building the
thing that was already decided. A planning pass is a uniquely tempting
moment to relitigate scope -- the code is open, the seams are visible,
and every seam looks like an invitation. This skill resists that
invitation on purpose. It plans the smallest, safest path to the one
slice already accepted, and nothing else.

## Gather before planning

1. **Whether the slice is already done.** Before reading anything else,
   check whether the behavior the accepted slice describes already
   exists at the target branch's HEAD. Search the codebase for the
   symbols, routes, and behaviors the slice would introduce, look for
   tests that already exercise them, and check recent commits and any
   slice tags newer than whatever handed this slice off (a
   next-best-slice recommendation, a ticket, a one-line ask) for signs
   it already landed. This isn't a formality -- real planning effort has
   been spent, in practice, on slices that turned out to be already
   shipped, and that effort is only recoverable by checking first.

   If the slice is fully present -- the behavior implemented, the
   acceptance evidence already satisfied by passing tests, a commit or
   tag that shipped it -- say so plainly: "already implemented at
   `<SHA>`," with the specific files, tests, and commit or tag that
   prove it, and stop there. Producing a plan for work that's already
   done isn't a smaller or safer version of this skill's job; it isn't
   this skill's job at all, the same way planning against nothing
   accepted yet isn't (see the refusal below). If the slice is only
   partially present, or present but not actually satisfying the
   accepted acceptance evidence, say exactly what already exists and
   what's still missing, and plan only the missing part -- the accepted
   goal still frames what "missing" means, but the plan itself closes
   only the actual gap, not the whole slice again.
2. **The accepted slice** -- its goal, why it was chosen now, what it's
   supposed to prove, its stated non-goals, and its acceptance evidence
   -- from whatever handed this off: a next-best-slice recommendation, a
   ticket, a one-line ask. This is the plan's only source of what to
   build. If it's ambiguous about a specific behavior, that ambiguity
   gets named as a known risk or resolved with the smallest possible
   judgment call -- never quietly filled in with an assumption that
   expands what the slice does.
3. **The real codebase, read, not guessed.** A repository map or
   orientation report tells you where things generally live; only
   reading the actual files this slice will touch tells you where the
   seams really are, what the existing invariants actually are, and
   what would break. A plan grounded in a description of the
   architecture instead of the architecture itself is a plan that
   guesses, and guesses are exactly what turn into rework once someone
   starts implementing.
4. **Whatever the accepted slice already settled about verification.**
   Its stated acceptance evidence is the baseline the verification
   strategy has to satisfy exactly -- a starting point to make concrete,
   not a floor to build past.
5. **Whether a likely seam quietly requires a new ownership decision.**
   The accepted slice fixes *what* to build; naming implementation seams
   still involves deciding *how*, and sometimes "how" means introducing a
   new production dependency, an external service, or a substantial
   custom implementation of something that looks like a solved problem
   (retry logic, caching, auth, rate limiting, parsing a standard
   format). That choice isn't this plan's to make quietly just because a
   seam needs to be named. **REQUIRED SUB-SKILL:** Use build-vs-adopt
   when a seam's implementation approach is genuinely undecided and looks
   material -- let it settle the approach before this plan names that
   seam around it. When the approach is obvious or already conventional
   for this codebase (the accepted slice already implies it, or it's
   another ordinary use of a dependency already in the project), that's
   not a new decision -- name the seam and move on.

If genuinely nothing accepted exists yet -- no recommendation, no
ticket, nothing to plan against -- don't invent a slice to plan around.
Say plainly that there's nothing accepted yet to plan from, and that
picking or justifying one is a different step in the workflow.

## What's in scope, and what only sounds like it

- **In scope**: exactly what the accepted slice's stated goal and
  acceptance evidence call for. The behavioral contract below should be
  traceable back to specific lines in that acceptance, not to whatever
  would also be nice to have.
- **Necessary implementation judgment**: the accepted slice describes
  *what*, not *how* -- some decisions (which function absorbs the
  change, whether it's a new helper or an inline branch) exist only
  because someone has to actually write code. Make these decisions, make
  them the smallest ones available, and say so plainly in the plan
  rather than let them silently balloon into a design choice nobody
  asked for.
- **Out of scope, however reasonable it sounds**: a refactor that would
  make the seam cleaner, a generalization that would make the next
  similar slice easier, an adjacent bug noticed while reading the code,
  a broader verification pass "while we're testing this anyway." None of
  these are what was accepted. Name them if they're worth naming --
  Explicit non-goals and Known risks exist for exactly that -- but plan
  none of them, and don't recommend that someone pick them up next.
  Choosing work is a different step in this workflow; this one only
  plans the slice already chosen.

## What must not change

Every slice plan names the invariants the implementation must preserve
-- existing behavior, contracts, or architectural boundaries that this
change must not cross, even when crossing one would make the
implementation easier or the resulting code slightly cleaner. An
invariant worth naming is usually one of:

- A contract something else already depends on (a function's existing
  signature, a data shape another module reads, a guarantee documented
  or tested elsewhere).
- A boundary the codebase already draws on purpose (a layer that isn't
  supposed to reach into another, a module that owns some piece of state
  exclusively).
- A property the accepted slice's own goal depends on staying true (if
  the goal assumes requests are idempotent, this plan can't quietly
  introduce a path where they aren't).

If the smallest implementation of the accepted goal seems to require
breaking one of these, that tension isn't a shortcut to take quietly --
name it explicitly as a known risk, and let the plan's seams and
behavioral contract reflect the version that holds the invariant, even
if it costs a little more implementation size. A plan that's smaller and
simpler only because it quietly voids an invariant is smaller and
simpler for whoever implements it and nobody else; everything downstream
that relied on the invariant inherits the cost instead.

## A verification strategy has a size, too

The same discipline that keeps implementation seams small applies to
verification: it should check exactly what the behavioral contract
promises, not everything reachable from the code this slice touches. A
slice that adds one new validation rule needs a check that the rule
fires and one that unrelated input stays untouched -- it doesn't need a
full regression pass over the module's other twelve rules, a coverage
audit of the whole file, or a "verify everything while we're in there."
A verification plan that's grown past the behavioral contract is usually
scope creep wearing a responsible-sounding coat. If the accepted slice's
acceptance evidence already named a check, this section makes that check
concrete -- it doesn't add a superset of it.

## What this skill refuses to do

Even when a request bundles a reasonable planning ask together with one
of these:

- Recommend different work, or a different slice than the one already
  accepted. If the accepted slice looks wrong once you've read the
  actual code, say so as a named risk -- don't quietly swap in a better
  idea and plan that instead.
- Redesign the feature, or propose an alternative approach to what the
  goal describes, because a cleverer one occurred to you while reading
  the code.
- Expand scope -- "while you're at it," an adjacent refactor, a
  generalization, a bug spotted nearby. Name it, plan none of it.
- Produce a roadmap, a backlog, or a list of next steps beyond this one
  slice.
- Review an implementation. This skill plans before code is written; if
  also asked to evaluate already-written code against this plan, say
  that's a separate pass and out of scope here.
- Rewrite architecture, even in service of making this one slice easier
  to build. An architectural change is a slice of its own, subject to
  its own justification -- not something this plan backs into because it
  happened to be convenient here.

If a request bundles a legitimate planning ask together with one of
these, plan the accepted slice as scoped above, and say plainly that the
rest is out of scope for this skill, rather than quietly folding it in
to be helpful.

## Report

Use this exact structure:

```
# Slice Plan: <slice name or one-line goal>

## Goal
<what this slice does, restated from the accepted recommendation --
not reinterpreted or expanded>

## Behavioral contract
<the specific, observable behavior the implementation must satisfy --
inputs, outputs, states, and edge cases the goal or acceptance evidence
actually names>

## Likely implementation seams
<where in the real codebase this will touch -- files, functions,
modules -- based on having read them, not guessed; "likely" because the
actual implementation may adjust once someone is in the code>

## Invariants
<what must remain true before and after -- existing contracts,
architectural boundaries, properties the goal depends on>

## Verification strategy
<the specific, minimal check(s) that would confirm the behavioral
contract holds -- scoped to it, not a general test pass>

## Explicit non-goals
<what this plan deliberately does not do, however tempting nearby --
refactors, generalizations, unrelated fixes, expanded scope>

## Known risks
<what could go wrong with even this minimal plan -- ambiguity in the
accepted slice, an invariant under tension, a seam that's genuinely
unclear until someone is in the code. A pre-existing bug noticed nearby
but unrelated to this slice belongs here as a one-line flag, never as
something this plan fixes or recommends fixing next>

## Completion evidence
<the concrete observation that would tell us this slice is actually
done -- tied directly to the behavioral contract and verification
strategy, not a general "tests pass">
```

Leave a section's body as "None." or an explicit note rather than
omitting it -- an absent section reads as "not considered," which is
worse than an honest empty result.
