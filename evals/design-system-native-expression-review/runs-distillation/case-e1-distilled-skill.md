# Design-System Native-Expression Review: ApiKeys.tsx (case-e1-api-keys)

**Design system:** Cloudscape (`@cloudscape-design/components` 3.0.900, `@cloudscape-design/collection-hooks` 1.0.60)

**Inferred user task:** A stand-alone account-settings page ("API keys") lets a user browse, free-text search, sort, and page through their account's API keys, seeing each key's name, environment (production/staging), active/revoked status, and creation date. No create/edit/delete/row-action affordances are present in this file — the visible task is browsing and inspecting an existing collection, not managing it end-to-end.

**Packages / versions:** resolved from `package-lock.json` — `@cloudscape-design/components@3.0.900` (declared `^3.0.900`), `@cloudscape-design/collection-hooks@1.0.60` (declared `^1.0.60`).

**Authority categories found in this corpus:** Cloudscape's own top-level structure (confirmed via its site index) exposes both **component guidance** (per-component pages with variant descriptions and dedicated "Do's and don'ts" guideline blocks — e.g. Table, Badge, Status Indicator) and **named patterns** (a distinct Patterns section, e.g. Patterns → Resource Management → View → Table view, and Patterns → General → Filter patterns) — both tiers were retrieved and used below, not assumed.

## Findings

### Finding 1: Table is composed as `variant="borderless"` directly under `ContentLayout`, which the table-view pattern's own guidance rules out for this page shape either way

