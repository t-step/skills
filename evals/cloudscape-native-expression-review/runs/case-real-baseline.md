# Baseline review: Identities.tsx

## Inferred user task

A single-service admin page for browsing the distinct IAM/SSO/federated callers ("principals") the Bedrock spend-guardrail meter has observed within a chosen lookback window (1 hour–30 days). Users scan the resulting table to identify a caller (by type, account, or SSO user), and from a given row either jump to creating a budget for that principal or open a per-principal activity/audit timeline. There is no create/edit/delete of identities themselves — this is a read-only, resource-identification and drill-in surface.

## Findings

### Finding 1: No filter control on a multi-property, potentially large table

**What it is:** The table has 8 candidate columns (principal, type, account, ARN, SSO user, first seen, last invoked, actions) and the `useCollection` hook is configured with `sorting` only — no `filtering`. Cloudscape's `Table` `filter` slot is never used; there is no `TextFilter`, `CollectionSelectFilter`, or `PropertyFilter` anywhere on the page. The only way to narrow results is the coarse 1-hour–30-day period `Select`.

**Evidence:** `pages/Identities.tsx` lines 80–87 (`useCollection<IdentityRow>(rows, { sorting: {...} })`, no `filtering` key) and lines 133–280 (the `<Table>` element has no `filter` prop).

**Cloudscape source:** `https://cloudscape.design/patterns/resource-management/view/table-view/` — building block F: *"Filter - optional: Text filter helps users with an extensive number of table rows to quickly find one or several resources with a matching query. The entire set of columns are used as a base for the filter."* Also `https://cloudscape.design/patterns/general/filter-patterns/`, whose selection criteria table maps filter choice to resource complexity: *"For complex products with large collection of resources, use the property filter so that users can combine multiple properties, values, and operators."* Type (6 known values), account, and SSO user are exactly the kind of discrete properties that pattern calls out for a collection-select or property filter, not just sorting.

**Why it matters:** A wildcard admin auditing many accounts (the code's own comments describe "multi-account installs" and "wildcard admins viewing many accounts") has no native way to isolate, e.g., `type = AgentService` or one account, and must instead scroll/sort a client-side list. This is a concrete gap against a documented, optional-but-expected building block for this exact pattern, not a generic UX complaint.

### Finding 2: Content-heavy table wrapped in `ContentLayout` with `variant="container"` instead of the `full-page` table variant

**What it is:** The page's entire content is this one table (`ContentLayout` → `Table variant="container"`), yet the table already needs `resizableColumns`, `stickyColumns={{first:1,last:1}}`, `wrapLines`, and `stickyHeader` to survive inside that container — the code's own comments (lines 139–142) explain these props exist because "the browser uses auto layout and long ARNs blow the table past the viewport."

**Evidence:** `pages/Identities.tsx` lines 109–148 (`<ContentLayout>` wrapping `<Table ... variant="container" resizableColumns ... stickyColumns={{ first: 1, last: 1 }}>`).

**Cloudscape source:** `https://cloudscape.design/patterns/resource-management/view/table-view/` — *"Don't use the content layout component on this type of page. Instead, use the 'full-page' variant of the table component to implement this pattern."* and the converse rule, *"Don't use the table view pattern for tables that aren't overly content-heavy. Instead, if a table only has a few columns, use a bordered table inside the content layout component."* An 8-column table with resizable/sticky/wrap-lines workarounds is squarely on the content-heavy side of that line.

**Why it matters:** The team is manually re-solving a viewport-overflow problem the `full-page` variant exists to solve for exactly this shape of page (single dedicated table, many columns). Adopting it is a more native fit than fighting the container's max-width with extra table props.

### Finding 3: Per-row Modal for activity drill-in where Split view/Split panel is the documented pattern

**What it is:** Clicking "Activity" on a row opens `PrincipalActivityModal`, a full `Modal` (`size="large"`) that fetches and renders that principal's activity timeline, replacing view of the underlying table while open.

**Evidence:** `pages/Identities.tsx` lines 267–274 (`Activity` button → `setActivityPrincipal(r.principal)`) and lines 281–287 (`<PrincipalActivityModal ...>`); `components/PrincipalActivityModal.tsx` lines 50–71 (`<Modal visible onDismiss={onDismiss} ... size="large">`).

**Cloudscape source:** `https://cloudscape.design/components/modal/` — *"It prevents interaction with the main page content, but keeps it visible with the modal as a child window in front of it."* `https://cloudscape.design/patterns/resource-management/view/split-view/` describes exactly this use case: *"Troubleshooting: Users need to quickly check or compare relevant resource details to troubleshoot an issue,"* and *"The split panel presents additional information about the selected resources... it opens automatically on resource selection"* — i.e., without blocking the table.

**Why it matters:** Investigating a principal's activity is inherently a look-then-go-back-to-the-table task (check one caller, then another). The modal forces a close/reopen cycle and blocks the table underneath for each check, whereas a selection-driven split panel keeps the table visible and scrollable while the activity timeline is shown, matching the documented troubleshooting use case more directly than a dialog interruption.

### Finding 4: No pagination on a table sized only by a 30-day lookback window

**What it is:** The table renders `collection.items` directly with no `Pagination` component and no `pagination` option passed to `useCollection`; the only volume control is the 1-hour–30-day period selector.

**Evidence:** `pages/Identities.tsx` lines 133–148 (no `pagination` prop on `<Table>`) and lines 80–87 (`useCollection` has no `pagination` key).

**Cloudscape source:** `https://cloudscape.design/patterns/resource-management/view/table-view/` — building block H: *"Pagination - optional: Pagination helps users with an extensive number of resources to navigate through them across multiple pages... Display the pagination even if the resources set fits in one page."*

**Why it matters:** At a 30-day window in an org with many callers (the page explicitly supports multi-account, wildcard-admin viewing), the unbounded row count is handled only by `stickyHeader` scroll. This is a secondary, lower-confidence finding relative to 1–3 since the pattern lists pagination as optional and the page could be a deliberate "compare everything" progressive-loading choice — but no such rationale is evidenced in the code or comments.
