# Baseline review: CertificatesTable.tsx + CertificateDetails.tsx

## Inferred user task

An operator manages a fleet of TLS certificates. `CertificatesTable.tsx` is the full-page list of certificates for the account, sortable/filterable/paginated, with a per-row action to open one certificate's own details page. `CertificateDetails.tsx` is that details page: identity/status, the domains (SANs) the cert covers, the load balancers it's attached to, and its renewal history. The task is "find a certificate, then inspect and act on it" — a standard resource-management list → details flow.

## Findings

### 1. Row navigation built as a `Button`+`onClick` action instead of a `Link` on the row-header cell

**Evidence:** `CertificatesTable.tsx` lines 55-56 make `domain` the row header but render it as plain text (`cell: (c) => c.domain`). Navigation instead lives in a separate `actions` column, lines 66-75:
```tsx
cell: (c) => (
  <Button variant="inline-link" onClick={() => navigate(`/certificates/${c.id}`)}>
    View details
  </Button>
),
```
This has no `href`; `navigate()` fires only from a synthetic `onClick`.

**Cloudscape source:** The Table component's own documented row-header example (from `https://cloudscape.design/components/table/`, playground source for the row-header column) is:
```
cell: item => <Link href="#">{item.name}</Link>,
sortingField: 'name',
isRowHeader: true,
```
i.e. the canonical pattern makes the row-header cell itself a `Link`, not a plain string paired with a separate action button. The Link component docs (`https://cloudscape.design/components/link/`) additionally warn: *"Do not use this handler for navigation, use the `onFollow` event instead."* (of `onClick`) and *"Use `onFollow` instead of `onClick` so users can open the links in a new tab."*

**Why it matters:** Because the action is a `Button` with no `href`, none of the native anchor affordances are available — Ctrl/Cmd+click or middle-click to open in a new tab, right-click → "Copy link address," or a status-bar URL preview on hover. Cloudscape's documented row-header + `Link`/`onFollow` combination exists specifically to keep those affordances while still doing client-side routing.

### 2. `TextFilter` only, despite a finite-value `status` property that is the obvious operational query

**Evidence:** `CertificatesTable.tsx` line 7 imports only `TextFilter`, used at line 77. `Certificate.status` (line 13) is a closed 3-value enum (`issued` / `expiring-soon` / `expired`) rendered via `StatusIndicator` (lines 25-26, 58-63) — for a certificate fleet, "show me what's expiring or expired" is the primary triage query, not a domain-name text search.

**Cloudscape source:** Filtering patterns (`https://cloudscape.design/patterns/general/filter-patterns/`): *"If the common behavior of users is to filter a resource by only one or two properties, use the collection select filter. For example: by 'status' or 'type'."* The Collection select filter component page gives the matching example: *"Use a select filter for commonly used properties and values... For example: Property: Status; Values: Error, Loading, Pending, Stopped, and Success."*

**Why it matters:** The existing property (`status`, small closed set) is exactly the documented use case for `CollectionSelectFilter`, which the surface doesn't use at all — free text is a weaker instrument for a query that is naturally a value pick.

### 3. `noMatch` filtering state is configured but overridden by a static `empty` prop, so the documented "zero results" state can never appear

**Evidence:** `CertificatesTable.tsx` lines 35-39 configure `useCollection` with `filtering: { empty: 'No certificates', noMatch: 'No matching certificates' }`. `collectionProps` is spread onto `<Table>` at line 43, but line 79 then sets `empty="No certificates"` explicitly on the same element. Because later JSX props win, this permanently overrides whatever `collectionProps.empty` resolved to.

**Cloudscape source:** The collection-hooks dev guide (`https://cloudscape.design/get-started/dev-guides/collection-hooks/`) defines `empty`/`noMatch` in the config as *"Content to display in the table/cards empty slot when there are no items initially provided"* / *"...when filtering returns no matched items"* respectively, and `collectionProps` as the *"Props object to spread on the table/cards component"* that carries this resolved content. The Table view pattern (`https://cloudscape.design/patterns/resource-management/view/table-view/`) distinguishes the two states explicitly: *"When there are no matched results for the applied filters, show a zero results state,"* with its own copy guidance (*"Zero results... No resources match your search... Clear filter"*).

**Why it matters:** Typing a filter query that matches nothing will still show "No certificates" (the empty-collection message) instead of the configured, more accurate "No matching certificates" with a path back (clear filter) — the `noMatch` value the developer explicitly wrote is dead code.

### 4. Breadcrumb link has an `href` but no `onFollow`, so it bypasses the router

**Evidence:** `CertificateDetails.tsx` lines 36-42:
```tsx
<BreadcrumbGroup
  items={[
    { text: 'Certificates', href: '/certificates' },
    { text: 'api.example.com', href: '#' },
  ]}
  ariaLabel="Breadcrumbs"
/>
```
No `onFollow` handler is wired to the `react-router` `navigate`/`Link` used elsewhere in this same surface (`useNavigate` in `CertificatesTable.tsx`).

**Cloudscape source:** BreadcrumbGroup's event docs state: *"onClick... Called when the user clicks on a breadcrumb item. Do not use this handler for navigation, use the `onFollow` event instead."* and *"onFollow... Called when the user clicks on a breadcrumb item with the left mouse button without pressing modifier keys (that is, CTRL, ALT, SHIFT, META)."* (from `https://cloudscape.design/components/breadcrumb-group/`).

**Why it matters:** With no `onFollow`, clicking "Certificates" falls through to the browser's default anchor behavior — a full page reload to `/certificates` — instead of a client-side route change, discarding the SPA's in-memory state. This is the mirror image of Finding 1: there, navigation has no `href`; here, `href` exists but isn't paired with the router via the documented event.
