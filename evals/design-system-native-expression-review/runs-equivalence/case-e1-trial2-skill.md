# Design-System Native-Expression Review: ApiKeys.tsx

**Design system:** Cloudscape

**Inferred user task:** A user views the complete list of API keys configured for their account (16 keys), each shown with a name, environment (`production`/`staging`), status (`active`/`revoked`), and creation date, and can locate specific keys within that list via filtering, sorting, and pagination.

**Packages / versions:** `@cloudscape-design/components` declared `^3.0.900`, locked `3.0.900` (resolved); `@cloudscape-design/collection-hooks` declared `^1.0.60`, locked `1.0.60` (resolved); `@cloudscape-design/global-styles` declared `^1.0.45`, locked `1.0.45` (resolved, not imported in this file). All fully resolved via the fixture's lockfile.

**Authority categories found in this corpus:** Component guidance (each component page has a separate "Usage" tab with Do/Don't general guidelines, Features, Writing guidelines, and Accessibility guidelines) and named patterns (e.g., "Table view" and "Filtering patterns" under Patterns → Resource management / General, each also with their own Do/Don't lists). Both a component tier and a composition/pattern tier exist in this corpus.

## Findings

### Finding 1: Table variant doesn't match either documented table-page composition for a few-column resource table

- **Finding:** The page renders its 4-column API-key table as the sole content of a `ContentLayout`, using `variant="borderless"`. Cloudscape's own "Table view" pattern explicitly branches on column count: content-heavy tables get the `"full-page"` variant with no `ContentLayout`; tables with only a few columns get a *bordered* table inside `ContentLayout`. This table has 4 columns — squarely in the "few columns" branch — but uses the borderless variant, which Cloudscape reserves for a table embedded among other content, not for a table that is a page's entire content.
- **Type:** documented composition
- **Materiality:** high
- **Confidence:** high
- **User task:** As stated above — a full-page view of the account's API keys.
- **Repository evidence:** `fixture/src/pages/ApiKeys.tsx` lines 37–81: the component returns `<ContentLayout header={...}><Table {...collectionProps} ... variant="borderless" ... /></ContentLayout>` with nothing else inside `ContentLayout`, and `columnDefinitions` has exactly 4 entries (`name`, `environment`, `status`, `createdAt`).
- **Authority evidence:**
  Primary — Cloudscape "Table view" pattern, General guidelines → Don't (`https://cloudscape.design/patterns/resource-management/view/table-view/`):
  > "Don't use the content layout component on this type of page. Instead, use the 'full-page' variant of the table component to implement this pattern."
  > "Don't use the table view pattern for tables that aren't overly content-heavy. Instead, if a table only has a few columns, use a bordered table inside the content layout component, with the default app layout content max-width."

  Corroborating — Table component, Usage → Features → Variant (`https://cloudscape.design/components/table/?tabId=usage`):
  > "Container — This table variant has its own visual container with shadows and borders. Use this variant to feature a table in a stand-alone container with its own hierarchy. For example: when using a table on a details page."
  > "Borderless — Use this variant to place a table inside a container with other content, such as key-value pairs. Use this variant to display a table without the shadows and borders surrounding a container. ... For example: when using a table in a dashboard item, expandable section, modal or within a split panel."
  > "Full page — This variant is for implementing the full page table view pattern. Use it for presenting and managing a table with many columns within a stand-alone page."

  Authority category: **named pattern** (primary Don't/Instead rule), corroborated by **component guidance** (variant definitions).
- **Evidence mode:** SYNTHESIS. The core prescriptive rule ("if a table only has a few columns, use a bordered table inside the content layout component") is a single VERBATIM Don't/Instead pairing from the named pattern page. Confirming that "a bordered table" refers to the documented `Container` variant, and that `Borderless` is documented for a different composition (table embedded among other content, not as sole page content), draws on the Table component's own variant definitions — a definitional cross-reference within the same design system's own docs, not a normative leap.
- **Applicability argument:**
  1. *Task match:* This page is exactly the shape the Table view pattern describes — "static data with multiple attributes displayed in a tabular format" as a page's entire content, with header, filter, and pagination as the only building blocks — not a superficially similar but different problem.
  2. *Current implementation solves the same problem:* Yes — it already lists/filters/paginates the same resource collection; nothing about the task changes.
  3. *Proposed alternative preserves the task:* Yes — changing `variant="borderless"` to `variant="container"` is a single prop value; it doesn't touch data, filtering, sorting, or pagination behavior.
  4. *Materiality:* The pattern page states this branch as an explicit Don't/Instead, not as one option among several equally valid ones. The current code takes the "keep ContentLayout" half of the few-columns branch (correct) but pairs it with the borderless chrome documented only for a table that shares a container with *other* content — a composition this page doesn't have, since the table is the page's only content. Neither of the two documented "shapes" (full-page-without-ContentLayout, or bordered-table-inside-ContentLayout) is what's implemented; the page is missing the border/shadow the docs assign to a standalone table.
- **Current expression:** `<Table variant="borderless" .../>` as the sole child of `<ContentLayout>`.
- **Native expression:** Keep `ContentLayout` (correct, given the table's few columns) and change the table to `variant="container"` (the bordered variant), matching the "Table view" pattern's explicit instruction for a few-column resource table.
- **Why it matters:** The current combination doesn't correspond to either of Cloudscape's two documented table-page compositions — it takes half of the "few columns" branch (ContentLayout) and half of a different, inapplicable composition's chrome (borderless, meant for a table sharing space with other content). A page built this way looks visually unbounded compared to how a Cloudscape-consistent app would present a comparable single-table resource page, and diverges from an explicit, named "Don't...Instead" instruction rather than a stylistic preference.
- **Boundary check:** This is a judgment about which of two documented, named table-page compositions matches this page's shape (few columns, table as sole content) — not a prop-deprecation or accessibility-mechanics defect on an otherwise-correct composition, and it isn't a generic aesthetic complaint since it's settled by an explicit pattern-level Don't/Instead pairing.

### Finding 2: First-column identifier is plain text, not a navigation link — resolution depends on missing detail-view intent

- **Finding:** The first table column (`name`) renders `item.name` as plain text. Cloudscape's Table guidance recommends the first column double as both the resource's unique identifier *and* the entry point to a details view. Nothing in this file establishes whether individual API keys have (or are meant to have) such a details view.
- **Type:** intent-dependent
- **Materiality:** medium
- **Confidence:** high (confidence that the surface genuinely doesn't resolve this — not confidence in a recommended direction)
- **User task:** As stated above.
- **Repository evidence:** `fixture/src/pages/ApiKeys.tsx` lines 50–55:
  ```
  {
    id: 'name',
    header: 'Name',
    cell: (item) => item.name,
    sortingField: 'name',
  },
  ```
  No `Link` import, no `onClick`/`navigate` call, and no row actions, item actions, or selection anywhere in the file — the table is entirely non-interactive beyond filter/sort/paginate.
- **Authority evidence:** Table component, Usage → General guidelines → Do → Columns (`https://cloudscape.design/components/table/?tabId=usage`):
  > "Use the first table column for unique identifiers of the items that are represented in the table (for example: name, id, and ARN). Also use the first table column for users to navigate to a details page that shows more information about the item."

  Also, Do → Cell: "Use the primary link variant instead of the secondary link variant in table cells to help users distinguish links from other text content in adjoining cells."
  Authority category: **component guidance**.
- **Evidence mode:** VERBATIM
- **Applicability argument:** The `name` value (e.g. `billing-key-01`) is exactly the sort of unique identifier the guidance names ("name, id, and ARN"), so that half of the guidance clearly applies. What's unresolved is the second half — whether this resource is individually addressable via a details page. Two plausible readings: (a) API keys are individually revisited resources — the `status: 'active' | 'revoked'` field implies a per-key lifecycle a user might want to inspect or act on individually, in which case the documented convention calls for a primary-variant `Link` in this column; (b) this table is a deliberately flat, terminal overview with no per-key drill-down planned, in which case plain text is already correct and there is no divergence. The bounded file supplies no evidence for either reading — no `Link` usage, no navigation handler, no per-row actions of any kind exist anywhere in the surface to signal that a details view exists or is intended.
- **Current expression:** Non-interactive text cell for `name`.
- **Native expression:** Uncertain, contingent on which reading applies; if (a), a primary-variant `Link` navigating to a per-key details view.
- **Why it matters:** If a details view for individual keys exists or is planned, this column diverges from the identifier-as-navigation convention used consistently across Cloudscape-built resource tables, producing an inconsistent entry point relative to the rest of a Cloudscape console. If no such view exists, there is no issue.
- **Boundary check:** This is about which documented column composition (identifier-as-link vs. identifier-as-text) matches the resource's addressability — not an accessibility or prop-mechanics defect on an already-correct choice, and it does not propose a different product goal than "view/manage API keys" under either reading.

### Finding 3: Single `TextFilter` vs. Collection select filter for two low-cardinality categorical columns — tied by Cloudscape's own criteria table

- **Finding:** The table filters on a resource with two low-cardinality categorical properties (`environment`: production/staging; `status`: active/revoked) using a single `TextFilter`. Cloudscape's "Filtering patterns" page provides a decision table for exactly this choice, and it ties Text filter and Collection select filter on this resource's complexity tier, differentiating them only by an unresolved user-behavior question.
- **Type:** intent-dependent
- **Materiality:** medium
- **Confidence:** high (confidence in the ambiguity itself, not in a direction)
- **User task:** As stated above.
- **Repository evidence:** `fixture/src/pages/ApiKeys.tsx` lines 28–35 (`useCollection` configured with only a `filtering` block, no `filteringProperties`) and lines 73–75 (`<TextFilter {...filterProps} filteringPlaceholder="Find API key" filteringAriaLabel="Filter API keys" />`). No `PropertyFilter` or `CollectionSelectFilter` import anywhere in the file.
- **Authority evidence:** Cloudscape "Filtering patterns" (`https://cloudscape.design/patterns/general/filter-patterns/`), full criteria table reproduced:

  | | Text filter | Collection select filter | Table property filter |
  |---|---|---|---|
  | Complexity of the resource | Simple resource (small set of properties) | Simple resource (small set of properties) | Complex resource (large set of properties) |
  | User goals | Find resources that match an exact text query | Find resources with overlapping, defined values | Find resources with multiple combinations of values |
  | Selection of values | – | Single selection of a value for each property | Multiple selection of values for each property |
  | Operators | – | "And" operator | "And", "Or", "Not", "And not" and "Or not" operators |

  And prose: "If users tend to know exactly the value or term they are looking for, use the text filter." / "If the common behavior of users is to filter a resource by only one or two properties, use the collection select filter. For example: by 'status' or 'type'." / "For complex products with large collection of resources, use the property filter so that users can combine multiple properties, values, and operators."
  Authority category: **named pattern** (decision table).
- **Evidence mode:** VERBATIM
- **Applicability argument:** Applying the anti-fundamentalism same-tier check: the "Complexity of the resource" row places Text filter and Collection select filter in the *same* tier ("Simple resource, small set of properties"). This resource has 4 displayed properties — unambiguously small — so Property filter's "large set of properties" tier is cleanly inapplicable here (ruled out, not merely a weaker alternative). Between Text filter and Collection select filter, however, the table's own "User goals" row differentiates them purely by user behavior ("if users tend to know exactly the value... " vs. "if the common behavior... is to filter by only one or two properties... by 'status' or 'type'"). That is a description of two different intents, not a stated direction — and this surface supplies no evidence resolving which applies: no comment, copy, telemetry, or code indicates whether users of this table typically type an exact key name, or want to slice the list by `environment`/`status`. The pattern's own worked example ("by 'status' or 'type'") is suggestively close to this resource's `status` field, but per the same-tier rule that proximity is not itself evidence of a direction.
- **Current expression:** A single `TextFilter` matching free text against the collection.
- **Native expression:** Uncertain — contingent on which user behavior predominates; either the current `TextFilter` is already correct, or a Collection select filter (letting users pick a defined `environment`/`status` value) would be more native. No confident recommendation is made.
- **Why it matters:** Named to flag what would need to be resolved (and by what evidence) rather than to assert a direction — Cloudscape's own decision table ties these two options on this resource's complexity tier, so picking one without surface-level evidence would be guessing, not applying documented guidance.
- **Boundary check:** This is a judgment between two documented, tied filtering compositions for this exact resource shape — not an implementation detail (both options are equally implementable and correct as components) and not a generic UX complaint, since it is grounded directly in the design system's own criteria table.

## Suppressed (low materiality or weak applicability)

- **Badge for the `environment` column:** Badge's own guidance ("Use badges for items that you want to label, categorize, or organize using text or numbers") could plausibly cover the 2-value `environment` field, but no citation states plain text is disfavored for categorical table values, and Badge's only explicit "Don't" ("Avoid using badges... to indicate status. Follow the guidelines for status indicator.") is about *not* using it for status — already correctly avoided here. Availability without applicability; suppressed as an equally-valid stylistic alternative.
- **Collection preferences (column visibility/order/sizing):** Table's Usage guidelines document Preferences as an optional feature, and the only "always provide preferences" condition is tied to defaults the app is imposing (e.g., a default sticky column). This 4-column table has no such defaults, so nothing in the docs forces exposing Preferences here. Suppressed as availability without applicability.
- **"Full-page" table variant as the fix for Finding 1 instead of the bordered/ContentLayout branch:** checked and ruled out — the Table view pattern's own Don't/Instead reserves `full-page` (with no `ContentLayout`) for content-heavy tables; a 4-column table doesn't meet that bar, so the bordered-table-inside-ContentLayout branch (Finding 1's recommendation) is the one that applies.

## Orientation notes

- `StatusIndicator` usage for `status` (`active` → `success`, `revoked` → `stopped`) matches Status indicator's documented type semantics (`https://cloudscape.design/components/status-indicator/?tabId=usage`: "Stopped/inactive — The resource, service, or process is no longer running, inactive, or severity is not relevant.").
- `Header`'s `counter={`(${API_KEYS.length})`}` is computed from the full, unfiltered collection size, matching Table's documented "always show the total number of items" / "only display the total number of items in the collection" convention rather than reflecting the filtered `items` count.
- Filtering, sorting, and pagination are enabled on a 16-item collection, consistent with Table's Do guidance to "only use filtering, pagination, and sorting if there are more than five items in the table."
- `ContentLayout` usage itself (rather than a bare full-page table with no `ContentLayout`) is the correct half of the Table view pattern's "few columns" branch for this 4-column table — only the table's `variant` prop is out of step with that same branch (see Finding 1).

## What was not evaluated

Implementation correctness — prop usage, `useCollection` configuration mechanics, TypeScript typing, deprecated APIs, and accessibility mechanics (e.g., `filteringAriaLabel` wording, ARIA labeling for sortable columns) — was not assessed. General UX/product judgment — whether "Manage API keys" as a task should include create/revoke/rotate actions, bulk selection, or a details/split-panel view at all — was not assessed as a product decision; only the two specific, directly citable alignment questions above (identifier-column convention, filter-mechanism convention) were reviewed.
