---
name: implementation-orientation
description: >-
  Before coding a concrete task in an unfamiliar-ish repository, runs a
  light, task-anchored pass for what could materially change the
  implementation: an existing mechanism to reuse instead of a new generic
  abstraction, a hidden correctness/security/identity/lifecycle constraint
  ordinary code could miss, or real ambiguity between two competing
  mechanisms -- never an architecture review or repo tour. EXPERIMENTAL,
  field-trial-only skill, strongly biased toward silence: "no material
  guidance beyond the task" is the normal, successful outcome. Use right
  before writing code for a task in a subsystem you don't fully own -- e.g.
  an FDE making customer-facing changes under time pressure -- or before
  delegating implementation to a coding agent. Not for open-ended repo
  exploration, picking what to build next, planning an already-chosen
  slice, or architecture review -- see repo-orientation, next-best-slice,
  slice-plan, and slice-review for those.
---

# Implementation Orientation

**Status: experimental, field-trial draft.** This skill exists to gather
prospective evidence, not to serve as a settled capability. It has not been
promoted, is not linked from other skills as a required step, and its
calibration is still being tested against real use. Treat "no findings" as
a completely normal result — the whole design premise is that most tasks
don't need this.

## The problem this targets

An engineer or coding agent picks up a concrete task in a codebase they
don't fully own. The task is well-specified enough to start coding, and the
obvious implementation is generically reasonable — it would work in most
codebases shaped roughly like this one. But *this* codebase already solved
part of this problem, has a boundary the task description doesn't mention,
or has two things that look interchangeable but aren't. The result: code
that passes review-by-skim, compiles, maybe even passes tests, and is
locally wrong — it reintroduces a security hole a shared helper already
closes, collides two things a discriminator was quietly keeping apart, or
stands up a second mechanism next to one that already owns the same
responsibility.

This is the FDE situation in particular: real implementation work, in a
codebase you don't deeply own, under time pressure, leaning on a coding
agent that has no way to know what it hasn't seen. This skill's job is a
short, cheap look before that code gets written — not a review after.

## Why the bias toward silence is the central design constraint

A controlled historical run of this idea across five codebases (one
internal, four public: FastAPI, Ruff, Immich, Home Assistant Core) found
real signal — a blind pass genuinely surfaced task-invisible constraints
that were later validated by the actual contributor's review cycle or by a
follow-up bug: a security/trust boundary a contributor initially missed and
had to rewrite in review; an identity/collision risk that the real
implementation had to add a discriminator to avoid; a two-parser semantic
divergence (fail-open vs. fail-closed) that a later bug traced back to;
a bootstrap invariant that had to reach code at creation time rather than
be patched on after.

The same run also over-produced findings. *Every* historical case came back
medium-or-higher signal, including cases that were, on inspection, ordinary
framework extension — adding a rule through a linter's normal registration
machinery, adding a platform integration through its normal scaffolding,
threading one new parameter through an already-conventional path. A tool
that always has something to say is not calibrated; it's a horoscope. If
this skill reports something on every invocation, it has already failed,
regardless of how correct any individual finding is.

So: silence is not the failure mode to avoid. Manufacturing a finding to
justify having been invoked is.

## When this runs

Given a concrete implementation task and a repository (or subsystem) to
implement it in. Most useful when:

- the repository or subsystem is unfamiliar or only partially familiar to
  whoever's about to implement,
- the change touches identity, migration, authorization, security/trust
  boundaries, concurrency, persisted state, or lifecycle behavior,
- the change extends an existing mechanism that has more than one plausible
  shape (a registry, a plugin system, a provider/handler pattern),
- multiple existing implementations of "roughly this" already exist in the
  repo and it's not obvious which one the new work should follow,
- an agent is about to be handed the task to implement unsupervised.

Least useful — expect and accept a fast "nothing here" — when:

- the change is copy/presentation-only,
- there's exactly one obvious sibling implementation and the task is
  straightforwardly additive,
