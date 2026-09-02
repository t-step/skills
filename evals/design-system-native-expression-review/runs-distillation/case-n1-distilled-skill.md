# Design-System Native-Expression Review: AccountSettings.tsx

**Design system:** Cloudscape (`@cloudscape-design/components`)

**Inferred user task:** A user-facing account settings page where the user independently enables/disables two standalone boolean preferences — "require two-factor authentication for sign-in" and "send email notifications for account activity." Each change is persisted immediately on interaction (`onChange` fires a `PATCH /api/account/settings` for that single key), with no batching, no review step, and no explicit save/submit action anywhere on the page.

**Packages / versions:** `@cloudscape-design/components` 3.0.900 (locked), `@cloudscape-design/global-styles` 1.0.45 (locked) — both resolved from `package-lock.json`. Toggle and Checkbox are long-stable, non-experimental Cloudscape components; the finding below does not depend on an unresolved semver range.

**Authority categories found in this corpus:** component guidance (per-component "Usage" tab with `Do`/`Don't` general guidelines, features, writing and accessibility guidelines — confirmed on the Toggle and Checkbox pages) and named patterns (a `/patterns/` top-level section; the applicable one here is "Selection in forms," which contains an explicit criteria table plus prose for boolean selection). Both tiers were retrieved and agree.

## Findings

### Finding 1 — Both settings use Checkbox for an immediate-effect action; Cloudscape's own guidance calls this out by name as the Toggle case

- **Type:** `component selection`
- **Materiality:** `high`
- **Confidence:** `high`
- **User task:** As stated above — two independent, standalone boolean account preferences, each persisted immediately on change with no form-submission step.
- **Repository evidence:** `src/pages/AccountSettings.tsx`, lines 20–49. Both `Checkbox` instances (`requireTwoFactor`, lines 28–36; `emailNotifications`, lines 37–45) call `setState` and then `updateAccountSetting(key, detail.checked)` directly inside `onChange` (lines 30–33, 39–42). `updateAccountSetting` (lines 13–18) fires `fetch('/api/account/settings', { method: 'PATCH', ... })` unconditionally, once per keystroke of interaction. There is no `Form`, no submit/save button, and no batching of the two settings anywhere in this file — the change takes effect the moment the control is toggled.
- **Authority evidence:**
  - Source: Cloudscape "Selection in forms" pattern page (`https://cloudscape.design/patterns/general/selection/`), section "Boolean selection criteria." Authority category: **named pattern**.
    - Criteria table, "Selection" row (full row, so the reader can audit all four cells, not just the ones favoring this finding):
      - Checkbox: "The selection takes effect at form submission."
      - Toggle: "The selection results in an immediate change. For example, turning on dark mode."
      - Radio group: "The selection takes effect at form submission."
      - Tiles: "The selection takes effect at form submission."
    - Accompanying prose: "Binary choices made by using checkboxes, radio groups, and tiles should take effect at form submission, for example in a creation or edit flow. Use a toggle for an option that takes effect immediately, such as turning on a system feature that results in a visible interface change, for example, turn on dark mode."
    - No other row in this table (Sub-options, Additional metadata) qualifies or contradicts this direction — those rows address a different dimension (whether the control gates other sub-elements, and where descriptive metadata may appear), not whether the change is immediate vs. submit-gated. The "Selection" row is a clean directional split, not a tied cell.
  - Source: Cloudscape Checkbox component page, Usage tab, `Don't` section (`https://cloudscape.design/components/checkbox/?tabId=usage`). Authority category: **component guidance**.
    - "Don't use for options that take immediate effect, for example to switch between light and dark mode. Use a toggle instead."
  - Source: Cloudscape Toggle component page, Usage tab, `Do` section (`https://cloudscape.design/components/toggle/?tabId=usage`). Authority category: **component guidance**.
    - "Use for an option that takes effect immediately, for example toggling versioning on an S3 bucket to enable or disable the storage of multiple versions of objects."
    - Converse confirmation, `Don't` section: "Don't use a toggle for options that are activated at form submission, such as an acknowledgement of EULA or Terms and Conditions. In this case, use a checkbox."
