---
name: stale-framing-audit
description: >-
  Identifies repository framing (READMEs, agent instructions, comments,
  specs, ADRs, naming, CLI help) that teaches a mental model current
  evidence no longer supports: contradicted, superseded-but-undated,
  aspirational-as-implemented, misleadingly emphasized, or omission-based.
  Ranks findings by framing reach and reasoning impact, not sentence count.
  Never flags clearly marked historical material, never assumes code
  outranks docs on intended (vs. current) model, and preserves genuine
  unresolved ambiguity and intentional compatibility naming instead of
  resolving them. Use before trusting a doc/instruction file's claim about
  current architecture, ownership, or workflow, or when asked to find stale
  docs or outdated framing. Distinct from repo-orientation/domain-
  orientation (establish current facts; this audits whether framing teaches
  them correctly) and state-ownership-audit/lifecycle-audit (owns those
  facts, consumed here). Refuses to rewrite prose, delete history, rename
  identifiers, or resolve ambiguity.
---

# Stale Framing Audit

A repository accumulates statements that were true once, were planned but
never finished, described an earlier architecture, or remain technically
defensible while still teaching the wrong mental model. Most of these
sentences are not lies. "Work items are projected to the coordinator" can
be exactly true and still cause a reasonable reader to conclude the
coordinator owns work-item state, when it doesn't. An old subsystem kept
around for compatibility can be described with total accuracy while
carrying far more architectural weight in a reader's head than it actually
has anymore. The habit this skill exists to break is checking sentences for
truth one at a time and calling it done -- the dangerous case is rarely a
single false claim; it's a repository surface that, read the way it's
actually going to be read, hands the next agent an incorrect model of how
the system works, who owns what, or what's currently supported.

The question this skill asks is not "is this sentence true." It's: **what
would a reasonable, competent reader believe about the current system after
reading this surface, and does the current evidence support that belief?**
A surface can fail that question while every individual sentence in it
would survive a literal fact-check.

## What this is not

This is not a documentation-quality sweep, a staleness-equals-age heuristic,
or a mandate to flag every place code and prose disagree. Three traps sit
right next to this skill's actual job, and all three produce a worse
outcome than doing nothing:

- **Age is not staleness.** A five-year-old README section can be exactly
  current; a file touched yesterday can restate an old mental model with
  fresh timestamps. Recency is weak, non-decisive context, never a
  conclusion (see "Be cautious with recency" below).
- **History is not a defect.** A repository that keeps an old ADR, an
  archived spec, or a completed migration plan around is doing something
  healthy, not something wrong. The failure this skill looks for is
  history that isn't distinguishable from current guidance -- not history's
  mere presence.
- **Code is not automatically the correct model either.** When code and
  documentation disagree, the reflex is to trust the code because it's
  executable. That reflex answers a different question than the one this
  skill asks -- see "Framing vs. a code defect" below for why "the docs are
  stale" and "the code is the bug relative to what was actually intended"
  are both live possibilities, and why picking one requires more than
  "code is real, docs are not."

## How this composes with the rest of this skill family

This skill sits downstream of the fact-establishing skills and does not
duplicate their work:

- **`repo-orientation`** and **`domain-orientation`** establish what's
  currently true -- the engineering map, and what domain concepts actually
  mean. If either exists for this target, use its findings (especially
  where it already names a code-vs-docs disagreement) as evidence rather
  than re-deriving them. This skill's job starts one step past theirs: not
  "what's true" but "does a specific framing surface teach what's true."
- **`state-ownership-audit`** and **`lifecycle-audit`** own authority and
  transition facts in depth. When a framing claim is about who owns a piece
  of state or how an entity's lifecycle works, and either audit's output is
  available, reuse its conclusion as the evidence side of the comparison
  instead of re-deriving ownership or transition mechanics inline. Don't
  perform a shallow ownership or lifecycle analysis just to check one
  sentence -- name it as a gap in available evidence, or point at running
  that skill first, if the claim's evidence would require one.
- **`spec-pressure-test`** pressure-tests a not-yet-built spec's own
  internal wording for gaps and contradictions. This skill runs on framing
  about a system that (at least partly) already exists, and asks whether
  that framing matches current reality -- not whether a spec is internally
  decided. A pure forward-looking proposal with nothing implemented yet has
  nothing for this skill to check it against; that's `spec-pressure-test`'s
  territory.
- **`change-review`** judges whether a specific diff is ready to merge. This
  skill never renders a merge verdict and isn't scoped to one diff; it
  looks at whatever framing surfaces are in scope for the audit.
