# Slice Review: Add pagination to the webhook delivery dashboard

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
- Pagination uses a fixed page size of 25 with no way to change it. Not
  blocking — nobody has asked for a different page size, this just
  replaces the old "last 100, unpaginated" list now that delivery volume
  has grown past what fits on one screen.

## Out of scope
None.

## Verification evidence
```
$ pytest webhooks/test_dashboard.py -v
test_renders_recent_deliveries PASSED
test_shows_success_and_failure_status PASSED
test_paginates_at_25_per_page PASSED
test_next_page_link_advances_offset PASSED
4 passed in 0.3s
```
Manually verified in staging: dashboard now paginates in pages of 25,
next/previous links work correctly against the real delivery log.

## Reasoning
Goal was to keep the delivery dashboard usable as delivery volume grows
past the 100-row unpaginated list added last time. Implemented as a
reusable pagination component wrapping the existing delivery-list query.
