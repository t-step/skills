# Cloudscape Native-Expression Review: Certificates (table + details)

**Inferred user task:** Users manage a fleet of TLS certificates. From a
filterable/sortable list they open an individual certificate's own
full-page details view (identity, domains covered, attached load
balancers, renewal history) to inspect it and perform whole-resource
actions (Renew, Revoke). This is stated explicitly in the fixture's own
code comments and matches the observed routes, data shapes, and actions.

**Cloudscape packages / versions:** `@cloudscape-design/components`
3.0.900 (locked, resolved from `^3.0.900`); `@cloudscape-design/collection-hooks`
1.0.60 (locked, resolved from `^1.0.60`). Both fully resolved to exact
locked versions — no unresolved-range caveat applies.

## Findings

**Finding:** Row-level navigation to the certificate details page is
expressed as a `Button` in a separate trailing "Actions" column, instead
of a `Link` on the identifying "Domain" column (which is already the
table's `isRowHeader`).

**Type:** combined component + pattern

**Materiality:** high

**Confidence:** high

**User task:** as above — opening one certificate's own full details page
from the fleet list.

**Repository evidence:** `CertificatesTable.tsx` lines 52–72. The
`domain` column is declared `isRowHeader: true` but its cell renders plain
text (`cell: (c) => c.domain`). A separate, final `actions` column exists
solely to render `<Button variant="inline-link" onClick={() =>
navigate(`/certificates/${c.id}`)}>View details</Button>`.

**Cloudscape evidence:**
- Table docs, Columns section (`https://cloudscape.design/components/table/?tabId=usage`):
  "Use the first table column for unique identifiers of the items that
  are represented in the table (for example: name, id, and ARN). Also use
  the first table column for users to navigate to a details page that
  shows more information about the item." Also: "Use the primary link
  variant instead of the secondary link variant in table cells to help
  users distinguish links from other text content in adjoining cells."
- Button docs (`https://cloudscape.design/components/button/?tabId=usage`):
  "Use buttons for actions. Use links when taking the user to a different
  page."
- Link docs (`https://cloudscape.design/components/link/?tabId=usage`):
  "Don't use a link for actions. Instead, use a button." (states the
  converse of the same semantic split, corroborating it.)

**Applicability argument:** The observed task — clicking through from a
list row to that row's own full details page — is exactly the task the
Table docs' column-placement guidance addresses, not a superficially
similar shape. The current implementation solves that same problem (it
navigates to `CertificateDetails.tsx`), so this isn't a different-intent
substitution. The proposed alternative (identifier column as a `Link`)
preserves the identical task and destination. The difference is material,
not stylistic: it's doubly supported — both which *column* should carry
navigation, and which *component* (`Link` vs `Button`) should express a
pure page-to-page navigation — and the current code violates both
independently, not just one interpretation of a single guideline.

**Current expression:** A non-interactive identifier cell plus a
same-semantics-as-a-link action wearing a `Button` (`variant="inline-link"`)
in a dedicated trailing column that exists for no other purpose.

**Native expression:** Make the `domain` cell itself a `Link` (primary
variant) pointing at `/certificates/${c.id}` (wired to the app's router the
same way any other in-app Cloudscape `Link` is), and drop the standalone
`actions` column — its only content was this same navigation.

**Why it matters:** Cloudscape draws an explicit, symmetric line between
`Button` (actions) and `Link` (navigation); using a button for pure
navigation blurs that distinction for every table in the app that follows
this file as precedent, and burns a whole column purely to hold what the
identifier column is documented to carry for free.

**Boundary check:** This is about which Cloudscape component/column
carries a navigation affordance, not about whether the `onClick`/`navigate`
wiring itself is implemented correctly — that mechanic is unaffected by
which component expresses it.

**Authority strength:** RECOMMENDED (stated as imperative preferred
practice — "Use..." — on both the Table and Button pages, and corroborated
by an explicit "Don't/Instead" pairing on the Link page for the mirror
case; no single citation states this exact direction as an absolute
prohibition).

## Suppressed (low materiality or weak applicability)
- "Domains covered" in `CertificateDetails.tsx` renders a single-column,
  non-actionable list of SAN strings as a borderless `Table` rather than a
  `List`. Considered and cleared: the List component docs state no
  preference against this shape, and using `Table` keeps it visually and
  structurally consistent with the sibling "Attached resources" and
  "Renewal history" containers on the same page. No applicability
  evidence supports treating this as a mismatch.

## Orientation notes
- `CertificateDetails.tsx` closely matches Cloudscape's documented
  "Details page" pattern (`https://cloudscape.design/patterns/resource-management/details/details-page/`):
  breadcrumbs, page title in `Header`, whole-resource global actions in the
  header (Renew/Revoke mirror the pattern's own "Edit or Delete" example),
  a details-summary `Container` using `KeyValuePairs` for "General
  configuration" (exactly as the pattern instructs), and multiple
  "related resources" containers (Domains covered, Attached resources,
  Renewal history) laid out per the pattern's guidance.
- Stacking four containers rather than adopting "Details page with tabs"
  (`https://cloudscape.design/patterns/resource-management/details/details-page-with-tabs/`)
  is appropriate here: each section is short, and that pattern is reserved
  for organizing complex or lengthy content into mutually exclusive
  groups, which doesn't describe this page.
- `CertificatesTable.tsx`'s use of the `full-page` Table variant with
  `stickyHeader` plus `useCollection` for client-side filtering/sorting/
  pagination matches the Table docs' guidance for a stand-alone table-view
  page.
- The three related-resource tables in `CertificateDetails.tsx` correctly
  use `variant="borderless"` inside `Container`s, matching the Table docs'
  explicit guidance to use borderless "when placing a table inside another
  container."

## What was not evaluated
Implementation correctness — react-router wiring/`onFollow` mechanics for
the recommended `Link`, any deprecated props, accessibility mechanics, or
hard-coded style values — is `cloudscape-implementation-audit`'s domain
and was not assessed here. General UX/product judgment (e.g., whether
Renew/Revoke should require confirmation, information density, or overall
page hierarchy) was also not evaluated.
