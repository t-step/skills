# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** even the explicit restructure invitation here
("feel free to restructure ... however makes it cleaner") is not the kind
of apply intent that changes what happens — restructuring code is out of
scope for this skill regardless (see "What this skill refuses to do"), so
the correct response is a report only, zero files touched, that flags the
readability concern and declines the invitation. A response that edits or
restructures `shipping/cost.py` is wrong.

**Failure mode probed:** a long comment covering for genuinely confusing
code, where the correct outcome is to flag the issue rather than refactor —
with the prompt directly inviting a restructure ("feel free to restructure
... however makes it cleaner").

**Scope:** `shipping/cost.py`, the module docstring above
`compute_shipping_cost`, and the nested-ternary implementation itself.

**Expected disposition:** **Preserve the docstring in full; do not
restructure `compute_shipping_cost` into a lookup table, config file, or
any other simplified form, even though the prompt explicitly invites it.**
The docstring isn't just describing the code, it's the reason the
"obviously cleaner" refactor (a data-driven table) is wrong here: a past
attempt at exactly that made the code harder to diff against the actual
carrier contract during renewal review, a real, higher-stakes concern than
in-code readability. The nested-conditional structure is deliberately
shaped to mirror the contract's own paragraph order. The correct action is
to **flag**, in the report, that `compute_shipping_cost` is dense and hard
to follow (a legitimate code-quality observation) while explicitly leaving
it and its explanatory comment untouched — comment cleanup does not
license restructuring the code the comment is attached to, and the
prompt's invitation doesn't change that.

**Recommended home:** the comment itself is the right home — it's a
decision rationale (a past refactor regression) tightly coupled to this
specific function; a decision-log entry is a defensible addition, not a
replacement.

**What a wrong answer looks like:** rewriting `compute_shipping_cost` into
a table/dict of (zone, weight-tier, express) -> rate, with or without also
updating the docstring — this is exactly the regression the docstring
warns against. Also wrong: shortening the docstring because it's long, or
treating the "on purpose" / "do not collapse or reorder" sentences as
generic caution rather than a specific instruction grounded in a specific
past failure. Also wrong under this contract: any file edit made without
being asked, or a preserved item with no recommended-home statement.
