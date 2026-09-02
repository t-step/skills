# Baseline review: CertificatesTable.tsx + CertificateDetails.tsx

## Inferred user task

An operator manages the account's fleet of TLS certificates: scan the fleet for certificates that are expiring or expired (`CertificatesTable.tsx`), narrow the list down by status when triaging, then open a single certificate (`CertificateDetails.tsx`) to inspect its configuration, the domains it covers, the load balancers it's attached to, and its renewal history, and from there take a lifecycle action (Renew or Revoke) on that one certificate.

## Findings

### Finding 1: Full-page table is wrapped in `ContentLayout` instead of carrying its own `header`

**What it is.** `CertificatesTable.tsx` renders `<ContentLayout header={<Header variant="h1" counter=... >Certificates</Header>}><Table variant="full-page" ... /></ContentLayout>` (lines 42–79). The page title/counter live on `ContentLayout`'s `header` slot, and `Table` itself is given no `header` prop at all.

**Repository evidence.** `fixture/src/pages/CertificatesTable.tsx:42-51` — `ContentLayout` wraps a `Table` with `variant="full-page"`; the `Header` with `variant="h1"` and the `counter` sit on `ContentLayout`, not on `Table`.

**Cloudscape source.** https://cloudscape.design/patterns/resource-management/view/table-view/ — under General guidelines, "Don't": *"Don't use the content layout component on this type of page. Instead, use the "full-page" variant of the table component to implement this pattern."* The same page's Building blocks section (D. Header) says: *"Enabling a sticky header is optional, but recommended, for these potentially lengthy list pages. If enabled, use the "awsui-h1-sticky" header variant so the title reduces its size on scroll."* This is confirmed by Cloudscape's own canonical example, `pages/table/full-page-variant.page.tsx` in `cloudscape-design/components` (fetched via GitHub in this session), which renders `<Table header={<Header variant="awsui-h1-sticky">Full-page table</Header>} stickyHeader variant="full-page" .../>` with no `ContentLayout` anywhere, and the `app-layout/with-table.page.tsx` example passes the same `Header` (including title, description, and actions) directly into `Table`'s `header` prop as the `AppLayout`'s `content`.

**Why it matters.** The fixture combines the one layout the pattern explicitly forbids (`ContentLayout`) with the "full-page" table variant that is meant to replace it, and separately drops the title/counter onto a component (`ContentLayout`'s `Header variant="h1"`) that isn't the one Cloudscape's own sticky-shrink behavior is wired to (`Header variant="awsui-h1-sticky"` on `Table`). The result works visually but sits outside the documented composition, and the sticky-header shrink-on-scroll behavior the pattern calls out won't engage. Moving the `Header` (with `counter`) into `Table`'s `header` prop and removing `ContentLayout` expresses the same "list of certificates" page exactly as Cloudscape's own table-view pattern and reference examples do.

### Finding 2: Status column uses free-text `TextFilter` instead of the documented `CollectionSelectFilter`

**What it is.** The table's only filter is a `TextFilter` (`CertificatesTable.tsx:74`, wired via `filterProps` from `useCollection`) searching across all columns. One column, `status`, is a closed, three-value enum (`issued` / `expiring-soon` / `expired`, `Certificate.tsx:14`, rendered via `StatusIndicator` at line 58) — exactly the kind of property Cloudscape names as the trigger for its select-filter pattern.

**Repository evidence.** `fixture/src/pages/CertificatesTable.tsx:8-9,36-40,74` (TextFilter + `useCollection` `filtering` config) and `:14,26-27,58-60` (the `status` enum and its column).

**Cloudscape source.** https://cloudscape.design/patterns/general/filter-patterns/ — the Criteria table contrasts "Text filter" ("Find resources that match an exact text query") against "Collection select filter" ("Find resources with overlapping, defined values... Single selection of a value for each property"), and the guidance text states: *"If the common behavior of users is to filter a resource by only one or two properties, use the collection select filter. For example: by "status" or "type"."*

**Why it matters.** "Status" is the doc's own worked example for when to reach for the select filter rather than free text. A text filter forces the user to type the exact status string ("expiring-soon") to isolate certificates needing renewal, where a `CollectionSelectFilter` (or a `PropertyFilter`, if other filterable properties are added later) lets them pick "Expiring soon" from a finite list of values — the more native expression of "find certificates by status" that Cloudscape's own criteria table calls for here.

### Finding 3: "Revoke" is a bare `Button` with no delete-confirmation pattern, despite documented cascading risk

**What it is.** `CertificateDetails.tsx:46-49` renders `<Button>Renew</Button><Button>Revoke</Button>` as plain header actions with no `onClick`, no modal, and no distinction from the non-destructive "Renew" action. The same page's "Attached resources" container (lines 14-17, 79-91) shows this certificate is attached to two Application Load Balancers (`alb-public-prod`, `alb-internal-prod`) — i.e., revoking it would break TLS termination on live infrastructure.

**Repository evidence.** `fixture/src/pages/CertificateDetails.tsx:46-49` (Revoke button) and `:14-17,79-91` (attached ALBs establishing cascading impact).

**Cloudscape source.** https://cloudscape.design/patterns/resource-management/delete/delete-with-additional-confirmation/ — *"Use delete with additional confirmation for single-resource deletion if the resource cannot be recreated, or if deleting the resource poses a risk of breaking other infrastructure or causing an outage."* Its building blocks specify a modal with a bold resource identifier ("Reassurance"), a warning alert stating cascading effects ("Consequences": *"State the possible consequences of the action like severity, outcome, and potential cascading effects of the action... Use the warning alert format"*), and a confirmation-text input field before the destructive action executes.

**Why it matters.** Revoke is an irreversible, in-context action tied to a single resource that the fixture's own data shows has dependents — precisely the case Cloudscape's guidance distinguishes from a plain button or even the lighter "simple confirmation" pattern. Wiring Revoke to a confirmation modal that names the two attached load balancers as a consequence expresses this destructive action the way Cloudscape's own delete patterns are documented to, rather than as an unguarded button click.
