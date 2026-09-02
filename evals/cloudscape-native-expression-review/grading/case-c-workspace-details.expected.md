# Grading key — Case C: WorkspaceDetails.tsx (combined component + pattern issue)

## Designed intent

Two individually-describable issues that are really one underlying
recommendation:

1. **Component-level**: the workspace's general-configuration facts
   (name, owner, region, plan, created date, status — six simple
   properties of one resource) are rendered as a one-row `Table`, when
   `KeyValuePairs` is the component built for exactly this job (per the
   details-page pattern's own instruction to *"use key-value pairs to
   organize content"* in the details summary container).
2. **Pattern-level**: those facts live *inside* the "Overview" tab
   instead of the persistent summary container the details-page-with-tabs
   pattern documents — *"this section serves as a summary that is always
   visible when users switch between the tabs"* / *"important information
   that applies to tasks in all the tabs."* Right now, switching to
   "Members" or "Activity" hides the workspace's own identity/status
   entirely.

The "Members" table and the "Activity" list are correctly-scoped,
deliberately unremarkable controls (false-positive material — a
per-tab table of a genuinely multi-row, filterable-in-the-future
resource is exactly what tabs are for).

## What a correct response looks like

**One finding, `Type: combined component + pattern`, high materiality** —
not two separate findings at two abstraction levels. The single
recommendation: pull the general-configuration facts out of the
"Overview" tab entirely, render them as `KeyValuePairs` in the details
summary container above/outside the `Tabs` (persistent across tab
switches), and let the remaining tabs hold only what's genuinely
tab-scoped (Members, Activity — possibly folding a leaner "Overview" tab
in if there's tab-specific content left, or dropping the Overview tab if
there isn't).

- Cites both the component fit (`KeyValuePairs`'s stated purpose: "lists
  of properties followed by their corresponding values") and the pattern
  structure (details-page-with-tabs' persistent-summary-container
  language + "Don't use tabs for hubs, navigation, steps, or containers
  that link the users to other pages" is not directly hit, but "always
  visible when switching tabs" is the operative rule the current
  structure violates by omission — the facts are *not* always visible).
- Applicability argument: this is a single resource (not a collection),
  the facts are simple scalar properties, and they're read on every tab
  visit implicitly (a user checking Members still wants to know which
  workspace they're looking at) — this is exactly the persistent-summary
  use case the pattern names.
- Boundary check: this is pattern/component alignment, not implementation
  correctness (the one-row `Table` and the `Tabs` are both mechanically
  valid Cloudscape usage) and not general UX ("it's confusing to lose
  context when switching tabs" would be the generic-UX-sounding version
  of this same observation — the response should ground it in the
  pattern's explicit persistence rule instead, not merely usability
  intuition).

## What would be wrong

- **Two separate findings** (one for the Table→KeyValuePairs swap, one
  for the tabs-persistence structure): this is exactly the "duplicated
  one issue across abstraction levels" failure mode `SKILL.md`'s
  `combined component + pattern` type and the rubric's question 8 exist
  to catch.
- **Only the component-level half reported** (Table → KeyValuePairs, with
  no mention of where it should live relative to the tabs): correct as
  far as it goes, but misses that the *placement* is equally material —
  moving to KeyValuePairs while leaving it inside the Overview tab would
  not actually fix the "hidden on other tabs" problem.
- **A finding on the Members or Activity tabs**: false positive — these
  are correctly-scoped, ordinary tab content and should not be flagged.
