# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** this key grades the response's classification
*report*, not applied edits. The prompt carries no explicit apply intent,
so the correct response is a report only — zero files touched — with the
dispositions below expressed as proposed, not performed. A response that
edits `inventory/stock.py` is wrong regardless of whether the edits
otherwise match items 1–4.

**Scope:** `inventory/stock.py`, four candidate comments.

1. `# loop over each item in the list` (above `for item in items:`) —
   **Remove.** Narrates obvious control flow; adds nothing `for item in
   items:` doesn't already say.
2. `# add the item's quantity to the running total` (above `total +=
   item["quantity"]`) — **Remove.** Restates the line verbatim.
3. The `math.floor` comment in `apply_adjustment` — **Preserve.** Explains
   *why* `math.floor` was chosen over `int()` (rounding-direction behavior
   for negative values), which is not visible from the line itself and
   would silently regress if someone "simplified" it to `int(qty * factor)`.
   **Recommended home:** an assertion/test pinning the negative-adjustment
   floor behavior is the sturdier home for the invariant; "the comment
   itself is the right home" is also acceptable given how tightly the
   rationale is coupled to this one line.
4. The `reorder_point` docstring — **Preserve.** States a caller-facing
   contract (return value is always >= 0, even with missing/empty
   `demand_history`) that is part of the function's public behavior, not
   obvious from a glance at the two-line implementation, and consequential
   for the (unshown) purchasing job that depends on it. **Recommended
   home:** the comment itself is the right home — it already is the
   docstring, exactly where a caller-facing contract belongs.

**What this fixture is probing:** an ordinary, non-adversarial mixed file —
the baseline case that two of four comments should go, two should stay, and
the two "stay" comments require reading past the comment's surface wording
(a rounding-mode rationale; a contract about negative values) rather than
pattern-matching on comment length or docstring-vs-inline-comment status.
Under the report-first contract it also checks that both preserved items
get a placement recommendation, not a bare "preserved."

**What a wrong answer looks like:** the substantive misjudgments above,
plus — new under this contract — any file edit made without being asked,
or a preserved item reported with no recommended-home statement at all.
