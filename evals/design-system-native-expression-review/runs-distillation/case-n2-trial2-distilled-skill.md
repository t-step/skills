# Design-System Native-Expression Review: CreateEnvironment.tsx

**Design system:** Cloudscape (`@cloudscape-design/components`)

**Inferred user task:** A user configures and submits a new infrastructure "environment" — general identity, compute (instance type/count/auto-scaling), networking (VPC/subnet/security group/public IP), storage (volume type/size/encryption), monitoring (detailed monitoring/log retention/alert email), and tags (owner/cost center/environment) — in one create flow, then clicks "Create environment" to submit all of it at once. This is a single-submission resource-provisioning form, not an editor for an existing resource.

**Packages / versions:** `@cloudscape-design/components` declared `^3.0.900`, locked `3.0.900` (resolved via `package-lock.json`). `@cloudscape-design/global-styles` declared `^1.0.45`, locked `1.0.45` (not directly imported in this file).

**Authority categories found in this corpus:** component guidance (individual component pages, e.g. Wizard, Toggle, Checkbox) and named patterns, including an explicit resource-management "Create resource" decision table that routes between Modal / Single page create / Multipage create by stated field- and group-count thresholds. No foundations-tier page was retrieved for this review (not needed to settle the candidate judgments below).

## Findings

**Finding:** The page implements a 6-group, 20-field resource-creation form as one continuously scrolling single page (stacked `Container`s inside one `Form`), when Cloudscape's own create-resource decision table places a configuration of this size and shape in the Multipage Create (Wizard) tier, not the Single Page Create tier the surface currently uses.

**Type:** documented composition

**Materiality:** high

**Confidence:** high

**User task:** As stated above — a single-submission environment-provisioning form spanning general identity, compute, networking, storage, monitoring, and tags.

**Repository evidence:** `CreateEnvironment.tsx` — one `ContentLayout` → `Form` → `SpaceBetween` composition (lines 92–224) containing six `Container` sections, each with its own `Header variant="h2"` (General 108, Compute 126, Networking 147, Storage 176, Monitoring 194, Tags 208), all rendered simultaneously with a single submit action (`Button formAction="submit"`, lines 101–103). `scripts/inspect_surface.py`'s factual JSX counts confirm: `Container: 6`, `FormField: 17`, `Checkbox: 3` (17 + 3 = 20 total interactive fields), `Select: 6`, `Input: 10`, `Textarea: 1` — no expandable "additional settings" section, no step navigation, no review step anywhere in the file.

**Authority evidence:** cloudscape.design/patterns/resource-management/create/ — decision table, "Length" row (VERBATIM, extracted from the page's own content JSON): *"Modal: = 1 field | Single page create: Between 2 and 15 fields in the primary section or up to 5 groups of settings | Multipage create: More than 16 fields in primary sections or more than 5 groups of settings."* Companion row "Complexity": *"Single page create: Flow does not require any category to have its own page | Multipage create: Concepts require in-depth interactions that benefit from having their own page."* Row "Error handling": *"Single page create: In creation page | Multipage create: In every single step and in summary step."* From cloudscape.design/patterns/resource-management/create/single-page-create/ (VERBATIM): *"Use single page create if you want your users to create a resource on a single page. This component is optimized for simple to medium-complex forms."* From cloudscape.design/patterns/resource-management/create/multi-page-create/ (VERBATIM): *"Use the multipage create, which employs the wizard component, when you want users to create resources by completing a set of interrelated tasks. We recommend multipage create for long or complex configurations."* And, on recommended step count (VERBATIM): *"You can use up to seven pages if necessary, but we recommend using three to five pages in the flow."* From cloudscape.design/components/wizard/ (VERBATIM): *"A multi-page form that guides a user through a complex flow or a series of interrelated tasks."* Authority category: **named pattern** (the decision table and the two create-resource pattern pages), corroborated by **component guidance** (Wizard's stated purpose).

**Evidence mode:** VERBATIM (the decision-table thresholds and the two patterns' "when to use" statements are quoted directly from the fetched pages; comparing this surface's own field/group counts against those thresholds is a direct factual application, not an inferential bridge across sources).

