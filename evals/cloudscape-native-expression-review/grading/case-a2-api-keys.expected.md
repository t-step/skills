# Grading key — Case A2: ApiKeys.tsx (equally valid composition, precision control)

## Designed intent

The precision control paired with Case A1: same component shape
(`Table` + `ContentLayout` + `Table variant="container"`, a header,
`TextFilter`, `Pagination`), same underlying finding *type* the run has
now been primed to look for by A1 (and, before it, Case A) — but here
the composition is the documented **correct** answer, not a mismatch.
Four columns (label, key, status, created) is squarely "a few columns,"
the table-view pattern's own stated exception for staying inside
`ContentLayout`: *"Don't use the table view pattern for tables that
aren't overly content-heavy. Instead, if a table only has a few columns,
use a bordered table inside the content layout component."* Eight rows
of a service owner's own API keys is a settings-shaped surface, not an
operational fleet/resource inventory. The header description paragraph
and "Create API key" action are present on both this case and Case A3 —
included here specifically so their presence, by itself, cannot be what
triggers or suppresses a finding.

## What a correct response looks like

**No material pattern-composition finding on the `ContentLayout` vs.
`full-page` question.** Correct responses may take either honest shape:

- Silence (no finding reported), or
- An affirmative "Orientation notes" entry confirming the composition
  against the pattern's own few-columns exception — this is the
  stronger, more diligent version of a correct answer (parallel to how
  Case D's skill run explicitly confirmed rather than merely omitting).

Either way, the response should not treat "Table wrapped in
`ContentLayout` with `variant=\"container\"`" as inherently suspect
merely because it shares that shape with a case the skill correctly
flagged elsewhere in the same run or session. If the response engages
the applicability test at all, it should note the small column count
and/or the settings-not-inventory task as the reason the exception
applies, not just assert "this one's fine" with no reasoning.

A `component selection` or other finding entirely unrelated to the
`ContentLayout`/`full-page` question (e.g., a genuinely well-evidenced
finding on a different axis) is not itself wrong, but is not what this
case is testing and should be judged independently on its own merits if
present.

## What would be wrong

- **A `ContentLayout`→`full-page` finding reported here**: the clearest
  possible false positive this case can produce — pattern/shape
  matching against A1's recently-reinforced rule rather than applying
  the few-columns exception and the settings-vs-inventory task
  distinction to this fixture's own facts.
- **A finding that cites the few-columns exception's language but still
  recommends `full-page`** (self-contradictory application of the cited
  authority): counts as a false positive with an additional citation
  problem.
- **Treating the header description or "Create API key" action as
  evidence either for or against the pattern-composition finding**: real
  Cloudscape guidance places header actions in either variant's own
  header regardless of which variant is chosen, so neither cue
  distinguishes this case from A1 or A3 — a response reasoning from
  "it has a description/action, so it needs ContentLayout" is reasoning
  from the wrong evidence, not the right conclusion for the wrong
  reason.
