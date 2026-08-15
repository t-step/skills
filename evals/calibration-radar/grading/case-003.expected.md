# Expected outcome — case-003 (locally-evidenced-strength + repeated-friction)

**What this fixture tests:** two specific classifications, and getting the
direction of "who was first" right.

## Selection

Should select 1, 2, and 4 (evidence-before-verdict guidance, abstention
special issue, GitHub review round-trip data) as strong signals — each
formalizes/converges on something, and both 1+2 point the same direction.
Item 3 (flaky test quarantine) is a legitimate but more ordinary
engineering-practice item — fine to include or leave out on its own merit,
shouldn't be the centerpiece either way. Items 5 (product launch) and 6
(routine linter update) should be excluded as noise.

## Local correlation and classification

- **Items 1 and 2** (evidence-before-verdict / abstention) → should cite
  slice-review's 2026-08-03 decisions and classify as **Locally evidenced
  strength** — critically, the response should notice and state that the
  local decision (2026-08-03) *predates* both external items (2026-06-20,
  2026-07-02)... actually check the fixture dates carefully: the external
  items are dated in June/July, the local decision is dated 2026-08-03,
  which is *after* both. A careful response should get this ordering
  right from the dates given (local decision came after the external
  items, not before) — this cell exists to check the response reasons
  from the actual dates in the fixtures rather than assuming "locally
  evidenced strength" always means the user got there first. Given the
  dates as provided, treating this as **Formalization gap** or as
  **Locally evidenced strength that happens to postdate two similar
  external pieces** (i.e., convergent, not necessarily causally prior) are
  both acceptable, provided the response reasons about the dates rather
  than ignoring them or asserting an ordering the fixture doesn't support.
- **Item 4** (GitHub review round-trip data) → should cite the case-105
  issue and the Valence whole-branch-review decision as **Repeated local
  friction** — two independent, real instances (different projects) of a
  single-pass review missing something a later pass caught. This is the
  strongest classification match in the fixture and should be treated as
  such (e.g., called out prominently in the summary, per SKILL.md's
  guidance to surface a materially strong correlation rather than bury
  it).
- **Item 3** (flaky test quarantine), if selected → no local evidence
  found.

## What would be a real failure here

- Ignoring the case-105 and Valence evidence and just saying "no local
  match" for item 4 — that would bury the strongest correlation in the
  fixture.
- Asserting the user's local practice predates the external items without
  checking the actual dates given.
- Treating the product-launch item (5) as a real signal.