**Applicability argument:**
1. *Task match, not superficial shape match:* the decision table's Length/Complexity rows exist precisely to route resource-creation forms between the three named patterns by field/group count and by whether settings form conceptually distinct domains — exactly this surface's situation (compute vs. networking vs. storage vs. monitoring are each a distinct AWS-style concern).
2. *Same problem:* the current implementation is unambiguously a "create resource" flow — the exact task category the table addresses.
3. *Same task preserved:* a wizard restructuring changes only navigation/structure, not the fields collected or the final submission.
4. *Material, not a tie:* this is the decisive point. The table's ranges are disjoint at the boundary (single page: "up to 5 groups"/"2–15 fields"; multipage: "more than 5 groups"/"more than 16 fields"). This surface has **6 groups and 20 fields** — past both multipage thresholds by a comfortable margin, not sitting at the ambiguous 5-group/15–16-field boundary where the "same-tier equivalence" caveat would apply. Nothing in the surface's own code or copy points the other way (e.g., no comment or product signal suggesting these are meant to feel like one flat, trivial form).

**Current expression:** Single Page Create shape — `ContentLayout` → `Form` → six stacked `Container`s, all 20 fields visible in one continuous scroll, one create action, no per-domain step boundaries, no review step, no "additional settings" deferral of any field.

**Native expression:** A Cloudscape `Wizard`-driven Multipage Create flow, most likely consolidating the current six `Container`s into the pattern's recommended 3–5 steps (e.g., General+Compute, Networking, Storage+Monitoring, Tags), ending in a review/summary step, with the top-level `Form` wrapper replaced by `Wizard`'s step-driven navigation and per-step error handling. The exact step grouping is a product decision beyond what the cited authority prescribes; only the shift from single-page to multi-step is supported with confidence.

**Why it matters:** The corpus's own decision table is built specifically to move a creation flow off a single unbroken page once it crosses a stated field/group threshold, and to move validation from one creation-page model to a per-step-plus-summary model (its own "Error handling" row draws exactly this distinction). At 20 fields across 6 conceptually separate settings domains, this surface sits well inside the range the design system's own criteria assign to the wizard-based pattern — not a borderline call a fluent Cloudscape implementer would leave as-is.

**Boundary check:** This is a judgment about which of Cloudscape's own documented create-resource compositions (single-page vs. multipage/wizard) fits a form of this size and structure — not a claim about incorrect `Container`/`Form`/`Select` API usage (implementation correctness) and not a generic "this form is too long" opinion (general UX); the recommendation rests on the corpus's own explicit field/group-count decision table for this exact task category.

## Suppressed (low materiality or weak applicability)

- **Select vs. RadioGroup/Tiles for the 2-option fields** (region, instance type, volume type): the fixture's small hardcoded option lists (2 entries each) are stub/mock data, not evidence about real-world list length — regions, instance types, and volume types are all realistically large or variable lists in production, so `Select` remains the appropriate component; not reported.
- **Attribute Editor pattern for the Tags section**: considered because "Tags" often maps to Cloudscape's `attribute-editing` pattern for arbitrary key-value resource attributes, but this surface's three tag fields (Owner, Cost center, Environment tag) are fixed, named, non-repeatable fields — not the open-ended, user-extensible key-value list that pattern addresses. No applicability.
- **A documented composition for the VPC → Subnet → Security group dependency chain**: no named pattern or composition guide surfaced in the retrieval performed for cascading/dependent select fields in this corpus; any recommendation here would rest on `INFERRED` reasoning only, below the materiality bar.

## Orientation notes

- `Checkbox` is used for `publicIp`, `encryptVolume`, and `detailedMonitoring` (lines 170, 188, 196) — correct per Cloudscape's documented split: Checkbox's own guidance states *"Don't use for options that take immediate effect, for example to switch between light and dark mode. Use a toggle instead,"* and Toggle's own guidance states *"Don't use a toggle for options that are activated at form submission, such as an acknowledgement of EULA or Terms and Conditions. In this case, use a checkbox."* All three booleans here take effect only on the deferred "Create environment" submit action, matching Checkbox's documented case.
- `Select` is used for region, instance type, VPC, subnet, security group, and volume type — valid component usage; the fixture's small option counts are stub data and shouldn't be read as evidence these should instead be RadioGroup/Tiles, since the underlying real-world lists (AWS regions, instance types, volume types) are inherently large/variable.

## What was not evaluated

Implementation correctness (prop usage, controlled-component wiring, numeric `Input` validation/min-max handling, accessibility mechanics, any hard-coded style values) was not audited beyond what `inspect_surface.py` reports as fact — no style/literal-value usage was flagged by the tool, but no deeper implementation review was performed. General UX/product judgment (whether 20 fields is the right amount of data to collect in one environment, field ordering/naming, whether the chosen defaults are sensible) is out of scope for this skill and was not assessed.
