# Design-System Native-Expression Review: CreateEnvironment.tsx (ORIGINAL, pre-distillation SKILL.md, comparison trial)

**Design system:** Cloudscape (`@cloudscape-design/components`)

**Inferred user task:** A single page ("Create environment") lets a user configure and submit creation of a new infrastructure environment/resource — general identity, compute, networking, storage, monitoring, and tagging settings — culminating in a single "Create environment" submit action. This is a standard AWS-console-style "create resource" flow.

**Packages / versions:** `@cloudscape-design/components` resolved via `package-lock.json` to `3.0.900` (declared range `^3.0.900`).

**Authority categories found in this corpus:** Cloudscape's own docs expose both component guidance (per-component pages, often thin/JS-rendered prose beyond a one-line purpose statement) and named resource-management patterns with an explicit decision/criteria table (`/patterns/resource-management/create/`, with child pages `single-page-create/`, `multi-page-create/`, `sub-resource-create/`). This is a real composition/pattern tier, not projected from another design system — it ships numeric decision criteria, not just prose.

## Findings

### Finding 1: Single sprawling Form should be a Wizard (multipage create), per Cloudscape's own documented Length criteria

- **Type:** combined selection + composition
- **Materiality:** high
- **Confidence:** high
- **User task:** Creating a new environment by configuring six related but distinct configuration domains (general identity, compute, networking, storage, monitoring, tags) and submitting them as one resource-creation action.
- **Repository evidence:** `CreateEnvironment.tsx` renders one `ContentLayout` → one `Form` → one `SpaceBetween` containing six `Container`s (General, Compute, Networking, Storage, Monitoring, Tags — lines 108–220), all visible at once with a single "Create environment" submit button (lines 96–105). Counting every bound control: General 3 (envName, description, region), Compute 4 (instanceType, instanceCount, autoScalingMin, autoScalingMax), Networking 4 (vpc, subnet, securityGroup, publicIp), Storage 3 (volumeType, volumeSize, encryptVolume), Monitoring 3 (detailedMonitoring, logRetentionDays, alertEmail), Tags 3 (ownerTag, costCenterTag, environmentTag) = **20 fields across 6 groups**, none placed in any "additional settings"/expandable section — every field is unconditionally visible as if primary.
- **Authority evidence:** From `https://cloudscape.design/patterns/resource-management/create/` (named pattern, verbatim), the full Criteria table:

  | | Modal | Single page create | Multipage create |
  |---|---|---|---|
  | Length | = 1 field | Between 2 and 15 fields in the primary section or up to 5 groups of settings | More than 16 fields in primary sections or more than 5 groups of settings |
  | Complexity | Basic text input fields and simple selects | Flow does not require any category to have its own page | Concepts require in-depth interactions that benefit from having their own page |
  | Recovery | Input is mutable after creation | Input mutable after creation | Input immutable after creation |
  | Error handling | In trigger page | In creation page | In every single step and in summary step |
  | Frequency | n/a | Frequent | Infrequent |
  | Sub-resource create | No | Yes | Yes |

  Plus: *"Use the multipage create, which employs the wizard component, when you want users to create resources by completing a set of interrelated tasks. We recommend multipage create for long or complex configurations."* (`multi-page-create/`) and, for single-page create: *"Use single page create if you want your users to create a resource on a single page. This component is optimized for simple to medium-complex forms... Be critical of the inputs you place in the primary section, and keep it as short as possible."* (`single-page-create/`). Authority category: **named pattern**.
