# Baseline review: FleetNodes.tsx

## Inferred user task
Per the file's own header comment (lines 35-38): give an operator the canonical inventory of every fleet node, with health and utilization, so they can scan for unhealthy nodes or over/under-utilized capacity. The page is a single, standalone, content-heavy resource table with no other content.

## Findings

### 1. Container table inside ContentLayout instead of the full-page table pattern
**What/where:** Lines 59-68 wrap an 8-column `Table` (`variant="container"`) in `ContentLayout`, with `Header variant="h1"`.

**Cloudscape source:** `https://cloudscape.design/patterns/resource-management/view/table-view/index.html.md` ("Don't" section): *"Don't use the content layout component on this type of page. Instead, use the 'full-page' variant of the table component to implement this pattern."* And `https://cloudscape.design/components/table/index.html.md` (Variant feature): *"Full page — This variant is for implementing the full page table view pattern. Use it for presenting and managing a table with many columns within a stand-alone page... Use this variant in conjunction with the `contentType="table"` property on the App Layout to maximize the available space."* It also recommends pairing full-page with the sticky, size-reducing `awsui-h1-sticky` header variant.

**Why it matters:** The code's own framing ("Nothing on the page besides the table," 8 columns) is exactly the scenario the docs name for the `full-page` variant, not `container`+`ContentLayout`. The current combination is the specific anti-pattern the table-view guidance calls out, and it forfeits the extra width/height `contentType="table"` gives a dense, many-column operational table.

### 2. TextFilter used for three finite categorical properties instead of a structured filter
**What/where:** Lines 139-144 wire only a `TextFilter` against `status`, `region`, and `instanceType` — all closed, finite-valued fields (3, 3, and 3 distinct values respectively in the fixture data, lines 24-26).

**Cloudscape source:** `https://cloudscape.design/patterns/general/filter-patterns/index.html.md`: *"If the common behavior of users is to filter a resource by only one or two properties, use the collection select filter... For complex products with large collection of resources, use the property filter so that users can combine multiple properties, values, and operators."* And `https://cloudscape.design/components/property-filter/index.html.md` ("Do"): *"Use a property filter pattern if users need more than two properties to find a specific item. If only two are required, use the collection select filter instead,"* and *"Use multi-select tokens for properties with discrete values or finite sets of numeric values. For example, State = Active, Pending, Canceled..."*

**Why it matters:** The stated task is scanning for unhealthy nodes and capacity outliers — i.e., filtering by `status` (and plausibly `region`/`instanceType`) rather than free text. With three enumerable properties in play, the docs' own decision criteria point past the two-property-capped collection select filter to a `PropertyFilter`, which natively supports discrete-value tokens (e.g., `Status = unhealthy`) instead of relying on users typing exact substrings into a blind text box.

### 3. CollectionPreferences omits column display preferences on an 8-column table
**What/where:** Lines 147-170 configure only `pageSizePreference` and `wrapLinesPreference`; there is no `contentDisplayPreference`/`visibleContentPreference` despite 8 columns and `resizableColumns` already being enabled (line 71), signaling the columns don't comfortably fit.

**Cloudscape source:** `https://cloudscape.design/components/collection-preferences/index.html.md` (Features): *"Column display preferences (table) — Users can choose which columns to display in a table view,"* and the table-view pattern's Preferences building block lists, among the settings preferences should manage, *"Which columns are visible or set to hidden"* and *"Order of the columns displayed."*

**Why it matters:** For an operator-facing inventory table this wide, letting operators hide columns they don't need (e.g., `instanceType` or `launchedAt` when just triaging health) is the documented mechanism for this exact situation; today the preferences dialog only touches density and wrapping.

### 4. Actions column not made sticky
**What/where:** The `actions` column (lines 128-137) holds a single in-context "Console" link but has no `stickyColumns` configuration on the `Table` (lines 66-73).

**Cloudscape source:** `https://cloudscape.design/patterns/general/actions/incontext-actions/index.html.md`: *"Tables: Place these in the last column... To maintain the visibility of available actions in table rows we recommend enabling the sticky table column feature to maintain visibility of the available actions."*

**Why it matters:** With `resizableColumns` and 8 columns, horizontal scrolling is expected on typical viewports; without `stickyColumns={{ last: 1 }}`, the one action every row exposes can scroll out of view — the exact case this guidance addresses.

### 5. "Launched" column uses a locale absolute string instead of the documented timestamp pattern
**What/where:** Line 125: `cell: (item) => new Date(item.launchedAt).toLocaleString()`.

**Cloudscape source:** `https://cloudscape.design/patterns/general/timestamps/index.html.md`: *"Relative timestamps are easier for users to read, so we recommend them for most use cases,"* and, for accessibility of any relative timestamp shown: *"Wrap the relative timestamp in a `<time>` element and set the `datetime` attribute to the absolute human-readable timestamp... allows users to hover over the timestamp to access the absolute human-readable format."*

**Why it matters:** `toLocaleString()` produces a raw, locale-dependent absolute string with no relative framing and no `<time>`/title fallback — not the format or the accessibility affordance Cloudscape's own timestamp guidance specifies. For an operations table this column is used to judge node age at a glance, which is what relative time is documented to optimize for.

None found regarding: `StatusIndicator` usage (lines 90, 32-33) — correctly maps status to indicator type per its documented purpose; the single inline-link `Button` for the "Console" action (lines 132-136) — matches the in-context-actions guidance for one persistent, repetitive per-row action; and use of `ProgressBar` for CPU/memory cells was considered and rejected — its docs restrict it to operations with a known duration and completion state, not static utilization metrics, so the current plain-text percentage rendering is not a native-expression gap.
