# Cloudscape Native-Expression Review: Identities page (sample-bedrock-spend-budget-guardrails)

**Inferred user task:** An admin views the distinct Bedrock-invoking IAM principals ("callers") observed by the metering system within a selectable lookback window (1 hour–30 days), scanning/sorting a many-column table (principal, type, account, ARN, SSO user, first/last seen) with configurable column visibility, and per-row can either start a budget-creation flow prefilled for that principal or inspect that principal's recent activity/audit history in place.

**Cloudscape packages / versions:** `@cloudscape-design/components` 3.0.1340 (locked, declared `^3.0.1340`, resolved); `@cloudscape-design/collection-hooks` 1.0.105 (locked, declared `^1.0.55`, resolved). Both fully resolved from `web/package.json` + the repo lockfile — no unresolved-range caveat applies to the findings below.

## Findings

### Finding 1: Full-page resource table wrapped in Content Layout instead of the documented full-page table variant

- **Type:** combined component + pattern
- **Materiality:** high
- **Confidence:** high
- **User task:** Viewing and managing the full set of distinct identities seen in the selected window — an 8-column, sortable, column-configurable resource table that *is* the page's entire content.
- **Repository evidence:** `src/pages/Identities.tsx` lines 110–129 wrap a `Header` (`variant="h1"`) and the table in `ContentLayout`; lines 133–149 render `Table` with `variant="container"`, `resizableColumns`, `stickyHeader`, `stickyColumns={{first:1,last:1}}`; lines 150–177 add a `CollectionPreferences` panel controlling 8 columns' visibility/order. Nothing else shares the page.
- **Cloudscape evidence:** Content Layout docs (cloudscape.design/components/content-layout): *"Don't use the content layout component for productive use cases such as resources creation, view, edit, and delete."* Table View pattern (cloudscape.design/patterns/resource-management/view/table-view): *"Use the 'full-page' `variant` of the table component for this pattern"* and *"Don't use the content layout component on this type of page. Instead, use the 'full-page' variant."* Table component docs: the `full-page` variant *"is for implementing the full page table view pattern... for presenting and managing a table with many columns within a stand-alone page,"* recommending sticky header plus `Header variant="awsui-h1-sticky"` (a real, current enum value) and pairing with `AppLayout contentType="table"`.
- **Applicability argument:** (1) Task match is exact, not superficial — the entire page is a many-column resource table being viewed/managed, precisely the Table View pattern's stated problem. (2) The current composition solves that same problem. (3) The proposed swap (drop `ContentLayout`, use `Table variant="full-page"` + `Header variant="awsui-h1-sticky"`) changes no data, column, action, or preference — same task, same functionality. (4) Both cited pages state this as an explicit prohibition ("Don't... Instead...") naming "view" of resources specifically, not a stylistic alternative — an experienced implementer would restructure this.
- **Current expression:** `ContentLayout` → `Header variant="h1"` → `Table variant="container"`.
- **Native expression:** Drop `ContentLayout`; use `Table variant="full-page"` with the table's own `Header variant="awsui-h1-sticky"`. Full realization also pairs with `contentType="table"` on the app's `AppLayout` (`src/App.tsx`), which is a single instance shared across many other routes (SpendDashboard, BudgetsAdminShell, InferenceProfiles, etc.) — that shared instance sits outside this bounded surface, so this is named as a real dependency rather than assumed away.
- **Why it matters:** Two independent authoritative pages give the same explicit instruction for exactly this scenario, and Content Layout's own docs single out "view" of resources as prohibited — this is the specific composition Cloudscape documents as wrong for this job, and it forfeits the full-page variant's sticky-header/density behavior built for many-column tables.
- **Boundary check:** This is about which page-structure/table-variant concept Cloudscape composes for a full-page resource table, not whether `ContentLayout` or `Table` are each implemented correctly (both are used validly per their own APIs).
- **Authority strength:** REQUIRED

### Finding 2: Modal used for per-row activity drill-in while browsing the identities table

