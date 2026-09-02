---
name: cloudscape-implementation-audit
description: >-
  Audits whether a bounded frontend surface (a page or small composed set
  of components) correctly implements Cloudscape Design System mechanics:
  component API usage, composition, styling/token mechanisms,
  Cloudscape-specific hooks/utilities, app-owned accessibility mechanics,
  and version-appropriate usage — judged against authoritative Cloudscape
  guidance retrieved for this task, never memory or a component's mere
  existence. Produces a small set of material, evidence-backed findings,
  each classified violation / recommended alignment / possible concern /
  unresolved, with materiality and confidence. Use when asked whether a
  frontend "does Cloudscape right," to review how a page uses Cloudscape,
  or before recommending Cloudscape implementation changes. Does not
  recommend swapping one Cloudscape component for another, does not
  redesign a page into a different Cloudscape pattern, and does not
  perform general React/UX/accessibility/performance review — see "Scope
  boundary."
---

# Cloudscape Implementation Audit

Primary question: **is this frontend implementing Cloudscape correctly?**
Not "is this a good design," not "is this the right component," not "is
this good React" — specifically whether the Cloudscape mechanics already
chosen are used the way Cloudscape's own documentation says to use them.

This is the lowest-level reviewer in a possible family (implementation
audit → component-selection review → experience review → alignment
synthesis). Its value depends entirely on staying at the implementation
layer; drifting upward makes it redundant with reviews that don't exist
yet and erodes the one thing this layer is for.

## Scope boundary

**In scope** — a finding belongs here only if it is about how Cloudscape
is implemented, not what was chosen:

- incorrect Cloudscape component API usage
- unsupported or incorrect component composition
- a native HTML control standing in for a Cloudscape primitive that
  provides the same behavior, where the substitution is semantically
  equivalent (not merely similar)
- custom implementation that recreates behavior Cloudscape already
  provides at the same abstraction level
- custom styling that bypasses or conflicts with documented Cloudscape
  styling/token mechanisms
- hard-coded visual values where a documented Cloudscape design token
  clearly applies
- incorrect use of Cloudscape-specific styling hooks or internals
- accessibility mechanics that are the application's responsibility when
  using a given Cloudscape component (documented required props/patterns,
  not general a11y best practice)
- unnecessary manual implementation of behavior for which Cloudscape
  provides an explicit developer utility at the same implementation level
- deprecated or unsupported Cloudscape implementation mechanisms, when
  authoritative evidence supports the claim
- implementation assumptions that conflict with the installed Cloudscape
  version

**Out of scope** — name these only in passing if at all, never as a
finding:

- **Component selection.** Never say a different Cloudscape component
  would have been a better choice ("Alert would be better than Flashbar,"
  "Cards would suit this better than Table") unless the component
  actually in use is *directly contradicted* by documented implementation
  guidance for that component — in which case the finding is about the
  contradiction, not about which component is nicer.
- **Pattern composition.** Never propose restructuring the page into a
  different Cloudscape product pattern (resource-management, split-view,
  create-resource, filtering, etc.) just because such a pattern exists.
- **General UX judgment.** Progressive disclosure, number of primary
  actions, information hierarchy, content density, navigation model,
  workflow design — silence, unless a specific Cloudscape implementation
  requirement is being violated, in which case cite that requirement, not
  a UX preference.
- **General frontend review.** React best practices, performance,
  security, general (non-Cloudscape) accessibility, code quality,
  architecture, style cleanup. A finding must matter *because this
  frontend uses Cloudscape* — if the same finding would apply to a plain
  React app with no design system at all, it does not belong in this
  audit.

Every finding must pass a boundary check before it's reported (see
"Finding contract"): state in one sentence why it's implementation-level
rather than one of the categories above. If you can't, cut the finding or
demote it to a one-line aside outside the findings list.

