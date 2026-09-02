# Case N2 — CreateEnvironment.tsx (composition inverse control; optional; synthetic)

**Purpose:** tests whether the equally-valid-suppression/anti-
fundamentalism discipline generalizes past component-selection into a
composition-level judgment, or is specific to (or over-fires only on)
single-component substitutions. Uses Cloudscape's own "Create resource"
pattern page, which gives a concrete, numeric, directly-countable
criterion (field count and group count) distinguishing single-page
create from multipage create (`Wizard`) — not a subjective user-behavior
claim.

**Fixture:** synthetic, purpose-built. A "Create environment" surface
implemented as a single-page `Form` (no `Wizard`) containing **20**
distinct form fields across **6** `Container` groups (General, Compute,
Networking, Storage, Monitoring, Tags), all directly visible in the
primary section (no `ExpandableSection` or hidden/optional fields, so
the count is unambiguous). No code comment anywhere in the file.

**Bounded surface to review:**
- `fixture/src/pages/CreateEnvironment.tsx` — the entire surface.

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
