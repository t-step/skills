# Case A2 — ApiKeys.tsx (equally valid composition; precision control; synthetic)

**Fixture:** synthetic, purpose-built for a hardening iteration on this
skill (not a real third-party repo). Superficially similar to Case A1
(`Table` + `ContentLayout` + `Table variant="container"`, a header,
filtering, pagination).

**Bounded surface to review:**
- `fixture/src/pages/ApiKeys.tsx` — the entire surface. A small settings
  table (`Table` + `useCollection` + `TextFilter` + `Pagination`) of a
  service owner's own API keys, wrapped in `ContentLayout` with
  `Table variant="container"`, a header description paragraph, and a
  "Create API key" header action. Four columns, eight rows.

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
