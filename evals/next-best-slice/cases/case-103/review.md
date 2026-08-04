# Slice Review: Fix PDF export mojibake for non-ASCII customer names

**Verdict:** Ready to merge

## Blocking
None.

## Required corrections
None.

## Non-blocking
- Font embedding adds ~80KB to each generated PDF. Negligible for this
  use case; not blocking.

## Out of scope
None.

## Verification evidence
```
$ pytest invoices/test_pdf_export.py -v
test_renders_french_accented_name PASSED
test_renders_japanese_name PASSED
test_renders_cyrillic_name PASSED
3 passed in 0.9s
```
Byte-compared each output against a known-good reference PDF. Manually
verified in staging with a live customer record containing an accented
name.

## Reasoning
Goal was to fix mojibake (garbled text) for non-ASCII customer names on
invoice PDFs via proper UTF-8 font embedding. Met exactly as scoped.
