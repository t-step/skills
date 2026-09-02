# Case E — CertificatesTable.tsx + CertificateDetails.tsx (pattern lookalike, wrong product intent; synthetic)

**Fixture:** synthetic, purpose-built for this skill's eval.

**Bounded surface to review:**
- `fixture/src/pages/CertificatesTable.tsx` — a resource table of TLS
  certificates, `variant="full-page"`, with a per-row "View details"
  button that navigates (via `react-router`) to a separate route.
- `fixture/src/pages/CertificateDetails.tsx` — the page that route
  renders: a full details page for one certificate (breadcrumb, header
  with Renew/Revoke actions, a `KeyValuePairs` general-configuration
  container, plus three further containers — domains covered, attached
  resources, renewal history — each holding a small `Table`).

Review both files together as one bounded surface (the table and the
page it navigates to).

**Cloudscape packages declared:**
`@cloudscape-design/components@^3.0.900` (locked `3.0.900`),
`react-router@^6.23.0`. Lockfile: `fixture/package-lock.json`.

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
