# Grading key — Case E: CertificatesTable.tsx + CertificateDetails.tsx (pattern lookalike, wrong product intent)

## Designed intent

The surface's shape — a table with a per-row "view details" action — is
exactly what a reviewer familiar with Cloudscape's split-view pattern
might expect to see recomposed with a `SplitPanel` for "quick browsing
without leaving the table." That temptation is the trap this case is
built to expose. `CertificateDetails.tsx` is a genuinely comprehensive
single-resource view: identity + status, every domain the certificate
covers, every load balancer it's attached to, and its renewal history —
four distinct, individually-organized fact groups, each already correctly
expressed with `Container`s and the appropriate component per group
(`KeyValuePairs` for the scalar facts, `Table` for the two real,
potentially-growing sub-collections). This is squarely what Cloudscape's
own split-view documentation calls out as the case its own pattern must
never replace: *"Always use details pages to display full resource
details of a single resource. A split view should never replace details
pages."*

## What a correct response looks like

**No material finding recommending split view / a split panel.** The
correct response explicitly considers and rejects the tempting
recommendation, rather than silently never generating it (silence here
would be indistinguishable from the case-A recall-gap failure mode this
eval also has to watch for) — ideally visible in "Orientation notes":
noting that the table+detail shape superficially resembles split view,
citing the "should never replace details pages" line, and stating that
the current separate-details-page navigation is the correct, already
Cloudscape-native expression of "inspect one certificate's full
configuration."

A response may still surface other, unrelated findings on this surface
if genuinely material and well-evidenced (this eval does not require a
fully clean report — only that the split-view temptation specifically is
rejected). None are required for this case to pass; the diagnostic
signal is entirely about the rejected recommendation.

## What would be wrong

- **A reported finding recommending split view / `SplitPanel`** for
  browsing certificates with contextual detail: overreach — fails the
  applicability test on its own terms (the pattern's authors explicitly
  say not to use it for full single-resource detail), and further fails
  the preserved-task check (a split panel would compress `CertificateDetails.tsx`'s
  four fact groups into a much smaller collapsible area, which does not
  preserve "inspect the certificate's full configuration" as a task).
  Grade E if the response asserts split view *is* applicable despite the
  explicit "should never replace" language (misreads or ignores the
  cited source); grade D if it hedges the recommendation but still
  reports it as a finding.
- **Silence with no evidence the temptation was considered**: not
  wrong on its face (a clean report is valid), but weaker evidence for
  this specific case's purpose than an explicit rejection — the grading
  question here (per the rubric) is whether the *right* conclusion was
  reached, and an explicit rejection is stronger, auditable evidence of
  that than unexplained silence.
- **A finding about the two embedded `Table`s inside `CertificateDetails.tsx`
  (e.g., "these should be a Cards view" or similar) presented as the
  case's main finding**: off the point this case is built to test, though
  not automatically wrong — grade independently per the rubric if it
  appears, but it does not substitute for correctly handling the
  split-view temptation.
