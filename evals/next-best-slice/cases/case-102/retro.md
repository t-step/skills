# Slice Retrospective: Add tenant-scoped row isolation (ORM layer)

## What we proved
Queries issued through the ORM are correctly scoped by `tenant_id` — backed
by the 12 passing tests and a manual staging check that tenant A cannot see
tenant B's records via the API.

## Assumptions validated
The ORM's query-builder hook is sufficient to enforce isolation for every
code path that goes through it.

## Assumptions falsified
None.

## Remaining uncertainty
Whether the 3 known raw-SQL call sites in the codebase (and any others not
yet found) leak cross-tenant data has not been checked — this slice only
touched the ORM path.

## Intentional non-goals
Auditing or fixing raw-SQL call sites was out of scope per goal.md, which
scoped this slice specifically to "add ORM-level isolation as the first
phase."

## Architectural consequences
A `tenant_id`-scoping hook now exists in the ORM layer. Any model accessed
through the ORM is automatically isolated by tenant.

## Follow-up questions
Are the 3 known raw-SQL call sites — and any undiscovered ones —
tenant-isolated or not?
