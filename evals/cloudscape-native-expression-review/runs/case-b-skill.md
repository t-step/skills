# Cloudscape Native-Expression Review: EndpointScaling (fleet cards)

**Inferred user task:** An on-call operator reviewing every inference endpoint in the fleet (22 endpoints, mixed regions) to compare invocation volume, p99 latency, and error rate side by side, in order to decide which endpoint(s) need a capacity ("Scale up") change. The page header states this explicitly: "Compare request volume, latency, and error rate across endpoints to decide which ones need to scale."

**Cloudscape packages / versions:** `@cloudscape-design/components` resolved to locked version `3.0.900` (declared range `^3.0.900`, `package-lock.json` in the fixture root).

## Findings

### Finding 1: Fleet comparison/scaling-decision task expressed as Cards instead of Table

- **Type:** combined component + pattern
- **Materiality:** high
- **Confidence:** high
- **User task:** see above — a multi-attribute, quantitative comparison across a fleet of same-shaped resources to make a scaling decision, not a glance-and-browse task.
- **Repository evidence:** `src/pages/EndpointScaling.tsx` renders all 22 `ENDPOINTS` through `<Cards>` (lines 46-88), one card per endpoint, with five stacked `sections` per card (`status`, `region`, `invocations`, `latency`, `errorRate`) plus a `Scale up` `<Button>`. No `sortingField`, no sort control, no `filter`, no `pagination`, and no `preferences` slot are present anywhere in the file — `inspect_surface.py` confirms the only Cloudscape imports are `ContentLayout`, `Header`, `Cards`, `StatusIndicator`, `Button`, `Box` (one JSX use each).
- **Cloudscape evidence:**
  - Table view pattern (`/patterns/resource-management/view/table-view/`): "Use table view pattern for static data with multiple attributes displayed in a tabular format. The best data type for a table view is data that is structured, easily comparable, and sortable."
  - Card view pattern (`/patterns/resource-management/view/card-view/`): "[Card view is] effective for glancing at small sets of similar resources with text, numerical, and imagery data sets" and "Use cards to display non-columnar, yet comparable data."
  - Table component usage guide (`/components/table/`, Cell section): "Right-align quantitative numeric data within table cells to make them easier to compare and contrast... This consistency helps users to quickly scan lists and compare values."
  - Table component usage guide, Multi-column sort: "useful when users need to analyze multi-dimensional data. For example: Grouping by instance type, then rank by highest CPU within each type to find over-provisioned instances" — a near-identical decision task to "which endpoint(s) need to scale."
  - Cards component usage guide (`/components/cards/`) lists Cards' only collection features as Filtering, Pagination, and Preferences — no sorting feature exists for Cards at all.
- **Applicability argument:** (1) The observed task — ranking/comparing 22 same-shaped resources across three quantitative metrics to pick which need action — matches Table view's stated problem ("comparing values in a large text and numerical data set," "structured, easily comparable, and sortable") much more closely than Card view's stated problem (glancing at a small set, with imagery in the mix — there is no imagery here, and 22 is not "small"). (2) The current Cards composition attempts the same comparison job but can only present the metrics as stacked, left-aligned text per card; it has no sort feature of any kind, so a user cannot rank endpoints by latency or error rate — the exact operation the stated task requires. (3) A Table with the same five columns and the same "Scale up" in-context row action preserves the identical task and data. (4) This is a structural gap, not a style preference: Table's multi-column sort is documented for literally this class of problem ("rank by highest CPU... to find over-provisioned instances"), and Cards has no comparable mechanism — an experienced Cloudscape implementer would restructure this to Table rather than treat Cards as an equally-valid alternative.
- **Current expression:** `Cards` with one card per endpoint, sections stacked vertically, no sorting/filtering/pagination.
- **Native expression:** A full-page `Table` (per the Table view pattern) with columns for status, region, invocations/min, p99 latency, and error rate — right-aligned for the three quantitative columns — single- or multi-column sortable, with the `Scale up` button as an in-context row action. This is the same data, same action, same task, expressed the way Cloudscape's own comparison-oriented component is documented to be used.
- **Why it matters:** The stated task is a ranking/triage decision across three quantitative metrics on 22 items. Cards cannot sort at all, so the operator must eyeball 22 stacked cards to find outliers; Table's sortable, right-aligned columns are the documented mechanism for exactly this kind of scan-and-compare decision. This is also supported indirectly: Cards' own usage guide says to add filtering and pagination once a collection exceeds five items, and this 22-item collection has neither — a sign the composition has already outgrown what Cards is set up to do well, independent of the Table comparison.
- **Boundary check:** This is a component/pattern alignment judgment (which Cloudscape collection component and which documented view pattern fits a comparison/ranking task), not an implementation-correctness or general-UX critique — no props are misused and no aesthetic complaint is being made.

## Suppressed (low materiality or weak applicability)

- **ContentLayout wrapping vs. the pattern's "full-page" variant building block.** Both the Table view and Card view pattern pages say "Don't use the content layout component on this type of page. Instead, use the 'full-page' variant" of the respective component. The current file wraps `Cards` in `ContentLayout` rather than using `variant="full-page"`. Suppressed because this single-file surface doesn't show whether `EndpointScaling` is meant to be the canonical, standalone top-level "view resources" page (where the full-page building blocks would apply) or a lighter page embedded within a larger content area (where `ContentLayout` + a container-variant collection is ordinary, valid Cloudscape composition) — that surrounding-app-shell context isn't available, and the effect is secondary to Finding 1.

## Orientation notes

- `StatusIndicator` is used to render endpoint health (`healthy`/`degraded`/`overloaded`) — matches Cards' guidance to "use icons in cards only to show status."
- `Header` is configured with `variant="h1"` and an item counter (`(${ENDPOINTS.length})`) — correct usage for a collection view's title/counter convention.
- `Button` is the correct primitive for the "Scale up" in-context action regardless of which collection component hosts it (Table or Cards both document button-based in-context row/card actions the same way).

## What was not evaluated

Implementation correctness — e.g., `Box float="right"` as the action-alignment mechanism, absence of `ariaLabels`/keyboard-navigation props, hard-coded numeric formatting — is `cloudscape-implementation-audit`'s domain and was not assessed here. General UX judgment (whether these are the right five metrics to show, whether 22 endpoints is the right scope for one view, visual density, color choices) was also not evaluated.