- **Type:** combined selection + composition
- **Materiality:** high
- **Confidence:** high (that the current variant choice is wrong); the exact replacement is genuinely open — see Applicability argument
- **User task:** see above — a stand-alone page presenting and letting the user filter/sort/page a collection of API-key resources.
- **Repository evidence:** `ApiKeys.tsx` lines 1, 37–44 (`ContentLayout` wraps an `h1` `Header` with `counter`/`description`) and lines 45–79 (`<Table ... variant="borderless" ... />` as the sole body content, with `filter`, `pagination`, and `collectionProps` from `useCollection` wired in). This file lives at `src/pages/ApiKeys.tsx`, i.e. a top-level routed page, not content nested inside another container.
- **Authority evidence:** Cloudscape's Table-view pattern page (`/patterns/resource-management/view/table-view/`), "Don'ts" list:
  > "Don't use the content layout component on this type of page. Instead, use the "full-page" variant of the table component to implement this pattern."
  > "Don't use the table view pattern for tables that aren't overly content-heavy. Instead, if a table only has a few columns, use a bordered table inside the content layout component, with the default app layout content max-width."

  Corroborating: Table's own component page (`/components/table/`), variant descriptions:
  > "Borderless — Use this variant to place a table inside a container with other content... Use when placing a table inside another container. For example: when using a table in a dashboard item, expandable section, modal or within a split panel."
  > "Full page — This variant is for implementing the full page table view pattern. Use it for presenting and managing a table with many columns within a stand-alone page... Use this variant in conjunction with the `contentType="table"` property on the App Layout to maximize the available space."

  Authority category: **named pattern** (primary) + **component guidance** (corroborating). Authority strength: **RECOMMENDED** (the finding rests on a synthesis of two Don't/Instead pairings whose exact resolution branches — see below — so per this skill's rule a synthesis defaults away from REQUIRED even though each cited Don't is individually REQUIRED-strength on its own page).
- **Evidence mode:** SYNTHESIS. Neither citation alone determines the outcome: the pattern page names two mutually exclusive corrective paths gated on whether the table is "content-heavy"/"many columns" vs. "a few columns," and the Table page's own variant descriptions are needed to show that `borderless` — the option actually chosen — is documented for a third scenario (nested inside another container) that doesn't describe this page at all. The bridge: (1) this page implements the table-view pattern's documented feature set (filter + sort + pagination + header + counter), so one of the pattern's two Don'ts applies; (2) `borderless`'s own documented use-cases (dashboard item, expandable section, modal, split panel) don't include "sole content of a top-level page's `ContentLayout`"; therefore the current variant matches neither of the two paths the pattern names as correct.
- **Applicability argument:** (1) Task match is direct, not superficial — this page implements exactly the feature set ("filtering," "sorting," "pagination," item counter in the header) the table-view pattern describes as its subject matter. (2) The current code solves that same problem (client-side filter/sort/paginate via `useCollection`, matching the pattern's documented "table with client-side operations" guidance for small item sets). (3) Either corrective path — full-page variant with `ContentLayout` removed, or the default bordered/container variant kept inside `ContentLayout` — preserves the same browsing/filtering task; neither invents a new one. (4) Materiality is high because this isn't a stylistic quibble: the pattern page states its constraint as two explicit Don't/Instead pairs, and the currently-chosen variant is documented, on Table's own page, as belonging to a third, inapplicable scenario. I cannot resolve with confidence which of the two named paths (full-page vs. few-column/bordered) is intended — 4 columns is a genuinely borderline count and the docs give no numeric threshold — so I am not picking a side (see "Native expression").
- **Current expression:** `ContentLayout` → `Header` (h1) → `Table variant="borderless"` with `filter`/`pagination`/sorting wired via `useCollection`.
- **Native expression:** One of two documented shapes, not invented here — whichever this table is meant to be: (a) if it's meant to stay a small, few-column list, keep `ContentLayout` but drop `variant="borderless"` in favor of Table's default bordered/container presentation ("a bordered table inside the content layout component, with the default app layout content max-width"); or (b) if it's meant to be the account's primary, content-heavy key-management surface, drop `ContentLayout` and use `variant="full-page"` paired with the App Layout's `contentType="table"`. Which applies depends on product intent not resolvable from this file alone — see the open branch noted above.
- **Why it matters:** Regardless of which path is intended, the page collides with an explicit "Don't... Instead" pairing from Cloudscape's own table-view pattern, and the variant actually chosen (`borderless`) is documented on Table's own page as meant for content nested inside another container (dashboard item, expandable section, modal, split panel) — none of which describes a top-level `ContentLayout` page. That's a documented-composition mismatch, not a stylistic preference, and a maintenance/consistency cost against any other Cloudscape-built resource-list page in the same app.
- **Boundary check:** This is about which page-level composition (bare `ContentLayout` vs. the App Layout `contentType="table"` slot) and which documented Table variant apply to a stand-alone resource-management page — `variant="borderless"` is a mechanically valid prop value (not an implementation defect), and the claim is grounded in the table-view pattern's own explicit Don't/Instead pairings, not a generic aesthetic opinion.

### Finding 2: Status is placed in the third column instead of the documented second column

- **Type:** documented composition
- **Materiality:** high
- **Confidence:** high
- **User task:** same as above; Status (active/revoked) is the field that determines whether a given key is currently usable.
- **Repository evidence:** `columnDefinitions` in `ApiKeys.tsx` lines 49–72: column order is `name` (idx 0), `environment` (idx 1), `status` (idx 2), `createdAt` (idx 3) — Environment occupies the second position, Status the third.
- **Authority evidence:** Table's own component page, "Do's" (component-specific guidelines):
  > "Use the first table column for unique identifiers of the items that are represented in the table (for example: name, id, and ARN)..."
  > "Use the second column for status when status is relevant, for example *Running*."
  Authority category: **component guidance**. Authority strength: **RECOMMENDED** (a positive "Do" directive, not a "Don't X instead Y" prohibition, but stated unconditionally once its own stated condition — "when status is relevant" — is met).
- **Evidence mode:** VERBATIM.
- **Applicability argument:** (1) Task match is exact, not superficial: this is literally a table column-ordering convention for the same component in the same kind of resource-listing composition. (2) The current table already gets column 1 right (Name as the unique identifier) and already treats Status as meaningful enough to warrant a dedicated `StatusIndicator` — so "when status is relevant" (the guidance's own qualifying condition) is resolved affirmatively by this surface's own code, not left ambiguous. (3) The proposed reorder (swap Environment and Status) preserves the exact same columns and task, just their position. (4) This is material, not cosmetic: Status directly gates whether the key functions at all, which is exactly the kind of "operationally relevant" field the guideline is written for.
- **Current expression:** Column order Name → Environment → Status → Created.
- **Native expression:** Column order Name → Status → Environment → Created, so Status occupies the documented second position.
- **Why it matters:** Status here isn't cosmetic — it determines whether the key is usable — and demoting it behind a purely categorical field (Environment) works against the scan-order convention Cloudscape's own Table guidance establishes for exactly this situation, and against consistency with any other Cloudscape resource table in the same product that follows it.
- **Boundary check:** This is a column-position/composition question grounded in Table's own explicit column-ordering guidance, not an API/props defect (both orderings are mechanically valid `columnDefinitions` arrays) and not a generic "better hierarchy" opinion.

### Finding 3: Environment is rendered as plain text where Badge is the documented component for exactly this kind of categorical property

- **Type:** component selection
- **Materiality:** medium
- **Confidence:** high
- **User task:** same as above; Environment (production/staging) categorizes each key, distinct from its operational Status.
- **Repository evidence:** `ApiKeys.tsx` lines 56–60, `environment` column: `cell: (item) => item.environment` — rendered as bare text. Contrast with the adjacent `status` column, lines 61–65, which already wraps its value in `<StatusIndicator type={statusType(item.status)}>{item.status}</StatusIndicator>`.
- **Authority evidence:** Badge component page (`/components/badge/`), general guidelines:
  > Do: "Use badges for items that you want to label, categorize, or organize using text or numbers."
  > Don't: "Avoid using badges, including severity badges, to indicate status. Follow the guidelines for status indicator."
  Authority category: **component guidance**. Authority strength: **RECOMMENDED** (affirmative "Do" guidance for the categorize/organize use case; the corpus reserves REQUIRED-style "Don't" language specifically for the status use case, which this surface already correctly avoids for Badge).
- **Evidence mode:** VERBATIM.
- **Applicability argument:** (1) Task match: Environment values (`production`/`staging`) are a categorization label on the resource, not a state of the resource's health or operation — precisely Badge's documented "label, categorize, or organize" purpose, and precisely distinct from the "indicate status" use case Badge's own guidance says to avoid (and which this surface correctly reserves for `StatusIndicator` on the adjacent column). (2) The current cell solves the same "let a user see which environment a key belongs to" problem, just without a categorization affordance. (3) Swapping to `<Badge>{item.environment}</Badge>` preserves the same data and task. (4) Materiality: the surface already demonstrates it knows how to reach for a semantically-matched component for an adjacent enum-shaped column (Status → StatusIndicator); Environment is the same shape of problem (a small, closed set of category values) and Badge is the component the docs name for exactly that.
- **Current expression:** Environment column renders `item.environment` as plain, unstyled text.
- **Native expression:** Environment column renders `<Badge>{item.environment}</Badge>` (or `<Badge color="...">`), consistent with Badge's documented "label, categorize, or organize" purpose.
- **Why it matters:** This isn't a broken component — plain text is valid — but the surface has already established, one column over, that it reaches for a purpose-built component to make an enum-shaped property scannable; leaving Environment as bare text creates an inconsistent visual vocabulary between two adjacent, analogous columns, against the design system's own stated purpose for Badge.
- **Boundary check:** This is a component-selection question — plain text vs. Badge for a categorical property — grounded in Badge's documented "label, categorize, or organize" purpose, not an implementation defect (the current cell is valid JSX) and not generic "make it prettier" UX critique.

## Suppressed (low materiality or weak applicability)

- **TextFilter vs. collection-select-filter / property-filter for Environment/Status.** Cloudscape's filter-patterns guidance differentiates the three filtering mechanisms by *user behavior* ("if users tend to know exactly the value... use text filter"; "if the common behavior of users is to filter by only one or two properties, use the collection select filter"; "for complex products with large collections... use the property filter") — an unresolved-user-intent condition this skill's own equivalence-tie rule says a nearby differentiating clause can't be used to pick a direction from. Here the surface's own copy (`filteringPlaceholder="Find API key"`, `filteringAriaLabel="Filter API keys"`) actually leans toward the text-filter's own documented use case ("find" a specific item you already know), and the dataset (16 rows, two 2-value categorical facets) doesn't clearly clear the "large collection of resources" bar the property-filter guidance names. Suppressed as weak applicability / already resolved toward the current choice by the surface's own copy, not merely low-confidence.
- **CollectionPreferences absence.** Table's own guidance lists Collection preferences as one of several optional "Features" for more complex collections, without a stated trigger threshold this 4-column table clearly meets. No "Don't omit preferences when X" pairing was found. Suppressed for weak applicability, not because it wasn't checked.

## Orientation notes

- `StatusIndicator` type mapping (`active` → `success`, `revoked` → `stopped`) matches Status Indicator's own documented "Stopped/inactive: The resource, service, or process is no longer running, inactive, or severity is not relevant" — a revoked key fits this definition; correct semantic usage, not a finding.
- Filtering/sorting/pagination are enabled on a 16-item table, matching Table's own guidance: "Only use filtering, pagination, and sorting if there are more than five items in the table."
- Client-side filtering/sorting/pagination via `useCollection` matches Table's documented "client-side operations" pattern for lists that aren't too big.
- The header's item counter (`counter={\`(${API_KEYS.length})\`}`) matches "Always show the total number of items next to the table title," in the documented parenthesized format.
- Single-column sort (`sortingField` on Name/Created only, no multi-sort) matches "Use single-column sort as the default."

## What was not evaluated

Implementation correctness — including the duplicated empty-state message (defined both in `useCollection`'s `filtering.empty` and again on `Table`'s `empty` prop), ARIA labeling mechanics on `TextFilter`/`StatusIndicator`, and general prop/API usage — was not assessed; its absence from this report is not a claim it's clean. General UX/product judgment — including the complete absence of any create/revoke/copy/delete affordance for what is otherwise a management-shaped page, and whether that's an intentional read-only surface — was also not assessed; naming it here is not a finding, since inventing that functionality would be a different product than what this file currently expresses.