**How this composes.** The future siblings this deliberately leaves
alone: whether the *right* Cloudscape component was chosen for the job,
whether the page should be restructured around a different Cloudscape
product pattern, and whether the overall experience (not just this one
surface) hangs together. None of those exist yet as skills; don't
informally perform their job here because "it would be useful" — an
under-scoped implementation audit that also freelances component and
pattern advice is harder to trust on the thing it actually owns. When a
surface's material concern genuinely sits at one of those layers, and no
implementation finding honestly resolves it, see "Escalation" below —
the narrow, rare exception to reporting nothing.

## Orient before auditing

You need enough local context to avoid false positives, not a repository
summary:

1. **Read the bounded surface** and whatever it directly composes (the
   files it imports and renders, not the whole app). Note internal
   wrappers around Cloudscape components, shared styling abstractions,
   design-system adapters, app-wide conventions, helper hooks, and
   generated code — a "violation" that's actually a deliberate,
   consistently-applied wrapper is not a finding.
2. **Run the deterministic inspector** (below) over the surface and its
   direct composed files before reasoning about it by eye. Treat its
   output as a checklist of candidate locations to reason about, not as
   findings themselves.
3. **Resolve the installed Cloudscape version** (below) before judging
   anything against current documentation.

Stop orienting once you can explain what each Cloudscape import in the
surface is doing and which native elements or custom styles sit outside
that — don't chase the rest of the codebase.

## Deterministic evidence layer

Two bundled scripts turn mechanical extraction into facts, so the audit's
own reasoning starts from evidence instead of a first read-through. Both
are design-system-agnostic (package prefixes and package names are passed
in, never hardcoded) — a future audit of a different design system reuses
them by passing that system's own prefixes and package names.

- **`scripts/inspect_surface.py`** — AST-based (tree-sitter), not regex,
  over one or more `.tsx`/`.ts` files:
  `uv run scripts/inspect_surface.py --package-prefix '@cloudscape-design/' FILE [FILE ...]`
  Emits, per file: which `@cloudscape-design/*`-matching imports are used
  and their named exports; every JSX tag and its count; every *native*
  interactive HTML element (`input`, `select`, `textarea`, `button`, `a`,
  `label`, `option`, `fieldset`, `legend`, `progress`, `meter`, `details`,
  `summary`, `dialog`, `form`) with line and attributes; every element
  carrying a `style`/`className`/`class` attribute with its raw source;
  and literal hex colors / CSS length values found inside those captured
  style spans specifically (never scanned across the whole file).
- **`scripts/resolve_versions.py`** — reads `package.json` and, if present,
  an npm `package-lock.json` (walking up to 3 parent directories to find
  it):
  `uv run scripts/resolve_versions.py --root FRONTEND_ROOT --package NAME [--package NAME ...]`
  Emits declared semver range vs. locked resolved version per package,
  and marks a package unresolved (not approximately known) when no
  lockfile pins it — this is a fact, not a guess at what version is
  "probably" in use.

Both emit facts only — no design judgment, no "this is wrong," no
Cloudscape-specific interpretation baked into the extraction itself. What
stays agentic, deliberately not automated:

- deciding whether a flagged native element is genuinely a Cloudscape
  substitution opportunity, or a legitimate case Cloudscape doesn't cover
- deciding whether a flagged style/className is a deliberate, documented
  escape hatch or an undocumented bypass
- mapping any of the above to a specific piece of authoritative Cloudscape
  guidance and to REQUIRED/RECOMMENDED/OPTIONAL/INFERRED
