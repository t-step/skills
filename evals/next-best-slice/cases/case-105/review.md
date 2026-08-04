# Slice Review: Add CSV export to the weekly sales report

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
- Export currently loads the entire report into memory before writing the
  CSV. Fine at the current report size (~2,000 rows); would need a
  streaming approach above that.

## Out of scope
None.

## Verification evidence
```
$ pytest reports/test_csv_export.py -v
test_formats_currency_columns PASSED
test_escapes_commas_and_quotes PASSED
2 passed in 0.04s
```
Manually exported the current weekly report and opened it successfully in
both Excel and Google Sheets.

## Reasoning
Goal was CSV export for the weekly sales report specifically, formatted
correctly for spreadsheet tools. Met and verified against both target
tools.
