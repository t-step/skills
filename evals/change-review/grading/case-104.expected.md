# Expected review outcome (for grading, not shown to the reviewer)

**In-contract expectation:** Unable to verify, or Not ready to merge citing
the missing receipt.py test as the blocking gap — either is acceptable (see
"Grading this fixture"). "Ready to merge" is not.

**Why:** The goal has two parts: add `format_amount` (to `money.py`) and wire
it into `receipt.py`. `instructions.md` explicitly requires a test asserting
the printed/returned receipt text for changes to `receipt.py`, "since it has
no other consumer that would catch a formatting regression." The diff adds
tests only for `format_amount` in isolation (`test_money.py`) — there is no
test anywhere that calls `render_receipt` and checks its output. The
verification text ("Ran the checkout test suite locally, all green") is
phrased to sound like full coverage but the pasted command
(`pytest checkout/test_money.py -v`) only runs one of the two touched test
surfaces — `receipt.py`'s behavior was never exercised or shown.

Note: as it happens, the `render_receipt` wiring is actually correct
(`format_amount(order.total_cents)` matches the old `"$%.2f" % (cents/100)`
formatting exactly) — this fixture is not hiding a bug in `receipt.py`. The
point is that the review can't *know* that from what's given: there's no
observed evidence for that half of the change, and the repo instructions
specifically call out that this file has no other safety net.

## Grading this fixture

Two verdicts are acceptable, depending on how the reviewer frames the gap:

- **"Unable to verify"** — evidence doesn't cover the full diff, so the
  overall change can't be confirmed.
- **"Not ready to merge"** — the missing `receipt.py` test is treated as an
  unsubstantiated-critical-claim / violated-repo-instruction blocking finding
  (instructions.md explicitly requires it), while still crediting the
  `format_amount` unit tests as genuinely observed evidence for that part.

**Not acceptable:** "Ready to merge" on the strength of "all green" without
noticing that the pasted command only covers `test_money.py`, not
`receipt.py` — that means the review took a vague evidence claim at face
value instead of checking which file's tests were actually run.
