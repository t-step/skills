# Slice Retrospective: Fix PDF export mojibake for non-ASCII customer names

## What we proved
Invoice PDF export now correctly renders French, Japanese, and Cyrillic
customer names via UTF-8 font embedding — backed by the three
byte-compared fixture tests and a staging check against a live record.

## Assumptions validated
Switching the font-embedding library fixes the encoding issue without
requiring any change to the PDF layout code.

## Assumptions falsified
None.

## Remaining uncertainty
Emoji and right-to-left scripts (Arabic, Hebrew) weren't in the fixture set
and are untested.

## Intentional non-goals
Right-to-left text layout support was explicitly out of scope per
goal.md — this slice fixed character rendering, not text direction.

## Architectural consequences
The PDF export module now has a general UTF-8-safe font-embedding helper.
Any future PDF this codebase generates (invoices, receipts, shipping
labels) can reuse it directly instead of reimplementing font handling.

## Follow-up questions
Does any other PDF template in the codebase have the same mojibake issue
this slice just fixed for invoices?
