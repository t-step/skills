# Cloudscape Native-Expression Review: RecentWorkspaces ("jump back in" shelf)

**Inferred user task:** Let a user glance at a small, fixed set of recently-opened workspaces and recognize/reopen the one they want. There is no cross-item metric comparison, filtering, bulk action, or resource-management (create/delete/edit) need — per the source's own comment, this is "a personal 'jump back in' shelf on the user's home page."

**Cloudscape packages / versions:** `@cloudscape-design/components` declared `^3.0.900`, locked/resolved `3.0.900` (from `resolve_versions.py` against the fixture's lockfile).

## Findings

### Finding 1: ContentLayout + full Card-view shell vs. a Dashboard-item shape — depends on how this surface is mounted

- **Type:** intent-dependent
- **Materiality:** high
- **Confidence:** high (the tension itself is well-evidenced; the correct single fix is not, which is exactly why this is intent-dependent)
- **User task:** as above.
- **Repository evidence:** `RecentWorkspaces.tsx` wraps a `Header variant="h1"` and a default-variant `Cards` (no `variant` prop) in `ContentLayout` (lines 30–66): 6 static items, no item counter on the header, no pagination/filter/selection, and no affordance linking out to a fuller workspaces list. The file's own comment (lines 25–29) describes the surface as one "shelf" on a home page, not an exhaustive management page.
- **Cloudscape evidence:**
  - Card view pattern (`/patterns/resource-management/view/card-view/`), **Don't**: *"Don't use the content layout component on this type of page. Instead, use the 'full-page' variant of the cards component to implement this pattern."*
  - Cards component (`/components/cards/`), Variant: *"Full page — takes up the full page. Use for presenting and managing cards on a standalone page"* vs. *"Default — renders the cards header within a container"*; Do: *"When used within the app layout, full-page cards must be the first component in the content slot."* Also Do: *"Always show the total number of items next to the cards collection title."*
  - Content layout component (`/components/content-layout/`): documented as *"page structure"* — a whole-page shell, usable standalone or in AppLayout's content slot, not a widget wrapper.
  - Dashboard items pattern (`/patterns/general/service-dashboard/dashboard-items/`): *"Dashboard items are self contained UI elements that address specific customer needs, such as navigating to a resource..."* Static dashboard item building blocks include a Header (title + counter), a bounded content area (chart/table/list), and *"G. View all — link that takes the user to a new page with the complete resource list."* Do: *"Avoid displaying long lists of data... instead use a separate page for this."*
- **Applicability argument:** The stated task ("navigate to a resource," bounded, non-exhaustive) matches Dashboard items' own problem statement much more closely than Card view's ("Cards view of all user resources within the AWS service" — a filterable/paginated/selectable resource-management page). None of Card view's other building blocks (breadcrumbs, side nav, filter, pagination, selection) appear here, so the surface isn't actually attempting that pattern's job — it has only borrowed Cards plus a ContentLayout+h1 shell the docs tie specifically to full pages. Two different native fixes both preserve the same task, and which applies turns on one fact absent from this bounded file: is `RecentWorkspaces` mounted as its own routed page, or nested as one section among others on a richer home page?
  - If it's the whole page: drop `ContentLayout`, use `variant="full-page"` Cards with a sticky h1 header and an item counter.
  - If it's one embedded shelf (the literal reading of the comment): follow the Dashboard items shape — a `Container`-based static item with a counted header and a "View all" link to a separate, complete workspaces page, not a page-level `ContentLayout` shell.
- **Current expression:** `ContentLayout(Header h1) > Cards` (default variant), no counter, no view-all/link-out, no pagination/filter.
- **Native expression:** Not stated with confidence — see the two branches above; resolving which requires seeing how this component is mounted in the app.
- **Why it matters:** ContentLayout and Card view are documented specifically for full resource-management pages; the "bounded preview + path to the full list" shape is documented specifically as Dashboard items. Using the former's shell for a task the surface's own comment frames as the latter risks reading, to a Cloudscape-fluent user, as the complete Workspaces management page — with no way to actually reach a complete list, filter, or manage resources.
- **Boundary check:** This is about which named Cloudscape pattern and accompanying composition (ContentLayout+full-page Cards vs. Container+dashboard-item) fits the stated task, not about the mechanics of components already chosen, and not a generic "could be nicer" critique.

## Suppressed (low materiality or weak applicability)

- **Missing item counter next to "Recent workspaces"** (Cards Do: "Always show the total number of items..."). Weak applicability: this guidance's value comes from collections where the full count isn't otherwise visible (paginated/filtered); here all 6 items are always on screen at once, so the counter adds negligible information. Folded into Finding 1 rather than reported standalone.
- **No filtering/pagination for 6 cards** (Cards Do: "Only use filtering and pagination if there are more than five cards"). The collection sits right at that threshold, but it's a fixed "recent" list — pagination/filtering wouldn't serve the stated task regardless of count. Low materiality.
- **Badge content restates its own color as text** (`<Badge color={item.colorTag}>{item.colorTag}</Badge>`, e.g. a blue badge reading "blue"). Badge's own guidance says to supplement color with text, which this technically does, but the text adds no information beyond the color already shown. This is a copy/content defect on an already-correctly-chosen component, not a component-selection problem — out of this skill's scope.

## Orientation notes

- **Cards** as the component choice for 6 non-columnar, visually-distinct, comparable-at-a-glance items is a reasonable fit per Card view's own problem statement ("glancing at small sets of similar resources... non-columnar, yet comparable data") — the concern above is about the surrounding shell, not the component itself.
- **StatusIndicator** (not Badge) for the active/archived state is the correct component per Badge's own explicit rule: *"Avoid using badges... to indicate status — use the status indicator component instead."* This surface already follows that rule correctly.
- **Link** as the card header's navigation affordance matches Card view's guidance that "each card links to the details view."

## What was not evaluated

Implementation correctness — e.g., whether `Link`'s variant prop should be `"primary"` per Cards' writing guidance, whether `StatusIndicator type="stopped"` is the most precise mapping for "archived," ARIA/keyboard mechanics, and Header counter prop wiring — is `cloudscape-implementation-audit`'s domain and was not audited here. General UX/product judgment (information density, whether a color name is a useful badge label, overall page layout quality) was likewise not evaluated.
