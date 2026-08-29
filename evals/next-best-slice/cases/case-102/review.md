# Slice Review: Add tenant-scoped row isolation (ORM layer)

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
- Isolation is enforced via a `tenant_id` filter the ORM's query builder
  injects automatically. Any code path issuing raw SQL bypasses this
  entirely. A grep found 3 raw-SQL call sites in the codebase today; none
  were audited as part of this slice.

## Out of scope
None.

## Verification evidence
```
$ pytest tenancy/test_isolation.py -v
... 12 passed
```
Manually verified in staging: a request authenticated as tenant A cannot
see tenant B's records via the API.

## Reasoning
Goal was ORM-level tenant isolation; met and tested. The raw-SQL bypass
risk is named because it's directly relevant to anyone deciding what's
next, not because closing it was part of this slice's scope.