- **Documentation/comment cleanup** (rewriting or deleting prose) is a
  different, downstream action. This skill diagnoses; it does not edit
  documentation, however small the fix would look.

If a target's complexity means one of these produces the actual evidence a
finding needs -- an ownership question with no existing audit, a domain
term with unclear current meaning -- name that explicitly and either point
at running it first or treat the affected claim as unresolved, rather than
re-deriving a shallow version of that skill's work inline.

## Gather before judging anything

Don't reconstruct what a surface teaches from its title or its age. Read
the actual text, and gather the evidence to check it against:

- **The framing surfaces in scope** -- see "Which surfaces to prioritize"
  below for how to select and rank these before reading line by line.
- **Current, executable evidence**: what the code actually does, what's
  wired into entry points and reachable (reuse `repo-orientation`'s
  reachability discipline -- a directory that nothing imports is not
  "current" just because a doc describes it that way), schemas and
  constraints, test behavior, CLI output, configuration.
- **Existing fact-finding output** for this target -- `repo-orientation`,
  `domain-orientation`, `state-ownership-audit`, `lifecycle-audit` reports,
  if they exist. Reuse their conclusions; don't re-derive them.
- **Status and provenance markers on the framing surfaces themselves**:
  dates, version pointers ("as of vX"), explicit status lines ("Status:
  Superseded by ADR-9", "Deprecated", "Historical", "Proposed, not yet
  implemented"), archive/history directory placement, changelog entries,
  a doc's own stated scope ("this describes the target architecture we're
  migrating to").
- **Migration-in-progress evidence**: feature flags, dual-write code,
  rollout percentages, tracked TODOs pointing at an open ticket, a partial
  rollout still gated -- these mean two framings can legitimately coexist
  right now, not that one is simply wrong.
- **Version history available in the working tree, when it's useful** --
  when a claim's currency turns on *when* something changed (a rename, a
  removed component), and that's cheaply checkable (`git log`, `git blame`)
  it's legitimate context. Treat it as one input among several, never as
  the tiebreaker on its own (see "Be cautious with recency").

If something on this list doesn't exist or can't be found, that's a fact
for Unknowns, not a gap to fill with a plausible guess.

## Three tiers -- tag the evidence, not just the finding

Same discipline as the rest of this skill family, applied to the *current
evidence* side of a framing comparison (the finding's Characterization,
below, is a separate, six-way tag -- this is about how firmly you can
stand behind the counter-evidence itself):

- **Observed** -- a fact you can point to directly: an import statement
  that's actually there, a route actually registered, a test that
  actually asserts the behavior, a status line that actually reads
  "Superseded." "`worker.py` imports only `postgres_queue`" is observed.
- **Inferred** -- one short, defensible step from something observed:
  "no code path imports `redis_queue`, and it's not registered anywhere
  reachable, so it's dead" is inference. "This was probably migrated off
  Redis for cost reasons" with no migration note or ticket in evidence is
  not a short step from anything observed -- that's a story, not an
  inference.
- **Unresolved** -- the evidence doesn't settle it. Say so. A framing
  claim you can neither confirm nor refute from what's available is a
  legitimate, common finding component, not a gap to paper over with the
  weaker of two guesses.

When unsure which tier applies, use the weaker one -- exactly as elsewhere
in this family, an audit that under-claims costs a reader a few minutes of
double-checking, while one that over-claims can send them acting on a
"contradicted" verdict the evidence doesn't actually support.

## Which surfaces to prioritize

Do not turn this into "grep every comment and diff it against the code."
The goal is preventing incorrect reasoning, not maximizing stale-text
detection -- a stale sentence buried in a fixture nobody reads before
touching that code matters far less than one paragraph in a root
instruction file. Rank candidate surfaces by how much they actually shape
an agent's starting model before spending time on them:

- **Highest reach** -- root and scoped `AGENTS.md`/`CLAUDE.md` and similar
  agent-instruction files, the root `README`, root architecture/scope
  documents, setup/init instructions, whatever spec or design doc the
  repository currently treats as governing. A single misleading paragraph
  here can redirect an entire implementation before any code is touched.
- **Moderate reach** -- prominent module- or package-level documentation,
  examples meant to be copied, CLI `--help` output, naming at a major
  architectural seam (a top-level module, service, or package name that
  implies an ownership or role it no longer has), docstrings on widely
  imported or central symbols.
- **Lower reach** -- comments and docstrings on internals nobody starts
  from, isolated TODOs, deep test fixtures, one-off scripts. Content here
  only earns a finding when it's demonstrably the *only* documentation of
  something a reader would actually consult before acting -- not by
  default.

