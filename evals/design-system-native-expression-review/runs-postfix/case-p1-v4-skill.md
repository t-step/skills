# Design-System Native-Expression Review: Message Queues (`MessageQueues.tsx`)

**Design system:** Cloudscape (`@cloudscape-design/components`, `@cloudscape-design/collection-hooks`, `@cloudscape-design/global-styles`)

**Inferred user task:** An operator views every message queue in the account side by side to compare throughput (messages/second) and backlog age (oldest message age) across all of them at once, in order to decide which queues need scaling attention right now. While triaging, the operator can search for a queue by name, or narrow the list down to queues in a specific status (healthy/backlogged) or region (us-east-1/us-west-2). This is stated almost verbatim in the surface's own code comment (`src/pages/MessageQueues.tsx:29-33`) and matches the `Header` description prop ("Compare message throughput and backlog age across queues to decide which need scaling attention.").

**Packages / versions:** Resolved via `scripts/resolve_versions.py` against the fixture's `package-lock.json`:
- `@cloudscape-design/components`: declared `^3.0.900`, locked `3.0.900`
- `@cloudscape-design/collection-hooks`: declared `^1.0.60`, locked `1.0.60`
- `@cloudscape-design/global-styles`: declared `^1.0.45`, locked `1.0.45`

**Authority categories found in this corpus:** Cloudscape's `llms.txt` index exposes both a component-guidance tier (`/components/*`, each with a "General guidelines" Do/Don't list, features, and API) and a named task/pattern tier (`/patterns/*`), including explicit decision-criteria tables comparing sibling components for the same job (e.g. "Choosing between table view and card view," and the three-way text/collection-select/property filter comparison in "Filtering patterns"). Both tiers were used below.

## Findings

### Finding 1: 24 shared-metadata, numeric/status queues are rendered as `Cards` where Cloudscape's own decision criteria for this exact profile point to `Table`

- **Type:** `combined selection + composition`
- **Materiality:** `high`
- **Confidence:** `high`
- **User task:** As stated above — comparing throughput and backlog age across all 24 queues to decide which need scaling attention.
- **Repository evidence:** `src/pages/MessageQueues.tsx:34-101`. `useCollection<MessageQueue>(QUEUES, { pagination: { pageSize: 12 }, sorting: {} })` feeds a `Cards` component (`cardsPerRow`, four `cardDefinition.sections`: status via `StatusIndicator`, region, `messagesPerSecond`, `oldestMessageAgeSec`) wrapped in `ContentLayout`. `QUEUES` (line 18) is a fixed array of 24 items; every item carries the identical four fields — no item has metadata another item lacks. Notably, `sorting: {}` is passed to `useCollection` but nothing in the `Cards` composition consumes a sort column or exposes sorting in the UI — `Cards` has no per-column sort affordance to attach it to.
- **Authority evidence:** Cloudscape's "View resources" pattern page (`/patterns/resource-management/view/index.html.md`) gives this decision table for choosing between table view and card view, reproduced in full:

  |  | Table view | Card view |
  | --- | --- | --- |
  | Number of resources in the data set | 9 or more resources in 99% of use cases | 5 or less resources in 99% of use cases |
  | Metadata* being displayed | Shared metadata between resources | Different metadata across resources (different types of databases with different data) |
  | Metadata type | Data that is displayed in columns (text, numerical, status, sparkline) | Data that can be displayed as visuals (charts, videos) |

  (* "The configuration details of a resource. Example: 'date created.'")

  Supporting prose from the same page: "Use a table if the resources share the same metadata, and your users will be comparing resources to determine which to take action on. Use the card view if users will not be comparing between a large number of resources to determine which to take action on." The Card view pattern page's own "Do" list states: "Use cards to display non-columnar, yet comparable data." The Table view pattern page's own "Do" list states: "Use table view pattern for static data with multiple attributes displayed in a tabular format. The best data type for a table view is data that is structured, easily comparable, and sortable," and its "Don't" list adds: "Don't use the table view pattern for tables that aren't overly content-heavy. Instead, if a table only has a few columns, use a bordered table inside the content layout component, with the default app layout content max-width."

  Authority category: **named pattern**.