- the task's own specification already names the binding mechanism to use,
- the change is mechanical (a generated-file update, a routine refactor
  with no behavioral seam).

Don't force it either direction from this list — treat it as a prior, not a
gate. A "least useful" shape can still turn up something real; a "most
useful" shape can still come back empty. The materiality test below is
what actually decides the output, every time.

## Investigate — scoped by the task, not the repo

The point is not to build a repository map (that's `repo-orientation`'s
job, and a much bigger one). Read only enough to answer these, starting
from the task and working outward through what it actually touches:

1. **Where does this responsibility live?** Find the module, class, or
   subsystem that already owns the thing the task is asking to add to or
   extend. If nothing owns it yet, that's itself worth noting.
2. **How does this subsystem already solve this class of problem?**
   Read the actual code for the nearest existing analog — not a summary of
   it, not what a README claims about it.
3. **Is there a real extension mechanism, or competing precedent?** A
   registry, a plugin base class, a provider pattern, or more than one
   existing implementation that isn't obviously "the" one to follow.
4. **Are there hidden correctness/security/state/lifecycle/identity
   constraints?** Something the task description doesn't mention that a
   naive implementation would violate — a trust boundary, a uniqueness
   invariant, a concurrency guard, a bootstrap ordering requirement.
5. **Are there non-obvious touchpoints an implementer could plausibly
   miss?** Not every adjacent file — specifically the ones a first read of
   the task wouldn't surface, that a working implementation genuinely needs.
6. **Given 1–5, is there actually anything worth reporting beyond ordinary
   implementation work?** This question is not rhetorical — answer it
   honestly, after doing 1–5, not before.

Stop investigating once these are answered. A task-anchored pass that
balloons into reading half the repository has stopped being this skill and
started being `repo-orientation`.

## The materiality test

A finding earns a place in the report only if knowing it *before*
implementation could plausibly:

- change the implementation approach,
- avoid a correctness, security, or data-integrity mistake,
- preserve an invariant that matters,
- resolve a genuinely non-obvious design choice,
- prevent standing up a second mechanism for a responsibility something
  else already owns,
- or name a non-obvious implementation boundary ordinary first-pass coding
  could miss.

If a candidate finding doesn't clear one of these, it doesn't go in the
report — not even as a footnote, not even because it was interesting to
discover, not even because inspection effort was already spent finding it.

### Never let these count as material on their own

None of the following is, by itself, evidence that something belongs in
the report:

- It appears repeatedly in the codebase.
- It's framework or platform boilerplate.
- It's generated code, or a generated-client/snapshot update.
- It belongs to a registration list, a plugin manifest, or similar
  scaffolding.
- Normal tests or CI would mechanically catch it if done wrong.
- It's an "obvious adjacent file" — the kind any competent implementer
  would touch without being told.
- It's standard fixture or test placement.
- It helps locate code but doesn't change what gets built.

**Repetition is not policy.** Seeing the same shape five times does not
make it a convention worth reporting — it might just be five instances of
generated code, mechanically mirrored plugin registration, or templated
adapters that carry no decision. Only repeated code that performs the *same
relevant responsibility* and would *materially inform this task's
implementation choice* counts — and even then, report the responsibility
and mechanism, not "this pattern appears N times" as though frequency were
the argument.

**Don't reason from pattern names.** Calling something "a Factory" or "this
should be a Strategy" is not analysis — it's a label standing in for
analysis that didn't happen. Factory and Strategy can legitimately coexist;
a registry can select strategies while a factory constructs them; a service
layer can be right in one subsystem and redundant in another. Reason about
*responsibilities* instead — construction, selection, behavioral
substitution, state ownership, dispatch, persistence, authorization,
lifecycle, identity, validation — and ask which existing thing in this
repo already owns the relevant one. The failure this skill exists to catch
is an agent reaching for a reasonable-sounding generic abstraction when the
subsystem already has a different, working mechanism that owns the same
responsibility — not "the code doesn't match a pattern-book diagram."

## Output

