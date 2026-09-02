# Baseline review: RecentWorkspaces.tsx

## Inferred user task

A personal "jump back in" shelf on a home page: the user recognizes one of six recently-opened workspaces (by name and a self-assigned color tag) and re-opens it with one click. There is no cross-item comparison, sorting, filtering, or bulk action — the code's own comment makes this scoping explicit.

## Findings

### Finding 1: `Cards` has no `header` slot, so the documented item counter is missing

**What it is:** The `<Cards>` collection (`fixture/src/pages/RecentWorkspaces.tsx:38-65`) is rendered with no `header` prop at all. The only title on the page is the `ContentLayout`'s own `<Header variant="h1">` (lines 32-36), which is page-level chrome, not the collection's own header. Cloudscape's Cards component reserves a `header` slot specifically for this, and its default `variant` is `"container"`, which per the Header component's own docs takes an h2 inside a container.

**Evidence:** `fixture/src/pages/RecentWorkspaces.tsx:38-65` — `<Cards items={WORKSPACES} trackBy="id" cardDefinition={...} cardsPerRow={...} empty="..." />` with no `header=`.

**Cloudscape source:**
- https://cloudscape.design/components/cards/ (Usage tab) — "Always show the total number of items next to the cards collection title." and "Use header component to display additional information, such as item counter, info link, action buttons, or description text." Also: "Use the h2 variant of the header component in the container header of the default cards variant."
- https://cloudscape.design/components/header/ (API tab) — the `counter` slot: "Specifies secondary content that's displayed to the right of the heading title. This is commonly used to display resource counters in table and cards components."

**Why it matters:** This is a documented, not cosmetic, gap — Cloudscape's own guidance treats the item count as a required part of every cards collection, surfaced through the `Header` component's `counter` slot inside the Cards' own `header`, not the surrounding page chrome. The fix is additive and cheap: `header={<Header variant="h2" counter="(6)">Recent workspaces</Header>}` on the `Cards` component (six items is a hardcoded, known count here, so no dynamic wiring is needed).

### Finding 2: Empty state is a bare string instead of the documented heading + action structure

**What it is:** `empty="No recent workspaces"` (line 64) passes a plain string. Cloudscape's Empty states pattern defines a specific structure for this slot — a bold heading, an optional description, and (per a "Do") an action button — and Cards' own API example demonstrates exactly this structure in the `empty` slot.

**Evidence:** `fixture/src/pages/RecentWorkspaces.tsx:64` — `empty="No recent workspaces"`.

**Cloudscape source:** https://cloudscape.design/patterns/general/empty-states/ — "Empty state is applicable to table, card view and service dashboards." Structure given as Heading / Description (optional) / Action button, and under Do: "Always provide an action. Having no recourse creates confusion and prevents users from moving forward. If no action can be provided, include a link in the description to navigate users to the page where they can complete the action." The Cards API page's own code sample for the `empty` slot renders `<Box><SpaceBetween><b>No resources</b><Button>Create resource</Button></SpaceBetween></Box>`, not a bare string.

**Why it matters:** A user who has never opened a workspace hits a dead end with the current string — no path forward is offered, which is exactly the failure mode the "Always provide an action" guideline calls out. A native fix following the documented pattern would render a heading plus an action (e.g., a link to browse/open a workspace, which is the only way to ever populate this "recent" list).

### Finding 3: Card header `Link` omits the documented `fontSize="inherit"`

**What it is:** The card header at line 42 — `header: (item) => <Link href={...}>{item.name}</Link>` — doesn't set `fontSize`. The Cards component's own API documentation for the `cardDefinition.header` property explicitly instructs setting a font size on links placed there.

**Evidence:** `fixture/src/pages/RecentWorkspaces.tsx:42` — `header: (item) => <Link href={`/workspaces/${item.id}`}>{item.name}</Link>,`.

**Cloudscape source:** https://cloudscape.design/components/cards/ (API tab), `cardDefinition` property description — "header ((item) => ReactNode) - Responsible for displaying the card header. You receive the current item as an argument. Use fontSize=\"inherit\" on link components inside card header." (Note: `variant` is not a needed change here — https://cloudscape.design/components/link/ (API tab) confirms `Link`'s `variant` "default is secondary, except inside the following components where it defaults to primary: Table, Cards, ..." so the link is already primary-styled by virtue of being inside `Cards`.)

**Why it matters:** This is a narrow, low-confidence finding — Cloudscape's own Cards usage-tab example code (the "Common cards" playground sample) actually sets `fontSize="heading-m"` on its card-header link rather than `"inherit"`, so the API docs' instruction and the reference example disagree in practice. Worth setting explicitly either way (currently it silently falls back to `Link`'s default `body-m`), but this should be treated as a minor polish item, not a strong defect.
