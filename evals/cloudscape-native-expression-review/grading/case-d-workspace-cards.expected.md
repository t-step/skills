# Grading key — Case D: RecentWorkspaces.tsx (equally valid alternative)

## Designed intent

`Cards` is mechanically correct. The collection is small (6 items), each
item carries a small visual element (a colored tag badge — not a photo,
but genuinely non-columnar/glanceable content per the pattern's own
framing), and the task, per the header's own copy, is "recognize the one
I want and reopen it" — browsing/recognition, not cross-item metric
comparison. Per the "View resources" guidance this eval's authors
retrieved: cards suit "users will not be comparing between a large
number of resources" and content with "different metadata to be
displayed at the same time in a constrained space" — six items with a
tag, a status, and a relative time is exactly this shape, not the
"same metadata type... comparing... determine which to take action on"
shape that favors Table. `Table` would also technically work — that's
the point. Neither the pattern guidance nor the data shape gives a strong
pull toward switching.

## What a correct response looks like

**No material finding.** The response may note, in "Orientation notes,"
that it considered a Table alternative and confirmed Cards is
well-supported for this task (small set, non-comparison browsing,
visual/glanceable content) — this is the affirmative "checked and
cleared" discipline the skill's report template asks for, distinct from
never having considered it.

If a candidate is generated and then suppressed, it should be suppressed
for weak applicability / equally-valid-alternative reasoning specifically
— not for low materiality alone (the collection-size/comparison-task
distinction is exactly what should drive the "no, this doesn't apply"
conclusion, not a vague sense that switching wouldn't matter much).

## What would be wrong

- **A reported finding recommending Table**, on the reasoning "Table is
  the primary collection component" or "the data is structured and could
  be columns": this is the "component existence/structural plausibility
  treated as a mandate" failure mode — exactly what this case exists to
  catch. Grade D regardless of how the finding is phrased, since it fails
  the applicability test (task is browsing, not comparison; the docs'
  own comparison-driven criterion for Table isn't met).
- **A finding that correctly avoids recommending Table, but frames it as
  a firm requirement that Cards must always be used for small
  collections**: overcorrection — the point isn't that Cards is mandated
  here, it's that both are legitimately supported and switching wouldn't
  be material. The report should reflect that even-handedness, not invert
  the fundamentalism the wrong direction.
