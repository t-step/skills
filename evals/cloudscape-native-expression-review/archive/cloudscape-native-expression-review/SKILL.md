---
name: cloudscape-native-expression-review
description: >-
  Reviews a bounded frontend surface (a page or small composed set of
  components) for material opportunities to express its user task more
  natively using Cloudscape's documented component vocabulary and
  established patterns, judged against authoritative Cloudscape guidance
  retrieved for this task, never memory or a component's mere existence.
  Combines component selection ("right component for this job?") and
  pattern composition ("does this match an established Cloudscape pattern
  for this task?") as one operation. Produces a small set of material,
  evidence-backed findings with an applicability argument and a
  preserved-task/boundary check. Use when asked whether a frontend "does
  Cloudscape natively," to review whether the right Cloudscape concepts
  were chosen for a page, or before recommending a component/pattern
  change. Does not audit already-chosen mechanics for correct
  implementation; no general UX or product-redesign review — see "Scope
  boundary."
---

# Cloudscape Native-Expression Review

Primary question: **given the user task this bounded surface expresses,
does it use Cloudscape's component vocabulary and established patterns the
way a Cloudscape-fluent implementer would naturally express that same
task?** Not "is this implemented correctly" (implementation correctness is
a distinct, lower-level concern — a surface can be mechanically flawless
and still contain a strong native-expression opportunity, or vice versa:
mechanically imperfect but already the right concept). Not "is this
generally good UX." Specifically: were the right Cloudscape concepts
chosen and composed for this task.

This skill deliberately owns both component selection and pattern
composition as one operation, not two. Many real opportunities are only
visible from the pattern level down (a local component choice only reads
as wrong once you see the surrounding composition) or only cohere as one
recommendation that happens to touch both a component and the pattern it
sits inside. Splitting them here would force artificial, premature
boundaries this skill's own evaluation exists to test — see
`evals/cloudscape-native-expression-review/RESULTS.md` for whether that
combination held up or should be split later.

## Scope boundary

**In scope** — a finding belongs here only if it is about which Cloudscape
concept was chosen and how it's composed, not how it's implemented:

- a bespoke, hand-rolled UI concept where Cloudscape ships a more
  semantically appropriate component for the same job
- a mechanically valid Cloudscape component used for a job a different,
  specific, documented Cloudscape component fits better
- several individually valid components composed in a way that materially
  diverges from an established Cloudscape pattern for the same user task
- a custom interaction structure (filtering, detail inspection, resource
  management, creation, editing, selection, navigation) where Cloudscape
  documents a materially more native composition for that same task
- a local component-selection problem that only becomes visible from the
  surrounding pattern
- a pattern-level mismatch that implies one or more component
  substitutions
- a case where the current implementation is mechanically valid but
  non-native enough that an experienced Cloudscape practitioner would
  likely restructure it

A finding may be component-level, pattern-level, or both at once — see
"Finding contract." Don't force a finding into an artificial single-level
taxonomy when the underlying recommendation genuinely spans both.

**Out of scope** — name these only in passing if at all, never as a
finding, unless directly necessary to establish the native-expression
judgment itself:

- **Implementation correctness.** Deprecated props, incorrect API usage,
  raw HTML standing in for a Cloudscape primitive, hard-coded style/token
  values, unsupported component composition mechanics, app-owned
  accessibility implementation defects on an already-correctly-chosen
  component. These are out of scope for this skill regardless of whether a
  separate implementation-level review exists. If an implementation detail
  is necessary evidence for a component/pattern judgment (e.g., a prop that
  only exists on the component you're recommending against), cite it
  minimally as supporting evidence, not as its own finding.
- **General UX critique.** "Too many actions," "poor hierarchy,"
  "confusing workflow," "needs progressive disclosure," "too dense,"
  "navigation feels awkward" — silence, unless a specific Cloudscape
  component or pattern page provides concrete, citable evidence for a more
  native expression of the *same* task. This skill is not a general UX
  reviewer; a generic usability observation wearing a Cloudscape citation
  is still a generic usability observation.
- **Product redesign.** Never invent a different user goal than the one
  the surface is already serving. A recommendation must preserve the
  apparent task being performed — restructuring a page to serve a
  *different* purpose than it currently serves is not a finding, it's a
  different product. If the intended task can't be established with
  enough confidence to choose between two native expressions, classify the
  candidate as `intent-dependent` (see "Finding contract") or don't report
  it.

Every finding must pass a boundary check before it's reported (see
"Finding contract"): state in one sentence why this is component/pattern
alignment rather than implementation correctness or general UX. If you
can't, cut the finding.

**How this composes.** Implementation correctness (API usage, props,
tokens, app-owned accessibility mechanics) is a distinct, lower-level
concern this skill does not own, whether or not a separate review of that
layer exists. Nor does this skill own whether the overall multi-surface
experience hangs together (a future, not-yet-built alignment/synthesis
layer). Don't informally perform either job here because it would be
useful; a review that also freelances implementation mechanics or
cross-page experience advice is harder to trust on the thing it actually
owns.

An earlier experimental skill, `cloudscape-implementation-audit`, explored
the implementation-correctness layer directly and is preserved as
historical evidence at `evals/cloudscape-implementation-audit/` — its
findings on evidence discipline, version-resolution mechanics, and a
concrete, adversarially-confirmed overreach on a pattern-level question
directly informed this skill's scope boundary and its "Anti-fundamentalism
rule." It is intentionally not an active skill; this skill does not depend
on it and does not hand off to it.

## Core reasoning procedure

For the bounded surface:

### 1. Establish the user task

Infer conservatively from the route/page purpose, labels and copy,
actions present, the data being displayed or edited, surrounding source,
and nearby type/API names. State the inferred task in one or two
sentences before doing anything else. Do not fabricate deeper product
intent than the evidence supports — see "Missing intent," below.

### 2. Characterize the current expression

Identify the major Cloudscape components in play, any custom UI
abstractions, the important interaction structure, and what conceptual
job each major element appears to perform. Don't judge yet — this step is
inventory, not evaluation.

Run `scripts/inspect_surface.py` over the surface and its directly
composed files first:

```
uv run scripts/inspect_surface.py --package-prefix '@cloudscape-design/' FILE [FILE ...]
```

This gives a factual JSX/import inventory (which Cloudscape components are
used, how many times, alongside which native elements) to reason from,
rather than reconstructing that inventory by eye. It reports facts only —
it has no opinion about whether a component choice is native or not; that
judgment is entirely this skill's own.

Where the fixture's installed Cloudscape version is knowable, resolve it
with `scripts/resolve_versions.py` the same way:

```
uv run scripts/resolve_versions.py --root FRONTEND_ROOT --package NAME [--package NAME ...]
```

Component and pattern *concepts* rarely change across minor versions the
way implementation mechanics (API shape, props, deprecations) do, so
version resolution matters less here than it would for an
implementation-level review — but an unresolved semver range still means
"current docs may not fully apply" is worth naming if a finding's
applicability plausibly depends on it.

### 3. Retrieve relevant Cloudscape guidance

Use the supplied `llms.txt`-shaped discovery index (or equivalent
authoritative snapshot) purely as a table of contents for selective
retrieval — never cite its one-line description as if it were the
guidance itself. Fetch the actual linked pages.

Retrieval priority, stopping as soon as a level settles the question:

1. **Official component guidance** — the specific component's own docs
   page and dev guide, for both the component currently used and any
   candidate alternative.
2. **Official pattern guidance** — the pattern page whose problem
   statement most closely matches the observed user task.
3. **Official foundation guidance**, only when needed to interpret
   component/pattern applicability (rare for this skill — foundations
   mostly govern visual/token mechanics, an implementation-level concern
   outside this skill's scope).
4. **Agent inference** — reasoned judgment with no direct documentation
   citation. Always the last resort, always labeled `INFERRED`, and an
   `INFERRED` finding is never reported as a `violation`-strength claim
   (this skill uses its own Type/Materiality/Confidence vocabulary rather
   than a violation/alignment scale — see "Finding contract" — but the
   same discipline applies: don't claim more certainty than the citation
   supports).

Do not ingest Cloudscape wholesale. Retrieve the minimum relevant material
for the candidate finding in front of you, not a survey of the whole
component or pattern library.

Two hard rules:

- **Examples and demos are not authority.** A demo showing a component or
  pattern used a certain way does not establish that way as required, or
  even recommended — demos illustrate, they don't mandate.
- **Existence does not imply a rule.** That Cloudscape ships a
  purpose-built component or documents a named pattern for something
  adjacent to what the surface does is never, by itself, evidence the
  surface should adopt it. See "Anti-fundamentalism rule."

### 4. Compare intent to native vocabulary and patterns

Ask, in order, and stop as soon as the answer is no:

- Does Cloudscape provide a component intended for this exact UI concept?
- Does the existing component serve the documented semantic purpose it's
  being used for?
- Does Cloudscape document a recurring pattern matching this user task?
- Does the current composition materially differ from that pattern?
- Is the documented pattern *actually applicable* to this task, or merely
  superficially similar (same shape, different problem)?
- Would the proposed alternative preserve the same product semantics —
  the same user task, not a different one?
- Is this a meaningful alignment improvement, or just another valid
  implementation of the same task?

### 5. Apply a high materiality bar

Do not report: aesthetic preference, an equally valid alternative, a minor
deviation, "Cloudscape has a component for this" with no applicability
evidence, or "the docs show it this way" with no normative or semantic
support behind the citation. Prefer one to three strong findings over
exhaustive commentary. A clean result — no material findings — is valid
and expected on many surfaces; don't manufacture one to avoid reporting a
clean review.

## Anti-fundamentalism rule

**The existence of a Cloudscape component or pattern is never, by itself,
sufficient evidence that the frontend should use it.** Every
recommendation must establish applicability, not just availability. This
is the rule this skill's own evaluation exists to pressure-test most
directly — see the equally-valid and wrong-intent pressure cases in
`evals/cloudscape-native-expression-review/`.

For pattern-level findings specifically, require evidence that:

1. the observed user task materially matches the documented pattern's
   stated problem — not just a superficial shape match (same layout,
   different problem);
2. the current implementation solves substantially the same problem the
   pattern addresses;
3. the proposed Cloudscape-native expression preserves that same task;
4. the difference between current and proposed is material enough that an
   experienced Cloudscape practitioner would plausibly restructure the
   code because of it, not just note it as an alternative.

If any of these four is weak, downgrade the finding's confidence or
suppress it entirely. A pattern page's mere existence, or a component
page's mere description of what the component "is for," is retrieval-step
evidence, not applicability-step evidence — closing that gap is the part
of the job that can't be automated.

## Finding contract

Every reported candidate finding carries all of these fields. If any
field can't be filled honestly, keep investigating or drop the candidate.

- **Finding** — concise description of the native-expression opportunity.
- **Type** — exactly one: `component selection`, `pattern composition`,
  `combined component + pattern`, or `intent-dependent`. Use `combined`
  when the component-level and pattern-level observations are genuinely
  one underlying recommendation — don't split a single issue into two
  findings at two abstraction levels to make the report look more
  thorough.
- **Materiality** — `high` / `medium` / `low`. Suppress `low` from the
  final report by default (see "Apply a high materiality bar"); name what
  was suppressed and why, so a reader can tell "checked and cleared" apart
  from "never considered."
- **Confidence** — `high` / `medium` / `low`, about whether the finding is
  factually and semantically correct given the evidence gathered —
  independent of materiality.
- **User task** — the task this skill believes the surface supports, in
  one or two sentences, stated plainly enough that a reader can judge for
  themselves whether the rest of the finding actually preserves it.
- **Repository evidence** — exact file/location and enough observed
  interaction/component structure that a reader can verify the claim
  without re-deriving it.
- **Cloudscape evidence** — the exact authoritative source (component
  page, pattern page, dev guide — never the discovery index's one-line
  description) and the specific guidance it establishes: component
  semantics, pattern applicability, or a relevant constraint.
- **Applicability argument** — why the cited Cloudscape guidance actually
  applies to *this* task, addressing the four-point test in
  "Anti-fundamentalism rule" directly, not just restating the citation.
- **Current expression** — how the surface presently represents the
  concept or task.
- **Native expression** — how a Cloudscape-fluent implementation would
  likely express the same task instead, stated only when sufficiently
  supported by the cited evidence; if the supported alternative is
  uncertain, say so rather than inventing a confident replacement.
- **Why it matters** — the concrete, design-system-specific consequence
  (a documented constraint the current composition collides with, a
  materially worse fit for the stated task, a maintenance/consistency cost
  against the rest of a Cloudscape app) — not a generic "this would be
  nicer."
- **Boundary check** — one sentence stating why this is component/pattern
  alignment and not implementation correctness, general UX, or unrelated
  frontend advice.

**Authority strength.** Label every finding's cited evidence with exactly
one of `REQUIRED` (the cited material states this as an explicit
constraint — a documented "Don't... Instead" pairing, an explicit
prohibition), `RECOMMENDED` (stated as preferred practice, not absolute),
`OPTIONAL` (documented as one supported alternative among others, no
stated preference), or `INFERRED` (no direct citation settles it — this is
reasoned judgment, and it must never be reported with `REQUIRED` or
`RECOMMENDED` phrasing). A pattern page's own explicit "Don't do X,
instead do Y" is `REQUIRED` evidence for the specific rule it states, not
license to treat everything else about that pattern as mandatory — see
"Anti-fundamentalism rule."

**A native-expression finding does not need to be a violation.** Many
useful findings are honestly: *the current implementation is valid
Cloudscape usage, but Cloudscape's own guidance strongly favors a
different native expression for this specific task.* Label that
distinction honestly in "Why it matters" rather than inflating a
`RECOMMENDED`-strength preference into `REQUIRED`-strength language.

## Missing intent

If the user task can't be established with enough confidence from the
route, copy, actions, and surrounding code to choose between two
plausible, differently-native expressions, that is not a coin flip to
resolve by guessing which is "more Cloudscape-native" in the abstract.
Report the candidate as `Type: intent-dependent` — name both plausible
readings, name what evidence would resolve it (e.g., "whether this record
is meant to be individually revisited/addressable, or is a transient
by-product of another flow"), and do not pick one. Suppressing the
candidate entirely is also correct when even naming it wouldn't be useful.
Guessing and reporting a confident recommendation anyway is the specific
failure mode this category exists to prevent.

## Report

```
# Cloudscape Native-Expression Review: <surface name>

**Inferred user task:** <one to two sentences, from step 1>

**Cloudscape packages / versions:** <resolved or "range only, unresolved: ...">

## Findings
<For each surviving (non-suppressed) finding, all fields from "Finding
contract," in materiality order (high first). "None." if none survive
suppression — a clean result is valid.>

## Suppressed (low materiality or weak applicability)
<One line each: what and why suppressed. "None." if none.>

## Orientation notes
<Component/pattern candidates checked and confirmed as already-native,
correct usage — the affirmative "I looked and it's fine" record.
"None noted." if none.>

## What was not evaluated
<Implementation correctness (API usage, props, tokens, a11y mechanics) and
general UX/product judgment, named briefly so their absence doesn't read
as "checked and fine.">
```
