# Case E2 — CreateBackupSchedule.tsx (non-obvious equivalence; isolating case; synthetic)

**Purpose:** pressure-test the same equally-valid-suppression axis as
Case E1, but through a pair of alternatives that look and interact quite
differently (`RadioGroup`'s compact list of radio buttons vs. `Tiles`'
larger, selectable-box grid) rather than one literal "same cell of a
table" sentence. Correctly suppressing the replacement finding here
requires reconciling **two different Cloudscape criteria tables** on the
same corpus page (`patterns/general/selection`) — a "Boolean selection
criteria" table that ties `RadioGroup` and `Tiles` on every row, and a
separate "Single selection criteria" table that differentiates them by
metadata richness (descriptions/lists/images) for the general 2-7-option
case. The fixture is deliberately built so the *correct* table to apply
is the boolean one (a plain, metadata-free, form-submission-scoped
on/off choice) — recognizing that, instead of reflexively reaching for
the differentiating single-selection table, is the reconciliation this
case tests.

**Fixture:** synthetic, purpose-built. A "Create backup schedule" form
(`Form` + `Container` + `FormField`s, explicit `Submit`/`Cancel`
actions) containing one boolean, mutually-exclusive, plain-text
`RadioGroup` ("Keep only the latest backup" / "Keep full backup
history") alongside two unrelated, non-scoring fields (name, frequency).
No field carries icons, descriptions, or list/image metadata. No code
comment anywhere in the file.

**Bounded surface to review:**
- `fixture/src/pages/CreateBackupSchedule.tsx` — the entire surface.

**Cloudscape packages declared:**
`@cloudscape-design/components@^3.0.900` (locked `3.0.900`),
`@cloudscape-design/collection-hooks@^1.0.60`. Lockfile:
`fixture/package-lock.json`.

## Task given to the reviewer, verbatim (baseline framing)

> Review this bounded Cloudscape frontend surface for material
> opportunities to express the same user task more natively using
> Cloudscape's documented components and patterns. Ground every
> recommendation in code and authoritative Cloudscape guidance. Avoid
> implementation defects and generic UX critique.

## Task given to the skill run

Same fixture and surface. The skill run receives
`skills/design-system-native-expression-review/SKILL.md` and is told to
follow it exactly, including its report structure and its bundled
deterministic scripts (`--package-prefix '@cloudscape-design/'`).

The reviewer may fetch whatever `cloudscape.design` pages it needs to
ground its findings.