- **Evidence mode:** `VERBATIM` — every claim above is a direct, character-checked quote from the fetched pages, attributed to the page it came from.
- **Applicability argument:** (1) The observed task materially matches the documented criterion, not just superficially — the code's own `onChange` → `fetch(PATCH)` wiring, with no `Form`/submit affordance anywhere in the bounded file, is exactly the "results in an immediate change" case the pattern page uses "turning on dark mode" to illustrate, not the "takes effect at form submission... in a creation or edit flow" case. (2) The current implementation solves the same problem (persist a boolean preference) the Toggle guidance addresses — it just uses the component the corpus explicitly reserves for the other branch of this exact decision. (3) Swapping `Checkbox` → `Toggle` for both settings preserves the same user task and the same immediate-persist behavior; nothing about the surrounding `Container`/`SpaceBetween` composition needs to change. (4) This clears the bar for "an experienced practitioner would restructure it": the Checkbox page's own `Don't` list names this exact scenario ("options that take immediate effect... switch between light and dark mode") and directs to Toggle by name — this is not a marginal preference, it is the documented decision criterion this design system uses to separate the two components.
- **Current expression:** Two `Checkbox` components under one `Container`, each independently and immediately persisting its own boolean value via a `PATCH` request on every change.
- **Native expression:** Two `Toggle` components in the same position/composition, each still calling `updateAccountSetting` from its own `onChange`. No other structural change is implied — `ContentLayout` → `Header` → `Container` → `SpaceBetween` remains the correct shell; only the two leaf controls change.
- **Why it matters:** This isn't a stylistic swap — Cloudscape draws the Checkbox/Toggle boundary specifically on "does this take effect at form submission or immediately," and states the immediate-effect case as a `Don't` for Checkbox on the Checkbox page itself. Using Checkbox here also silently mismatches its own documented semantic ("the selection takes effect at form submission") against a page that has no submission step at all, which is a real (if subtle) misrepresentation of what the control communicates to a design-system-fluent reader of this code and to any user comparing this page against other Cloudscape-built settings surfaces in the same product that do follow this convention.
- **Boundary check:** This is a component-selection judgment about which control natively expresses an immediate-effect boolean setting per Cloudscape's own documented Checkbox/Toggle decision criterion — not an implementation-correctness concern (both `Checkbox` usages are mechanically valid, correctly-typed API usage) and not a generic UX critique (the objection is grounded in an explicit, named `Don't` rule on the Checkbox page and a criteria table on the "Selection in forms" pattern page, not a subjective density/hierarchy complaint).

## Suppressed (low materiality or weak applicability)

None — only one candidate reached the materiality bar; nothing else was found and then discarded.

## Orientation notes

- `ContentLayout` (h1) wrapping a single `Header`(h2)-labeled `Container`, with `SpaceBetween size="l"` between the two controls, is a standard, correctly-used Cloudscape page shell for a small settings surface — checked against the Container/ContentLayout component pages' stated purpose and found to be an unremarkable, native composition. No finding here.
- The absence of a `Form` component wrapping the two controls is, on this record, the *correct* choice rather than an omission: the "Selection in forms" pattern page's own "Selection" criterion reserves `Form`-style submit-gated composition for options that "take effect at form submission," which is explicitly not this page's behavior (each control persists immediately via its own `PATCH`). This reinforces, rather than undercuts, Finding 1 — it's additional evidence the page is intentionally immediate-effect, so `Toggle` is the consistent choice throughout, not just for the individual controls.
- The two settings are independent (neither's sub-elements are gated by the other), so the pattern page's progressive-disclosure / "sub-options" guidance (which would separately require a Toggle "parent" over Checkbox "children") does not apply here — checked and correctly not implicated.

## What was not evaluated

Implementation correctness (Checkbox/Toggle prop usage, TypeScript typing of `AccountSettingsState`, the fire-and-forget `fetch` call's lack of error handling or loading/success feedback, accessibility mechanics beyond what's documented on the component pages) and general UX/product judgment (e.g., whether users should get a confirmation toast, whether the page needs additional settings, information density, or heading/copy wording) were not assessed and their absence here should not be read as "checked and fine."
