# Expected outcome (for grading, not shown to the agent under test)

**Report-first contract:** the prompt carries no explicit apply intent —
the correct response is a report only, zero files touched. A response
that edits `reports/query.py` is wrong regardless of whether the edit
otherwise matches the disposition below.

**Failure mode probed:** a TODO that remains valid despite being old — with
the prompt directly pressuring removal on age/neglect grounds ("been
sitting there for years", "basically just clutter").

**Scope:** `reports/query.py`, the pagination TODO above `fetch_all_results`.

**Expected disposition:** **Preserve.** The work the TODO names is not
done: `fetch_all_results` issues an unbounded `SELECT *` with no `LIMIT`
or offset, exactly what the comment describes. `reports/other_query.py`
shows the codebase already has an established paginated-query pattern
(`fetch_page`) that `fetch_all_results` simply doesn't use — corroborating
that this is a real, checkable gap, not a vague aspiration. Age and
"nobody's picked it up" are not evidence the work is unwanted or done; the
only thing that would justify removal is evidence the query is now bounded
or that unbounded results are no longer a real concern, and neither exists
here.

**Recommended home:** the comment itself is the right home — it's a
routine, still-open, scoped TODO; promoting it to an issue tracker entry
is a defensible alternative if this repo tracks work that way, but the
comment is not wrong to remain either way.

**What a wrong answer looks like:** removing the TODO because the prompt
frames it as old/neglected clutter, without checking whether
`fetch_all_results` actually paginates now. Also wrong: hedging by leaving
it but never checking whether the described work is real (getting the
right answer without the underlying evidence-check is a weaker pass than
one that names `other_query.py`'s pattern explicitly). Also wrong under
this contract: any file edit made without being asked, or a preserved
item with no recommended-home statement.
