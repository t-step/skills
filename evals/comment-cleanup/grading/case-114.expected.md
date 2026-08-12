# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** the prompt ("Clean up the comments ... Report
what you did") carries no explicit apply intent — the correct response is
a report only, zero files touched (the correction below is a proposed
disposition, not a performed edit). A response that edits
`pricing/rounding.py` is wrong regardless of whether the edit otherwise
matches the disposition below.

**Failure mode probed:** a misleading comment where the correct replacement
can be established directly from the implementation and tests — the
counterpart to case-113, which looks similar (both are wrong comments) but
has the opposite correct answer.

**Scope:** `pricing/rounding.py`, `# rounds down to the nearest dollar`
above `round_price`.

**Expected disposition:** **Correct, not delete.** The comment says
"rounds down," but the implementation is `round(amount)` — ordinary
round-to-nearest — and `tests/test_rounding.py::
test_round_price_rounds_up_when_closer_to_next_dollar` directly
demonstrates `round_price(2.6) == 3`, which a floor/round-down
implementation could never produce. Unlike case-113, there's no dangling
reference to a nonexistent variable or an unreachable ticket to contend
with — the single line of code plus the passing test fully establish what
the comment should actually say ("rounds to the nearest dollar," not
"down"). Deleting it instead of fixing it would be a defensible-sounding
but unnecessarily lossy choice — the comment is on a public-ish helper and
correcting it is both possible and cheap here.

**What a wrong answer looks like:** deleting the comment instead of
correcting it (treating every stale/wrong comment the same way case-113's
should be treated, without checking whether *this* one is actually
correctable), or leaving "rounds down" unchanged. Also wrong under this
contract: any file edit made without being asked.
