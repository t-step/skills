# Design-System Native-Expression Review: MessageQueues.tsx

**Design system:** Cloudscape (`@cloudscape-design/components`, `@cloudscape-design/collection-hooks`, `@cloudscape-design/global-styles`)

**Inferred user task:** An operator-facing page that lists every message queue in the account (24 total) so the operator can compare throughput and backlog age across all of them at once and decide which need scaling attention right now. Secondary interactions: search by queue name, or narrow the list to a specific status or region while triaging. (Source: the `Header` `description` prop and the surrounding code comment in `MessageQueues.tsx`, lines 29-33 and 50.)

**Packages / versions:** Resolved from `fixture/package.json` + `fixture/package-lock.json`: `@cloudscape-design/components` declared `^3.0.900`, locked `3.0.900`; `@cloudscape-design/collection-hooks` declared `^1.0.60`, locked `1.0.60`; `@cloudscape-design/global-styles` declared `^1.0.45`, locked `1.0.45` (declared but not imported in this file).

**Authority categories found in this corpus:** Component guidance (`/components/...`, e.g. Cards, Content layout, Text filter, Collection select filter, Property filter, Status indicator) and named patterns (`/patterns/...`, e.g. View resources, Table view, Card view, Filtering patterns). Several pattern pages in this corpus double as explicit fit-tier/decision-criteria tables (a "Choosing between table view and card view" table, a filtering-patterns comparison table) rather than being purely illustrative — that table-based decision layer is treated as authoritative below, not as an example. No separate "composition guide" tier distinct from these pattern pages was found.

## Findings

### Finding 1: Cards + ContentLayout used for a task that Cloudscape's own criteria route to the full-page Table view pattern

- **Type:** combined selection + composition
- **Materiality:** high
- **Confidence:** high
- **User task:** Operators compare throughput and backlog age across all 24 message queues at once to decide which need scaling attention (stated verbatim in the `Header` `description`).
- **Repository evidence:** `MessageQueues.tsx` lines 44-101: the entire page is `<ContentLayout header={<Header variant="h1" counter={...} description="Compare message throughput and backlog age across queues to decide which need scaling attention.">Message queues</Header>}>` wrapping a single `<Cards ... cardsPerRow={[{cards:1},{minWidth:500,cards:2},{minWidth:992,cards:3}]} />`. The 24 synthetic items (`QUEUES`, lines 18-25) share an identical schema — `status` (2 discrete values), `region` (2 discrete values), `messagesPerSecond` (number), `oldestMessageAgeSec` (number) — and each card section (lines 63-87) renders a bare text value, a number, or a `StatusIndicator`; there is no per-item imagery or rich/heterogeneous content.
- **Authority evidence:**
  - "Choosing between table view and card view" (`patterns/resource-management/view/index.html.md`), reproduced in full:

    |  | Table view | Card view |
    | --- | --- | --- |
    | Number of resources in the data set | 9 or more resources in 99% of use cases | 5 or less resources in 99% of use cases |
    | Metadata* being displayed | Shared metadata between resources | Different metadata across resources (different types of databases with different data) |
    | Metadata type | Data that is displayed in columns (text, numerical, status, sparkline) | Data that can be displayed as visuals (charts, videos) |

    Plus the accompanying prose: "Use a table if the resources share the same metadata, and your users will be comparing resources to determine which to take action on. Use the card view if users will not be comparing between a large number of resources to determine which to take action on."
  - Table view pattern, "Don't": "Don't use the content layout component on this type of page. Instead, use the 'full-page' variant of the table component to implement this pattern." (`patterns/resource-management/view/table-view/index.html.md`)
  - Card view pattern, "Don't" (same rule, shown for symmetry — this constraint is not specific to whichever collection component is chosen): "Don't use the content layout component on this type of page. Instead, use the 'full-page' variant of the cards component to implement this pattern." (`patterns/resource-management/view/card-view/index.html.md`)
  - Content layout component, "Don't": "Don't use the content layout component for productive use cases such as resources creation, view, edit, and delete." (`components/content-layout/index.html.md`) — the linked "view" target is the same View resources pattern page quoted above.
  - Authority category: named pattern (View resources / Table view / Card view decision table and prose) + component guidance (Content layout "Don't").