Keep it compact — this is an orientation pass, not a report on everything
that was read. Use this structure:

```
# Implementation Orientation: <task, one line>

## Material guidance
<1-3 findings maximum by default. For each:
  - the finding, stated as guidance for the implementer
  - concrete repository evidence (file/function, not a paraphrase)
  - why it matters to this implementation
  - confidence (high / medium / low)>

## Likely scope
<Only touchpoints that are non-obvious or decision-relevant — not a file
list. Omit this section entirely if everything worth touching is already
obvious from the task.>

## Open decisions
<Only genuine ambiguity the repository evidence does not resolve — two or
more real mechanisms with no clear answer between them. Omit if none.>
```

When investigation turns up nothing that clears the materiality test, don't
force these sections to have content. Use exactly this instead:

```
# Implementation Orientation: <task, one line>

No material implementation-specific guidance found beyond the task and the
established local implementation path.
```

That is a complete, successful report. Do not pad it with a summary of
what was inspected, a list of files read, or reassurance that the search
was thorough — showing work is not the job here.

Never produce a long architecture essay, dump every file inspected, or
surface low-value orientation just to demonstrate effort. If it doesn't
clear the materiality test, it stays out — including from an internal
"routine orientation" bucket you noticed along the way. Noticing something
during investigation is not the same as it belonging in the report.

## Finding categories (internal — not report headings)

Useful for judging your own draft before writing the report:

- **Material constraint** — a correctness/security/state/identity/
  lifecycle/external-contract/project-policy boundary. Goes in Material
  guidance.
- **Meaningful precedent** — an existing extension mechanism or analogous
  implementation that would materially change how this task should fit.
  Goes in Material guidance.
- **Genuine ambiguity** — two or more plausible approaches where the
  repository doesn't establish a clear answer. Goes in Open decisions.
- **Routine orientation** — useful while investigating, doesn't clear the
  materiality test. Stays out of the report entirely, even briefly.

## What this skill refuses to do

- Manufacture a finding because it was invoked. "Nothing material" is a
  correct, complete answer, not an excuse to keep looking until something
  turns up.
- Report something solely because it's repeated, generated, framework
  boilerplate, part of a registration list, mechanically CI-catchable, an
  obvious adjacent file, standard fixture placement, or a routine
  generated-client/snapshot update.
- Call something a project convention or invariant merely because several
  examples exist, without checking they share the *relevant responsibility*
  and would actually change this implementation.
- Reason from a pattern name (Factory, Strategy, Repository, …) as a
  substitute for reasoning about responsibilities.
- Produce a general architecture review, a code-quality audit, or a
  repo-wide tour — see `repo-orientation` for whole-repository mapping.
- Choose or justify what to build next — see `next-best-slice` /
  `next-best-product-slice`.
- Turn one already-accepted slice into an implementation plan — see
  `slice-plan`. This skill runs earlier and narrower: it looks for
  repository-specific traps before planning starts, it does not produce the
  plan itself.
- Review a diff or claim work is done — see `slice-review`.
- Write the implementation.

If a request bundles this in with one of those ("orient me and then plan
it," "check for gotchas and just build it") — run the orientation pass
first, exactly as scoped here, then carry any material findings forward
into the requested downstream work rather than stopping and handing the
user back to another skill themselves. A no-material-guidance result is
not a reason to interrupt the downstream work either — it just means the
downstream work proceeds with nothing extra to account for. The point of
staying narrowly scoped is that the orientation pass itself must not turn
into the plan or the implementation, not that the user has to manually
re-invoke something else once it's done. The intended flow is task →
orientation preflight → the requested planning/implementation, carrying
findings forward — not task → orientation → stop.

## Field-trial logging

This skill is being field-tested, not benchmarked in the usual sense.
`evals/implementation-orientation/FIELD-LOG.md` tracks real (non-eval)
invocations, but filling it in is not part of running this skill — it's
maintained retrospectively by whoever is operating the field trial,
outside the invocation itself. This skill does not write to it, and
running the skill has no side effects on the repo.
