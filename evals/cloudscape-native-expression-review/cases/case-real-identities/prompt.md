# Case Real — Identities.tsx (real, unmodified, pinned-SHA fixture)

**Fixture:** `aws-samples/sample-bedrock-spend-budget-guardrails`, pinned
SHA `588b62598a842896583d1ef516ae38597e00dc4e`, cloned read-only at
`/Users/thomasestep/Developer/cloudscape-eval-fixtures/sample-bedrock-spend-budget-guardrails/`
(see `evals/design-system-calibration/SETUP.md` for full provenance and
reclone commands). Not copied into this repo — read from that checkout
directly, and do not modify it.

**Bounded surface to review:**
- `web/src/pages/Identities.tsx` (+ `web/src/components/Principal.tsx` and
  `web/src/components/PrincipalActivityModal.tsx`, which it composes) — a
  collection/resource page: a table of distinct Bedrock callers with
  filtering/preferences and row-level drill-in via a modal.

**Cloudscape packages (declared):**
`@cloudscape-design/components@^3.0.1340` (locked `3.0.1340`),
`@cloudscape-design/collection-hooks@^1.0.55`,
`@cloudscape-design/global-styles@^1.0.45`. Frontend root: `web/`.

**Why this surface is reused from `cloudscape-implementation-audit`:**
its iteration-2 eval ran the frozen implementation-audit skill against
this exact surface and produced a `violation`-classified finding
recommending `Table variant="full-page"` over `ContentLayout` +
`Table variant="container"`, citing the table-view pattern page's
`"Don't use the content layout component on this type of page. Instead,
use the 'full-page' variant"` — and an independent adversarial verifier
graded that finding **D (overreach)**, specifically because a pattern-page
citation was used to license a page-composition recommendation at
`REQUIRED` implementation-audit strength, which sits outside that skill's
own declared scope (`skills/cloudscape-implementation-audit/SKILL.md`,
"Scope boundary": "never propose restructuring the page into a different
Cloudscape product pattern"). Full detail:
`evals/cloudscape-implementation-audit/RESULTS-ITERATION-2.md`, section 6.

This eval does **not** hand that prior verdict to the reviewer as an
answer key — the run below gets the same fixture and the same baseline
framing as every other case, with no reference to the prior result. The
comparison against that prior verdict happens afterward, in this eval's
own `RESULTS.md`, as the central real-world validation question: can this
skill reach the same substantive observation the sibling skill reached
for, but correctly scoped as component/pattern reasoning instead of an
implementation-audit `violation`?

There is deliberately no `grading/case-real-identities.expected.md` —
nobody decided this surface's "correct" native-expression findings in
advance, the same real-fixture discipline
`evals/cloudscape-implementation-audit/README.md` used.

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
