# Cloudscape Native-Expression Review: QuotaRequests

**Inferred user task:** View the log of quota-increase requests filed against this account, scan them by quota/region/status/submission date, and select any one request to review its full field set (current/requested value, region, requester, submitted date, status) and, while it's still pending, withdraw it. The surface's own comment states nothing else in the app links to an individual request and there is no per-request route — this is a transient log entry a user reviews and acts on, not a persistently addressable resource with its own place in the information architecture.

**Cloudscape packages / versions:** `@cloudscape-design/components` 3.0.900 (resolved via `package-lock.json`; declared range `^3.0.900`, single locked version, no ambiguity).

## Findings
None.

## Suppressed (low materiality or weak applicability)
- **Split view (Table + Split panel) instead of Table + Modal for viewing a row's detail** — considered and suppressed. Split view's documented objectives (cloudscape.design/patterns/resource-management/view/split-view/) are resource identification *within a group of similar resources*, monitoring, and troubleshooting/comparison across multiple selected resources, with content required to be "selective... concise to minimize cognitive load." This surface's job is reviewing the complete field set of one already-identified request and optionally withdrawing it — not comparing or browsing among several. The pattern's own guidance ("A split view should never replace details pages... always use details pages to display full resource details of a single resource") argues against using split panel as a stand-in for full-record viewing, so it doesn't strictly resolve toward split view either. Applicability is weak on both the task-match and content-fit legs of the four-point test — suppressed rather than reported.
- **Details page instead of Modal for the request's full detail** — considered and suppressed. The Details page pattern (cloudscape.design/patterns/resource-management/details/details-page/) is for a resource with a permanent place in the app's navigation (breadcrumbs, page title, side navigation). The surface's own comment establishes there is no per-request route and nothing else links to an individual request; adopting a details page would mean inventing routing/IA this task doesn't have, which is a product-redesign move, not a native-expression correction — out of scope per the skill's own boundary.

## Orientation notes
- `Table` with `variant="full-page"` as the primary resource-collection surface for a flat log of requests — standard, native usage; no grouping/hierarchy or nested-resource structure that would call for a different table pattern.
- `Button variant="inline-link"` as the per-row "View" action, rather than a `Link` — correct given there is no URL to navigate to (no per-request route); the action opens a modal, so a non-navigating `Button` is the right primitive, consistent with the task's own constraint.
- `Modal` + `KeyValuePairs` for the full-record detail view, with a conditional footer action (`Withdraw request`) scoped to pending status — a legitimate, focused "review one item and optionally act on it" composition; the Table view pattern (cloudscape.design/patterns/resource-management/view/table-view/) explicitly leaves the detail-viewing mechanism open to the implementer rather than mandating split panel or a details page, so Modal is not a documented deviation.
- `StatusIndicator` mapping `pending`/`approved`/`denied` to `in-progress`/`success`/`error` — matches documented status-type semantics.

## What was not evaluated
Implementation correctness (API usage, prop mechanics, accessibility labeling details, hard-coded values) is `cloudscape-implementation-audit`'s domain and was not assessed here. General UX/product judgment was also out of scope, including whether an unconfirmed "Withdraw request" action inside a read-detail modal deserves its own confirmation step — that is a mechanics/UX question, not a component- or pattern-selection one, and is named here only so its absence doesn't read as "checked and fine."