- **Evidence mode:** `VERBATIM` (table and quotes reproduced above, checked against the fetched page text).
- **Applicability argument:** All three rows of the decision table independently point the same direction for this surface, with no same-tier ("use either") row to reconcile: (1) 24 resources is well above the "9 or more" table-view threshold and far above the "5 or less" card-view threshold; (2) every queue carries the identical four fields (status, region, throughput, oldest-message-age) — "shared metadata between resources," the table-view criterion, not "different metadata across resources"; (3) all four displayed values are text/numeric/status — "data that is displayed in columns," the table-view criterion — none are the charts/images/video that would justify cards. The surface's own stated task ("compare... across all of them at once... decide which need scaling attention") is exactly the "users will be comparing resources to determine which to take action on" scenario the table-view guidance names. Because the table only has four columns, the applicable alternative is specifically a bordered `Table` inside the existing `ContentLayout` (per the Table view page's own "Don't" clause above), not the full-page/side-nav "table view" pattern shell — so this recommendation preserves the surface's existing page structure, changing only the collection-view component.
- **Current expression:** `Cards` with `cardsPerRow` breakpoints and four `cardDefinition.sections`, no sorting exposed despite `useCollection`'s `sorting: {}` config being present.
- **Native expression:** A bordered `Table` (default variant, not full-page) inside the same `ContentLayout`/`Header`, with `columnDefinitions` for name, status (`StatusIndicator`, unchanged), region, throughput, and oldest-message-age, with the throughput and oldest-message-age columns made sortable — finally giving the already-declared `useCollection` `sorting` config somewhere to attach.
- **Why it matters:** A comparison/triage task across a large, shared-metadata, all-numeric/status data set is precisely the profile Cloudscape's own decision table assigns to `Table`, not `Cards`, on every axis it measures. Concretely, `Cards` has no per-column sort mechanism, so an operator cannot rank the 24 queues by throughput or by backlog age — the two values the task exists to compare — without scanning by eye across three rows of cards; a `Table` gives that ranking natively via sortable columns, which is exactly the capability the surface's dead `sorting: {}` config was reaching for.
- **Boundary check:** This is a judgment about which collection-view component and interaction structure natively serves a numeric cross-item comparison task, not about `Cards`' API correctness or a generic "cards feel busy" aesthetic complaint.

### Finding 2: Triage by "a specific status or region" is a stated user goal with no discrete filter component, only free-text `TextFilter`

- **Type:** `combined selection + composition`
- **Materiality:** `high`
- **Confidence:** `medium`
- **User task:** Same as above; specifically the stated sub-goal "narrow the list down to a specific status or region while triaging," alongside "search by queue name."
- **Repository evidence:** `src/pages/MessageQueues.tsx:89-95` wires only `TextFilter` (`filterProps` from `useCollection`) as the collection's filter. `status` has exactly two finite values (`'healthy' | 'backlogged'`), `region` has exactly two (`'us-east-1' | 'us-west-2'`) (lines 12-13). There is no `CollectionPreferences`, `PropertyFilter`, or select-based filter anywhere in the file.
- **Authority evidence:** Cloudscape's "Filtering patterns" page (`/patterns/general/filter-patterns/index.html.md`) gives this decision table, reproduced in full:

  |  | Text filter | Collection select filter | Table property filter |
  | --- | --- | --- | --- |
  | Complexity of the resource | Simple resource (small set of properties) | Simple resource (small set of properties) | Complex resource (large set of properties) |
  | User goals | Find resources that match an exact text query | Find resources with overlapping, defined values | Find resources with multiple combinations of values |
  | Selection of values | - | Single selection of a value for each property | Multiple selection of values for each property |
  | Operators | - | "And" operator | "And", "Or", "Not", "And not" and "Or not" operators |

  Same page, prose: "If the common behavior of users is to filter a resource by only one or two properties, use the collection select filter. For example: by 'status' or 'type'." The Collection select filter component page's own "Do" list states: "Use a select filter if users need a maximum of two properties to find a specific item. If more than two are required, use a property filter instead," with a worked example naming "Property: Status; Values: Error, Loading, Pending, Stopped, and Success," and the "Collection view" section describes the filter working "as soon as the user selects a value from a select filter or enters text into the accompanying text filter" — i.e., the two are a documented combination, not exclusive alternatives.

  Authority category: **named pattern** (Filtering patterns decision table) + **component guidance** (Collection select filter page).
