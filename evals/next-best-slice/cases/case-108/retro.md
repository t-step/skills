# Slice Retrospective: Add per-row CSV import validation for bulk product upload

## What we proved
Malformed rows (missing SKU, invalid price format, duplicate SKU within
the same file) are now rejected individually with a row-numbered error
message, while valid rows in the same file still import — backed by the
four passing tests and a real 200-row pilot merchant file that matched the
merchant's own manual review.

## Assumptions validated
Partial import with per-row errors is more useful to merchants than the
previous all-or-nothing behavior — the pilot merchant had explicitly asked
for this in earlier feedback, and the real-file test confirmed the
behavior works as intended.

## Assumptions falsified
None.

## Remaining uncertainty
None significant for the validation logic itself; very large files
(10,000+ rows) haven't been tested for import time.

## Intentional non-goals
Any change to how errors are communicated beyond the in-app message list
(e.g. an emailed report) was out of scope per goal.md.

## Architectural consequences
A reusable `RowValidator` interface now exists, with per-row error
collection already built. Any future bulk-import feature can reuse the
same per-row validation and error-reporting pattern without rebuilding it.

## Follow-up questions
Should invalid rows produce a downloadable, pre-filled corrected-template
file?
