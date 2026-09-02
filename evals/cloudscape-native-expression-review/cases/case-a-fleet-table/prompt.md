# Case A — FleetNodes.tsx (right components, wrong pattern; synthetic)

**Fixture:** synthetic, purpose-built for this skill's eval (not a real
third-party repo).

**Bounded surface to review:**
- `fixture/src/pages/FleetNodes.tsx` — the entire surface. A resource
  table (`Table` + `useCollection` + `TextFilter` + `Pagination` +
  `CollectionPreferences`), wrapped in `ContentLayout` with
  `Table variant="container"`. The page's only content is this table —
  no other content blocks, no dashboard tiles, no supplementary text.

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
`skills/cloudscape-native-expression-review/SKILL.md` and is told to
follow it exactly, including its report structure and its bundled
deterministic scripts.

The reviewer (baseline or skill) may fetch whatever `cloudscape.design`
pages it needs to ground its findings.
