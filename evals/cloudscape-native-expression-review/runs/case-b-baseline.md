# Baseline review: EndpointScaling.tsx

## Inferred user task
Per the file's own comment (lines 29–33) and header description (line 40): an on-call operator needs to compare invocation volume, p99 latency, and error rate side by side across all 22 inference endpoints, to decide which one(s) require a capacity change ("Scale up").

## Findings

### 1. A columnar, sortable comparison task is expressed with the Cards pattern instead of the Table pattern
**Evidence:** Lines 46–85 render `ENDPOINTS` (22 items, line 17) through `<Cards>` with five per-item value sections (`status`, `region`, `invocations`, `latency`, `errorRate`), each a plain scalar — no imagery, no free-form content. The stated purpose (lines 29–33, 40) is explicitly to compare these values across all endpoints and rank by severity.

**Cloudscape source:** `https://cloudscape.design/patterns/resource-management/view/table-view/` — "Use table view pattern for static data with multiple attributes displayed in a tabular format." / "The best data type for a table view is data that is structured, easily comparable, and sortable." The card-view pattern's own "Related patterns" section (`https://cloudscape.design/patterns/resource-management/view/card-view/`) describes table view as: "effective for quickly identifying categories or comparing values in a large text and numerical data set" — and card view's "Do" guidance instead frames cards as for "non-columnar, yet comparable data," treated as "a quick reference."

**Why it matters:** The data here is exactly columnar and numeric (three independently comparable metrics per resource, 22 resources), which is the table-view pattern's documented target, not card-view's. Table also natively supports single- and multi-column sort — the docs give the directly analogous example "Sorting S3 objects by Storage Class then Size to identify cost optimization opportunities across tiers" — which would let the operator sort by error rate then latency to surface the worst endpoints first. Cards has no equivalent sort affordance, so today the operator must visually scan all 22 cards to rank them, contradicting the page's own stated purpose.

### 2. Collection is wrapped in `ContentLayout` instead of using the pattern's full-page variant
**Evidence:** Lines 1, 35–45: `ContentLayout` wraps `Header` and `Cards`; the `Cards` element (line 46) does not set `variant="full-page"`.

**Cloudscape source:** `https://cloudscape.design/patterns/resource-management/view/card-view/` (Don't): "Don't use the content layout component on this type of page. Instead, use the 'full-page' variant of the cards component to implement this pattern." (The table-view page states the identical rule for the table's full-page variant.)

**Why it matters: **This is an explicit, named anti-pattern for exactly this page archetype — a single collection of resources with a header counter and description (lines 37–43) and no other content. The full-page variant is documented to carry the page-level chrome (header integration, spacing) that this page is manually reconstructing via `ContentLayout`, which the docs call out by name as the wrong container for a resource collection page.

### 3. No text filter for what the pattern defines as an "extensive" resource set
**Evidence:** Lines 46–88: the `Cards` configuration has no filter/`TextFilter` companion; all 22 items (line 17) render at once with only responsive column count (`cardsPerRow`, line 86) — nothing to narrow by region or status.

**Cloudscape source:** `https://cloudscape.design/patterns/resource-management/view/card-view/` (Building blocks, Filter - optional): "Text filter helps users with an extensive number of table rows to quickly find one or several resources with a matching query." (Same wording appears in the table-view pattern's Filter building block.)

**Why it matters:** 22 endpoints spanning 4 regions and 3 status tiers is the scenario this building block targets. Without it, an operator who wants to isolate a specific region or the `degraded`/`overloaded` subset (the two states relevant to the page's own decision task) must manually scan the full card grid instead of using the pattern's documented filter mechanism.

### 4. No selection/bulk-action mechanism despite the header's plural framing
**Evidence:** Lines 76–83: each card exposes an individual `Button` ("Scale up") with no `selectionType` set on `Cards`. Header description (line 40) reads "...decide which **one(s)**..." — plural.

**Cloudscape source:** `https://cloudscape.design/patterns/resource-management/view/card-view/` (Building blocks, Selection - optional): "Cards can be selected individually or in bulk (multiple selection) by using the checkbox mechanism. Actions initiated after selection affect only the selected, visible cards."

**Why it matters:** The page's own copy anticipates that more than one endpoint may need the same corrective action in a single triage pass. The documented bulk-selection building block for this exact pattern exists to let an operator select several overloaded/degraded endpoints and issue one "Scale up" action, rather than clicking a separate button per card — a capability the current implementation forgoes entirely.
