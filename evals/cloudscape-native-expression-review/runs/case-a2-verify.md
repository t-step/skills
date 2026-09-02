# Adversarial verification — Case A2: ApiKeys.tsx

Reviewed: `evals/cloudscape-native-expression-review/runs/case-a2-skill.md` against
`evals/cloudscape-native-expression-review/grading/case-a2-api-keys.expected.md`,
the fixture at
`evals/cloudscape-native-expression-review/cases/case-a2-api-keys/fixture/src/pages/ApiKeys.tsx`,
and live Cloudscape documentation fetched during this verification.

This is a precision-control case: the designed-correct answer is **no
material finding** on the `ContentLayout` vs. `full-page` question. The run
under test reported zero findings, so there is no finding to grade A–E on
the rubric's letter scale in the usual sense. Per the rubric, this case is
instead graded on whether the review's *stated reasoning* (Orientation
notes + Suppressed) is genuinely correct, not just silent.

## Claim-by-claim verification

### 1. Orientation note: `ContentLayout` + `Table variant="container"` for a 4-column table — "few columns" exception

**Claim in review:** quotes the Table view pattern's "Don't" list as:
> "Don't use the content layout component on this type of page. Instead,
> use the 'full-page' variant of the table component," immediately
> followed by "Don't use the table view pattern for tables that aren't
> overly content-heavy. Instead, if a table only has a few columns, use a
> bordered table inside the content layout component."

**Verified against:** `https://cloudscape.design/patterns/resource-management/view/table-view/index.html.md`

