# Case B — EndpointScaling.tsx (wrong component, otherwise reasonable composition; synthetic)

**Fixture:** synthetic, purpose-built for this skill's eval.

**Bounded surface to review:**
- `fixture/src/pages/EndpointScaling.tsx` — the entire surface. A
  collection of 22 inference endpoints rendered with `Cards`, each card
  showing identical status/region/invocations/latency/error-rate fields
  plus a "Scale up" action. Page structure (`ContentLayout` + `Header`
  with a task-describing `description`) is otherwise ordinary.

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
