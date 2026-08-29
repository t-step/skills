---
name: state-ownership-audit
description: >-
  Determines who has authority to write a piece of mutable state (a row,
  cache, index, projection, queue message, external mirror, config copy, or
  coordinator artifact) versus who holds a subordinate copy, and whether
  writes, sync, disagreement handling, and failure/recovery preserve that
  authority. Centers on facts, not stores: authoritative representation,
  every legitimate writer, each other representation's sync mechanism, the
  real consistency requirement, and any second-writer or
  circular-authority hazard -- tagged observed, inferred, or
  unresolved/conflicting, never inferred from durability or naming alone.
  Use before changing how or where a fact is written, before trusting a
  "source of truth" comment, or when asked who owns this state or whether
  two things must stay in sync. Distinct from domain-orientation (meaning,
  not write authority) and lifecycle-audit (transition mechanics for one
  entity -- hand off, don't redo). Refuses to invent a source of truth or
  redesign ownership.
---

# State Ownership Audit

Two rows, three caches, and a search index can all say something about the
same underlying fact, and disagree about who gets to change it. The pull is
always toward a comfortable-sounding shortcut: whatever's in the database is
the truth, whatever's named `source_of_truth` is the truth, whatever
survives a restart is the truth. None of those are evidence. A cache also
survives a restart. A comment also claims things it doesn't enforce. A
database row can hold a value nothing currently has standing to have
written, left over from code that used to run.

This skill's only job is to determine, from evidence, which representation
of a fact actually has authority to change it, who else is allowed to write
it, which other representations are legitimately subordinate, and whether
the writes, synchronization, disagreement handling, and failure/recovery
paths around that fact actually preserve the authority they imply. It does
not redesign the ownership model, does not invent a coordinator or
reconciliation job to fix what it finds, and does not treat intentional
staleness or partitioned authority as a defect just because two things
technically disagree for a while.

## Unit of analysis: a fact, not a store

The habit this skill exists to break is auditing tables instead of facts.
A **fact** is one real decision or piece of information the system tracks
-- "this order has been paid," "this tenant's plan tier," "this replica's
last-applied offset" -- not a row, column, or file. The relationship
between facts and storage locations runs both ways, and both directions
matter:

- **One fact, several stores.** A user's display name might live in a
  `users` row, a search index, a CDN-cached profile page, and a session
  token's claims. That's one fact worth one audit entry, with four
  representations -- not four unrelated things to inventory separately.
- **One store, several facts.** A single `users` row might hold an
  `email` column the identity service alone may change and a
  `display_name` column the profile service alone may change. That's two
  facts sharing a table, not one. Auditing "the `users` table" as a unit
  would blur two entirely separate authority questions into one.

Decide what counts as one fact by what changes together and is validated
together, not by what's colocated in the same schema object. When it's
genuinely unclear whether two values are one fact or two, say so as an
unresolved question rather than picking a granularity that makes the
write-up tidier.

## What earns a full entry

Not every mutable field is a state-ownership question. Producing a full
entry for every column in every table is the database/schema-audit failure
mode this skill exists to avoid. Before giving a fact its own entry, check
that it clears at least one of these:

- **More than one representation exists** -- a cache, index, replica,
  projection, queue message, external-system mirror, config copy, or
  coordination artifact holds a copy or derivation of it, beyond its
  single authoritative store.
- **More than one writer has apparent or actual standing** -- more than
  one code path, service, job, or actor can plausibly or actually write
  it, whether or not that turns out to be legitimate.
- **Its authority is scoped, conditional, or transferable** in a way
  that's easy to get wrong -- see "Authority is not always global" below.
- **The target itself raises the question** -- a ticket, comment, spec,
  incident, or test explicitly claims or questions synchronization,
  canonicality, or "staying in sync" for it.

A fact with exactly one representation, one writer, and unconditional
global authority is **clean**. Name it in one line under "Facts in scope"
and move on -- it doesn't get a full entry. A target where everything is
clean (a straightforward CRUD service, one database, one writer per field)
is fully and honestly served by a short report saying so. Padding it with
full entries for every field to look thorough is a worse outcome than a
short, honest "nothing more to say here."

## How this composes with the rest of this skill family

- **`repo-orientation`** already produces a "Systems of record and
  ownership" section naming where authoritative state lives at a glance.
  If it exists for this target, start from it as a pointer to where to
  look, not as a finished answer -- it's deliberately shallow (one line
  per system), while this skill exists specifically to go deeper: legitimate
  writers, synchronization mechanics, disagreement behavior, hazards.
  Don't re-derive entry points, build commands, or the engineering map;
  that's out of scope here.