Fetched twice (once for content, once specifically for Do/Don't ordering).
Actual page text, first two items of the "Don't" list, in order:
1. "Don't use the content layout component on this type of page. Instead,
   use the 'full-page' variant of the table component **to implement this
   pattern**."
2. "Don't use the table view pattern for tables that aren't overly
   content-heavy. Instead, if a table only has a few columns, use a
   bordered table inside the content layout component**, with the default
   app layout content max-width**."

**Verdict:** Accurate. The review's quotes are real, in the correct order,
and the "immediately followed by" adjacency claim is correct (these are
literally the first two Don't bullets). The review trims a trailing clause
off each quote ("to implement this pattern" / ", with the default app
layout content max-width") without an ellipsis — a minor completeness
nitpick, not a misrepresentation; neither dropped clause changes the
guidance's meaning.

**Applicability (rubric Q2, Q3, Q5):** The fixture has 4 columns (label,
key, status, created), uses `Table variant="container"` inside
`ContentLayout` — exactly the second Don't's named correct alternative
("bordered table inside the content layout component"). `variant="container"`
does render as a bordered table. This is a correct, specific application of
the exception to this fixture's actual facts (column count), not a bare
appeal to the pattern's existence. This is exactly what the grading key
requires ("note the small column count ... as the reason the exception
applies").

### 2. Suppressed: Table view vs. Card view by item count

**Claim:** View resources pattern gives "9 or more resources in 99% of use
cases" for Table view and "5 or less resources in 99% of use cases" for
Card view; metadata-type criterion ("data displayed in columns (text,
numerical, status)") favors Table.

**Verified against:** `https://cloudscape.design/patterns/resource-management/view/index.html.md`

Confirmed both thresholds verbatim, and the data-type criterion (fetch
returned "Data that is displayed in columns (text, numerical, status,
sparkline)" for Table view vs. "visuals (charts, videos)" for Card view —
review drops "sparkline" from its quote, immaterial).

**Verdict:** Accurate and well-reasoned suppression. 8 rows genuinely sits
in the gap between the two stated thresholds; the review correctly notes
this ambiguity rather than picking a side, and correctly treats the
decisive metadata-type criterion (all 4 columns are plain data cells, no
visuals) as resolving the ambiguity toward Table. This is a sound
application of rubric Q5 ("could the current implementation be equally
valid Cloudscape usage") — yes, and the review shows its work rather than
asserting it.

### 3. Suppressed: inline Copy to clipboard on the "Key" column

**Claim:** documented inline-variant use case is "a long URL within a
table or an Amazon Resource Name (ARN) within a list of key-value pairs."

**Verified against:** `https://cloudscape.design/components/copy-to-clipboard/index.html.md`

The page does document both examples (a long URL within a table; an ARN
within a list of key-value pairs) as separate illustrative bullets under
the inline variant's use case, not as one continuous sentence. The review
presents them concatenated with "or" as if one quoted string. This is a
minor quotation-fidelity slip (rubric Q2 concern) — the substance is
accurate, the verbatim-quote framing is not strictly verbatim.

**Verdict:** Does not change the outcome — this candidate was already
correctly suppressed at low confidence (masked key, no evidenced need to
copy it elsewhere), and the underlying documentation claim is substantively
correct even if the quotation mechanics are slightly loose.

### 4. Orientation note: `TextFilter` for filtering

**Claim:** Filtering patterns documents TextFilter for a "simple resource
(small set of properties)" where users "know exactly the value or term
they are looking for."

**Verified against:** `https://cloudscape.design/patterns/general/filter-patterns/index.html.md`

Confirmed near-verbatim ("Simple resource (small set of properties)" /
"tend to know exactly the value or term they are looking for" — review
drops "tend to," immaterial). Also confirmed the review's implicit
contrast (collection-select-filter for one/two-property filtering by
status/type; property-filter for complex, multi-property resources) is
accurate to the source, correctly supporting the review's conclusion that
TextFilter neither under- nor over-powers this 4-flat-property task.

**Verdict:** Accurate.

### 5. Orientation note: `Pagination` shown for 8 rows

**Claim:** "Display the pagination even if the resources set fits in one
page."

**Verified against:** same table-view pattern page — exact match, verbatim.

**Verdict:** Accurate.

### 6. Orientation note: `Header` composition (counter, description, actions)

**Claim:** matches the Header component's documented slots.

**Verified against:** `https://cloudscape.design/components/header/index.html.md`

Confirmed counter, description, and actions are each documented as
optional Header features. The claim that they are "demonstrated together"
in one example is a mild overstatement (the fetch found them documented as
separate optional slots, not necessarily one single combined example), but
this is minor supporting color, not load-bearing for the case's core
question, and not contradicted by the source.

**Verdict:** Accurate in substance; a small overstatement on presentation
that does not affect the case verdict.

### 7. Suppressed: missing revoke action despite header copy

**Claim:** header promises revocation but no row action/selection exists;
suppressed as out of scope for this skill (total absence of implementation,
not a component/pattern-selection problem) rather than reported as a
pattern-composition finding.

**Verdict:** Correct application of SKILL.md's scope boundary. SKILL.md's
"Out of scope" section (product redesign / inventing functionality) and
the Finding contract's boundary-check requirement support treating a
wholesale missing feature as outside this skill's given-a-composition,
judge-the-composition remit. This is good, disciplined reasoning that
strengthens confidence in the reviewer's overall judgment quality, even
though it isn't what this case specifically tests.

## Checking against this case's specific failure modes

Per `case-a2-api-keys.expected.md`'s "What would be wrong":

- **A `ContentLayout`→`full-page` finding reported here:** not present. ✓
- **A finding citing the few-columns exception but still recommending
  `full-page`:** not present — the review cites the exception and
  correctly concludes the current composition *is* the exception's
  recommended alternative. ✓
- **Treating the header description or "Create API key" action as
  evidence for/against the pattern-composition finding:** not present.
  The review's Header-composition Orientation note treats the header's
  slots as evidence for the *Header component's* correct usage, not as
  evidence for the `ContentLayout` structural decision. The header
  description is used elsewhere only to motivate the separate,
  correctly-out-of-scope "missing revoke" observation — never smuggled in
  as a reason `ContentLayout` was the right (or wrong) container choice. ✓

## Case-level verdict

**Match.** This is a genuine, correctly-reasoned "checked and cleared,"
not a right-answer-for-wrong-reasons result. The review:

- Reaches the designed-correct outcome (no `ContentLayout`/`full-page`
  finding).
- Takes the grading key's explicitly-preferred *stronger* form — an
  affirmative Orientation-notes entry rather than silence — and grounds it
  in the pattern's actual few-columns exception applied to this fixture's
  real column count (4), exactly the reasoning the grading key asks for.
- Every substantive Cloudscape citation checked (table-view Don'ts, View
  pattern item-count/data-type thresholds, filter-patterns guidance,
  pagination guidance, Header slots) was verified against the live docs
  and found accurate in substance; the only issues found were minor
  quotation-trimming/concatenation slips (dropped trailing clauses, one
  two-bullet quote presented as one continuous string) that do not
  misrepresent what the cited pages say.
- Avoids every specific trap this case is designed to catch: no
  ContentLayout→full-page finding, no self-contradictory citation, and no
  reasoning from header description/actions toward the container
  decision.
- The additional Suppressed-section judgment calls (Card view, Copy to
  clipboard, missing revoke) are independently sound and consistent with
  SKILL.md's materiality bar and scope boundary, which further supports
  that the "None" findings result reflects real, careful checking rather
  than a shortcut to silence.

No real finding is being missed here after all — the current
`ContentLayout` + bordered `Table` composition is, per the pattern's own
stated exception, the documented correct answer for a 4-column settings
surface, and the review's own affirmative record demonstrates that with
accurate citations.
