# Case A3 — Endpoints.tsx (semantic pattern match requiring inference; synthetic)

**Fixture:** synthetic, purpose-built for a hardening iteration on this
skill (not a real third-party repo). Unlike Case A/A1, the source
carries no comment describing the page's intended task — the user task
must be inferred from the route/page name, header copy, header action,
column set, and data shape. The composition also includes a header
description paragraph and a "Create endpoint" header action, which A/A1
do not have.

**Bounded surface to review:**
- `fixture/src/pages/Endpoints.tsx` — the entire surface. A resource
  table (`Table` + `useCollection` + `TextFilter` + `Pagination` +
  `CollectionPreferences`) of every inference endpoint in the account,
  wrapped in `ContentLayout` with `Table variant="container"`, a header
  description, and a "Create endpoint" header action. Six columns,
  twenty-six rows, one discrete-valued column (`status`).

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
