# Baseline review: WorkspaceDetails.tsx

## Inferred user task

A user lands on a single workspace's details page to (1) glance at the workspace's own general configuration (name, owner, region, plan, created date, status) — stable facts that don't belong to any particular sub-view — and (2) drill into two related collections scoped to that workspace: its members and its recent activity. The file's own comment (lines 30-33) states this intent explicitly: the general-configuration facts are "relevant no matter which tab a user is currently looking at."

## Findings

### Finding 1: Single-row `Table` used to render workspace properties should be `KeyValuePairs`

**Evidence**: Lines 73-89. The Overview tab renders a `Table` whose `columnDefinitions` map one property to one column (Name, Owner, Region, Plan, Created, Status) and whose `items` is a single-element array (`[{}]`) with a synthetic `trackBy`. This is a table being forced to hold exactly one row of unrelated scalar facts, not a collection of comparable items.

**Cloudscape source**: `https://cloudscape.design/components/key-value-pairs/` — "Key-value pairs are lists of properties (labels) followed by their corresponding values." Its recommended value types explicitly include "Status indicator: For example, to show the status of a task, failed or successful," which matches the `StatusIndicator` currently embedded in a table cell at line 83. By contrast, Table's own usage guidance (`https://cloudscape.design/components/table/?tabId=usage`) is built entirely around collections — "Only use filtering, pagination, and sorting if there are more than five items," "Only use selection if the user can take action on the items in the collection" — none of which apply to a fixed one-row property grid.

**Why it matters**: `KeyValuePairs` is the component Cloudscape defines for exactly this data shape (label → value, including a status value), while `Table` carries a full contract (row identity, `trackBy`, selection/sort/pagination affordances) that is meaningless for a single synthetic row and is only being satisfied here with placeholder values (`trackBy={() => 'workspace-overview-row'}`).

### Finding 2: General configuration should not be a tab at all — it belongs in the details-page "summary container," with `Tabs` reserved for Members/Activity

**Evidence**: Lines 62-120. All three of Overview, Members, and Activity are modeled as `Tabs` entries, even though the code's own comment (lines 30-33) distinguishes Overview as page-level, always-relevant configuration, unlike Members/Activity which are tab-appropriate sub-views.

**Cloudscape source**: `https://cloudscape.design/patterns/resource-management/details/details-page/` defines building block D, "Details summary container: Place the most relevant information about the resource in this container. To organize content, use key-value pairs," and prescribes its title text: "For the details summary container, use this text: *General configuration* / *[Resource type] settings*." The companion pattern `https://cloudscape.design/patterns/resource-management/details/details-page-with-tabs/` reinforces this with an explicit Don't: "Don't introduce tabs if you can group your content into meaningful sections on a Details page. The number of sections is not an indicator of whether to use tabs."

**Why it matters**: The documented details-page anatomy already has a named slot for exactly this content (a persistent summary container above/alongside tabs), and the docs explicitly warn against using tabs merely because there's more than one section. Moving Overview out of `Tabs` into a `Container` titled "General configuration" (using `KeyValuePairs`, per Finding 1) would make the general configuration visible regardless of which tab is active — matching what the code comment already says is the intended behavior — and would leave `Tabs` holding only the two genuinely tab-appropriate, mutually exclusive collections (Members, Activity), consistent with Tabs' own guidance to "use tabs for organizing discrete blocks of information."

### Finding 3: Activity entries collapse actor/action/timestamp into an opaque string instead of following Cloudscape's timestamp pattern

**Evidence**: Lines 24-28 and 112-117. Each `ACTIVITY` entry is a single pre-formatted string, e.g. `'Priya Nair updated the workspace plan to Team (2 hours ago)'`, rendered as plain `List` item content via `renderItem`.

**Cloudscape source**: `https://cloudscape.design/patterns/general/timestamps/` specifies a structured label pattern for exactly this kind of feed entry: "Use the format: *[label] [timestamp] by [name]*. The name is the user or service that made the change. For example: *Template edited 6 hours ago by plrs*," with labels following "*[Noun] [verb]*" (e.g., "Template edited"). It also requires, under accessibility guidelines, that relative timestamps be wrapped so the absolute time remains available: "Wrap the relative timestamp in a `<time>` element and set the `datetime` attribute to the absolute human-readable timestamp... Set the `<time>` element's `title` attribute to the absolute human-readable timestamp, which allows users to hover over the timestamp."

**Why it matters**: The current entries already follow the doc's semantic content shape (actor, verb-phrase, relative time) but bake it into one undifferentiated string rather than the label/timestamp/source structure the pattern defines — losing the ability to render the timestamp as a distinguishable, hoverable, accessible element with its absolute-time equivalent, which is the specific native affordance this documented pattern exists to provide for activity/history feeds.

## Not flagged (considered, not material)

- The header's `Edit`/`Delete` action buttons (lines 48-55) match the details-page pattern's building block C exactly ("Header or global buttons — Use when the actions will affect the entire resource. For example: Edit or Delete"), so no finding there.
- Using `List` for the Activity feed itself is consistent with List's guidance ("Use a list to display two or more items... vertically"); the finding is about the entries' internal structure (Finding 3), not the component choice.
- The two-level breadcrumb (`Workspaces > eng-platform-prod`, lines 41-47) is one level short of the details-page pattern's documented three-level example (`[Service name] > [Resources type] > [Resource name/ID]`), but this fixture doesn't show enough of the surrounding app to confirm a service-name level is missing rather than absent by design, so this is not raised as a standalone finding.