- recognizing internal wrappers, adapters, and conventions (the inspector
  reports raw JSX/import facts; it does not know that `<InputField>` is a
  local wrapper around Cloudscape's `Input`)
- everything in "Finding contract" and "Materiality"

If a candidate signal seems worth a helper the inspector doesn't already
give you, weigh it against this: a helper is worth building only if it
improves repeatability, precision, or evidence quality over reading the
code directly — not because it would be convenient. Don't extend these
scripts into a general design-system linter; a fact the inspector can't
cheaply and mechanically decide belongs to the audit's own reasoning, not
to a new heuristic bolted onto the script.

## Version discipline

Before judging any fixture:

1. Identify its installed or declared Cloudscape packages (`package.json`).
2. Resolve the installed version from a lockfile where one exists
   (`resolve_versions.py`).
3. When no lockfile pins a package, treat the version as a range, not a
   fact — say so explicitly in any finding that depends on
   version-specific behavior, rather than assuming the latest docs apply.
4. Prefer local package/type evidence (the installed package's own
   TypeScript types, changelog, or shipped source, when reachable) over
   current upstream documentation when they could plausibly diverge —
   current `cloudscape.design` docs describe the current release, not
   necessarily whatever range or older pin a given fixture targets.
5. If a finding's validity depends on behavior that might differ between
   the fixture's resolved (or possible) version and current docs, say so
   in the finding rather than asserting current behavior applies.

## Authority model

The supplied `llms.txt`-shaped discovery index (or equivalent) is a table
of contents, not the authority itself. Use it to locate the minimum
relevant official material, then read that material — never cite the
index entry's one-line description as if it were the guidance.

Retrieval priority, in order, stopping as soon as a level settles the
question:

1. **Version-appropriate installed package/API evidence** — the
   fixture's own installed types/source for the resolved (or
   range-constrained) version.
2. **Official component or developer guidance** — the component's own
   docs/dev guide, or a dev guide (styling, tokens, accessibility
   utilities) that directly governs the mechanism in question.
3. **Official foundation guidance**, only when it directly governs
   implementation (a documented token, a documented mechanism) — not
   general design philosophy.
4. **Official patterns**, only to establish a concrete implementation
   rule already in play (e.g., a pattern page states a required prop
   usage) — never to justify recomposing the page into that pattern.
5. **Agent inference** — reasoned judgment with no direct documentation
   citation. Always the last resort, and always labeled as such.

Two hard rules:

- **Examples and demos are not authority.** A demo showing a component
  used a certain way does not establish that way as required or even
  recommended — demos illustrate, they don't mandate.
- **Existence does not imply a rule.** That Cloudscape ships a `Link`
  component does not, by itself, mean every `<a>` tag is a violation —
  the finding needs documented guidance that the native substitution is
  discouraged or that the component is the documented mechanism for that
  exact case, not just that an alternative exists.

Label every finding's authority with exactly one of:

- **REQUIRED** — the cited material states this as a constraint (a
  required prop, a documented incompatibility, an explicitly unsupported
  pattern).
- **RECOMMENDED** — the cited material states this as preferred practice,
  not a hard constraint.
- **OPTIONAL** — the cited material documents this as a supported
  alternative among others; there is no preference stated.
- **INFERRED** — no direct citation settles it; this is your reasoned
  judgment. An INFERRED finding must never be reported as a violation —
  see "Finding contract."

## Finding contract

Every reported finding carries all nine fields. If any field can't be
filled honestly, the finding isn't ready to report — either keep
investigating or drop it.