- **Evidence mode:** `SYNTHESIS` (the recommendation bridges the pattern-tier decision table, the Collection select filter component page's own guidance/example, and the surface's own code comment — see below).
- **Applicability argument:** The "Complexity of the resource" row of the filtering-patterns table places Text filter and Collection select filter in the **same tier** ("Simple resource (small set of properties)" for both) — per this skill's anti-fundamentalism rule, that tie is not by itself evidence that Collection select filter should replace or supplement Text filter here; the differentiating "User goals" row ("exact text query" vs. "overlapping, defined values") only describes two different user intents, not a directional preference. What resolves the tie is the surface's own copy: the code comment names *both* intents explicitly and separately — "search by queue name" (an exact-text-query goal, matching Text filter) *and* "narrow the list down to a specific status or region" (an overlapping/defined-value goal over exactly two finite-valued properties, matching Collection select filter's own stated ceiling of "a maximum of two properties," with "status" as the component page's own worked example). Because the surface itself supplies evidence resolving which intent applies — both, for different fields — the finding stands: it is not that Text filter is wrong, it is that a second, documented filter component is needed for the second stated goal that Text filter's own definition ("match an exact text query") doesn't cover. `PropertyFilter` was considered and is not the better fit — the resource is a "simple resource (small set of properties)" per the same table, which is the Text-filter/Collection-select-filter tier, not the "complex resource (large set of properties)" tier `PropertyFilter` targets.
- **Current expression:** A single `TextFilter` bound to `useCollection`'s `filterProps`, matching against the full item text (including status/region strings) only as an incidental side effect of free-text substring matching.
- **Native expression:** Keep `TextFilter` for the name-search goal, and add a `CollectionSelectFilter` (up to two properties, per the component's own stated ceiling) for status and region, composed alongside it exactly as the Collection select filter page's own "Collection view" behavior describes — filtered "as soon as the user selects a value from a select filter or enters text into the accompanying text filter."
- **Why it matters:** As implemented, "narrow the list down to a specific status or region" is only reachable by an operator typing the literal string `"healthy"`, `"backlogged"`, `"us-east-1"`, or `"us-west-2"` into a free-text box with no discoverable affordance that those are the valid values — the surface has no UI element that names or exposes the finite value sets at all. Cloudscape's own component page names exactly this shape (two finite-valued properties, "status" as the literal example) as the case `CollectionSelectFilter` exists to serve natively.
- **Boundary check:** This is a component-selection judgment about which documented filter component matches a second, explicitly-stated user goal (narrowing by a finite property) that the chosen component's own definition doesn't cover — not a critique of `TextFilter`'s prop usage or a generic "add more filters" UX preference.

## Suppressed (low materiality or weak applicability)

- **`PropertyFilter` instead of `CollectionSelectFilter`** — considered for Finding 2. Suppressed: the Filtering patterns table places this resource in the "simple resource (small set of properties)" tier for both `TextFilter` and `CollectionSelectFilter`, not the "complex resource (large set of properties)" tier `PropertyFilter` targets; with two properties and two values each, `PropertyFilter`'s combinable-operator machinery (`and`/`or`/`not`) has no applicability here.
- **Split view (collection + `SplitPanel`)** — considered given the "decide which need scaling attention" phrasing might imply per-queue drill-down. Suppressed: the pattern's own guidance is explicit that split view is only an optional extension "when your users go through workflows such as monitoring or troubleshooting, which often require an additional layer of details," and "don't use a split view when standard table/card view with separate details page meets your user's need." Nothing in this bounded surface (no per-item route, link, or detail affordance) evidences that need — reporting it would be inventing intent the code doesn't support, not naming an `intent-dependent` candidate worth surfacing.

## Orientation notes

- `ContentLayout` + `Header` (`variant="h1"`, `counter`, `description`) is the correct, native page-structure choice for this bounded surface, and — once the Cards→Table change above is made — remains correct: the Table view pattern's own "Don't" guidance directs tables with only a few columns to stay inside `ContentLayout` rather than adopting the full-page/side-nav "table view" pattern shell, which is exactly this surface's existing structure.
- `StatusIndicator` for the `status` field is the component's documented purpose verbatim ("A status indicator communicates the state of a resource... in a compact form that is easily embedded in a card, table, list, or header view") and is correct regardless of whether the collection view is `Cards` or `Table`.
- `Pagination` with `pageSize: 12` against 24 items is used correctly per the pattern guidance to "Display the pagination even if the resources set fits in one page" — no change needed here.
- `TextFilter` itself (as one of two filter components, see Finding 2) is a valid, documented choice for the name-search goal; the finding is additive, not a replacement.

## What was not evaluated

Implementation correctness — `Cards`/`Table`/`TextFilter`/`Pagination` prop usage and API shape, the mock-data generation logic for `QUEUES`, whether `messagesPerSecond`/`oldestMessageAgeSec` should be formatted through a units/number-formatting utility, and app-owned accessibility mechanics (e.g. `ariaLabels` completeness) — was not assessed. General UX judgment (density, color choices, whether 12 is the right page size, whether the page needs a details/drill-down route beyond what's already discussed under "Suppressed") was likewise out of scope for this review.