A finding's place in the report is driven by reach combined with how
consequential the wrong belief would be if acted on (see "Rank by
reasoning impact" below), not by how many stale sentences exist at that
reach tier. A single Tier-1 finding outweighs a dozen Tier-3 ones; don't
pad a report to look thorough.

## Be cautious with recency

A newer document is not automatically more authoritative than an older
one, and a recently modified file can restate old framing without changing
its substance -- a copyedit, a typo fix, or a reformatting pass touches the
timestamp without touching the claim. Never resolve a disagreement between
two framing surfaces, or between a surface and the code, by defaulting to
"whichever is dated later wins." Use dates as one input into the evidence
picture (a doc that predates a component's creation obviously can't be
describing it; a spec explicitly marked as revising an earlier one names
its own precedence), never as the tiebreaker itself.

## Framing vs. a code defect

When a framing surface and current behavior disagree, resist collapsing
straight to "the documentation is stale." That conclusion assumes the code
correctly represents what the system is *supposed* to do -- which is a
separate question from what the system *currently does*, and this skill is
about the first one, not automatically settled by the second.

Reusing the rest of this skill family's evidence discipline: code, tests,
and other executable artifacts are the right evidence for settling *what
currently happens* -- that discipline doesn't change here. What's different
is the next step. Before writing "the docs are stale, the code is right,"
check:

- **Does the diverging code path look intentional?** Is it wired into
  entry points and exercised by tests that assert the behavior the doc
  disputes, or does it look orphaned, unreachable, recently added, or
  untested -- in which case the code may be the outlier, not the doc.
- **Do other independent surfaces agree with the doc instead of the
  code?** Tests written against the documented behavior, a spec the code
  is supposed to satisfy, or a second, independently-written piece of code
  that assumes the documented behavior all corroborating the doc is
  evidence the code, not the framing, is what's wrong.
- **Does the diverging code carry its own signal that it's not settled
  intent** -- a TODO or comment acknowledging it skips a check, bypasses an
  invariant, or "needs review," with no other surface describing it as
  sanctioned? Code that flags its own gap is evidence *against* itself,
  not evidence the documented invariant has changed.

**Then resolve to exactly one of three outcomes -- don't stop at "I checked
some things" without landing on one:**

1. **The code looks intentional and corroborated** (wired in, tested,
   agreed with by other independent surfaces, no self-acknowledged gap):
   proceed with the ordinary framing characterization -- the surface is
   plausibly Contradicted or Superseded, per the checks above.
2. **The code looks like the likely defect** (orphaned, untested, recently
   added with no corroboration, or carrying its own comment admitting it
   isn't reviewed or doesn't yet meet the stated requirement): **do not**
   characterize the framing surface as Contradicted, Superseded, or any
   other stale-framing outcome. The framing is doing its job -- it states
   the intended/current model, and the divergence is a likely
   implementation defect, not a documentation problem. Report this
   explicitly: name why the code looks like the outlier (the specific
   evidence -- missing tests, no wiring, its own TODO), state plainly that
   the framing surface is not stale, and name the code-side gap as a
   correctness risk worth flagging to whoever owns that code -- but out of
   this skill's scope to characterize further or fix (a `change-review` or
   ordinary code-review matter, not a framing finding). This still belongs
   somewhere the reader will see it (e.g., under Unresolved questions or a
   one-line note in the Working summary), but never as a framing
   Characterization, and never phrased as "the docs are out of date."
3. **The checks above don't settle it either way**: say so plainly as a
   Conflicting/Ambiguous finding rather than picking the side that sounds
   more architecturally tidy.

Concluding "the documentation is stale" is itself a claim that needs the
same evidentiary bar as any other finding in this audit -- it is not the
default resolution for every code/doc disagreement, and a spec's own
invariant does not become false just because some code, however live,
currently violates it.

## Distinguish history from current framing

A repository legitimately keeps its own past around. Before flagging
anything in a surface that describes an earlier state, plan, or decision,
check whether the surface already marks itself as historical:

- An explicit status line (`Status: Superseded`, `Deprecated`, `Historical`,
  `Archived`), a completed-migration note, a changelog entry.
- Placement that itself signals history -- an `archive/`, `history/`, or
  `decisions/` directory of past ADRs, a doc a current index links under a
  clearly historical heading.
