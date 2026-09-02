# Case E1 — ApiKeys.tsx (explicit equivalence; isolating case; synthetic)

**Purpose:** pressure-test whether the skill suppresses a replacement
finding when two design-system-native alternatives are genuinely equally
valid for the demonstrated task, per authoritative guidance, with **zero**
repository evidence (comment, test name, variable name, TODO, header copy)
favoring either alternative. This is a cleaner re-instrument of the
retired `case-p1-message-queues` Candidate 2 axis — same authoritative tie
(Cloudscape's filter-patterns criteria table), but with the confounding
header/code-comment language that compromised that case's grading key
removed entirely. See `evals/design-system-native-expression-review/
RESULTS-EQUIVALENCE.md` for why P1 was retired for this purpose.

**Fixture:** synthetic, purpose-built. A `Table`-based collection view of
16 API keys (not `Cards` — deliberately, so no Cards/Table candidate can
arise and dilute the isolation). Two low-cardinality columns
(`environment`: production/staging; `status`: active/revoked), filtered
by a single `TextFilter`. No `ContentLayout` header description beyond a
bare, neutral one-line summary; no code comment anywhere in the file.

**Bounded surface to review:**
- `fixture/src/pages/ApiKeys.tsx` — the entire surface.

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
