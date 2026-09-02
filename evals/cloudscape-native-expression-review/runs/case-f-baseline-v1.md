# Baseline review: QuotaRequests.tsx

## Inferred user task

A user monitors quota-increase requests filed against their account: scan a short log-style table (quota name, region, status, submission date), open a row to review its full field set (current/requested value, region, requester, submission date, status), and, if the request is still pending, withdraw it. There is no per-request route — the modal is the only detail surface (per the file's own header comment, lines 59-64).

## Findings

### Finding 1: The row-header column is inert text; the "view details" affordance is duplicated into a separate Actions column

**What it is:** `quotaName` is marked `isRowHeader: true` (line 77) but rendered as plain text (`cell: (r) => r.quotaName`). The actual trigger for viewing a request's detail lives in a separate, later `actions` column as an `inline-link` Button labeled "View" (lines 86-95). This means the column Cloudscape designates as the row's identifying column carries no interaction, while an unrelated column five cells to the right duplicates the same "open this row" job the identifier column should be doing.

**Repository evidence:** `fixture/src/pages/QuotaRequests.tsx` lines 77, 86-95.

**Cloudscape source:** `https://cloudscape.design/components/table/index.html.md` — General guidelines → Do → Columns: *"Use the first table column for unique identifiers of the items that are represented in the table (for example: name, id, and ARN). Also use the first table column for users to navigate to a details page that shows more information about the item."* This is reinforced structurally: every table code sample on that page that sets `isRowHeader: true` pairs it with `cell: item => <Link href="#">{item.name}</Link>` — the row-header column is consistently the link.

**Why it matters:** This is a direct, named convention for exactly this row shape (identifier column doubling as the entry point to detail), not a generic call to "add affordance." Making `quotaName` a `Link`/`inline-link` Button that opens the modal removes the redundant Actions column outright (there is no other per-row action here besides withdraw, which only exists inside the already-open modal), simplifying the table to four columns while matching the documented pattern.

### Finding 2: Status is the third column instead of the second

**What it is:** Column order is Quota (id), Region, Status, Submitted, Actions (lines 77-95) — Status is placed after Region rather than immediately after the identifier column.

**Repository evidence:** `fixture/src/pages/QuotaRequests.tsx` lines 77-85.

**Cloudscape source:** `https://cloudscape.design/components/table/index.html.md` — General guidelines → Do → Columns: *"Use the second column for status when status is relevant, for example Running."* This immediately follows the guidance on using the first column for the unique identifier, i.e. the two rules are meant to compose (identifier, then status).

**Why it matters:** Status is the single most decision-relevant field in this table (pending vs. approved vs. denied governs whether a request even has a withdraw action). The doc's ordering rule puts exactly this kind of field second so it scans immediately after the identifying label; here it's pushed to third position behind Region, which is a lower-salience filter/grouping attribute.

### Finding 3: A read-only, single-resource detail view is expressed as a Modal rather than the split-view/split-panel pattern Cloudscape documents for this exact objective

**What it is:** Selecting a row opens a `Modal` containing only a `KeyValuePairs` of six read-only fields, plus (for pending items) a `Withdraw request` button (lines 100-129). No form input, no confirm/cancel choice about to be made when the modal opens — it's a pure "look at the resource's fields" surface, with an occasional action nested inside.

**Repository evidence:** `fixture/src/pages/QuotaRequests.tsx` lines 100-129.

**Cloudscape source:**
- `https://cloudscape.design/components/modal/index.html.md` — General guidelines → Do: *"Use a modal primarily to confirm or cancel a choice. For example, deleting a resource."* The same page's Features → Content section enumerates the common modal content types — Alert, Input fields/selects, Tiles, Checkboxes/radio groups/toggles — none of which is "a read-only key-value summary of a resource."
- `https://cloudscape.design/patterns/general/secondary-panels/index.html.md` — Criteria table maps *"View resources"* objective to *"Split panel"*, described as the use case *"Reviewing resource information ... in a table or card view."*
- `https://cloudscape.design/patterns/resource-management/view/split-view/index.html.md` — Objectives: *"Resource identification: Users need to quickly view key details to identify resources within a group of similar resources."*

**Why it matters:** Cloudscape has a named, purpose-built pattern (split view, built on the Split Panel component) for "select a row in a table, see its details in place," and its own docs steer Modal usage toward confirm/cancel-style interruptions instead. Using Modal here works, but it isn't the pattern Cloudscape's guidance points to for this specific "browse then inspect one row" task — and it also forces the `Withdraw request` action to live inside a viewing surface rather than in-context on the table, which the split-panel doc explicitly discourages combining with header-style actions ("Don't repeat the action buttons from the table/cards header in the split panel") but is silent on for row-level actions, so this is offered as a fit observation rather than a rule violation of equal weight to Findings 1-2.
