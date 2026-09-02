# Cloudscape Native-Expression Review: Quota Requests

**Inferred user task:** View a full-page log of quota-increase requests filed against the account; select a request to inspect its complete field set (current/requested value, region, requester, submission date, status) and, if the request is still pending, withdraw it. Individual requests have no dedicated route or entry point elsewhere in the app — the detail view exists only as an in-context follow-up to browsing the list.

**Cloudscape packages / versions:** `@cloudscape-design/components` 3.0.900 (resolved; declared range `^3.0.900`)

## Findings

### Finding 1: Row detail is shown in a Modal instead of a Split panel

- **Type:** combined component + pattern
- **Materiality:** high
- **Confidence:** high
- **User task:** as stated above — browse a list of requests, then glance at one request's full detail (and optionally withdraw it) without losing the list.
- **Repository evidence:** `src/pages/QuotaRequests.tsx` — each row exposes an inline-link `Button` labeled "View" (lines 90–94) that opens a `Modal` (lines 100–129) containing a `KeyValuePairs` with all six fields (119–126) and a footer with a conditional "Withdraw request" action plus "Close" (106–115). The table itself already uses `variant="full-page"` (line 71). The surrounding comment (59–64) states there is no per-request route and nothing else links to an individual request.
- **Cloudscape evidence:**
  - Modal (`/components/modal/`) "Do": *"Use a modal primarily to confirm or cancel a choice… for example, deleting a resource."* Its documented content types are alerts/descriptions, input fields/selects for creation, tiles for comparison, and checkboxes/radios/toggles for preferences — no documented use case for passively viewing a read-only record's fields.
  - Split panel (`/components/split-panel/`) "Do": *"Hide the split panel on close when an additional trigger is not necessary… Common use cases… Displaying supplemental content or details… Content similar to a modal, where keeping the context of the main page is important."* Its Features section states it "acts similarly to a modal, but it keeps the main page in view instead of overlaying it."
  - Split view pattern (`/patterns/resource-management/view/split-view/`): objectives are resource identification, monitoring, and troubleshooting via a table/cards paired with a split panel that "opens automatically on resource selection" and presents "additional information about the selected resources."
  - Resource details pattern (`/patterns/resource-management/details/`): a details page is for when a service needs "everything at a glance" on a dedicated route, contrasted explicitly with split view, which "provides users with a subset of resource details" without a route.
- **Applicability argument:** (1) The task — quick, in-context inspection of one selected record's fields while the rest of the list stays visible, with no dedicated page — matches split panel's documented "supplemental content or details" use case exactly, not modal's documented "confirm/cancel" or "collect input" purposes. (2) The current modal solves the identical problem split panel is written for: showing a record's fields after a selection, in place. (3) Swapping to split panel preserves the task precisely — same six fields, same conditional withdraw action (which split panel's header-action slot documents for "actions users can perform on the underlying content") — it invents no new navigation or product goal. (4) The mismatch is material, not stylistic: a modal blocks and dims the entire table while a user is just glancing at one request, defeating the "browse while comparing" intent implied by a full-page table of requests, whereas split panel exists specifically to avoid that trade-off.
- **Current expression:** Row → inline-link "View" button → full-screen-blocking `Modal` with `KeyValuePairs` + footer actions.
- **Native expression:** A split panel (likely the "discrete" type, since only one request is inspected at a time and no cross-request comparison is implied) opened by the row action or by making the table row selectable, showing the same `KeyValuePairs` content and the same conditional withdraw action as a header action, while the request table remains visible and interactive. A "comparison" split panel with `Table` `selectionType` would also satisfy the pattern's guidance, but the discrete trigger is the closer fit given the current one-request-at-a-time design.
- **Why it matters:** Modal is documented as primarily a confirm/cancel and data-entry surface, not a passive-detail viewer; using it here stretches it past its documented vocabulary and, unlike split panel, blocks the very list the user is trying to browse — undermining the full-page table's own purpose. Split panel is the purpose-built, explicitly documented mechanism for this exact "select → see details in place" interaction.
- **Boundary check:** This is a component/pattern choice for the same detail-viewing task, not an implementation defect in Modal or KeyValuePairs, and it does not propose a different product goal — no route or navigation structure is invented.

## Suppressed (low materiality or weak applicability)

- **Details page (with tabs) as the native expression instead of split panel** — considered, since the modal does show the request's complete field set. Suppressed because the surface explicitly has no per-request route and nothing else links to an individual request; recommending a dedicated details page would require inventing navigation that doesn't exist today, which is a product-redesign move, not a native-expression one. Split panel preserves the current no-navigation task instead.

## Orientation notes

- `ContentLayout` + `Header` (h1, with counter) + `Table` `variant="full-page"` matches the table view pattern's documented building blocks for a full-page resource list.
- `KeyValuePairs` for the label/value field set is the documented component for this exact job.
- `StatusIndicator` mapping `approved`→success, `pending`→in-progress, `denied`→error is standard three-state status usage.
- Modal's footer using `Box float="right"` + `SpaceBetween` for grouping the conditional action and primary "Close" button follows the component's own documented footer-slot guidance.

## What was not evaluated

Implementation correctness — Modal a11y wiring (`closeAriaLabel`, focus handling), Button variant/prop usage, KeyValuePairs API details, any deprecated props or token usage — is `cloudscape-implementation-audit`'s domain and was not assessed here. General UX/product judgment (e.g., whether six fields is the right amount of detail, whether "Withdraw request" is the correct action set, whether a per-request route should eventually exist) was also not evaluated.
