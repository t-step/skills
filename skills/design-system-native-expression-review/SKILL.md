---
name: design-system-native-expression-review
description: >-
  Reviews a bounded frontend surface for material opportunities to
  express its user task more natively using a specific design system's
  own documented component vocabulary and compositions, judged against
  authoritative guidance retrieved for this task and this design system,
  never memory or a component's mere existence. Combines component
  selection and documented composition as one operation, discovering
  which authority categories this design system's own docs actually
  expose rather than assuming a fixed hierarchy. Findings carry an
  explicit evidence mode (verbatim/paraphrase/synthesis/inferred). Works
  with any design system (Cloudscape, Material UI, etc.) given that
  system's documentation. Use when asked whether a frontend "does
  <design system> natively," to review whether the right design-system
  concepts were chosen for a page, or before recommending a component/
  composition change. Does not audit implementation correctness; no
  general UX or product-redesign review — see "Scope boundary."
---

# Design-System Native-Expression Review

Primary question: **given the user task this bounded surface expresses,
does it use the selected design system's documented vocabulary and
compositions in the way a design-system-fluent implementer would
naturally express that same task?** Not "is this implemented correctly"
(implementation correctness is a distinct, lower-level concern — a
surface can be mechanically flawless and still contain a strong
native-expression opportunity, or vice versa: mechanically imperfect but
already the right concept). Not "is this generally good UX."
Specifically: were the right concepts, from *this* design system's own
documented vocabulary, chosen and composed for this task.

This skill deliberately owns both component selection and documented
composition as one operation, not two. Many real opportunities are only
visible from the composition level down (a local component choice only
reads as wrong once you see the surrounding composition) or only cohere
as one recommendation that happens to touch both a component and the
composition it sits inside. Splitting them here would force artificial,
premature boundaries.

## Lineage