- **Finding** — concise description of the implementation issue.
- **Classification** — exactly one: `violation` (REQUIRED authority
  contradicted), `recommended alignment` (RECOMMENDED authority not
  followed), `possible concern` (real signal, but authority or repo
  context leaves it OPTIONAL/INFERRED or genuinely uncertain), or
  `unresolved` (evidence conflicts or is insufficient to classify
  further, named anyway because it's material enough to flag).
  A finding whose authority strength is INFERRED can be `possible
  concern` or `unresolved`, never `violation`; a `recommended alignment`
  finding needs RECOMMENDED or stronger authority, not INFERRED.
- **Materiality** — `high` / `medium` / `low`. Low-materiality findings
  are normally suppressed from the final report (see "Materiality").
- **Confidence** — `high` / `medium` / `low`, about whether the finding
  is factually correct given the evidence gathered — independent of
  materiality.
- **Repository evidence** — exact file/line and enough observed behavior
  that a reader can verify the claim without re-deriving it.
- **Cloudscape evidence** — the exact authoritative source (page, dev
  guide, API doc) and the specific guidance supporting the finding —
  never just the index entry's description.
- **Authority strength** — `Required` / `Recommended` / `Optional` /
  `Inferred`, per "Authority model."
- **Why it matters** — the concrete Cloudscape-specific consequence
  (broken theming under a token override, a documented a11y gap, behavior
  that diverges from the rest of a Cloudscape app, etc.) — not a generic
  "this is bad practice."
- **Native implementation** — what the surface should do instead, stated
  only when sufficiently supported by the cited evidence; if the
  supported fix is uncertain, say so rather than inventing a confident
  replacement.
- **Boundary check** — one sentence stating why this is an
  implementation-audit finding and not component-selection, pattern
  composition, general UX, or general frontend review.

## Materiality

Suppress low-materiality findings from the final review by default —
this audit is not a linter and completeness is not the goal. A finding
earns `high` or `medium` materiality when an experienced frontend
engineer working in this design system would plausibly change the code
because of it; `low` covers technically-correct-but-inconsequential
observations (a token that would save one hard-coded hex value with no
visible or theming impact, a native element substitution with no
behavioral difference in this exact usage). A clean result — no material
findings — is a valid, complete outcome; do not manufacture findings to
avoid reporting one.

## Escalation

Occasionally a surface's material concern genuinely sits at
component-selection, pattern-composition, or experience level — not at
the implementation level this audit judges — and the local Cloudscape
mechanics involved are otherwise valid. Don't silently drop that issue,
and don't reach for an implementation-shaped fix that isn't really
there. Record a rare, narrow **escalation** instead: enough evidence to
justify handing the surface to a higher-level reviewer, nothing more.

An escalation is not a lower-confidence finding, and not a place to park
something you suspect but can't evidence. Two hard gates before writing
one:

- You have concrete implementation *and* Cloudscape evidence that the
  material concern sits above this audit's layer — not just "this could
  arguably also be considered at a higher level" (that's true of almost
  any finding and does not, by itself, justify escalating).
- No implementation-level finding, at any classification, honestly
  resolves what you're seeing. If you can state it as a Finding with a
  real "Boundary check" that keeps it at implementation level, write
  that finding instead — it is not an escalation.

Every escalation carries exactly four fields:

- **Boundary reached** — exactly one of: component selection / pattern
  or experience / product-intent dependent.
- **Trigger evidence** — the concrete implementation fact plus the
  Cloudscape source it collides with (a cited pattern or component page
  and the repository fact it doesn't resolve at this layer).
- **Why no implementation finding** — one to two sentences on why this
  audit cannot responsibly resolve it without changing jurisdiction.
- **Suggested next review** — name only the reasoning category that
  should look at it next (e.g., "component-selection review," "pattern/
  experience review"). Never the higher-level recommendation itself — no
  component name, no pattern name, no restructuring proposal, even
  phrased as a gentle suggestion or a "consider."

Escalations do not count as findings and are never classified
violation/recommended alignment/possible concern/unresolved. They should
be rare — most surfaces, including most surfaces with real implementation
findings, produce none. Escalating more than one thing in a single
review is a signal to re-check whether escalation is being used as a
soft landing for a candidate finding that didn't earn its evidence,
rather than a genuine reasoning-boundary case.

## Report

```
# Cloudscape Implementation Audit: <surface name>

**Cloudscape packages / versions:** <resolved or "range only, unresolved: ...">

## Findings
<For each surviving (non-suppressed) finding, all nine fields from
"Finding contract," in materiality order (high first). "None." if none
survive suppression.>

## Escalations
<For each escalation, all four fields from "Escalation." "None." if none
— this is the expected, common case, including on surfaces that also
have real Findings.>

## Suppressed (low materiality)
<One line each: what and why suppressed. "None." if none.>

## Orientation notes
<Wrappers/adapters/conventions identified that prevented false positives,
if any. "None noted." if none.>

## What was not evaluated
<Anything intentionally out of scope per this audit's boundary that a
reader might otherwise expect covered — component choice, pattern
composition, general UX/frontend concerns — named briefly so silence
doesn't read as "checked and fine.">
```
