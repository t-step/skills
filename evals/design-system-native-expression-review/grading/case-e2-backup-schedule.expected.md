# Grading key — Case E2: CreateBackupSchedule.tsx (non-obvious equivalence)

## Designed intent

Tests the same equally-valid-suppression axis as E1, but through a pair
of Cloudscape components that look and interact quite differently
(`RadioGroup` vs. `Tiles`) and whose equivalence is **not** stated in one
literal sentence — it requires reconciling two different criteria tables
on the same page (`patterns/general/selection`) and recognizing which one
actually governs this fixture's shape. This is intentionally less
mechanically obvious than E1.

## Candidate — `RadioGroup` alone vs. replacing it with `Tiles` for "Retention policy"

**Verdict: MUST SUPPRESS.**

- **Repository evidence establishing task/user intent (item 1):**
  `CreateBackupSchedule.tsx`'s "Retention policy" field is a two-option,
  plain-text `RadioGroup` (`"Keep only the latest backup"` /
  `"Keep full backup history"`) inside a `Form` with explicit
  `Submit`/`Cancel` actions — the selection only takes effect when the
  operator clicks "Create schedule." Neither option carries a
  description, icon, list, or image. Nothing in the file states or
  implies a need for more visual prominence, additional per-option
  metadata, or any reason the choice should be presented as tiles rather
  than radio buttons.
- **Authoritative evidence establishing equivalence (item 2):**
  Cloudscape's `/patterns/general/selection/index.html.md` page
  (live-verified 2026-09-02) contains a **"Boolean selection criteria"**
  table (governing on/off, two-option choices) that ties `RadioGroup` and
  `Tiles` on every row relevant here: "Selection" — both **"The selection
  takes effect at form submission"** (matching this fixture's Submit-
  gated form exactly); "Additional metadata" — both **"can be included
  for both the on and off options"** (a *capability* both share, not a
  requirement either needs). No row in this table ranks one over the
  other for a plain boolean choice.
- **Evidence that could reasonably be read in the opposite direction
  (item 3):** The same page's separate **"Single selection criteria"**
  table (governing the general 2-7-option case, not specifically
  boolean) differentiates `RadioGroup` ("descriptions") from `Tiles`
  ("descriptions, lists, or images") by metadata richness — a reviewer
  could reach for this table instead and conclude `Tiles` is "more
  capable" in the abstract. This is the reconciliation trap the case is
  built to test. It must be rejected on two independent grounds: (a) this
  fixture's choice is specifically boolean and form-submission-scoped, so
  the boolean-selection table — which ties the two — is the one that
  actually governs it, not the general single-selection table; and (b)
  even under the general table's own logic, `Tiles`' documented rationale
  ("Use for selections that require additional metadata to compare
  mutually exclusive options") does not apply, because this fixture's two
  options carry no metadata of any kind to compare — `Tiles`' advantage is
  conditional on a need this surface does not demonstrate.
- **Why the expected result does not depend on hidden grader
  interpretation (item 4):** Grounded in Cloudscape's own live-fetched
  "Boolean selection criteria" table text and SKILL.md's own point-4
  same-tier-equivalence rule ("a decision table... places the current
  implementation and the proposed alternative in the same documented
  tier... point 4 fails: suppress the candidate or reclassify it
  `intent-dependent`"). The reconciliation in item 3 is not a judgment
  call invented for this grading key — it follows directly from which
  table's stated scope (boolean vs. general single-selection) actually
  matches this fixture's demonstrated shape (two plain, mutually-
  exclusive, metadata-free, submission-gated options).
- **Would removing any single fixture comment or prose annotation change
  the expected result (item 5)?** **No** — there is no comment in this
  fixture. The only prose is the two `RadioGroup` item labels
  themselves, which are load-bearing for establishing this is a plain,
  metadata-free boolean choice (removing them would remove the fixture's
  content, not a fixture *comment*), and the `Header` title ("Create
  backup schedule"), which carries no filtering/selection-preference
  language to remove.

**Acceptable outcomes:** omitted entirely; named as a suppressed/
orientation-note candidate; or reported as `intent-dependent` if a
response genuinely cannot resolve which of the two selection-criteria
tables governs (though the fixture is designed so this should be
resolvable, not left ambiguous). **Not acceptable:** reporting `Tiles` as
a replacement for `RadioGroup` at any materiality/confidence level, with
or without a metadata-richness justification that the fixture does not
actually supply.

## What would be wrong, summarized

- **Reporting the `Tiles` candidate** at any confidence/materiality
  level.
- **Applying the single-selection table's metadata-richness
  differentiation to this specifically-boolean, metadata-free fixture**
  without naming and resolving the boolean-selection table's tie first —
  a report-side failure identical in kind to reporting the candidate
  outright, since it manufactures directionality from a table whose own
  stated scope (2-7 general options) doesn't cleanly cover a plain
  on/off choice already governed by the tied table.
- **Fabricated or non-verbatim quotation** — graded separately under
  citation fidelity, never folded into the materiality verdict above.