- **Evidence mode:** VERBATIM
- **Applicability argument:** (1) The observed task — creating an environment with six configuration domains — is exactly the "create resource" problem this pattern addresses, not a superficial shape match. (2) The current implementation solves that same problem end to end (one submit, all fields). (3) A wizard restructuring (steps per domain + review page) preserves the identical task and payload; nothing about `handleSubmit`'s flat `payload` object requires a single-page shape. (4) The surface independently clears **both** disjunctive Length sub-criteria for Multipage create: 20 fields exceeds the "more than 16" threshold, and 6 groups exceeds the "more than 5 groups" threshold — while Single page create's own band tops out at "15 fields... or up to 5 groups." Neither threshold is close; both are exceeded by a clear margin, which is exactly the "material enough that an experienced practitioner would plausibly restructure" bar. Same-tier equivalence check: the Recovery, Complexity, and Error-handling rows differentiate (not tied) between Single-page and Multipage; only the "Sub-resource create" row ties both at "Yes," and that row is not the one this finding relies on, so it doesn't undercut point 4. The Frequency row is explicitly gated ("Only use frequency as a criterion if you're unsure which pattern to use") and Length is independently dispositive here, so Frequency need not be resolved.
- **Current expression:** One `Form`/`ContentLayout` composition with all 20 fields always visible in six stacked `Container`s, no primary/additional-settings split, one submit action at the bottom.
- **Native expression:** A `Wizard`-based multipage create flow (per the multi-page-create pattern's building blocks): 3–5 steps grouping the current six domains (e.g., General+Compute, Networking, Storage+Monitoring, Tags), each step a single page with its own `Container`(s), a review/summary step that echoes each container in the same order with inline edit links back to its step, and standard wizard exit/unsaved-changes handling — rather than one long scroll with a single terminal submit.
- **Why it matters:** This isn't cosmetic — Cloudscape's own numeric criteria table exists precisely to route forms of this size and breadth away from single-page create; staying single-page here means every validation error, every "did I fill this in" check, and the entire mental model of the task is dumped on the user in one 20-field wall, which the pattern's Length/Complexity/Error-handling rows are specifically designed to avoid at this size.
- **Boundary check:** This is a composition-level (and consequent component-level) choice between two Cloudscape-documented create-resource patterns for the same task, not an implementation defect or generic UX complaint — it is settled by Cloudscape's own quantitative decision table applied to facts counted directly from the code.

### Finding 2: "Tags" container (Owner / Cost center / Environment tag) vs. TagEditor

- **Type:** intent-dependent
- **Materiality:** medium (if the open-tagging reading applies) / low (if the fixed-schema reading applies)
- **Confidence:** low, on which reading applies
- **User task:** Attaching organizational metadata ("tags" per the container's own header) to the new environment.
- **Repository evidence:** `CreateEnvironment.tsx` lines 208–220: a `Container` headed "Tags" holding exactly three fixed `FormField`+`Input` pairs — "Owner," "Cost center," "Environment tag" — with no add/remove affordance and no arbitrary-key input.
- **Authority evidence:** `https://cloudscape.design/components/tag-editor/`: *"An extension of the attribute editor built with integrated logic. With the tag editor, users can create, edit, or delete resource tags."* Authority category: **component guidance** (the corpus's tag-editor page has essentially no further prose beyond this purpose statement in static retrieval — its props/interactive demo content did not surface via fetch).
- **Evidence mode:** PARAPHRASE
- **Applicability argument:** TagEditor is purpose-built for open-ended, user-managed key/value resource tag CRUD (arbitrary count, arbitrary keys). This surface's "Tags" container could plausibly be either (a) genuine AWS-style resource tagging where "Owner/Cost center/Environment" are just an organization's conventional starter keys and users should be able to add/remove more — in which case TagEditor is the documented native fit and three bespoke fixed `Input`s under-serve the task — or (b) a deliberately fixed, exactly-three-field governance/compliance schema (no extensibility intended), in which case TagEditor's add/remove/arbitrary-key machinery doesn't fit a fixed schema any better than plain `FormField`+`Input`s do, and existence of TagEditor is not, by itself, evidence it should be used here (anti-fundamentalism rule). Nothing in the code (no "add tag" affordance, no dynamic array state, no key/value pair modeling) resolves which is intended.
- **Current expression:** Three named, fixed `FormField`+`Input` pairs, cardinality exactly three, no extensibility.
- **Native expression:** Uncertain — stated only conditionally: if arbitrary/extensible tagging is the actual intent, `TagEditor` is the native component; if exactly three fixed governance fields is the actual intent, the current expression is already reasonable and no change is indicated.
- **Why it matters:** Only material under one of the two readings; naming it lets a reader with the missing product context (does this org allow ad hoc tags beyond the three shown?) resolve it themselves.
- **Boundary check:** This is a component-selection question (bespoke fixed fields vs. the design system's purpose-built tag-management component) for the same conceptual job (attaching tags), not a UX or implementation critique — but it is reported as intent-dependent rather than a firm recommendation because the task's actual extensibility can't be established from this bounded surface.

## Suppressed (low materiality or weak applicability)

- **Log retention (days) modeled as `Input type="number"` rather than `Select`.** AWS console log-retention pickers are conventionally a fixed enumerated list, which would argue for `Select` (the component this exact file already uses correctly for every other closed-choice field: region, instance type, VPC, subnet, security group, volume type). Suppressed because nothing in this bounded surface's code, types, or copy evidences that log retention is domain-constrained to an enumerated set here — asserting that would fabricate deeper product intent than the evidence supports (see "Establish the user task").
- **Auto-scaling minimum/maximum as two separate `Input` fields.** No Cloudscape-documented component or pattern for paired min/max range entry was found; this is an equally-valid plain-Input expression with no applicability evidence for an alternative.
- **`Container` count/nesting itself.** Both single-page-create and multi-page-create building blocks describe the same `Container`+h2-`Header` composition for grouping fields ("You can have more than one container on a page" / "Consider using multiple containers if the choice is highly complex"), so the container-per-domain structure is not itself the problem — only the page-level single-vs-multipage choice is (folded into Finding 1 rather than reported separately).

## Orientation notes

- **`Checkbox` for `publicIp`, `encryptVolume`, `detailedMonitoring`.** Correct choice: Checkbox — *"Checkboxes enable users to turn an option on or off"* — versus Toggle — *"Toggles enable users to turn an option on or off, **and can result in an immediate change**"* (both `https://cloudscape.design/components/checkbox/` and `/toggle/`, verbatim). All three booleans here are pending form state applied only on "Create environment" submit, not immediate-effect toggles, so Checkbox is already the documented-correct choice.
- **`Select` for Region, Instance type, VPC, Subnet, Security group, Volume type.** Each is a closed, small, predefined option set (1–2 options in this fixture) bound via `selectedOption`/`onChange` — standard, correctly-scoped `Select` usage; no evidence in this surface of the free-text/large-dynamic-list scenario that would motivate `Autosuggest` instead.
- **Overall `ContentLayout` → `Form` → `Container`/`FormField` composition.** Matches the building blocks documented on both the single-page-create and multi-page-create pattern pages (form header, container-per-domain, form-field-per-input, action buttons in a horizontal `SpaceBetween`) — the components chosen are individually correct; only the single-page-vs-multipage top-level composition choice is in question (Finding 1).

## What was not evaluated

Implementation correctness — e.g., whether `type="number"` `Input`s should carry `min`/`max`/`step` constraints, wrapping Cloudscape's `Form` in a raw native `<form onSubmit>` element, absence of client-side validation/error states on any field, controlled-input mechanics — was not assessed; it is a distinct, lower-level concern this skill does not own. General UX and product judgment — field ordering, label wording, whether six domains are the right grouping, information density, whether this task should exist at all — were likewise not evaluated.
