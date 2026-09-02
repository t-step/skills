# Case C — WorkspaceDetails.tsx (combined component + pattern issue; synthetic)

**Fixture:** synthetic, purpose-built for this skill's eval.

**Bounded surface to review:**
- `fixture/src/pages/WorkspaceDetails.tsx` — the entire surface. A single
  workspace's details, structured as breadcrumb + header (persistent) and
  a `Tabs` component with three tabs: "Overview" (the workspace's general
  configuration facts, rendered as a one-row `Table`), "Members" (a
  proper multi-row `Table` of users), and "Activity" (a `List`).

**Cloudscape packages declared:**
`@cloudscape-design/components@^3.0.900` (locked `3.0.900`). Lockfile:
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
