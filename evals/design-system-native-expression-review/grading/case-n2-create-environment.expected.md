# Grading key — Case N2: CreateEnvironment.tsx (composition inverse control, optional)

## Designed intent

Tests whether the equally-valid-suppression/anti-fundamentalism
discipline generalizes to a composition-level judgment (single-page
create vs. multipage create/`Wizard`), using a concrete, directly
countable numeric criterion rather than a subjective user-behavior claim
— and whether a real, well-evidenced composition finding still gets
reported rather than swept up in general suppression caution.

## Candidate — single-page `Form` used for a 20-field, 6-group creation flow instead of multipage create (`Wizard`)

**Verdict: MUST REPORT.**

- **Repository evidence establishing task/user intent (item 1):**
  `CreateEnvironment.tsx` is a single, non-`Wizard` `Form` containing six
  `Container` groups (General, Compute, Networking, Storage, Monitoring,
  Tags) and 20 distinct form fields, all directly visible in the primary
  section with no `ExpandableSection` or hidden/optional content:
  General (3: name, description, region), Compute (4: instance type,
  instance count, autoscaling min, autoscaling max), Networking (4: VPC,
  subnet, security group, public IP checkbox), Storage (3: volume type,
  volume size, encryption checkbox), Monitoring (3: detailed monitoring
  checkbox, log retention, alert email), Tags (3: owner, cost center,
  environment tag). Total: 20 fields, 6 groups, both directly countable
  from the file with no ambiguity about what counts as "primary section"
  content.
- **Authoritative evidence establishing the differentiator (item 2):**
  Cloudscape's `/patterns/resource-management/create/index.html.md` page
  (live-verified 2026-09-02), "Length" criteria row: single-page create
  — **"Between 2 and 15 fields in the primary section or up to 5 groups
  of settings"**; multipage create — **"More than 16 fields in primary
  sections or more than 5 groups of settings."** Supporting prose: "Use
  the multipage create, which employs the wizard component, when you
  want users to create resources by completing a set of interrelated
  tasks. We recommend multipage create for long or complex
  configurations."
- **Evidence that could reasonably be read in the opposite direction
  (item 3):** A reviewer could argue the six groups are not "interrelated
  tasks" but independent, unordered settings sections, so a wizard's
  step-by-step sequencing doesn't fit. This should be named and weighed,
  but does not overturn the verdict: the cited Length criterion is framed
  as a standalone numeric threshold ("Between 2 and 15... or up to 5
  groups" / "More than 16... or more than 5 groups"), not conditioned on
  interrelatedness, and this fixture clears *both* thresholds
  independently (20 > 16 fields; 6 > 5 groups) — the same "two
  independent, quantified criteria both point the same direction" shape
  the retired P1 case's own Candidate 1 grading key treated as
  sufficient materiality on its own.
- **Why the expected result does not depend on hidden grader
  interpretation (item 4):** Grounded in a live-fetched, directly
  countable numeric threshold from Cloudscape's own create-pattern page,
  applied to a fixture whose field/group counts are unambiguous and
  independently verifiable by a reader (no field is hidden, deferred, or
  conditionally rendered).
- **Would removing any single fixture comment or prose annotation change
  the expected result (item 5)?** **No** — there is no comment anywhere
  in this fixture. The finding rests entirely on the countable structure
  (20 fields, 6 `Container`s), not on any comment or prose describing the
  fields as numerous or complex.

**Acceptable outcomes:** reporting a `documented composition` or
`combined selection + composition` finding recommending `Wizard`/
multipage create in place of the single-page `Form`, at `medium`-to-
`high` materiality, citing the Length criterion (`RECOMMENDED` authority
strength — the page states this as guidance, not an absolute
prohibition). **Not acceptable:** suppressing this candidate as "just
another valid way to lay out a form," or hedging it as
`intent-dependent` without naming a specific, evidenced reason the
interrelatedness objection in item 3 should override two independently-
clearing numeric thresholds.

## What would be wrong, summarized

- **Suppressing or hedging this finding** — the over-suppression failure
  this optional case exists to detect at the composition level.
- **Missing the candidate entirely** (recall failure).
- **Fabricated or non-verbatim quotation** — graded separately under
  citation fidelity, never folded into the materiality verdict above.
