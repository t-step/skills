# Grading key — Case E1: ApiKeys.tsx (explicit equivalence)

## Designed intent

Isolates one narrow question, cleanly, with no confound: when Cloudscape's
own authoritative criteria table places the current component
(`TextFilter`) and a documented alternative (`CollectionSelectFilter`) in
the *identical* cell for this resource's complexity tier, and the
**bounded surface supplies zero evidence** — no comment, no header
description language, no variable/prop name — resolving the table's only
differentiating row ("user goals"), does the skill suppress the
replacement candidate, or report it anyway?

This is a direct re-instrument of the retired `case-p1-message-queues`
Candidate 2 axis. That case's own grading key asserted "the fixture shows
no code, comment, or header language establishing which lookup mode
operators actually use" — a claim the post-fix round (`RESULTS-POSTFIX.md`
§3) found to be **factually false**: `MessageQueues.tsx`'s own header
comment ("Operators can search by queue name, or narrow the list down to
a specific status or region while triaging") does supply exactly that
resolving language, giving four independent trials a legitimate,
non-fabricated argument to hang a finding on. `ApiKeys.tsx` removes that
comment (and every other trace of filtering-intent language) entirely.

## Candidate — `TextFilter` alone vs. adding a `CollectionSelectFilter` for `environment`/`status`

**Verdict: MUST SUPPRESS.**

- **Repository evidence establishing task/user intent (item 1):**
  `ApiKeys.tsx`'s only task-establishing text is the `Header`'s
  `description="Manage API keys for this account."` and the bare column
  set (name, environment, status, created). Nothing in the file — no
  comment, no placeholder text beyond the generic `"Find API key"`, no
  variable or prop name — states or implies that operators look up keys
  by environment or status specifically, as opposed to searching by name,
  or simply browsing/paging through the list. `environment` and `status`
  are both two-valued columns, but a column merely *having* low
  cardinality is a fact about the data shape, not evidence of an actual
  user goal to filter by it — conflating the two is exactly the
  availability-for-applicability substitution SKILL.md's anti-
  fundamentalism rule exists to block.
- **Authoritative evidence establishing equivalence (item 2):**
  Cloudscape's `/patterns/general/filter-patterns/index.html.md` page
  (live-verified 2026-09-02), criteria table, "Complexity of the
  resource" row: **"Simple resource (small set of properties)"** for both
  `TextFilter` and `CollectionSelectFilter` — an identical cell, not a
  ranked pair. The only differentiating row is "User goals": "Find
  resources that match an exact text query" (`TextFilter`) vs. "Find
  resources with overlapping, defined values" (`CollectionSelectFilter`)
  — both are claims about user *behavior*, not about which component is
  more native for this resource's complexity tier.
- **Evidence readable in the opposite direction (item 3):** A reviewer
  could argue that `environment`/`status` being finite, named,
  enumerable values is itself evidence users would want to select rather
  than type them — this is the same move the four P1 post-fix trials
  made with the actual confounding comment, generalized to work even
  without one. It should be named and rejected explicitly: the filter-
  patterns table's "User goals" row is about demonstrated behavior
  (established by copy, code, or an explicit product requirement), not
  about a property's cardinality — cardinality is already fully priced
  into the tied "Complexity of the resource" row, so re-deriving a
  direction from cardinality a second time double-counts the same fact
  under the other row's label. This file supplies no behavioral evidence
  either way.
- **Why the expected result does not depend on hidden grader
  interpretation (item 4):** Grounded entirely in SKILL.md's own frozen
  text — the "Anti-fundamentalism rule"'s point 4 and "Same-tier
  equivalence controls point 4" paragraph name this exact shape (a
  criteria table tying current and proposed, differentiated only by an
  unresolved user-behavior row) as a mandatory suppress-or-
  `intent-dependent` case, and "Apply a high materiality bar" separately
  names "an equally valid alternative" as something that must not be
  reported. No reading of SKILL.md licenses reporting this candidate
  given this fixture's total absence of resolving evidence.
- **Would removing any single fixture comment or prose annotation change
  the expected result (item 5)?** **No** — there is no comment or prose
  annotation in this fixture beyond the generic column headers and a
  one-line, filtering-silent `Header` description. Nothing exists to
  remove that the expected result depends on. This is the property the
  retired P1 case lacked.

**Acceptable outcomes:** omitted entirely; named as a suppressed/
orientation-note candidate; or reported as `intent-dependent` explicitly
naming that the "user goals" row is unresolved by this surface. **Not
acceptable:** reporting `CollectionSelectFilter` (alone or alongside
`TextFilter`) as a `component selection`/`documented composition`/
`combined` finding at any materiality or confidence level — including a
hedged one that also concedes the current approach is valid (SKILL.md's
own "sharpest form of the failure" language, carried over unchanged from
the P1 grading key).

## What would be wrong, summarized

- **Reporting the `CollectionSelectFilter` candidate** at any confidence/
  materiality level — the disqualifying failure this case exists to
  detect.
- **Manufacturing a directional claim from column cardinality alone**
  (see item 3) without any surface evidence of actual user behavior —
  scores as a report-side failure identical in kind to reporting the
  candidate outright, even if dressed as `INFERRED` or `SYNTHESIS`.
- **Fabricated or non-verbatim quotation** presented inside quotation
  marks as literal Cloudscape source text — graded separately under
  citation fidelity, never folded into the materiality verdict above.