- **Type:** combined component + pattern
- **Materiality:** medium
- **Confidence:** medium
- **User task:** While scanning the Identities table, check a specific principal's recent activity/audit history for context — plausibly for several rows in turn — without losing the table.
- **Repository evidence:** `Identities.tsx` lines 267–274 (the "Activity" row action sets `activityPrincipal`), lines 281–287 (conditionally renders `PrincipalActivityModal`). `PrincipalActivityModal.tsx`: a `Modal` (`size="large"`) wrapping the shared `ActivityTable` (`tableVariant="borderless"`), fetched via `api.listPrincipalActivity`, with no pagination or row cap — its own comment describes it as "the durable log of warnings, enforcement, and identity/budget changes... newest first."
- **Cloudscape evidence:** Split View pattern (cloudscape.design/patterns/resource-management/view/split-view): its stated objectives are "resource identification" and "troubleshooting" — to "quickly view sub-resources or additional attributes" and "check or compare relevant resource details" *while browsing a collection*. Modal docs (cloudscape.design/components/modal): *"Keep the text short and interactions to a minimum. Try to avoid scrolling content,"* and modals are not meant as substitutes for split panels for content-heavy needs.
- **Applicability argument:** (1) Task match: the user is mid-browse of the Identities collection and wants contextual detail on one resource without leaving that context — split view's exact stated purpose, not a shape-only match. (2) Current implementation solves that same problem (per-principal activity detail). (3) A split panel rendering the same `ActivityTable` for the selected row preserves the identical task and data. (4) Weaker than Finding 1: nothing forbids modals outright here, and this rests on converging guidance ("avoid scrolling content" + split view's stated browsing/troubleshooting purpose) rather than one explicit rule naming this exact scenario.
- **Current expression:** Clicking "Activity" sets local state and mounts a `Modal` containing the unbounded `ActivityTable`, with its own loading/error handling, fully occluding the Identities table underneath.
- **Native expression:** A `SplitPanel` bound to the selected principal, rendering the same `ActivityTable` (borderless, as already used) as its content, keeping the Identities table visible/interactive and letting the user switch principals without a close/reopen cycle.
- **Why it matters:** A split panel keeps the underlying table live during the "check several principals in turn" workflow the task implies, and avoids stacking an unbounded, scrolling activity log inside a modal against the component's own "avoid scrolling content" guidance.
- **Boundary check:** This is about which container Cloudscape composes for in-place contextual detail while browsing a collection, not the internal correctness of `Modal` or `ActivityTable`.
- **Authority strength:** RECOMMENDED

## Suppressed (low materiality or weak applicability)

- **No pagination on the Identities table.** The Table View pattern's optional "Pagination" building block recommends showing pagination "even if the resources set fits in one page," but documents no row-count threshold, and the bounded surface gives no evidence of expected identity volume. Suppressed as low-confidence; largely downstream of Finding 1 (adopting the full-page variant would naturally reopen this question).
- **`severity-high`/`severity-medium` Badge colors used for principal-type categorization** (`Principal.tsx`), rather than literal severity. Badge is the confirmed-correct component for this categorization job (see Orientation notes); which specific color token is picked within an already-correct component is a token/semantic question for `cloudscape-implementation-audit`, not a component-selection finding here.

## Orientation notes

- **Lookback-window `Select`** (`Identities.tsx` lines 117–124): a plain `Select` with five fixed relative-range presets (1h/6h/24h/7d/30d), no custom/absolute range. DateRangePicker docs are explicit: *"If a use case does not require users to set a custom absolute or relative range, don't use the date range picker component. Instead, to provide pre-configured relative ranges only, use the select component."* This is exactly that case — confirmed correct.
- **Row actions** (`Identities.tsx` lines 246–277): exactly two actions ("Create budget", "Activity") as inline-link `Button`s in the last column, with `stickyColumns={{first:1,last:1}}` keeping them visible. Matches in-context-actions guidance: *"one or two repetitive actions as a link or icon button"* plus the recommendation to enable sticky columns for row-action visibility.
- **"Create budget" navigates to a dedicated route** (`/budgets?principal=...`) rather than opening a modal — matches Modal guidance's preference for multipage create flows over modal chains/multi-step content.
- **`Badge` in `PrincipalCell`** (`Principal.tsx`) categorizes principal type alongside a text label — matches Badge's documented purpose ("label, categorize, organize"), distinct from `StatusIndicator` (health/status), and satisfies "supplement color with text."
- **`CollectionPreferences`** with `contentDisplayPreference` (column visibility/order) and `wrapLinesPreference` — a correctly composed instance of the table view pattern's preferences building block.

## What was not evaluated

- **Implementation correctness** — `CopyToClipboard`'s `popoverRenderWithPortal` usage, the memoized `accountComparator` sort-identity workaround, any deprecated-prop usage, and a11y mechanics of the raw `<code>`/`<span style={{fontFamily}}>` cells. That is `cloudscape-implementation-audit`'s domain.
- **General UX/product judgment** — information density of 8 columns, whether "Type" (plain text column) duplicates the badge already shown in the Principal cell, copy/wording of descriptions, and whether the 30-day roll-off policy belongs elsewhere in the UI.
- **`ActivityTable`'s other variants** (`self`, `admin`) and the pages that use them (`MyActivity`, `AdminActivity`) — outside this bounded surface, not reviewed.
