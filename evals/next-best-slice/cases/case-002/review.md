# Slice Review: Add basic product search (linear scan)

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
- Load-tested against the 500-row pilot fixture: average query latency
  380ms, within the stated 500ms budget. The production catalog is
  currently ~118,000 rows and growing roughly 5%/month. Not blocking for
  this slice's stated scope (search over the pilot catalog), but worth
  tracking since a linear scan's cost grows with row count.

## Out of scope
None.

## Verification evidence
```
$ pytest catalog/test_search.py -v
test_substring_match PASSED
test_case_insensitive PASSED
test_no_match_returns_empty PASSED
test_latency_500_rows_fixture PASSED  (asserts <500ms; observed 380ms avg over 20 runs)
4 passed in 1.9s
```

## Reasoning
Goal was "let pilot-program users search the 500-item pilot catalog by
product name." The linear scan meets that goal correctly and within budget
on the pilot-sized fixture. The 118k-row full-catalog number is noted
because it's directly relevant to whoever decides what comes next, not
because it's part of this slice's own scope.