This skill generalizes an earlier, Cloudscape-only skill (preserved at
`evals/cloudscape-native-expression-review/`) to work with any design
system's own documentation, given that system's authoritative source.
Two design decisions exist specifically because of what that
generalization exposed: authority-category discovery is corpus-adaptive
rather than assuming a fixed hierarchy (see step 3, below), and the
Finding contract carries an explicit evidence-mode label (see "Finding
contract") to make citation fabrication auditable rather than assumed
absent. Full evaluation history — the Cloudscape-only baseline, the MUI
generalization round, the morph regression, the post-fix refinement, and
the equivalence-isolation round that retired an early, compromised
suppression instrument in favor of the E1/N1/N2 fixtures — lives in
`evals/design-system-native-expression-review/README.md` and its
`RESULTS*.md` files. Read those before assuming a specific finding shape
is validated or still open; don't infer eval status from this file.

## Scope boundary

**In scope** — a finding belongs here only if it is about which
design-system concept was chosen and how it's composed, not how it's
implemented:

- a bespoke, hand-rolled UI concept where the design system ships a more
  semantically appropriate component for the same job
- a mechanically valid component used for a job a different, specific,
  documented component fits better
- several individually valid components composed in a way that
  materially diverges from a composition this design system's own
  documentation establishes for the same user task
- a custom interaction structure (filtering, detail inspection, resource
  management, creation, editing, selection, navigation) where this
  design system documents a materially more native composition for that
  same task
- a local component-selection problem that only becomes visible from the
  surrounding composition
- a composition-level mismatch that implies one or more component
  substitutions
- a case where the current implementation is mechanically valid but
  non-native enough that an experienced practitioner of this design
  system would likely restructure it

A finding may be component-level, composition-level, or both at once —
see "Finding contract." Don't force a finding into an artificial
single-level taxonomy when the underlying recommendation genuinely spans
both.

**Out of scope** — name these only in passing if at all, never as a
finding, unless directly necessary to establish the native-expression
judgment itself:

- **Implementation correctness.** Deprecated props, incorrect API usage,
  raw HTML standing in for a design-system primitive, hard-coded
  style/token values, unsupported component composition mechanics,
  app-owned accessibility implementation defects on an already-correctly-
  chosen component. These are out of scope for this skill regardless of
  whether a separate implementation-level review exists. If an
  implementation detail is necessary evidence for a component/
  composition judgment (e.g., a prop that only exists on the component
  you're recommending against), cite it minimally as supporting evidence,
  not as its own finding.
- **General UX critique.** "Too many actions," "poor hierarchy,"
  "confusing workflow," "needs progressive disclosure," "too dense,"
  "navigation feels awkward" — silence, unless a specific documented
  component or composition provides concrete, citable evidence for a more
  native expression of the *same* task. This skill is not a general UX
  reviewer; a generic usability observation wearing a design-system
  citation is still a generic usability observation.
- **Product redesign.** Never invent a different user goal than the one
  the surface is already serving. A recommendation must preserve the
  apparent task being performed — restructuring a page to serve a
  *different* purpose than it currently serves is not a finding, it's a
  different product. If the intended task can't be established with
  enough confidence to choose between two native expressions, classify
  the candidate as `intent-dependent` (see "Finding contract") or don't
  report it.
- **Cross-surface synthesis and implementation mechanics generally.**
  Whether the overall multi-surface experience hangs together is a
  separate, not-yet-built alignment layer this skill doesn't own, and
  implementation mechanics (API usage, props, tokens, app-owned
  accessibility mechanics) are a distinct, lower-level concern, whether
  or not a separate review of either layer exists. Don't informally
  perform either job here because it would be useful — a review that
  freelances outside what it actually owns is harder to trust on the
  thing it does own.

Every finding must pass a boundary check before it's reported: state in
one sentence why this is component/composition alignment rather than
implementation correctness or general UX (this is the Finding contract's
"Boundary check" field). If you can't, cut the finding.

## Core reasoning procedure

For the bounded surface:

### 1. Establish the user task

Infer conservatively from the route/page purpose, labels and copy,
actions present, the data being displayed or edited, surrounding source,
and nearby type/API names. State the inferred task in one or two
sentences before doing anything else. Do not fabricate deeper product
intent than the evidence supports — see "Missing intent," below.

### 2. Characterize the current expression

Identify the major design-system components in play, any custom UI
abstractions, the important interaction structure, and what conceptual
job each major element appears to perform. Don't judge yet — this step is
inventory, not evaluation.

Run `scripts/inspect_surface.py` over the surface and its directly
composed files first:

```
uv run scripts/inspect_surface.py --package-prefix 'PACKAGE_PREFIX' FILE [FILE ...]
```

Pass the actual package-import prefix(es) for the design system under
review (e.g. `@cloudscape-design/` for Cloudscape, `@mui/material`
plus `@mui/icons-material` for Material UI — repeat `--package-prefix`
for each). This gives a factual JSX/import inventory to reason from
rather than reconstructing it by eye; it reports facts only, with no
opinion on whether a choice is native — that judgment is entirely this
skill's own. It matches on source-string prefix, so it handles both deep
per-component subpaths and barrel imports in the same file — check its
full `design_system_imports` list rather than assuming one import
convention.

Where the fixture's installed design-system version is knowable, resolve
it with `scripts/resolve_versions.py` the same way:

```
uv run scripts/resolve_versions.py --root FRONTEND_ROOT --package NAME [--package NAME ...]
```

Version resolution matters less here than for an implementation-level
review, since component/composition *concepts* rarely change across
minor versions the way API shape or props do — but if a finding's
applicability plausibly depends on an unresolved semver range, name that.

### 3. Discover this design system's authority structure, then retrieve

Do not assume the retrieval hierarchy that happened to fit one design
system applies universally. Before retrieving anything for a specific
candidate judgment:

1. **Inspect the supplied authoritative discovery source** (an
   `llms.txt`-shaped index or equivalent authoritative snapshot) purely
   as a table of contents for selective retrieval — never cite its
   one-line description as if it were the guidance itself.
2. **Identify which meaningful authority categories actually exist** in
   this corpus. A design system may expose some or all of: component
   guidance, named task/product patterns, composition guides, usage
   guides, accessibility guidance, foundations, worked examples, demos.
   These labels are corpus-dependent — record what this corpus actually
   has, not what a different design system's corpus happened to have.
3. **Retrieve the strongest authority relevant to the candidate judgment**
   in front of you, fetching the actual linked pages, never the index's
   description. Stop as soon as a category settles the question.
4. **Do not invent a missing authority tier.** If this corpus has no
   task/pattern-level layer, say so plainly in the finding's authority
   evidence and reason from whichever tier(s) it does have, dropping to
   agent inference (labeled `INFERRED`, see "Finding contract") when
   nothing settles the question.

**A category present in one design system's documentation must not be
projected onto another.** Multiple component pages, worked examples,
demos, or guides do not become an implicit "pattern layer" merely because
a different design system's corpus has one. If a corpus's component pages
are the only meaningful authority tier available for a given question,
reason honestly at that tier rather than manufacturing composition-level
authority that doesn't exist there. Naming the absence of a tier is a
finding-quality signal, not a deficiency to paper over — see "Evidence
mode," below, for how a claim built by combining multiple component
pages (in the explicit absence of a composition/pattern-tier page) must
be labeled.

Two additional rules:

- **Examples and demos illustrate, they don't mandate** — unless the
  authoritative prose surrounding that example or demo explicitly states
  a recommendation or constraint, in which case the stated constraint,
  not the example itself, is the authority.
- **Existence does not imply a rule.** That the design system ships a
  purpose-built component or documents a named pattern, composition
  guide, or example for something adjacent to what the surface does is
  never, by itself, evidence the surface should adopt it. See
  "Anti-fundamentalism rule."

Do not ingest the whole documentation set. Retrieve the minimum relevant
material for the candidate finding in front of you, not a survey of the
whole component library.

### 4. Compare intent to documented vocabulary and compositions

Ask, in order, and stop as soon as the answer is no:

- Does the design system provide a component intended for this exact UI
  concept?
- Does the existing component serve the documented semantic purpose it's
  being used for?
- Does this corpus document a recurring composition or named pattern
  matching this user task — and does that authority category actually
  exist here (see step 3)? If it doesn't, skip straight to the
  applicability-of-inference question below rather than forcing a
  composition-shaped question onto a corpus with no composition tier.
- Does the current composition materially differ from that documented
  composition?
- Is the documented composition *actually applicable* to this task, or
  merely superficially similar (same shape, different problem)?
- Would the proposed alternative preserve the same product semantics —
  the same user task, not a different one?
- Is this a meaningful alignment improvement, or just another valid
  implementation of the same task?

### 5. Apply a high materiality bar

Do not report: aesthetic preference, an equally valid alternative, a
minor deviation, "the design system has a component for this" with no
applicability evidence, or "the docs show it this way" with no normative
or semantic support behind the citation. Prefer one to three strong
findings over exhaustive commentary. A clean result — no material
findings — is valid and expected on many surfaces; don't manufacture one
to avoid reporting a clean review.

## Anti-fundamentalism rule

**A component, composition, named pattern, guide, or example existing in
the design system is never, by itself, sufficient evidence that the
frontend should use it.** Every recommendation must establish
applicability, not just availability.

For composition-level findings specifically, require evidence that:

1. the observed user task materially matches the documented
   composition's stated problem — not just a superficial shape match
   (same layout, different problem);
2. the current implementation solves substantially the same problem the
   composition addresses;
3. the proposed native expression preserves that same task;
4. the difference between current and proposed is material enough that
   an experienced practitioner of this design system would plausibly
   restructure the code because of it, not just note it as an
   alternative.

If any of these four is weak, downgrade the finding's confidence or
suppress it entirely. A pattern or composition page's mere existence, or
a component page's mere description of what the component "is for," is
retrieval-step evidence, not applicability-step evidence — closing that
gap is the part of the job that can't be automated.

**Same-tier equivalence controls point 4.** Before finalizing point 4,
reconcile the *complete* authoritative material you retrieved for this
candidate — not only the excerpt you plan to quote. If that material
places the current and proposed expressions in the same suitability tier
(a tied decision-table cell, fit-tier classification, or unranked "use X
or use Y" pairing) rather than stating a directional preference between
them, point 4 fails: suppress the candidate or classify it
`intent-dependent`. A nearby differentiating clause — another row of the
same table, a different page's "use X if Y" — does not by itself overturn
a tie your own retrieval surfaced, including when that clause
differentiates by an unresolved user intent or behavior ("if users tend
to..."); that describes two different intents, not a direction. Check
whether *this bounded surface's own code, comments, or copy* — never a
property of the data itself, like a column's cardinality, and never the
authority page — resolves which intent applies. If it doesn't, this is a
"Missing intent" candidate: classify `intent-dependent` or suppress it,
don't pick a direction because one reading sounds more specific than the
other. This is not a default preference for the current implementation —
when the surface itself resolves the intent, or evidence genuinely
independent of the tied material establishes a task-specific advantage,
the finding still stands.

## Finding contract

Every reported candidate finding carries all of these fields. If any
field can't be filled honestly, keep investigating or drop the candidate.

- **Finding** — concise description of the native-expression opportunity.
- **Type** — exactly one: `component selection`, `documented
  composition`, `combined selection + composition`, or
  `intent-dependent`. Use `combined` when the component-level and
  composition-level observations are genuinely one underlying
  recommendation — don't split a single issue into two findings at two
  abstraction levels to make the report look more thorough. Do not encode
  a design-system-specific authority hierarchy into this field — it
  names what kind of *change* is being proposed, not what kind of source
  supports it (that's "Authority evidence," below).
- **Materiality** — `high` / `medium` / `low`. Suppress `low` from the
  final report by default (see "Apply a high materiality bar"); name what
  was suppressed and why, so a reader can tell "checked and cleared"
  apart from "never considered."
- **Confidence** — `high` / `medium` / `low`, about whether the finding
  is factually and semantically correct given the evidence gathered —
  independent of materiality.
- **User task** — the task this skill believes the surface supports, in
  one or two sentences, stated plainly enough that a reader can judge for
  themselves whether the rest of the finding actually preserves it.
- **Repository evidence** — exact file/location and enough observed
  interaction/component structure that a reader can verify the claim
  without re-deriving it.
- **Authority evidence** — the exact authoritative source (component
  page, named pattern page, composition/usage guide, foundation page —
  never the discovery index's one-line description), the specific
  guidance it establishes, and an honest **authority category** label for
  what kind of source it actually is: `component guidance`, `named
  pattern`, `guide`, `foundation`, `synthesis` (built from more than one
  cited source), or `inference` (no citation settles it). This label
  reports what exists in this corpus; it must never claim a category this
  corpus doesn't have. When the cited authority is a decision table,
  criteria table, or fit-tier classification, include enough of it here
  that a reader can audit the tier/direction question without
  re-fetching it, and explicitly disclose any row that qualifies,
  equalizes, or contradicts the finding's direction. Never quote a
  differentiating row while silently omitting one that ties the current
  and proposed approaches in the same tier — that is not an honest
  citation of that table, regardless of intent.
- **Evidence mode** — exactly one of `VERBATIM`, `PARAPHRASE`,
  `SYNTHESIS`, or `INFERRED`, describing how the cited authority backs
  the claim:
  - **VERBATIM** — text copied literally from the authoritative source.
    Must be copy/paste-verifiable against that source. Quotation marks
    may only be used for this mode. Before emitting a VERBATIM claim,
    re-check the quoted string character-for-character against the
    actual fetched source text (not memory, not an earlier paraphrase)
    and confirm it's attributed to the page it actually came from; if it
    doesn't match exactly, fix the quote or relabel the claim
    PARAPHRASE.
  - **PARAPHRASE** — one cited authoritative source supports the fact or
    guidance; the wording is the reviewer's own. Never present it as a
    quotation.
  - **SYNTHESIS** — the claimed guidance follows from multiple cited
    sources. Cite every load-bearing source and state the inferential
    bridge explicitly (what each source contributes, and how they
    combine). Never fabricate a single sentence that none of the cited
    sources actually contains. A synthesis does not automatically inherit
    the normative strength of its constituent sources — see "Authority
    strength," below.
  - **INFERRED** — no authoritative citation directly settles the
    judgment. Label the reasoning as such; never phrase it with
    `REQUIRED` or `RECOMMENDED` authority strength.
- **Applicability argument** — why the cited authority actually applies
  to *this* task, addressing the four-point test in "Anti-fundamentalism
  rule" directly, not just restating the citation.
- **Current expression** — how the surface presently represents the
  concept or task.
- **Native expression** — how a design-system-fluent implementer would
  likely express the same task instead, stated only when sufficiently
  supported by the cited evidence; if the supported alternative is
  uncertain, say so rather than inventing a confident replacement.
- **Why it matters** — the concrete, design-system-specific consequence
  (a documented constraint the current composition collides with, a
  materially worse fit for the stated task, a maintenance/consistency
  cost against the rest of an app built on this design system) — not a
  generic "this would be nicer."
- **Boundary check** — the one-sentence check required by "Scope
  boundary," reported here.

**Authority strength.** Label every finding's cited evidence with exactly
one of `REQUIRED` (the cited material states this as an explicit
constraint — a documented "Don't... Instead" pairing, an explicit
prohibition), `RECOMMENDED` (stated as preferred practice, not absolute),
`OPTIONAL` (documented as one supported alternative among others, no
stated preference), or `INFERRED` (no direct citation settles it — this
is reasoned judgment, and it must never be reported with `REQUIRED` or
`RECOMMENDED` phrasing).

Authority strength and evidence mode are independent axes, but they
interact: a `VERBATIM` or `PARAPHRASE` citation may support any strength
actually justified by what the source states. A `SYNTHESIS` does **not**
become `REQUIRED` or `RECOMMENDED` merely because its constituent pages
are individually authoritative — the synthesis itself, as an act of
reasoning bridging those sources, must be independently justified at the
claimed strength; when in doubt, a `SYNTHESIS` should default to
`OPTIONAL` or `INFERRED` rather than borrowing strength from its parts. A
pattern or composition page's own explicit "Don't do X, instead do Y" is
`REQUIRED` evidence for the specific rule it states, not license to treat
everything else about that pattern as mandatory — see
"Anti-fundamentalism rule."

**A native-expression finding does not need to be a violation.** Many
useful findings are honestly: *the current implementation is valid usage
of this design system, but its own guidance strongly favors a different
native expression for this specific task.* Label that distinction
honestly in "Why it matters" rather than inflating a `RECOMMENDED`-
strength preference into `REQUIRED`-strength language.

## Missing intent

If the user task can't be established with enough confidence from the
route, copy, actions, and surrounding code to choose between two
plausible, differently-native expressions, that is not a coin flip to
resolve by guessing which is "more native" in the abstract. Report the
candidate as `Type: intent-dependent` — name both plausible readings,
name what evidence would resolve it (e.g., "whether this record is meant
to be individually revisited/addressable, or is a transient by-product
of another flow"), and do not pick one. Suppressing the candidate
entirely is also correct when even naming it wouldn't be useful. Guessing
and reporting a confident recommendation anyway is the specific failure
mode this category exists to prevent.

## Report

```
# Design-System Native-Expression Review: <surface name>

**Design system:** <name of the design system this review is grounded in>

**Inferred user task:** <one to two sentences, from step 1>

**Packages / versions:** <resolved or "range only, unresolved: ...">

**Authority categories found in this corpus:** <what this design
system's documentation actually exposes — e.g. "component guidance and
named patterns" or "component guidance only, no separate composition/
pattern tier" — from step 3>

## Findings
<For each surviving (non-suppressed) finding, all fields from "Finding
contract," in materiality order (high first). "None." if none survive
suppression — a clean result is valid.>

## Suppressed (low materiality or weak applicability)
<One line each: what and why suppressed. "None." if none.>

## Orientation notes
<Component/composition candidates checked and confirmed as already-
native, correct usage — the affirmative "I looked and it's fine" record.
"None noted." if none.>

## What was not evaluated
<Implementation correctness (API usage, props, tokens, a11y mechanics)
and general UX/product judgment, named briefly so their absence doesn't
read as "checked and fine.">
```