- **`domain-orientation`** characterizes what a concept *means* and gives
  it a one-line "Canonical representation," "Other representations," and
  "Authority" field as part of a broader semantic map. This skill starts
  where that field stops: not "which component has standing to write it,"
  stated once, but the full legitimate-writer inventory, every subordinate
  representation's actual sync mechanism, what happens on disagreement, and
  whether a second writer has quietly appeared. If a domain-orientation
  report already exists for this target, reuse its concept inventory as a
  starting point rather than re-deriving what the concepts mean.
- **`lifecycle-audit`** owns the full state/transition/invariant
  characterization for an entity that carries its own lifecycle, and its
  own mechanism/consistency-requirement analysis for how two lifecycles
  interact. When a fact in this audit turns out to be carried by a
  lifecycle-bearing entity, name it as a lifecycle-audit candidate and
  consume its owner/mechanism/consistency findings rather than
  re-deriving state-machine mechanics here -- but still ask this skill's
  own questions on top: can a second writer bypass the lifecycle's owner,
  and does authority over the fact shift between components as the entity
  moves through its lifecycle (see "Lifecycle interplay" below), which
  lifecycle-audit does not ask.
- **`spec-pressure-test`** pressure-tests a not-yet-built spec for places
  its own wording fails to decide who owns a piece of state -- its
  "Ownership and authority" category exists for exactly that gap, and
  explicitly defers a full ownership mapping to a deeper pass once a
  system has that much interacting state. This skill is that deeper pass,
  but it runs on a *decided* system -- an implementation, or a spec/design
  whose ownership model is actually settled, not one still being
  adversarially checked for whether it decided anything at all. Given an
  undecided spec, report what's unresolved as unresolved; don't manufacture
  scenarios to attack wording that spec-pressure-test already owns.
- **`change-review`** and **`evidence-verification`** judge whether a change
  or a claimed outcome is correct -- consumers of an ownership map, not
  producers of one. This skill doesn't review a diff or verify a "done"
  claim.

If a target's complexity turns out to need one of these instead -- or in
addition -- say so explicitly and hand off, rather than absorbing that
work into this report.

## Ground before characterizing anything

Inspect what's actually there. A plausible architecture-convention guess is
not evidence:

- **Every write path**, not just the intended API -- direct writes, admin
  tools, batch jobs, migrations, backfills, replication targets, and event
  consumers that write back, found by tracing mutations broadly, not by
  trusting a single documented entry point.
- **Validation and invariant checks performed at the moment of a write** --
  what does a write path actually check before it's allowed to proceed, and
  against which representation?
- **Recovery, rebuild, bootstrap, and seed code** -- what does the system
  reconstruct from, and what would be permanently lost if a given
  representation were wiped?
- **Explicit reconciliation, conflict-resolution, last-write-wins, or
  epoch/fencing logic** -- what actually happens, mechanically, when two
  representations disagree.
- **Migration and backfill direction** -- which system seeded which,
  which often reveals precedence nothing else states directly.
- **Tests encoding expected behavior under disagreement or partial
  failure** -- these often state a tiebreak or a tolerance more plainly
  than any prose does.
- **API/contract definitions** distinguishing read replicas or read-only
  mirrors from write endpoints.
- **Incident postmortems, tickets, or comments describing an actual past
  disagreement** and how (or whether) it was resolved.
- **Existing `repo-orientation` or `domain-orientation` output** for this
  target, reused as a starting inventory rather than re-derived.

If something on this list doesn't exist or can't be found, that's a fact
for Unknowns, not a gap to fill with a plausible-sounding guess.

## Three tiers, with a fourth outcome for ownership specifically

Same discipline as the rest of this skill family:

- **Observed** -- a write path, a validation check, a rebuild routine, or a
  reconciliation rule you can point to directly.
- **Inferred** -- one short, defensible step from something observed:
  "every write to this cache happens inside the same handler that also
  commits the database row, and no other code path touches the cache key,
  so this cache is a same-transaction derivative of that row" is inference.
  "This was probably built as a cache for performance" with no write path
  actually traced is not a short step from anything observed -- that's a
  story.
- **Unresolved** -- the evidence doesn't settle it at all. Say so plainly.
- **Conflicting** -- evidence exists on more than one side and disagrees
  with itself: a comment names one authority while the executable write
  path establishes another; two components each behave as if they alone
  may write the fact, and nothing in the target says which one is right.
  Report both sides and what conflicts, named as its own outcome -- don't
  quietly resolve a conflict by picking whichever side sounds more
  architecturally sensible. This is a distinct, common, and legitimate
  audit result, not a failure to dig deeper.

