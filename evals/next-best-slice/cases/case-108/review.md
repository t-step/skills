# Slice Review: Add per-row CSV import validation for bulk product upload

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
None.

## Out of scope
None.

## Verification evidence
```
$ pytest catalog/test_bulk_import.py -v
test_missing_sku_rejected_with_row_number PASSED
test_invalid_price_format_rejected_with_row_number PASSED
test_duplicate_sku_within_file_rejected PASSED
test_valid_rows_still_import_when_others_fail PASSED
4 passed in 0.12s
```
Manually uploaded a real 200-row pilot merchant file containing several
known-bad rows; the import completed with the 197 valid rows imported and
3 per-row errors shown, matching the merchant's own manual review of the
file.

## Reasoning
Goal was per-row validation with partial import (valid rows succeed, bad
rows reported individually) rather than the previous all-or-nothing
behavior. Met and verified against a real merchant file.
