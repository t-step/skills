---
name: domain-orientation
description: >-
  Maps what a codebase's domain concepts actually mean before
  consequential changes begin: first-class concepts vs. implementation
  artifacts, terms used for each (and where a term drifts or collides
  across layers), canonical vs. derived/cached representations,
  authority, observed invariants, relationships, domain boundaries, and
  disagreements between code, schema, tests, and docs. Claims are tagged
  observed, inference, or unresolved; meaning comes only from codebase
  usage, never a name's implied meaning. Use before touching core
  entities, before trusting two similar-sounding fields mean the same
  thing, or when asked to understand the domain model. Distinct from
  repo-orientation (engineering map -- reuse, don't redo), lifecycle-audit
  (transition analysis for lifecycle-bearing entities -- flags candidates,
  stops there), spec-pressure-test (not-yet-built specs, not existing
  code), and slice-review/task-composition (consume this, don't produce
  it). Refuses to redesign the model, resolve drift, or invent semantics.
---

# Domain Orientation

Before an agent changes code that touches `Order`, `Account`, `Session`, or
any other named concept, it has usually already decided what that concept
means -- often within the first few seconds of seeing the name, before
reading a single line of how the codebase actually uses it. That decision
is frequently wrong in a way that's invisible until the change ships: the
`Order` here is a job-queue's processing sequence, not a retail purchase;
the `status` field that looks authoritative is a nightly-refreshed cache of
something else that's authoritative; the `Customer` in this service and the
`Account` in that one look interchangeable and aren't, or are, and nothing
says which.

This skill's only job is producing that missing piece: a compact map of
what the domain concepts in front of an agent actually mean, according to
how the codebase itself defines, validates, stores, and uses them --
before the agent starts planning or implementing anything on top of an
assumed meaning that was never checked.

## What "domain" means here

Not necessarily a business domain. Every codebase has a domain -- the set
of concepts and rules the software is actually about -- distinguished from
the engineering scaffolding used to implement it. Sometimes that's a
business domain (orders, customers, payments). Sometimes it's a technical
or tooling domain with its own real vocabulary and rules (a job scheduler's
`job`/`lease`/`worker`, a build system's `target`/`artifact`/`cache key`).
Sometimes it's both at once. Determine which from evidence in front of
you, not from assuming every codebase secretly has a business domain
underneath, and not from refusing to look because "this is just
infrastructure, there's no domain here." A domain orientation that forces
retail-style vocabulary onto a compiler, or that shrugs off a compiler as
domain-free, has both made the same mistake: substituting an assumed shape
for the one the evidence actually shows.

## How this composes with the rest of this skill family

This skill sits between `repo-orientation` and the skills that consume
domain understanding for a specific purpose. Know the boundary on both
sides before starting:

- **`repo-orientation`** builds the engineering operating map: entry
  points, build/test commands, technical systems of record, where code
  belongs. If one already exists for this target, use it as a pointer to
  where to look -- don't re-derive entry points or verification commands
  here; they're not this skill's deliverable. This skill starts where that
  one stops: not "where does the state live and how do I run this" but
  "what does the state actually mean, and can I trust the name."
- **`lifecycle-audit`** owns the full characterization of an entity that
  carries its own lifecycle -- states, transitions, triggers, invariants,
  and the mechanism/consistency analysis between two interacting
  lifecycles. When this skill notices a concept that appears to have more
  than one meaningful state with its own transitions, name it as a
  lifecycle-audit candidate and stop there. Do not inline a state/
  transition/interaction analysis here; that's a different, deeper
  procedure with its own admission bar and vocabulary, and redoing it
  inline produces a shallower, less trustworthy version of the same
  answer.
- **`spec-pressure-test`** pressure-tests a not-yet-built spec's stated
  requirements for gaps and ambiguity. This skill characterizes the
  semantics an *already-existing* implementation embodies. Don't run this
  skill to find holes in a spec, and don't run spec-pressure-test to
  understand what current code means.
- **`slice-review`, `task-composition`, and implementation-planning
  skills** consume domain understanding to review a diff or plan work.
  This skill produces the understanding; it does not review, plan, slice,
  or choose what to build.

If a target's complexity turns out to genuinely need one of these deeper
or narrower passes, say so explicitly and point at it, rather than
absorbing that work into this report.

## Gather before characterizing anything

Inspect what's actually there. Don't reconstruct domain meaning from what
a name would suggest in a typical system of this apparent kind:

- Persisted schema, migrations, and the model/entity classes built on
  them -- but treat these as a starting inventory, not the finished map.
- Validation code, domain-specific exceptions, and guard clauses -- this
  is usually where a real business rule lives, as distinct from purely
  technical/format validation (a max-length check is not a domain
  invariant; "a refund cannot exceed the original charge amount" is).
- API/contract definitions (request/response shapes, GraphQL schema,
  protobuf, OpenAPI) -- these often reveal which fields are treated as
  authoritative externally versus internal-only, and frequently use
  different names than the storage layer for the same concept.
- Tests that assert domain/business behavior specifically, not just CRUD
  round-trips -- these often state an invariant or a term's meaning more
  explicitly than the implementation code does.
- Naming across layers: does the same underlying concept carry different
  names in the schema, the API, the internal service code, and the UI?
  Does the same name mean different things in different modules or
  services?
- Comments, docstrings, READMEs, and design docs describing domain
  concepts -- claims to check against executable evidence, not facts to
  repeat. When they conflict with what the code actually does, the code
  wins and the conflict itself is worth naming, exactly as in
  `repo-orientation`.
- Historical residue: deprecated-but-still-read fields, migrations that
  renamed or merged a concept, dual-write code, a `_v2` sibling of an
  existing class -- often the strongest evidence of terminology drift or
  of a representation that used to be canonical and no longer is.
- Existing `repo-orientation` or `lifecycle-audit` output for this target,
  if available -- reuse it rather than re-deriving overlapping ground.

If something on this list doesn't exist or can't be found, that's a fact
for Unknowns, not a gap to fill with a plausible-sounding guess.

## Three tiers -- tag every claim

Same discipline as the rest of this skill family, applied to domain
claims specifically:

- **Observed** -- a term, field, validation rule, or relationship you can
  point to directly: "`status` is an enum with exactly these four values,
  written only by `mark_paid`/`mark_shipped`" is observed.
- **Inference** -- one short, defensible step from something observed:
  "`Order` and `PurchaseOrder` share a foreign key into the same
  `line_items` table and no code path treats them as separate identity
  spaces, so they're the same concept under two names" is inference.
  "This was probably renamed during a migration to sound more modern" is
  not a short step from anything observed -- that's a story, not an
  inference.
- **Unresolved uncertainty** -- the evidence doesn't settle it: two
  plausible owners for the same fact, a term used only once with nothing
  to confirm or rule out an intended meaning, no evidence either way on
  whether two similarly-named concepts are meant to converge. State it
  plainly; this is a common and legitimate output, not a failure to dig
  deeper.

When unsure which tier applies, use the weaker one. A term's real-world or
"usual" meaning is never itself evidence -- a class named `Order` is not
assumed to mean a retail purchase order, a `Member` is not assumed to be a
`Customer`, and a `Session` is not assumed to be a login session, until the
codebase's own definitions, validation, and usage say so.

## Selecting what belongs in the map

The habit this skill exists to break is treating "list the ORM models" or
"summarize the schema" as the deliverable. Neither is a domain map: one
inventories persistence, the other's a data dictionary. This skill
optimizes for what's decision-useful -- what an agent needs to not
misunderstand or corrupt domain state -- not for exhaustive coverage of
every class, table, or field.

Before giving something its own entry in the map, check that it clears a
bar:

- **First-class domain concept** -- referenced by name across more than
  one layer (schema, API, business logic, tests), carries an observed
  invariant or business rule of its own, or is central to whatever change
  or question motivated this orientation. These earn a full entry.
- **Implementation artifact** -- a join table with no independent meaning,
  generic framework scaffolding (session/audit-log tables with no
  domain-specific rule), a technical cache with no invariant of its own.
  Name that it exists and what it's for in one line; it doesn't get a full
  entry. Don't let bulk substitute for importance here any more than in
  `repo-orientation` -- twenty generated DTO classes are not twenty domain
  concepts.

A domain concept is not only a noun with fields. In workflow- or
rules-heavy systems, the load-bearing domain concepts are often verbs,
policies, or processes with no single persisted row of their own -- "what
makes a deploy eligible for promotion," "what a gate checks before it
passes" can matter more than any one entity's schema. Don't force every
concept into an entity-with-fields shape just because that shape is easier
to write down; if the real semantics live in a policy function or a rules
table, characterize it as that.

Scope to what's actually needed. If the request names a specific area of
the domain or an intended change, prioritize evidence and characterization
there over a whole-domain sweep. A full sweep is appropriate for a
genuinely unfamiliar codebase or an explicit whole-domain request -- even
then, stay selective about depth per concept rather than producing a
uniformly exhaustive entry for everything that exists.

## Characterize each first-class concept

For every concept that clears the bar above, capture what the evidence
actually supports. Omit or mark **Unknown** any field it doesn't:

- **Terms used** -- every name the codebase itself uses for this concept,
  and where each appears (schema, API, internal code, UI copy). One
  concept, one entry, however many names it goes by.
- **Why first-class** -- the concrete evidence that earned it a full
  entry.
- **Canonical representation** -- where the authoritative state actually
  lives.
- **Other representations** -- every other place a copy, projection,
  cache, or convenience derivation of it exists, each labeled as such,
  never given its own peer entry. This generalizes `lifecycle-audit`'s
  authoritative-representation field to concepts that never carry a
  lifecycle at all -- a `Money`/`Price` value object with a cached
  currency-converted copy needs this distinction just as much as a
  stateful entity does.
- **Authority** -- which component, module, or service actually has
  standing to write it. Not who reads it.
- **Observed invariants / business rules** -- constraints on valid values
  or combinations that the code actually enforces, distinguished from
  purely technical validation (format, length, type).
- **Relationships** -- to other first-class concepts, as observed
  (foreign keys, composition, explicit references) -- not invented from
  what would make domain sense.
- **Lifecycle** -- "None observed" if it doesn't carry independent states
  of its own, or "Candidate for `lifecycle-audit`" with the one-line
  reason if it does. Stop there; don't characterize the transitions
  yourself.
- **Unknowns** -- specific to this concept.

A concept with a clean, simple picture is fully and honestly served by a
short entry that says so -- don't pad a field that has nothing more to
say.

## Build the terminology map

A separate, often the single most valuable, section: every term that means
different things in different places, or where two terms plausibly name
the same underlying concept but nothing confirms it. This is not the same
list as the concept entries above -- it's specifically about naming
collisions and near-misses, surfaced explicitly rather than silently
resolved one way or the other while writing the concept entries.

For each: the term(s) involved, where each is used, what the evidence
shows (same concept under different names; same concept with real
semantic drift between uses; genuinely different concepts that happen to
share or resemble a name), and what's unresolved. Resist collapsing two
similar-sounding terms into one just because a reader (including the user
asking for this orientation) suggests they're "obviously" the same --
name the concrete evidence for treating them as same, different, or
undetermined, rather than taking the suggestion on faith.

## Domain boundaries

Name a boundary between subsystems or bounded contexts only where evidence
shows one: separate schemas, separate services, an explicit translation or
anti-corruption layer, a term that's deliberately given different meanings
in each side with something (code, docs) acknowledging the split. A
`contexts/billing/` and `contexts/auth/` directory pair sitting side by
side is not proof of a bounded-context split by itself -- exactly the same
"don't infer intent from a name alone" discipline `repo-orientation` uses
for `legacy/`/`v2/`/`experimental/` applies here to context-looking
directory names. Where a shared-looking term crosses a real seam, state
whether the two sides mean the same thing, related-but-distinct things, or
whether that's unresolved.

## Surface disagreements, don't resolve them

When code, schema, tests, comments, docs, or naming disagree about what a
concept means or how it behaves, name the disagreement explicitly rather
than silently picking the side that sounds more authoritative. Executable
evidence (code that runs, a schema that's enforced, a test that currently
passes) outweighs prose (a comment, a docstring, a README) when they
conflict, exactly as in `repo-orientation` -- but the fact that they
disagree is itself a finding worth keeping, not something to quietly
erase once the "winning" side is decided.

## What this skill refuses to do

Even when a request bundles it in:

- Build the engineering/operating map -- entry points, build/test
  commands, technical systems of record. That's `repo-orientation`; reuse
  it if it exists, don't recreate it here.
- Perform a full lifecycle audit -- states, transitions, triggers,
  invariants, and interaction mechanism/consistency for a specific entity.
  That's `lifecycle-audit`; name a candidate and stop.
- Pressure-test a spec or plan document's stated requirements. That's
  `spec-pressure-test`, and it runs on not-yet-built material; this skill
  runs on what's already implemented.
- Review a diff or PR, judge merge readiness, or verify a completed
  change. That's `slice-review`.
- Decompose work, slice a plan into sessions, or choose what to build
  next. That's `task-composition` or `next-best-slice`.
- Propose a target domain model, rename concepts, resolve terminology
  drift, or recommend a refactor to "clean up" a confusing boundary or
  naming collision. Name the drift and the evidence behind it; resolving
  it is a downstream human or design decision, not this skill's output.
- Invent domain semantics from a name's common or familiar meaning, or
  from what a codebase "of this kind" usually looks like.
- Give every persisted field, table, or class its own entry regardless of
  whether it clears the first-class bar -- see "Selecting what belongs in
  the map."
- Treat prose describing a concept as more authoritative than the
  executable evidence it conflicts with, or silently drop the conflict
  once a side is chosen.
- Fabricate a bounded-context boundary from directory or module names
  alone, without a real seam in evidence.

If a request combines this with one of these -- "map the domain and then
redesign it," "orient me and tell me what to build next" -- produce the
domain map as scoped here, then say plainly that the rest is out of scope,
rather than quietly folding it in or silently dropping half the request.

## Report

Use this exact structure:

```
# Domain Orientation: <target>

## Scope and evidence inspected
<What was actually read, and what area this covers -- the whole domain or
a named part of it. Name any existing repo-orientation/lifecycle-audit
output reused, and anything relevant that couldn't be inspected.>

## Domain shape
<One or two sentences: is this a business domain, a technical/tooling
domain, or a hybrid, and what evidence supports that characterization.>

## First-class domain concepts
### <concept>
- Terms used: <...>
- Why first-class: <...>
- Canonical representation: <...>
- Other representations (derived/projected/cached/convenience copies):
  <... or "None observed.">
- Authority: <...>
- Observed invariants / business rules: <... or "None observed beyond
  technical validation.">
- Relationships: <...>
- Lifecycle: <None observed. | Candidate for lifecycle-audit -- <why>.>
- Unknowns: <...>
(repeat per concept)

## Implementation artifacts noted but not modeled
<What looked like a domain concept but didn't clear the bar, and why.>

## Terminology map
<Terms that drift, collide, or plausibly overlap across the codebase, per
term evidence, and what's unresolved -- or "None identified.">

## Domain boundaries
<Observed seams vs. name-only appearances, and what crosses them -- or
"Not established from available evidence.">

## Disagreements between evidence sources
<Code vs. docs/comments/tests/naming conflicts, named rather than
silently resolved -- or "None identified.">

## Unresolved questions
<The real open questions the evidence doesn't settle.>

## Working summary
<A compact operating model of what the domain actually means here -- a
few sentences to a short paragraph -- another agent could read before
planning or implementing on top of it.>
```

Leave a section's body as "Not established from available evidence." or
"None identified." rather than omitting the heading. Keep the whole report
tight: a domain orientation that takes longer to read than it would take
to just ask a domain expert has defeated its own purpose. A target with a
small, clean set of concepts and no meaningful drift or ambiguity is fully
and honestly served by a short report that says so and stops.