When unsure which tier applies, use the weaker one. An audit that
under-claims authority costs a reader a few minutes of double-checking; one
that over-claims can send someone changing the wrong representation and
watching the "canonical" one silently overwrite them.

## What does not establish authority

None of these settle who owns a fact, on their own:

- **Stored in a database.** Durability isn't authority -- a nightly-
  refreshed cache also persists across restarts.
- **Named `source_of_truth`, `canonical_id`, `master_copy`, or similar.**
  A name is a claim someone made, not evidence of what the write paths,
  validation, and recovery code actually do.
- **More durable-looking or more "permanent" than the alternative** (a
  compiled lockfile versus the manifest that generated it, a committed
  Terraform state file versus the manifest that produced the plan) --
  durability differences frequently exist for reproducibility or
  performance, not because the more durable copy is where the decision
  originates.
- **Exposes an API and the alternative doesn't.** Exposure is a read/write
  surface, not a standing determination -- a read-only API in front of a
  replica is still a replica.
- **Written more frequently than another representation.** Write
  frequency reflects traffic patterns, not authority.
- **A comment or docstring asserts it's canonical.** Prose is a claim to
  check against executable evidence, exactly as in `repo-orientation` and
  `domain-orientation` -- when they conflict, name the conflict as a
  Conflicting-tier finding rather than trusting the comment.
- **Survives a restart, or outlives the process that populated it.**
  Persistence characteristics of a copy say nothing about where the real
  decision was made.

What actually establishes authority is positive evidence of one of these:
what a rebuild or bootstrap path treats as the seed; what a
conflict-resolution or reconciliation mechanism treats as correct when
representations disagree; what a write-time validation check reads before
permitting a write; which system another system defers to and never
overrides, even when both could plausibly answer (a webhook handler that
only ever accepts an external provider's state and has no code path that
lets local logic override it, for example).

## Authority is not always global

Before assuming a fact has exactly one owner for all time and all
instances, check which shape the evidence actually supports:

- **Global** -- one authority for every instance of the fact, with no
  observed exception.
- **Scoped / partitioned** -- authority is divided along a real dimension
  (per-tenant, per-shard, per-region, per-key range), and each partition's
  owner is authoritative only within its own slice. Two partitions each
  legitimately writing "their own" copy of a similarly-shaped fact is not
  a multi-writer hazard; it's partitioned authority, and should be named
  as such along with the partitioning dimension.
- **Conditional** -- authority depends on a mode, flag, or environment
  (e.g., a feature flag routes writes to a new service for some accounts
  and leaves a legacy path authoritative for the rest). Name the
  condition and what determines it.
- **Transferable** -- authority moves over time via an explicit mechanism:
  leader election, a lease, an epoch/fencing token, a handoff protocol.
  For these, specifically check whether a write path that could execute
  under a stale claim to authority (a former leader that hasn't yet
  learned it lost leadership) is actually guarded against writing -- an
  unguarded write path under transferable authority is one of the more
  serious hazards this skill looks for, not a detail to skip past once
  the transfer mechanism itself is named.

A fact can combine shapes (globally scoped by tenant, and within a tenant,
transferable between two replicas during failover). Name the actual shape;
don't force it into "global" because that's simpler to write down.

## Characterize each fact that clears the bar

For each fact selected under "What earns a full entry," capture what the
evidence actually supports. Omit or mark **Unknown** any field it doesn't
reach:

- **Fact** -- the real decision or information this represents, in the
  target's own terms, not the name of a column.
- **Authoritative representation & authority scope** -- where the real
  value lives, and its shape (global / scoped / conditional / transferable,
  per "Authority is not always global"), each tagged observed / inferred /
  unresolved / conflicting.
