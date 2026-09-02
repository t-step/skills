# Grading key — Case F: QuotaRequests.tsx (missing intent)

## Designed intent

The Modal shows a genuinely medium-detail field set (6 fields) for a
resource with a status lifecycle and one action — evidence that could
plausibly support either of two readings, deliberately balanced rather
than leaning toward one:

- **Reading 1 — Modal is fine as-is.** Quota requests are transient,
  resolved-and-forgotten records (approved/denied ones have no further
  action at all); nothing else in the app deep-links to one; the field
  count and interaction (glance, maybe withdraw, dismiss) is squarely
  within Modal's documented supported shape (no tabs, no expandable
  sections, no chained modal — every Modal "Don't" is respected).
- **Reading 2 — this should be a details page.** The resource has a
  persistent identity (`id`), a status lifecycle, and an action tied to
  that lifecycle — the same shape real, addressable resources have
  elsewhere in this fixture family (e.g., Case E's certificates).

Neither reading is contradicted by the code; the code was deliberately
built not to settle it (no per-request route either way, no copy stating
whether users would want to revisit or share a link to one specific
request, no cross-page reference to an individual request).

## What a correct response looks like

**`Type: intent-dependent`, reported or explicitly named rather than
silently guessed.** The response should name both plausible readings
(transient/resolved-and-forgotten vs. persistent/addressable resource),
name what evidence would resolve it (e.g., "whether requests are ever
revisited/linked-to after submission, or a routing/permalink convention
elsewhere in the app for similar transient records"), and not assert a
confident recommendation either direction. Suppressing the candidate
entirely (not mentioning it at all) is also an acceptable, correct
outcome per SKILL.md's "Missing intent" section — the failure mode this
case exists to catch is a *confident, unsupported* recommendation, not
under-reporting.

## What would be wrong

- **A confident recommendation to convert this to a details page** (or
  the reverse — confidently asserting Modal is correct with no
  acknowledgment of the alternative reading): this is exactly the
  "confident recommendation despite missing user intent" failure mode.
  Grade D regardless of which direction is chosen, since the applicability
  argument for either reading requires product intent the code doesn't
  supply — a response that picks one anyway is asserting more certainty
  than the evidence supports.
- **Treated as a clear Modal-composition violation** (e.g., misreading
  this as resembling Case E's rejected split-view temptation, or
  misapplying Modal's "avoid tabs/expanded sections" Don't — neither
  applies here, since this Modal has no tabs or expandable sections):
  factually wrong regardless of directional confidence, grade E.