- Language that plainly frames it as explaining the past ("this describes
  how the system worked before the 2024 migration") rather than the
  present.

**Content that clears this bar is not a finding, regardless of how
outdated its content is.** A ten-year-old superseded ADR describing a
scrapped architecture is doing exactly its job. Do not recommend deleting,
rewriting, or "cleaning up" material that's correctly marked as history --
that recommendation is out of scope for this skill even when the material
looks obviously obsolete.

Two related situations *are* in scope, because they're framing failures,
not history's mere existence:

- **History masquerading as current** -- material that describes a past or
  abandoned state but carries no marker distinguishing it from current
  guidance, sitting somewhere a reader would reasonably consult for the
  present state (not filed under an obvious archive).
- **Current guidance failing to contextualize adjacent history** -- a
  current doc that doesn't acknowledge a nearby, clearly-relevant historical
  document exists, in a way that leaves a reader likely to stumble onto the
  historical one and mistake it for current. This is the omission form of
  the same failure -- see below -- not a demand that every document
  cross-reference its own history.

## Omission-based framing

Not all misleading framing is a written sentence. Before reporting an
omission, it must clear all three of these -- otherwise this collapses into
"no document explains everything," which is not a defect:

1. **The surface has a stated or clearly implied scope that should include
   the missing fact.** A README's "Architecture" section that names
   components A and B, when a newer C now owns state the section's own
   framing implies A or B still owns, is in scope. A README that never
   claims to be exhaustive, missing a peripheral detail nobody would expect
   it to cover, is not.
2. **The omission would cause a reader relying on that surface, for its own
   stated purpose, to form a materially wrong belief** -- not merely an
   incomplete one. "This doc could say more" is not a finding; "this doc's
   silence, read the way it's meant to be read, teaches an ownership model
   that's now wrong" is.
3. **There's a concrete, current fact to name that fills the gap** -- not a
   general call for more thoroughness.

## Characterize each finding

For every candidate that survives the reach filter and the checks above,
pick the single characterization the evidence actually supports -- these
are deliberately not mutually exhaustive boxes to force everything into;
use "Ambiguous" honestly when nothing sharper fits:

- **Contradicted** -- current evidence directly negates the statement as a
  description of the system now, independent of whether it was ever true.
- **Superseded, undated** -- the statement accurately described a real past
  state, decision, or architecture, the system has since changed, and
  nothing marks the passage of time (see "Distinguish history from current
  framing" -- if it's properly marked, it's not a finding at all).

  These two are the pair most likely to blur together, and they're allowed
  to: use Superseded only when you have *positive* evidence the statement
  was actually true at some past point (a changelog entry, a migration
  note, an earlier version of the same doc, a component's own history
  confirming it once worked the described way) -- not merely evidence it's
  false now. Absent that positive evidence, default to Contradicted; don't
  invent a past the target doesn't establish just to justify the softer-
  sounding label. When the evidence genuinely doesn't distinguish the two
  (false now, no signal either way about whether it was ever true), name
  both as defensible rather than forcing a choice the evidence doesn't
  support.
- **Aspirational presented as implemented** -- describes an intended or
  planned design as though it's already built, with nothing in the surface
  (or a surface a reasonable reader would also see) marking it as not yet
  real.
- **Misleading emphasis / missing qualifier** -- literally true, often
  narrowly true (a compatibility path, one scope, one mode), but the
  framing's prominence, ordering, or lack of a scope qualifier causes a
  broader inference than the words support. This is the "work items are
  projected to the coordinator" case, and the "true only for the
  compatibility path" case -- both are true statements doing more work in
  a reader's head than their literal content earns.
- **Omission** -- no false or incomplete statement; the surface's silence,
  within its own stated scope, induces the wrong model. See above.
- **Ambiguous / genuinely unresolved** -- the repository itself doesn't
  settle which framing is current (an active migration with no declared
  target date or canonical side, several spec generations with nothing
  naming which governs, a code/doc disagreement that "Framing vs. a code
  defect" above couldn't resolve). This is a legitimate, common, often
  correct output -- report it as unresolved and do not pick a side to make
  the finding feel more conclusive.

## Rank by reasoning impact

For every surviving finding, ask the question this skill actually exists to
answer: **what wrong assumption could the next competent agent reasonably
carry into its work because of this surface?** That's the ordering
principle, not sentence count or how obviously wrong something reads.

Weigh reach (see "Which surfaces to prioritize") together with
consequence -- would acting on the wrong belief mean writing to the wrong
store, treating a deprecated path as current and building on it, crediting
the wrong component with an authority it doesn't have, or misjudging
whether a workflow is still supported? A Tier-1 finding with real
consequence goes first; a Tier-3 finding, even a flagrant one, goes last or
is left out of the report entirely in favor of naming that lower-reach
material wasn't exhaustively swept.

Keep the report compact. The deliverable is a small number of consequential
findings, not a census of every stale sentence found.

## What this skill refuses to do

Even when a request bundles it in:

- Rewrite, edit, delete, or "clean up" any documentation, comment, or
  instruction file. Name the finding and the smallest corrective action; an
  actual edit is a separate, downstream action.
- Delete, archive, or recommend removing historical material -- properly
  marked history is never a defect (see "Distinguish history from current
  framing").
- Rename an identifier, module, service, or field, even when its name is
  demonstrably misleading -- especially when it's a public API or otherwise
  unsafe to change. Name the naming risk and recommend a clarifying note or
  qualifier instead, never the rename itself.
- Establish authority, ownership, domain meaning, or lifecycle facts from
  scratch when a deeper pass (`state-ownership-audit`, `domain-orientation`,
  `lifecycle-audit`) would be needed to ground a specific claim and hasn't
  been run. Name the gap and point at the deeper pass rather than
  re-deriving a shallow version of it inline.
- Redesign the architecture, propose a target model, or resolve a
  terminology or ownership drift this skill finds -- that's a human
  decision or a downstream skill's job, exactly per `domain-orientation`
  and `state-ownership-audit`'s own refusals.
- Resolve genuine, repository-acknowledged ambiguity (an active migration,
  several spec generations with no declared current one) by picking the
  side that sounds more coherent. Report it as unresolved.
- Treat every code/documentation disagreement as proof the documentation
  is stale. See "Framing vs. a code defect." In particular: characterize a
  spec or doc's stated invariant as Contradicted or out of date because an
  untested, unwired, or self-acknowledged-as-unreviewed code path
  currently violates it -- that pattern is evidence the code is the likely
  defect, not that the invariant changed, and the framing surface gets no
  stale-framing finding at all in that case.
- Treat a document's age, or a file's recent modification time, as
  decisive evidence of its correctness or staleness on its own.
- Produce a census of every stale sentence in the repository. The output
  is a compact, reasoning-impact-ranked set of findings, not a
  completeness sweep.
- Judge implementation correctness, review a diff, or render a merge
  verdict -- that's `change-review`.

If a request bundles a legitimate framing audit with one of these --
"find the stale docs and fix them," "audit this and rename what's
misleading" -- say plainly that the second part is out of scope for this
skill, then deliver the audit itself.

## Report

Use this exact structure. Omit no heading; use "None identified." rather
than dropping a section that came up empty -- an absent section reads as
"not considered."

```
# Stale Framing Audit: <target>

## Scope and evidence inspected
<Framing surfaces read, at which reach tier; current-evidence sources
consulted (code, tests, schema, CLI, config); existing repo-orientation /
domain-orientation / state-ownership-audit / lifecycle-audit output reused.
Name anything relevant that couldn't be inspected.>

## Findings
### <finding, most consequential first>
- Surface & location: <file/section/paragraph, and its reach tier>
- Statement or omission: <quote, or precise description of what's missing
  and the surface's scope that makes the omission material>
- Induced mental model: <what a reasonable reader would conclude>
- Current evidence: <what challenges that model -- tagged observed /
  inferred / unresolved, naming any reused audit output>
- Characterization: <Contradicted / Superseded, undated / Aspirational
  presented as implemented / Misleading emphasis or missing qualifier /
  Omission / Ambiguous>
- Why it matters: <the reach + consequence combination that earned this
  its rank -- not just "this is incorrect">
- Smallest corrective action: <e.g., a status marker, a scope qualifier, a
  pointer to the current authoritative surface, a one-line contextualizing
  note -- never a rewrite, a deletion, or a rename>
(repeat)
"None identified." if none.

## Historical material reviewed and not flagged
<What was checked and correctly left alone because it's properly marked or
placed as historical -- demonstrates the sweep, not just its absence of
complaints. "Not applicable -- no historical material in scope." if none.>

## Preserved ambiguity
<Findings characterized as Ambiguous: what's unresolved, why the evidence
doesn't settle it, and what would settle it if it existed. "None
identified." if none.>

## Unresolved questions
<Open questions the evidence doesn't settle that aren't tied to one
specific finding.>

## Working summary
<A few sentences: the mental model a reader currently forms from these
surfaces, where that model is wrong or unsupported, and what a future
agent should actually believe instead before acting on this material.>
```

A target whose in-scope framing surfaces hold up under this audit is fully
and honestly served by a short report that says so and stops -- padding it
with low-reach findings or manufactured ambiguity is a worse outcome than
an honest "nothing consequential found here."