- **Legitimate writers** -- every code path, service, or actor with
  observed standing to write the authoritative representation. If a
  writer's legitimacy is itself in question, name it here as a hazard
  rather than silently including or excluding it (see "Hunt for
  multi-writer and second-authority hazards" below).
- **Other representations** -- every projection, cache, index, replica,
  queue message, external mirror, config copy, or coordination artifact
  that also holds a copy or derivation of this fact. For each: what kind
  it is, how it's synchronized (same-transaction / synchronous push /
  asynchronous or event-driven push / pull-on-read / periodic batch /
  manual or on-demand regeneration / opportunistic best-effort / none
  observed), and whether it's fully reconstructable from the authority or
  would lose information if wiped (a representation that can't be fully
  rebuilt from its stated authority is not purely derived -- treat the
  information it alone carries as its own fact and give that fact its own
  authority determination, rather than leaving it folded into an entry that
  implies it's a safe-to-discard copy).
- **Consistency requirement & disagreement behavior** -- one of: no joint
  constraint; shared invariant with tolerable disagreement (name the
  staleness window, bounded or not); requires active reconciliation (name
  the specific invariant or correctness property at risk); ambiguous.
  This is shared vocabulary with `lifecycle-audit`'s mechanism/consistency
  analysis, applied here to a fact and its representations rather than to
  two interacting lifecycles. Alongside it, state what actually happens
  when representations disagree -- an observed tiebreak (authoritative
  wins on rebuild, last-write-wins by timestamp, epoch/fencing, manual
  resolution) or "none observed," which is itself a finding.
- **Reconciliation & recovery** -- any explicit reconciliation mechanism;
  what happens if a write to the authority succeeds but a synchronization
  step to another representation fails partway (retried, dead-lettered,
  silently dropped, or unaddressed); whether the authoritative store
  itself can be reconstructed after loss, and from what.
- **Lifecycle interplay** -- "None observed," or "Candidate for
  `lifecycle-audit`" with the reason, naming which lifecycle stage(s), if
  known, shift authority to which component. Stop there; the state/
  transition mechanics belong to that skill, not this one.
- **Unknowns** -- specific to this fact.

A fact with a clean, simple picture is fully and honestly served by a short
entry that says so.

## Hunt for multi-writer and second-authority hazards

This is the actual point of the audit, not a byproduct of the inventory
above. For every fact in scope:

1. **List every write path to the authoritative representation**,
   including ones nobody would call "the API" -- admin tools, one-off
   scripts, migrations, batch jobs. A write path found only by tracing
   mutations, not by reading the documented interface, is exactly the kind
   this step exists to catch.
2. **For every other representation, ask whether anything ever sets its
   value independent of a read or derivation from the authority.** A cache
   *invalidated* (its key deleted, to be recomputed from the authority on
   next read) is not a hazard. A cache *populated* with a value computed or
   supplied independently of the authority is a second writer to the same
   conceptual fact, whether or not the two values usually happen to agree.
3. **Check reconstructability as a hazard test, not just a description.**
   If wiping a "derived" representation would lose information nothing
   else has, something is quietly authoring facts through what everyone
   is calling a cache. Flag this explicitly rather than letting the
   "Other representations" entry imply it's disposable.
4. **Under transferable or conditional authority, check for a fencing or
   validity guard on every write path that could execute under a stale
   claim to authority.** An absent guard here is a hazard even if no
   concrete incident is on record -- the mechanism for a former owner to
   write after losing authority either doesn't exist, is prevented, or is
   unaddressed, and which of those three is true is worth stating plainly.
5. **Check for circular authority** -- a claims authority over a fact by
   reading B, and B's own authority for a related fact depends on reading
   A. When two representations each defer to the other, nothing actually
   resolves a disagreement between them; name this explicitly rather than
   picking one side to call authoritative because the audit needs an
   answer.
6. **Check for a fact with no clear owner of resolution** -- a case where
   representations disagree, no reconciliation mechanism exists, and
   nothing in the evidence indicates who or what is responsible for
   noticing or fixing it. This is a real, reportable finding on its own,
   distinct from "requires active reconciliation" (which implies a
   mechanism exists or should) -- here, name plainly that resolution
   currently belongs to no one.

Flag what you find; do not propose the fix. Naming that a legacy batch job
writes the same column an API also writes, with no ordering guarantee
between them, is this skill's job. Designing the migration that removes one
of the writers is not.

## Separate mechanical findings from design judgment

Some findings are structural facts, checkable directly against the target:

- "Two code paths write `Subscription.plan_tier`: the billing webhook
  handler and the admin console's direct update endpoint."
- "The search index is repopulated only by consuming the CDC stream off
  the `orders` table; no code path writes to the index directly."
- "No fencing check exists in `apply_write()`; a replica that has lost
  leadership but hasn't yet observed the new leader can still accept and
  persist a write."

These carry high confidence and belong in the report without much hedging.

Some conclusions require architectural or domain judgment past what the
evidence alone proves:

- "The admin console's direct write is illegitimate and should route
  through the webhook path instead."
- "This fact should have one global owner instead of per-region
  authority."
- "This staleness window is too wide for the invariant it's supposed to
  support."

State these as judgments, with the structural finding that motivates each
one named explicitly, not with the same confidence as the mechanical
findings above.

## What this skill refuses to do

Even when a request bundles it in:

- Give every mutable field, column, or table its own entry regardless of
  whether it clears the bar in "What earns a full entry" -- see that
  section.
- Propose a new source of truth, canonical store, reconciliation mechanism,
  sync job, or coordinator as the fix for a hazard or gap it finds. Name
  the hazard; the remedy is a human design decision.
- Perform full lifecycle state/transition/invariant characterization, or
  the mechanism/consistency analysis between two lifecycles -- that's
  `lifecycle-audit`. Name a candidate and consume its output; don't redo it.
- Characterize general domain meaning, terminology drift, or bounded-
  context boundaries -- that's `domain-orientation`. Reuse it if it exists.
- Rebuild the engineering/operating map -- entry points, build/test
  commands, general systems-of-record listing -- that's `repo-orientation`.
- Manufacture scenarios to attack a not-yet-decided spec's wording for
  failing to assign ownership -- that's `spec-pressure-test`'s "Ownership
  and authority" category. Report an undecided spec's ownership as
  unresolved; don't adversarially test wording that skill already owns.
- Review a diff, judge merge-readiness, or verify a "done" claim -- that's
  `change-review` (and, for Bindle mechanical evidence pointers specifically,
  `evidence-verification`).
- Treat a legitimately partitioned, conditional, or transferred authority
  as if it should be a single global owner.
- Treat an intentional, bounded eventual-consistency window as a defect
  merely because two representations can disagree for a while.
- Infer authority from storage location, durability, a `source_of_truth`-
  style name, a comment, API exposure, or write frequency alone -- see
  "What does not establish authority."
- Silently pick a side when evidence about authority conflicts. Report the
  conflict as its own outcome and say what's unresolved.
- Redesign, rename, or fix the ownership model, beyond naming exactly the
  correction one specific hazard requires -- and even then, only if asked.

If a request bundles a legitimate ownership audit with one of these --
"map out who owns this state and then fix it," "audit this and design the
sync mechanism" -- say plainly that the second part is out of scope for
this skill, then deliver the audit itself.

## Report

Use this exact structure. Omit no heading; use "None identified." or
"Not established from available evidence." rather than dropping a section
that came up empty:

```
# State Ownership Audit: <target>

## Scope and evidence inspected
<What was actually read to ground this audit -- code, schema, configs,
tests, tickets, incident notes, existing repo-orientation/domain-orientation
output reused. Name anything relevant that couldn't be inspected.>

## Facts in scope
<Which facts cleared the bar in "What earns a full entry," and a one-line
note on what was excluded as clean (single representation, single writer,
unconditional global authority) rather than omitted silently.>

## Fact-by-fact characterization
### <fact>
- Fact: <...>
- Authoritative representation & authority scope: <where, and global /
  scoped / conditional / transferable -- tagged observed / inferred /
  unresolved / conflicting>
- Legitimate writers: <...>
- Other representations: <kind, sync mechanism, reconstructability -- for
  each>
- Consistency requirement & disagreement behavior: <no joint constraint /
  shared invariant with tolerable disagreement (window) / requires active
  reconciliation (invariant named) / ambiguous -- plus the observed
  tiebreak or "none observed">
- Reconciliation & recovery: <...>
- Lifecycle interplay: <None observed. | Candidate for lifecycle-audit --
  why, and which stage(s) shift authority>
- Unknowns: <...>
(repeat per fact)

## Multi-writer and second-authority hazards
<The consolidated, ranked-by-consequence output of "Hunt for multi-writer
and second-authority hazards" -- each hazard naming the specific write
paths or representations involved. "None identified." if the hunt found
none -- a real, useful result.>

## Unresolved or conflicting ownership
<Facts where evidence disagrees with itself (Conflicting tier), or is
insufficient to determine authority at all (Unresolved tier), preserved
explicitly rather than resolved toward whichever side sounds more
sensible. "None identified." if none.>

## Findings
### Structural (mechanical, high confidence)
<Facts checkable directly against the target.>

### Judgment calls (semantic, human decision needed)
<Conclusions past what the evidence alone proves, each with the structural
finding that motivates it.>

## Unresolved questions
<Open questions the evidence doesn't settle that aren't tied to one
specific fact's ownership tier -- e.g., whether the target intends a
boundary this audit couldn't confirm either way.>

## Working summary
<A few sentences to a short paragraph: for each consequential fact, where a
decision to change it is supposed to originate, what else may become
stale, and what restores consistency -- what another agent needs before
touching any of this state.>
```

A target where every fact in scope is clean, or where the audit turns up
no hazard and no unresolved conflict, is fully and honestly served by a
short report that says so and stops -- padding it with speculative hazards
or hypothetical disagreements is a worse outcome than an honest "nothing
more to say here."
