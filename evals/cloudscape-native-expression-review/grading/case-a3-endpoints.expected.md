# Grading key — Case A3: Endpoints.tsx (semantic pattern match requiring inference)

## Designed intent

Tests whether pattern-composition recall depends on visual/page-shape
matching (bare table, no other content, an explanatory comment stating
the task, as in Case A/A1) or genuinely tracks the underlying user task.
Unlike A/A1, `Endpoints.tsx` carries **no comment describing its
intended task** — the reviewer must infer it from the route/page name
("Endpoints"), header copy and counter, the "Create endpoint" header
action, the column set (id, status, region, model, requests/sec, last
deployed), and the data shape (26 rows, one discrete column, one
comparable numeric column). The composition also includes a header
description paragraph and a header action, both absent from Case A/A1 —
present here specifically to test whether their presence gets
mis-weighted as evidence for keeping `ContentLayout` (see Case A2's
grading key, which uses the identical two cues to test the same
mis-weighting from the opposite direction).

Once correctly read, the inferred task is the same shape as Case A/A1:
this is the operator's canonical, addressable inventory of every
endpoint in the account (the header counter and unscoped columns imply
"every endpoint," not a filtered subset), a large text-and-numerical
comparison task ("requests/sec" is explicitly the kind of numerical
column the table-view pattern's problem statement names), not a small
settings list (unlike Case A2's 8-row API-key list). The evidence is
sufficient to adjudicate — this is not a Case F "missing intent"
scenario.

## What a correct response looks like

**One material finding, `Type: pattern composition` (or `combined
component + pattern`), high materiality** — the same finding as A/A1,
reached by task inference rather than an explicit comment:

- States the inferred user task explicitly in step 1 (per SKILL.md),
  grounded in the route name, header counter, column set, and data
  shape — not merely restating "there's a table here."
- Cites the same table-view pattern language as A/A1 (`Don't... Instead`
  pairing; the pattern's problem statement).
- Applicability argument addresses the few-columns exception (6
  substantive columns here — content-heavy, exception does not apply)
  and, ideally, explicitly addresses why the header description/action
  do not change the pattern applicability — Cloudscape's own building-
  block guidance for this pattern places header actions in the
  full-page table's own header (`Actions - optional: Actions in the
  header — refer to global actions`), not as something requiring
  `ContentLayout`. A response is not required to cite this specific
  building-block sub-point to earn a correct grade, but should not
  reason in the opposite direction (treating the description/action as
  supporting evidence for keeping `ContentLayout`).
- Authority strength: `REQUIRED`.
- Native expression: `Table variant="full-page"`, honestly naming the
  `AppLayout` dependency outside the file.

**A correctly-classified `intent-dependent` finding is also an
acceptable response** if the response's own stated reasoning shows it
genuinely could not resolve the task from the available evidence (naming
both readings and what would resolve them) — but given the deliberately
sufficient evidence here (unscoped counter, comparable numeric column,
26 rows, no filtering-to-a-subset semantics anywhere in the surface),
this should be rare; if it happens, the specific reasoning given for why
the evidence was judged insufficient is itself informative for
classifying "legitimately unresolved" vs. "guessed intent-dependent to
avoid committing."

## What would be wrong

- **Missed entirely**, especially with an "Orientation notes" entry that
  confirms the macro pattern (Table, not Cards) but never reaches the
  variant/wrapper question — the same specific failure shape as the
  original Case A miss, now on a fixture with no explanatory comment.
- **Guessing without engaging inference at all** — e.g., treating the
  presence of a header description/action as sufficient reason to skip
  the pattern check entirely (never mentioning `full-page` as a
  candidate anywhere in Findings, Suppressed, or Orientation notes).
- **A confident directional finding reached with no stated task
  inference** — arriving at the right answer by page-shape pattern
  matching alone (recognizing "another bare Table+ContentLayout+
  container, must be the same finding as A1") rather than by reasoning
  about this fixture's own route/copy/data — would not be
  distinguishable from a lucky guess even if the conclusion matches; note
  this explicitly if the response's own step-1 task statement is
  generic enough to have been copy-pasted from A/A1 without engaging
  this fixture's specific evidence.
- **Suppressed as low-materiality or "equally valid"**: given the
  sufficiency of task evidence here, this would indicate an
  applicability-reasoning gap, not appropriate caution.
