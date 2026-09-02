# Case N1 — AccountSettings.tsx (inverse control: materially non-equivalent; isolating case; synthetic)

**Purpose:** the inverse control for cases E1/E2. Tests whether the
skill still reports a real, materially-grounded finding when two
alternatives are both officially supported but Cloudscape's own guidance
states a concrete, checkable differentiator — and whether the anti-
fundamentalism/equally-valid-suppression discipline has been
over-generalized into suppressing findings that shouldn't be suppressed.

**Fixture:** synthetic, purpose-built. An "Account settings" surface
with two boolean settings rendered as `Checkbox`, each wired directly:
`onChange` calls `setState` **and** an immediate `fetch('/api/account/
settings', { method: 'PATCH', ... })` in the same handler. There is no
`<form>` submit boundary, no `Button` of any kind, and no save/confirm
affordance anywhere in the file — the only way these settings are
persisted is the immediate `PATCH` call inside `onChange`.

**Bounded surface to review:**
- `fixture/src/pages/AccountSettings.tsx` — the entire surface.

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
