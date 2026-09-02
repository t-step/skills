# Case P1 — MessageQueues.tsx (real primary issue + seductive equally-valid alternative; isolating case; synthetic)

**Fixture:** synthetic, purpose-built to test candidate-suppression
discipline specifically (not recall, not general applicability). Not
structurally identical to any prior case: a `Cards`-based collection
view (not `Table`), a new resource type (message queues), a new
secondary temptation axis embedded in the same file.

**Bounded surface to review:**
- `fixture/src/pages/MessageQueues.tsx` — the entire surface. A
  collection view of 24 message queues rendered with `Cards` +
  `useCollection` + `TextFilter` + `Pagination`, wrapped in
  `ContentLayout`. The page's header description states the task
  explicitly: comparing throughput and backlog age across all queues to
  decide which need scaling attention. Two discrete-valued columns
  (`status`: healthy/backlogged; `region`: us-east-1/us-west-2), the rest
  numeric.

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
