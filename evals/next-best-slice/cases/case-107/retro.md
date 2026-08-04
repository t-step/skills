# Slice Retrospective: Add cursor-based pagination to the admin activity log

## What we proved
Default-limit pagination with a `next_cursor`, and continuation via that
cursor, both work correctly against a 10,000-row staging fixture — backed
by the three passing tests.

## Assumptions validated
A cursor-based approach avoids needing a total-count query (a slow
`COUNT(*)` on a large table) to support pagination.

## Assumptions falsified
None.

## Remaining uncertainty
Performance against the full production activity-log table (~40 million
rows) is untested — only the 10,000-row staging fixture was measured.

## Intentional non-goals
Any UI to jump to a specific page number was out of scope — goal.md scoped
this slice to cursor-based next/previous only.

## Architectural consequences
A generic `CursorPaginator` class now exists and could be reused for other
large tables (e.g. the audit-log or notifications tables) without
rebuilding pagination logic from scratch.

## Follow-up questions
Does `CursorPaginator` perform acceptably against the full 40-million-row
table, not just the 10,000-row fixture?
