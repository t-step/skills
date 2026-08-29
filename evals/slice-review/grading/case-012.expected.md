# Expected review outcome (for grading, not shown to the reviewer)

**Scenario type:** exploratory, "ranking among real findings" — a
different shape from both case-009 (many true cosmetic items, no material
one) and case-011 (one hidden material item among cosmetic noise, requiring
extra reasoning to surface at all). Here, several genuinely true findings
of *substantially different severity* are all reasonably easy to notice on
a normal read of the diff. The question is not detection — it's whether
the report's structure (bucket placement, ordering, space, wording)
tracks the real materiality gap between them, rather than treating them as
an undifferentiated list of "things I noticed."

**In-contract, non-exploratory part — three tiers of real findings:**

**Tier 1 — material, diff-demonstrable, goal-contradicting:**
`rows_to_csv` builds each line with plain `','.join(...)`, with no quoting
or escaping. The goal explicitly states output "must be valid CSV that
opens correctly in Excel and Google Sheets, including field values that
contain commas or double-quote characters" — and the diff does not do
this. Concretely: `rows_to_csv([{"name": "Smith, Jane", "amount": 100}],
["name", "amount"])` produces `"name,amount\nSmith, Jane,100\n"`, which a
standard CSV parser reads back as **three** fields (`Smith`, ` Jane`,
`100`) instead of two — the comma inside the value is indistinguishable
from a field separator. This silently corrupts output for realistic data
(names, addresses, free-text notes containing commas) rather than crashing
or erroring, which makes it worse operationally, not better: nothing
signals the corruption at write time. None of the 4 tests in the diff use
a value containing a comma or a quote character, so the passing test suite
provides no evidence against this — it is the single behavior the goal
text calls out by name, and it is exactly what's untested.

**Tier 2 — legitimate, secondary maintainability/verification concerns:**
- `str(row[c])` on a `dict` missing key `c` raises a raw `KeyError` (e.g.
  `KeyError: 'amount'`) with no validation or clearer error — for a
  report-download feature likely to hit real, occasionally-malformed row
  data, this is a real operability concern (an obscure crash instead of an
  actionable message), and it's untested.
- `str(row[c])` on a `None` value renders the literal text `"None"` in the
  output cell instead of an empty string — a real but lower-severity
  correctness/UX issue (a report cell showing the word "None" instead of
  being blank), also untested.

These two are legitimate findings, not blocking, and clearly less severe
than Tier 1: neither contradicts an explicit goal statement the way the
escaping gap does, and both are contained, single-cell effects rather than
a structural corruption of the whole row.

**Tier 3 — minor, unlikely to affect whether this ships:**
1. `lines` is a generic variable name.
2. The list-comprehension-then-join pattern
   (`[...].join(...)`-shaped) is repeated near-identically for the header
   and for each data row, instead of being factored into one small helper
   — harmless duplication.
3. `rows_to_csv` always appends a trailing `'\n'`, while the sibling
   `rows_to_json` (immediately above) returns no trailing newline — a
   minor inconsistency; the goal doesn't specify trailing-newline
   behavior, so this is not a contract violation, just a style note.

**Grading approach:** this is exploratory. There is no presumed-correct
selection or count for Tier 2/3 items — the hard requirements below check
only that the *tiering* (not the exhaustive list) is respected.

## Hard requirements

1. The Tier 1 escaping/quoting gap is identified in substance: the review
   must name, concretely, that comma (and/or double-quote) values in a
   field are not escaped/quoted, and that this breaks the CSV structure —
   not just a vague "should validate input more" comment.
2. Tier 1's severity is not materially understated: it must appear in
   **Blocking** or **Required corrections**, never **Non-blocking** or
   **Out of scope**, and must not be omitted.
3. The verdict is consistent with that classification: **"Ready to merge"
   is not acceptable** for this fixture. "Not ready to merge" or "Ready
   after minor corrections" are both acceptable — SKILL.md leaves the
   Blocking-vs-Required-corrections line to reviewer judgment, and a
   defensible case exists either way (the fix is a one-line swap to
   `csv.writer`/manual quoting, but it touches output correctness for the
   feature's stated purpose).
4. Whatever the review's overall severity ranking, **no Tier 3 item is
   placed above Tier 1 in a Blocking or Required-corrections bucket, and
   no Tier 3 item is described in language implying it is as important as
   the escaping gap** (e.g., a Blocking list that puts a naming nit
   alongside the escaping defect with no differentiation would fail this).
5. The 4 passing tests are not cited as evidence that CSV output is
   correct in general — if credited, only for what they actually cover
   (comma-free, quote-free, non-`None` values), not extended to comma-
   containing, quote-containing, missing-key, or `None`-valued input.
6. No speculative or invented blocker is introduced (e.g., claims about
   file encoding, streaming/memory limits for large exports, or
   internationalization concerns not grounded in the diff or goal as
   given).

## Observational dimensions (record, do not fail on)

- Which Tier 2 and Tier 3 items are surfaced, and which are omitted.
- Whether Tier 2 items (KeyError, `None`-rendering) are placed in a
  visibly different bucket/prominence than Tier 3 items, or lumped
  together as an undifferentiated Non-blocking list.
- Ordering: does Tier 1 appear first/most prominently, with Tier 2 and
  Tier 3 following in decreasing space/detail, or is ordering incidental
  (e.g., diff order, alphabetical, or Tier 3 items appearing before Tier
  2)?
- How much report space (bullets, explanation depth) each tier receives
  relative to the others.
- Whether the review explicitly references the goal's own escaping
  requirement as the reason Tier 1 outranks the others, or arrives at the
  same ranking without citing it.
- Whether a stable ranking axis is visible (e.g., "silently wrong output"
  ranked above "loud crash on bad input" ranked above "cosmetic"), or the
  three tiers read as arbitrarily ordered.
