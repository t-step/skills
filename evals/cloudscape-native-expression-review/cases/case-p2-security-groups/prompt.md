# Case P2 — SecurityGroups.tsx (real primary issue + independent material secondary issue; isolating case; synthetic)

**Fixture:** synthetic, purpose-built to test whether a genuinely
independent, materially-earned second finding survives once a primary
finding is already established (the mirror image of Case P1). A new
resource type (security groups), structurally distinct from every prior
`ContentLayout`/`full-page` case.

**Bounded surface to review:**
- `fixture/src/pages/SecurityGroups.tsx` — the entire surface. A
  stand-alone resource-inventory table (`Table` + `useCollection` +
  `TextFilter` + `Pagination`) of 28 security groups, wrapped in
  `ContentLayout` with `Table variant="container"`, no other page
  content. Selection is implemented by hand: two raw
  `<input type="checkbox">` elements (a per-row checkbox and a
  page-level "select all" checkbox) driving local component state, paired
  with a header "Delete selected" button — `Table`'s own
  `selectionType`/`selectedItems`/`onSelectionChange` mechanism is never
  used.

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