- **Evidence mode:** SYNTHESIS — the recommendation bridges the View-resources decision table (which component fits this data shape) with three independently-stated "Don't use Content layout here" rules from three different pages (Table view, Card view, and Content layout itself). Each individual quoted sentence is VERBATIM against the fetched source text; the combination into one applicability judgment is the reviewer's synthesis.
- **Applicability argument:** (1) The stated task — "Compare message throughput and backlog age across queues to decide which need scaling attention" — is essentially a restatement of the doc's own Table-selection criterion: "your users will be comparing resources to determine which to take action on." (2) The current Cards-based implementation already delivers a working comparison/triage view, so this is a component/shell-choice problem, not an unaddressed task. (3) Switching to a full-page Table with the same four data columns preserves the identical comparison task; nothing about the user goal changes. (4) All three rows of the decision table point the same direction (24 ≥ 9 resources, shared metadata across all queues, purely columnar data types: status/region/two numbers, no images or charts) — there is no equalizing row favoring Card view for this data shape — and the Content-layout prohibition is stated three separate times for this exact page category, which rules out "this is just an example," not a stated rule.
- **Current expression:** `ContentLayout` (with an `h1` `Header`) wrapping a `Cards` component (up to 3 cards per row, one section per field).
- **Native expression:** A full-page `Table` (the "full-page" `variant`, per the Table view pattern's building blocks) with `status`, `region`, `messagesPerSecond`, and `oldestMessageAgeSec` as columns — enabling column sort, which this comparison-across-queues task can use directly — composed as the page's own structural header rather than nested inside `ContentLayout`.
- **Why it matters:** With 24 shared-schema, purely columnar resources, the comparison this page exists for is exactly what Cloudscape states Table is optimized for ("data that can fit into data cells, and can be sorted and compared"), while Cards are optimized for "non-columnar data, like charts or images" — neither of which this page has. Staying with Cards also forgoes column sorting for a task framed entirely around comparing values to decide what needs attention, and the `ContentLayout` shell is a documented anti-pattern for this page category independent of which collection component is chosen.
- **Boundary check:** This is a documented composition/component-selection judgment — which collection pattern and page shell Cloudscape's own criteria assign to this exact data shape and task — not an implementation-correctness defect or a generic UX opinion; it is grounded in a fit-tier decision table and three explicit "Don't" rules.

### Finding 2: No dedicated control for the page's own stated "narrow by status or region" task; TextFilter alone doesn't natively cover it

- **Type:** combined selection + composition
- **Materiality:** medium
- **Confidence:** high
- **User task:** "Operators can search by queue name, or narrow the list down to a specific status or region while triaging" (verbatim from the code comment, `MessageQueues.tsx` lines 29-33).
- **Repository evidence:** `status: 'healthy' | 'backlogged'` and `region: 'us-east-1' | 'us-west-2'` (lines 12-13) — two finite, 2-valued properties. The only filter control rendered is `<TextFilter {...filterProps} filteringPlaceholder="Find message queue" filteringAriaLabel="Filter message queues" />` (lines 89-95); `useCollection`'s `filtering` config only supplies `empty`/`noMatch` copy (lines 36-39) — no property-scoped filtering is wired up anywhere in the file.
- **Authority evidence:**
  - Filtering patterns criteria table (`patterns/general/filter-patterns/index.html.md`), reproduced in full:

    |  | Text filter | Collection select filter | Table property filter |
    | --- | --- | --- | --- |
    | Complexity of the resource | Simple resource (small set of properties) | Simple resource (small set of properties) | Complex resource (large set of properties) |
    | User goals | Find resources that match an exact text query | Find resources with overlapping, defined values | Find resources with multiple combinations of values |
    | Selection of values | - | Single selection of a value for each property | Multiple selection of values for each property |
    | Operators | - | "And" operator | "And", "Or", "Not", "And not" and "Or not" operators |

    Plus: "If the common behavior of users is to filter a resource by only one or two properties, use the collection select filter. For example: by 'status' or 'type'."
  - Collection select filter, "Do": "Use a select filter if users need a maximum of two properties to find a specific item. If more than two are required, use a property filter instead." (`components/collection-select-filter/index.html.md`)
  - Property filter, "Do": "Use a property filter pattern if users need more than two properties to find a specific item. If only two are required, use the collection select filter instead." (`components/property-filter/index.html.md`)
  - Collection select filter, "Displaying results": "The collection is filtered as soon as the user selects a value from a select filter or enters text into the accompanying text filter." (`components/collection-select-filter/index.html.md`) — documents Text filter and Collection select filter coexisting, which is the composition proposed here.
  - Authority category: named pattern (Filtering patterns table) + component guidance (Collection select filter / Property filter "Do" rules, converging from both directions).
- **Evidence mode:** SYNTHESIS — no single page states "use Collection select filter for a status+region queue-narrowing task" verbatim; the claim bridges the Filtering-patterns table with two independent component pages that state the identical 2-property threshold rule pointing the same direction.
- **Applicability argument:** (1) The task is not inferred — the code's own comment names it explicitly ("narrow the list down to a specific status or region"). (2) Today that need is only reachable as a side effect of `TextFilter`'s whole-item substring match (typing "healthy" or "us-east-1"), not through the documented mechanism for finite-property narrowing. (3) Adding a select-based filter for `status`/`region` preserves the same task and is additive — `TextFilter` stays for name search, exactly as the Collection select filter's own "Displaying results" section documents the two coexisting. (4) Same-tier check: the "Complexity of the resource" row places Text filter and Collection select filter in the *same* tier ("Simple resource"), so complexity alone does not differentiate them — reproduced above in full, not just the differentiating rows. But the table's other three rows (User goals, Selection of values, Operators) do differentiate directionally toward Collection select filter for a defined-value, two-property narrowing goal, and two independent component pages each state the same 2-property threshold rule for this exact case — this is evidence within the same retrieved corpus for this candidate, not an unrelated separate citation overriding the tied row.
- **Current expression:** a single `TextFilter` bound to `useCollection`'s default whole-item text matching; no property-scoped filter control exists for `status` or `region`.
- **Native expression:** Keep `TextFilter` for name search, and add a select-based filter (Cloudscape's Collection select filter) for `status` and `region`, composed alongside the text filter as documented.
- **Why it matters:** A user cannot reliably discover or invoke "show only backlogged queues" through a text box labeled "Find message queue" — Cloudscape explicitly reserves this exact two-property, finite-value scenario for a different, purpose-built filter component, converging from both the Collection select filter and Property filter pages.
- **Boundary check:** This is about which documented filtering component/composition matches a task the surface's own comment states, not a generic "add more filters" UX opinion, and not an implementation defect in the existing `TextFilter`.

## Suppressed (low materiality or weak applicability)

- **Property filter as the filtering upgrade for status/region.** Considered and rejected, not merely lower-priority: Property filter's own "Do" guidance states "If only two are required, use the collection select filter instead," and the Filtering-patterns table places Property filter in the "Complex resource (large set of properties)" tier, while this resource has exactly two filterable, finite-valued properties (`status`, `region`). Property filter is the more powerful and far more heavily documented component (the most natural "obvious" reach), which is exactly why it needed to be checked against the corpus's own stated threshold rather than assumed — and that threshold rules it out for this specific task in favor of Collection select filter (Finding 2).

## Orientation notes

- `StatusIndicator` for the `status` field is correct, native usage — it matches the component's documented purpose ("communicates the state of a resource ... in a compact form that is easily embedded in a card, table, list, or header view").
- `useCollection` + `Pagination` + `trackBy="id"` for client-side filtering/pagination/sorting matches the Cards component's own dev guidance for "Cards with client-side operations ... implemented using collection hooks."
- `ariaLabels={{ cardsLabel: 'Message queues' }}` on `Cards` follows the accessibility guidance to provide alternative text for the collection.
- Pagination is shown even though pagination is one of the things flagged for restructuring in Finding 1; the presence of pagination itself (rather than, say, infinite scroll) is correct per both the Table view and Card view patterns' own "Pagination" building block.

## What was not evaluated

Implementation correctness — deprecated props, prop-level API usage, hard-coded values, `trackBy`/`ariaLabels` wiring mechanics, or app-owned accessibility implementation on already-correctly-chosen components — was not assessed. General UX or product judgment (information density, copy quality, whether 12-per-page pagination is the right size, visual hierarchy) was also not assessed; only which Cloudscape-documented component/composition choice best expresses the stated task was in scope.
