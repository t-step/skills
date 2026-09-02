# Design-System Native-Expression Review: CreateBackupSchedule.tsx

**Design system:** Cloudscape Design System

**Inferred user task:** A single-page form for creating a new backup schedule: the user names the schedule, chooses a backup frequency (Daily/Weekly/Monthly), and chooses a retention policy (keep only the latest backup vs. keep full history), then submits to create the schedule or cancels. This is a standard "create resource" flow with a small, fixed set of fields.

**Packages / versions:** `@cloudscape-design/components` 3.0.900 (resolved from package-lock.json), `@cloudscape-design/collection-hooks` 1.0.60, `@cloudscape-design/global-styles` 1.0.45 — all fully resolved, no unresolved semver ranges.

**Authority categories found in this corpus:** Cloudscape's own `llms.txt` index exposes: component guidance (112 components), named patterns organized by category (General; Resource management — create/edit/delete/view/details; Data visualization; Service dashboards; Onboarding), foundations, demos, and Generative AI guidance. This corpus does have a genuine pattern/composition tier distinct from component pages — both were consulted below.

## Findings

### Finding 1: Frequency field uses Select for a 3-option single choice where Cloudscape's own selection-pattern criteria places option sets this small in Radio group / Tiles, not Select

- **Finding:** The "Frequency" field is implemented with `Select` offering exactly three fixed options (Daily, Weekly, Monthly), with no search, icons, descriptions, or tags. Cloudscape's documented single-selection criteria table assigns option counts of 2–7 to Radio group / Tiles and reserves Select (and Autosuggest) for 8+ options.
- **Type:** `component selection`
- **Materiality:** `high`
- **Confidence:** `high`
- **User task:** The user must pick exactly one of three named, mutually-exclusive backup cadences before creating the schedule; no search, filtering, or growth beyond these three values is evidenced anywhere in the surface (`FREQUENCY_OPTIONS` is a static, hard-coded 3-item array).
- **Repository evidence:** `CreateBackupSchedule.tsx` lines 13-17 define `FREQUENCY_OPTIONS` as a static 3-item array (`Daily`, `Weekly`, `Monthly`); lines 58-64 render it via `FormField label="Frequency"` wrapping a `Select` bound to `selectedOption`/`onChange`. No option carries a description, icon, or tag. By contrast, the adjacent "Retention policy" field (lines 65-74), also a single choice among 2 named options, is implemented with `RadioGroup`, not `Select` — i.e., the surface already uses the small-option-set pattern once, just not consistently.
- **Authority evidence:** Cloudscape pattern page "Selection in forms" (`https://cloudscape.design/patterns/general/selection/`), section "Single selection criteria," reproduced in full:

  | | Radio group | Tiles | Select | Autosuggest |
  |---|---|---|---|---|
  | Number of options | 2 to 7 options | 2 to 7 options | 8+ options | 8+ options, including user generated inputs |
  | Additional metadata per option | Descriptions | Descriptions, lists, and/or images | Icons, descriptions, and/or tags | Icons, descriptions, and/or tags |

  Immediately below the table, the page states verbatim: "The fastest way for users to find and select an option in a list of seven or fewer options is to see all the options at once as a group of checkboxes, radio buttons, or tiles. For groups of eight or more options, we recommend using a select or autosuggest list. This will reduce the space the selection pattern takes on the page and help the user find options within larger groups."

  Authority category: **named pattern**.
