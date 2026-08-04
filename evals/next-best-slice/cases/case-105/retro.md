# Slice Retrospective: Add CSV export to the weekly sales report

## What we proved
The weekly sales report can be exported to a correctly formatted,
correctly escaped CSV file, verified against the current ~2,000-row report
size and confirmed to open correctly in both Excel and Google Sheets.

## Assumptions validated
None beyond baseline correctness of the formatting and escaping.

## Assumptions falsified
None.

## Remaining uncertainty
Behavior on much larger reports is untested — finance has mentioned
wanting a "full year" report, which would be roughly 100,000 rows —
including both memory usage during export and whether spreadsheet tools
can even open a file that size.

## Intentional non-goals
Exporting any report besides the weekly sales report, and any format
besides CSV, were both out of scope per goal.md.

## Architectural consequences
A generic `export_to_csv(report)` helper now exists and can be reused by
any report object that implements the same row-iteration interface.

## Follow-up questions
Which other reports should get the same export option next?
