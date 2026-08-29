# Slice Retrospective: Add basic product search (linear scan)

## What we proved
`search_products(query)` correctly does case-insensitive substring matching
against product names, and returns within budget (380ms avg, budget 500ms)
against the 500-row pilot fixture — backed by the four passing tests.

## Assumptions validated
The assumption that pilot users could be served correctly by a simple
in-memory linear scan, at the pilot's dataset size, was validated.

## Assumptions falsified
None — nothing in this slice's own goal claimed the linear scan would hold
at full-catalog scale, so nothing about that has been proven or disproven
here; see Remaining uncertainty.

## Remaining uncertainty
Behavior against the full ~118,000-row production catalog is untested. The
380ms figure was measured on 500 rows; a linear scan's cost grows with
catalog size, and nothing in this slice's evidence establishes what latency
the full catalog would actually produce.

## Intentional non-goals
Any indexed or full-text search backend was explicitly out of scope —
goal.md scoped this slice to "get search working correctly for the pilot,"
not to production scale.

## Architectural consequences
A `search_products(query)` entry point and the pilot UI's search box now
exist and are wired together; nothing before this slice let a user search
the catalog at all.

## Follow-up questions
At what catalog size does the linear scan stop meeting a reasonable latency
budget?