- **Evidence mode:** `VERBATIM` (table and quoted sentence reproduced exactly as fetched from the live page).
- **Applicability argument:** (1) The observed task — choose one of a small, fixed, named set of options with no metadata — is exactly the problem this criteria table addresses (it is keyed directly on option count and metadata need, both of which are known and small here: 3 options, plain text labels, no icons/descriptions/tags). (2) The current `Select` does solve the same underlying problem (single choice among the three values) — this is not a semantic mismatch, just a size mismatch against the documented threshold. (3) Swapping to `RadioGroup` (or `Tiles`) preserves the identical task: the user still picks exactly one of the same three named frequencies. (4) Materiality: the table's own stated rationale — visibility of all options at once being "the fastest way for users to find and select" — applies directly at n=3, which sits well inside the 2-7 bucket, not near an ambiguous boundary; and the page uses `RadioGroup` for a same-shape decision (Retention) one field below, so an experienced Cloudscape implementer following this page's own conventions would very plausibly make Frequency consistent with it. This is a directional recommendation ("we recommend... for 8+", implying the smaller-set controls for fewer), not a same-tier tie between Select and Radio group at this option count — the table places them in different, non-overlapping brackets for n=3, so the anti-fundamentalism same-tier check does not apply here. (Radio group and Tiles are the same-tier options *with each other* at 2-7 options; the finding does not pick between them for that reason — see Native expression.)
- **Current expression:** A `Select` dropdown bound to a static 3-item `SelectProps.Option[]` array, requiring an extra open/close interaction to see or change the value.
- **Native expression:** A `RadioGroup` (already the pattern used one field below, for Retention) or `Tiles` presenting all three frequency options simultaneously, consistent with the 2-7-option bracket of Cloudscape's own selection criteria. Between Radio group and Tiles, the documentation does not state a directional preference at this option count (both occupy the same row) — that choice is not resolved by this page and is not part of this finding; RadioGroup is the more consistent choice only because the surface already establishes that convention for Retention.
- **Why it matters:** The current choice sits outside Cloudscape's own documented option-count threshold for Select (8+), for a field with exactly 3 static, textual options — the scenario the guidance singles out as better served by immediate at-a-glance visibility. It also creates an inconsistency within this single form: two structurally identical "pick one named option from a short static list" fields (Frequency, Retention) are expressed with two different Cloudscape selection controls for no evidenced reason, working against the same page's own established convention.
- **Boundary check:** This is a component-selection judgment (Select vs. Radio group/Tiles for a fixed 3-option single choice), grounded in Cloudscape's own documented option-count criteria — not an implementation defect (the `Select` usage is API-correct) and not a generic UX complaint (the case for change is the design system's own stated selection-pattern rule, not a subjective "dropdowns are annoying" preference).

## Suppressed (low materiality or weak applicability)

- Whether the page should be restructured to wrap its fields in Cloudscape's own native `<form>`-submission conventions (the surface hand-wraps `Form` in a raw `<form onSubmit>` to drive `Button formAction="submit"`) — considered, but this is submission/composition *mechanics*, not a choice between documented design-system concepts, so it falls under this skill's implementation-correctness exclusion and was not investigated further as a candidate.

## Orientation notes

- **Overall page composition (ContentLayout > Header + Form > Container > FormField/SpaceBetween) matches Cloudscape's documented "Single page create" pattern.** Per `https://cloudscape.design/patterns/resource-management/create/`, the "Criteria" table specifies Single page create for "Between 2 and 15 fields in the primary section" with "Basic text input fields and simple selects" and a flow that "does not require any category to have its own page." This surface has exactly 3 fields (name, frequency, retention), all basic inputs, on one page — squarely inside that bracket. No case for a multipage Wizard (documented for "More than 16 fields... or more than 5 groups of settings," or "concepts [that] require in-depth interactions"). This is the correct pattern choice.
- **"Retention policy" field's use of `RadioGroup` (not `Toggle`) is correctly chosen.** Cloudscape's "Selection in forms" pattern's boolean-selection criteria states verbatim: "Binary choices made by using checkboxes, radio groups, and tiles should take effect at form submission, for example in a creation or edit flow," reserving `Toggle` for "an option that takes effect immediately... resulting in a visible interface change." Retention policy takes effect only when the schedule is created (at form submission), and it has 2 named options within the documented 2-7 range for Radio group — both conditions favor Radio group, which is what's used.
- **Actions placement (`Form`'s `actions` slot holding Cancel/Create via `SpaceBetween direction="horizontal"`) is the standard, documented composition for primary/secondary form actions** and was not further investigated as a candidate since no divergence was observed.

## What was not evaluated

Implementation correctness (React/Cloudscape API usage, prop validity, the raw `<form>` wrapper's submission mechanics, hard-coded style values, accessibility mechanics) and general UX/product judgment (field ordering, copy quality, whether additional schedule-configuration fields should exist) were not assessed — their absence here should not be read as "checked and fine."
