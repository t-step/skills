# Grading key — Case N1: AccountSettings.tsx (inverse control)

## Designed intent

The inverse control for E1/E2: two alternatives (`Checkbox`, `Toggle`)
are both officially supported Cloudscape components, but the design
system's own guidance states a concrete, checkable differentiator, and
this fixture's repository evidence unambiguously satisfies that
differentiator. Tests whether the equally-valid-suppression discipline
has been over-generalized into suppressing findings that are actually
material — the failure mode this task brief calls "over-suppression."

## Candidate — `Checkbox` used for immediate-effect settings instead of `Toggle`

**Verdict: MUST REPORT.**

- **Repository evidence establishing task/user intent (item 1):**
  `AccountSettings.tsx`'s two settings (`requireTwoFactor`,
  `emailNotifications`) are each rendered as `Checkbox`, and each
  `onChange` handler calls `setState` **and** `updateAccountSetting`,
  which issues an immediate `fetch('/api/account/settings', { method:
  'PATCH', ... })` in the same handler. There is no `<form>` element, no
  `Button` of any kind, and no separate save/submit/confirm step anywhere
  in the file — the PATCH call inside `onChange` is the *only* mechanism
  by which these settings are persisted. This is unambiguous, structural,
  code-level evidence of immediate effect, independent of any comment or
  copy (there is none in this fixture).
- **Authoritative evidence establishing the differentiator (item 2):**
  Cloudscape's `/patterns/general/selection/index.html.md` page
  (live-verified 2026-09-02), "Boolean selection criteria" table,
  "Selection" row: **"The selection takes effect at form submission"**
  (`Checkbox`) vs. **"The selection results in an immediate change. For
  example, turning on dark mode."** (`Toggle`). Supporting prose, same
  page: "Binary choices made by using checkboxes, radio groups, and
  tiles should take effect at form submission, for example in a creation
  or edit flow. Use a toggle for an option that takes effect immediately,
  such as turning on a system feature that results in a visible interface
  change, for example, turn on dark mode." This is a stated, directional
  criterion — not a same-tier tie — with `Checkbox` and `Toggle` on
  opposite sides of it.
- **Evidence that could reasonably be read in the opposite direction
  (item 3):** A reviewer could argue the `fetch` call might be
  best-effort/optimistic and the "real" save could still happen
  elsewhere, or that a future confirmation step is planned. This fixture
  forecloses that reading deliberately: there is no confirmation dialog,
  no pending/loading state gating a separate commit action, and no other
  file or route referenced from this surface — the PATCH is issued
  unconditionally and synchronously with the checkbox toggle, with
  nothing else in the bounded surface suggesting a deferred commit step.
  A response may still narrate this consideration and dismiss it (that is
  good practice), but dismissing it is not required for a MUST-REPORT
  verdict, since the code structure alone (no `<form>`, no `Button`, no
  submit-shaped affordance anywhere) already independently establishes
  immediate effect.
- **Why the expected result does not depend on hidden grader
  interpretation (item 4):** Grounded in the same live-fetched Cloudscape
  table used for E2, applied in the opposite direction it's designed to
  support — the table states a directional criterion, this fixture's
  code satisfies the `Toggle` side of it unambiguously, and SKILL.md's
  own anti-fundamentalism rule explicitly preserves this outcome: "when...
  evidence genuinely independent of the tied table establishes a
  meaningful native-expression advantage specific to the observed task,
  the finding still stands." Suppressing this candidate on general
  "equally valid" grounds would misapply the equivalence discipline to a
  case that isn't tied.
- **Would removing any single fixture comment or prose annotation change
  the expected result (item 5)?** **No** — there is no comment or prose
  annotation of any kind in this fixture beyond component labels
  ("Require two-factor authentication for sign-in",
  "Send email notifications for account activity") and the `Header`
  title/variant, none of which name "immediate effect" or reference
  Toggle/Checkbox at all. The finding rests entirely on the code
  structure (bare `onChange` → `fetch`, no form/submit boundary), not on
  any comment written to force the answer.

**Acceptable outcomes:** reporting a `component selection` finding
recommending `Toggle` in place of `Checkbox` for one or both settings, at
`medium`-to-`high` materiality, citing the Boolean-selection-criteria
table's "Selection" row (`RECOMMENDED`-or-stronger authority strength,
since the page states this as the defining criterion for each
component's fit, not one alternative among unranked others). **Not
acceptable:** suppressing this candidate as "equally valid," reporting it
only as `intent-dependent` without naming why intent is actually resolved
here, or omitting it silently.

## What would be wrong, summarized

- **Suppressing or hedging this finding as equally valid / intent-
  dependent** — the specific over-suppression failure this case exists to
  detect. The Boolean-selection-criteria table's "Selection" row is a
  stated directional criterion, not a tie; nothing about this fixture
  resembles the same-tier shape that legitimately triggers suppression in
  E1/E2.
- **Missing the candidate entirely** (recall failure).
- **Fabricated or non-verbatim quotation** — graded separately under
  citation fidelity, never folded into the materiality verdict above.
