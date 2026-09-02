# Baseline review: QuotaRequests.tsx

## Inferred user task
A user browses a log of quota-increase requests filed against their account, opens one request to review its full detail (current/requested value, region, requester, submission date, status), and — if the request is still pending — withdraws it. Per the file's own header comment, nothing else in the app links to an individual request and there is no per-request route; this is a single, self-contained page.

## Findings

### 1. The read-only detail view uses a Modal where Cloudscape's own guidance points to a Split panel

**What it is:** Selecting a row opens a `Modal` (lines 104–133) containing a `KeyValuePairs` with the request's full field set (lines 121–131). This is a pure "view details of the selected row" interaction with no destructive/confirmatory framing for the view itself.

**Repository evidence:** `QuotaRequests.tsx:104-133` — `<Modal visible header={openRequest.quotaName} ...><KeyValuePairs columns={2} items={[...]} /></Modal>`, triggered by the row's "View" button at line 95.

**Cloudscape source:**
- Modal usage guidelines (https://cloudscape.design/components/modal/?tabId=usage): "Use a modal primarily to confirm or cancel a choice. For example, deleting a resource."
- Split panel usage guidelines (https://cloudscape.design/components/split-panel/?tabId=usage): "It is the primary component to implement split view, a pattern to display item collection with contextual item details," and "Omit the containers and place content like key-value pairs directly on the split panel when possible to reduce visual noise."
- Secondary panels pattern (https://cloudscape.design/patterns/general/secondary-panels/): the panel-selection criteria table lists Split panel's content as "Detailed view of one or more selected resource" and its use case as "Reviewing resource information."
- Split view pattern (https://cloudscape.design/patterns/resource-management/view/split-view/): "The split panel presents additional information about the selected resources. By default, it's closed on page load and opens automatically on resource selection."
- Resource details pattern (https://cloudscape.design/patterns/resource-management/details/): "your service could include a split view which provides users with a subset of resource details" — explicitly distinct from a full details page, and requiring no route.

**Why it matters:** The fixture's own scope note rules out adding a per-request route/details page, but Cloudscape already has a documented, route-free pattern for exactly this shape of interaction (browse a table, inspect one selected item's fields in place) — the split view pattern pairing `Table` with `SplitPanel`. The current Modal repurposes a component whose documented purpose is confirming/canceling a choice for a passive, non-committing "view" action, which is the split panel's job. Moving the `KeyValuePairs` into a `SplitPanel` (opened on row selection, single-select) would let users glance across multiple requests without re-opening and closing a blocking dialog each time, matching the documented split-view interaction model.

### 2. The "Withdraw request" action is embedded inside the detail-viewing surface instead of its own confirmation modal

**What it is:** The only destructive/state-changing action (`Withdraw request`, line 113) is rendered as a footer button inside the same Modal used to passively display the request's fields, alongside a `Close` button (lines 110-119). There is no separate confirmation step once withdrawal is invoked.

**Repository evidence:** `QuotaRequests.tsx:110-119` — the modal `footer` mixes `{openRequest.status === 'pending' && <Button>Withdraw request</Button>}` with the view-only `Close` action in one `SpaceBetween`.

**Cloudscape source:**
- Delete patterns (https://cloudscape.design/patterns/resource-management/delete/): "Delete with simple confirmation is used for single resource or bulk deletions that are not likely to break users' running infrastructure, but are still being performed on resources that cannot be quickly recreated. Use a modal to ask users to confirm that they wish to proceed with the deletion."
- Modal usage guidelines (https://cloudscape.design/components/modal/?tabId=usage): "Never launch another modal from within a modal," and "Use an action button to act on the entire contents of a modal... Use a modal primarily to confirm or cancel a choice."

**Why it matters:** Withdrawing a pending quota request is a single-resource, not-easily-undone state change with moderate cost to redo (re-filing the request) — the profile Cloudscape's delete-pattern criteria map to "delete with simple confirmation," i.e., its own dedicated confirm/cancel modal, not a footer button living inside a general-purpose detail-viewing dialog. Once finding 1 moves the read-only detail into a `SplitPanel` (which per its own docs shouldn't duplicate header/detail actions gratuitously), "Withdraw request" becomes the split panel's one contextual action; invoking it should open a dedicated confirmation `Modal` ("This will withdraw your request; you can resubmit it later" / Cancel / Withdraw request). This gives the Modal component the single, well-defined confirm/cancel job it's documented for, instead of overloading it as both a viewer and an actioner.

### 3. The full-page table doesn't use the header/sticky-header pairing Cloudscape suggests for that variant

**What it is:** The table uses `variant="full-page"` (line 70) with `<Header variant="h1" ...>` (line 76) and no `stickyHeader` prop.

**Repository evidence:** `QuotaRequests.tsx:69-79`.

**Cloudscape source:** Table usage guidelines (https://cloudscape.design/components/table/?tabId=usage), "Variant → Full page": "We suggest enabling the sticky header and using the 'awsui-h1-sticky' variant of the header with this variant, so the title reduces its size on scroll." (`awsui-h1-sticky` is a real documented Header variant value: https://cloudscape.design/components/header/?tabId=api — "awsui-h1-sticky - Use this for sticky headers in cards and tables.")

**Why it matters:** This is a narrower, lower-confidence finding: the same Table usage page's general sticky-header criteria ("more than 30 items per page... more than five columns... columns can be sorted") don't clearly apply to the fixture's 3-row, 5-column, unsorted sample data, so the omission may be immaterial at the fixture's current scale. But the full-page variant's own feature guidance suggests the sticky-header + `awsui-h1-sticky` header pairing unconditionally for that variant, and the fixture uses plain `h1` with no sticky behavior — worth reconciling if this table is expected to grow past a handful of rows.
